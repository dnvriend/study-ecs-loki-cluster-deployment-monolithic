#!/bin/bash
export AWS_PAGER=""
aws ecr delete-repository \
    --repository-name dnvriend-loki-all-loki-image \
    --force \
    --region us-east-1