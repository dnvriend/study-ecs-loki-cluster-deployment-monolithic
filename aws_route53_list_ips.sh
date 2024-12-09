#!/bin/bash
export AWS_PAGER=""
zone_id=$(aws route53 list-hosted-zones --query "HostedZones[?Name == 'services.vpc.'].Id" --output text)
aws route53 list-resource-record-sets --hosted-zone-id $zone_id  --output json | jq '.ResourceRecordSets[] | select(.Name == "loki.services.vpc.") | .ResourceRecords[].Value'