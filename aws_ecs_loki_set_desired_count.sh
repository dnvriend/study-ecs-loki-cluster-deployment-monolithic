#!/bin/bash
export AWS_PAGER=""
aws ecs update-service --cluster dnvriend-loki-all-cluster --service dnvriend-loki-all-loki-service  --output json --desired-count ${1:-0} | jq '.service | { desiredCount, pendingCount, runningCount }'
