#!/bin/bash
export AWS_PAGER=""
aws ecs describe-services --cluster dnvriend-loki-all-cluster --services dnvriend-loki-all-loki-service  --output json | jq '.services[0] | { desiredCount, pendingCount, runningCount }'
