# Infrastructure

CloudFormation templates, systemd units, NGINX config, and bootstrap scripts for zennlogic_ai_service.

## CloudFormation

- ec2-stack.yaml: EC2 instance, security, user-data bootstrap
- s3-bucket.yaml: S3 bucket for vector index snapshots
- ssm-params.yaml: SSM Parameter Store for API key
- iam-instance-profile.yaml: IAM role for SSM/S3
- security-groups.yaml: Security group rules
- outputs.yaml: Stack outputs

## Systemd

- zennlogic-ai-api.service: FastAPI REST API
- zennlogic-ai-mcp.service: MCP server

## NGINX

- zennlogic-ai-nginx.conf: Reverse proxy config

## User Data

- cloudinit.yaml: EC2 bootstrap script
