import json
import boto3

class DateTimeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles datetime objects by converting them to ISO format strings.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

ecs = boto3.client('ecs')
route53 = boto3.client('route53')


# need
def get_unique_ips(attachments: list[dict]) -> [str]:
    ips = []
    try:
        for attachment in attachments:
            for detail in attachment['details']:
                if detail['name'] == 'privateIPv4Address':
                    ips.append(detail['value'])
        return list(set(ips))
    except KeyError as e:
        print(f"Error: {e}")
        return []


# need
def get_tags(task_arn: str) -> [dict]:
    response = ecs.list_tags_for_resource(
        resourceArn=task_arn
    )
    if response.get('tags'):
        return response['tags']
    else:
        return []


# need
def update_route53_record(hosted_zone_id: str, dns_name: str, ip_addresses: [str]) -> None:
    if not ip_addresses:
        ip_addresses = ["127.0.0.1"]

    route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': dns_name,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': list(map(lambda ip: {'Value': ip}, ip_addresses))
                    }
                }
            ]
        })

# need
def get_all_task_arns(cluster_arn: str, service_name: str) -> [str]:
    all_tasks = []
    paginator = ecs.get_paginator('list_tasks')
    pages = paginator.paginate(cluster=cluster_arn, serviceName=service_name, desiredStatus='RUNNING') # Use desiredStatus
    for page in pages:
        all_tasks.extend(page['taskArns'])
    return all_tasks


# need
def get_tasks(cluster_arn: str, tasks: [str]) -> [dict]:
    if tasks:
        tasks_response = ecs.describe_tasks(cluster=cluster_arn, tasks=tasks)
        return tasks_response['tasks']
    return []


# need
def get_service_arn(cluster: str, service_name: str):
    response = ecs.describe_services(cluster=cluster, services=[service_name])
    return response['services'][0]['serviceArn']


def lambda_handler(event, context):
    print(json.dumps(event, cls=DateTimeEncoder))
    task_arn = event['detail']['taskArn']
    desired_status = event['detail']['desiredStatus']
    last_status = event['detail']['lastStatus']
    cluster_arn = event['detail']['clusterArn']
    group = event['detail']['group']
    service_name = group.split(':')[1]

    task_arns = get_all_task_arns(cluster_arn, service_name)
    tasks = get_tasks(cluster_arn, task_arns)
    ips = [ip for task in tasks for ip in get_unique_ips(task['attachments'])]
    service_arn = get_service_arn(cluster_arn, service_name)
    tags = get_tags(service_arn)
    for tag in tags:
        if tag.get('key') == 'HostedZoneId':
            hosted_zone_id = tag['value']
        if tag.get('key') == 'DnsName':
            dns_name = tag['value']

    # print all variables in one big f string
    print(f"""
        task_arn: {task_arn}
        desired_status: {desired_status}
        last_status: {last_status}
        cluster_arn: {cluster_arn}
        group: {group}
        service_name: {service_name}
        task_arns: {task_arns}
        tasks: {tasks}
        ips: {ips}
        service_arn: {service_arn}
        hosted_zone_id: {hosted_zone_id}
        dns_name: {dns_name}
        """)

    update_route53_record(hosted_zone_id, dns_name, ips)

    return {
        'statusCode': 200,
        'body': json.dumps('Task launch processed successfully!')
    }
