.PHONY: help deploy deploy-all deploy-network deploy-storage deploy-security deploy-application \
        delete delete-all delete-application delete-security delete-storage delete-network \
        validate validate-all update update-application update-security status logs get-api-key \
        test lint format format-check typecheck check fix quick-deploy prod-deploy scale-up scale-down examples \
        describe-network describe-storage describe-security describe-application test-cov

# Configuration variables
ENVIRONMENT ?= prod
REGION ?= us-east-1
S3_BUCKET_NAME ?= zennlogic-$(ENVIRONMENT)-data-bucket
KEY_NAME ?= zennlogic-ai-$(ENVIRONMENT)-key-pair
SSH_CIDR ?=
INSTANCE_TYPE ?= t3.micro
MIN_INSTANCES ?= 2
MAX_INSTANCES ?= 4
DESIRED_INSTANCES ?= 2

# Stack names
NETWORK_STACK := zennlogic-network-$(ENVIRONMENT)
STORAGE_STACK := zennlogic-storage-$(ENVIRONMENT)
SECURITY_STACK := zennlogic-security-$(ENVIRONMENT)
APPLICATION_STACK := zennlogic-application-$(ENVIRONMENT)

# Template paths
TEMPLATE_DIR := infra/cfn
NETWORK_TEMPLATE := $(TEMPLATE_DIR)/01-network.yaml
STORAGE_TEMPLATE := $(TEMPLATE_DIR)/02-storage.yaml
SECURITY_TEMPLATE := $(TEMPLATE_DIR)/03-security.yaml
APPLICATION_TEMPLATE := $(TEMPLATE_DIR)/04-application.yaml

##@ Help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-20s %s\n", $$1, $$2 } /^##@/ { printf "\n%s\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Validation
validate-all: ## Validate all CloudFormation templates
	@echo "==> Validating all templates..."
	@aws cloudformation validate-template --template-body file://$(NETWORK_TEMPLATE) --region $(REGION) > nul 2>&1 && echo "[OK] Network template valid" || echo "[FAIL] Network template invalid"
	@aws cloudformation validate-template --template-body file://$(STORAGE_TEMPLATE) --region $(REGION) > nul 2>&1 && echo "[OK] Storage template valid" || echo "[FAIL] Storage template invalid"
	@aws cloudformation validate-template --template-body file://$(SECURITY_TEMPLATE) --region $(REGION) > nul 2>&1 && echo "[OK] Security template valid" || echo "[FAIL] Security template invalid"
	@aws cloudformation validate-template --template-body file://$(APPLICATION_TEMPLATE) --region $(REGION) > nul 2>&1 && echo "[OK] Application template valid" || echo "[FAIL] Application template invalid"

validate: validate-all ## Alias for validate-all

##@ Deployment
deploy-network: ## Deploy network stack (VPC, subnets, IGW)
	@echo "==> Deploying network stack..."
	aws cloudformation create-stack \
		--stack-name $(NETWORK_STACK) \
		--template-body file://$(NETWORK_TEMPLATE) \
		--parameters ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
		--region $(REGION) \
		--capabilities CAPABILITY_IAM \
		--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile
	@echo "==> Waiting for network stack to complete..."
	aws cloudformation wait stack-create-complete --stack-name $(NETWORK_STACK) --region $(REGION)
	@echo "[OK] Network stack deployed"

deploy-storage: ## Deploy storage stack (S3, DynamoDB, Secrets Manager)
	@echo "==> Deploying storage stack..."
	aws cloudformation create-stack \
		--stack-name $(STORAGE_STACK) \
		--template-body file://$(STORAGE_TEMPLATE) \
		--parameters \
			ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
			ParameterKey=S3BucketName,ParameterValue=$(S3_BUCKET_NAME) \
		--region $(REGION) \
		--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile
	@echo "==> Waiting for storage stack to complete..."
	aws cloudformation wait stack-create-complete --stack-name $(STORAGE_STACK) --region $(REGION)
	@echo "[OK] Storage stack deployed"

deploy-security: ## Deploy security stack (IAM roles, security groups)
	@echo "==> Deploying security stack..."
	@if "$(SSH_CIDR)"=="" ( \
		aws cloudformation create-stack \
			--stack-name $(SECURITY_STACK) \
			--template-body file://$(SECURITY_TEMPLATE) \
			--parameters ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
			--region $(REGION) \
			--capabilities CAPABILITY_NAMED_IAM \
			--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile \
	) else ( \
		aws cloudformation create-stack \
			--stack-name $(SECURITY_STACK) \
			--template-body file://$(SECURITY_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=AllowedSSHCidr,ParameterValue=$(SSH_CIDR) \
			--region $(REGION) \
			--capabilities CAPABILITY_NAMED_IAM \
			--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile \
	)
	@echo "==> Waiting for security stack to complete..."
	aws cloudformation wait stack-create-complete --stack-name $(SECURITY_STACK) --region $(REGION)
	@echo "[OK] Security stack deployed"

deploy-application: ## Deploy application stack (ALB, Auto Scaling, EC2)
	@echo "==> Deploying application stack..."
	@if "$(KEY_NAME)"=="" ( \
		aws cloudformation create-stack \
			--stack-name $(APPLICATION_STACK) \
			--template-body file://$(APPLICATION_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=InstanceType,ParameterValue=$(INSTANCE_TYPE) \
				ParameterKey=MinInstances,ParameterValue=$(MIN_INSTANCES) \
				ParameterKey=MaxInstances,ParameterValue=$(MAX_INSTANCES) \
				ParameterKey=DesiredInstances,ParameterValue=$(DESIRED_INSTANCES) \
			--region $(REGION) \
			--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile \
	) else ( \
		aws cloudformation create-stack \
			--stack-name $(APPLICATION_STACK) \
			--template-body file://$(APPLICATION_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=InstanceType,ParameterValue=$(INSTANCE_TYPE) \
				ParameterKey=KeyName,ParameterValue=$(KEY_NAME) \
				ParameterKey=MinInstances,ParameterValue=$(MIN_INSTANCES) \
				ParameterKey=MaxInstances,ParameterValue=$(MAX_INSTANCES) \
				ParameterKey=DesiredInstances,ParameterValue=$(DESIRED_INSTANCES) \
			--region $(REGION) \
			--tags Key=Environment,Value=$(ENVIRONMENT) Key=ManagedBy,Value=Makefile \
	)
	@echo "==> Waiting for application stack to complete (this may take 10-15 minutes)..."
	aws cloudformation wait stack-create-complete --stack-name $(APPLICATION_STACK) --region $(REGION)
	@echo "[OK] Application stack deployed"
	@$(MAKE) status

deploy-all: validate-all deploy-network deploy-storage deploy-security deploy-application ## Deploy all stacks in order
	@echo "[OK] All stacks deployed successfully!"
	@$(MAKE) get-api-key

deploy: deploy-all ## Alias for deploy-all

##@ Updates
update-application: ## Update application stack only
	@echo "==> Updating application stack..."
	@if "$(KEY_NAME)"=="" ( \
		aws cloudformation update-stack \
			--stack-name $(APPLICATION_STACK) \
			--template-body file://$(APPLICATION_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=InstanceType,ParameterValue=$(INSTANCE_TYPE) \
				ParameterKey=MinInstances,ParameterValue=$(MIN_INSTANCES) \
				ParameterKey=MaxInstances,ParameterValue=$(MAX_INSTANCES) \
				ParameterKey=DesiredInstances,ParameterValue=$(DESIRED_INSTANCES) \
			--region $(REGION) \
	) else ( \
		aws cloudformation update-stack \
			--stack-name $(APPLICATION_STACK) \
			--template-body file://$(APPLICATION_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=InstanceType,ParameterValue=$(INSTANCE_TYPE) \
				ParameterKey=KeyName,ParameterValue=$(KEY_NAME) \
				ParameterKey=MinInstances,ParameterValue=$(MIN_INSTANCES) \
				ParameterKey=MaxInstances,ParameterValue=$(MAX_INSTANCES) \
				ParameterKey=DesiredInstances,ParameterValue=$(DESIRED_INSTANCES) \
			--region $(REGION) \
	)
	@echo "==> Waiting for application stack update..."
	aws cloudformation wait stack-update-complete --stack-name $(APPLICATION_STACK) --region $(REGION)
	@echo "[OK] Application stack updated"

update-security: ## Update security stack
	@echo "==> Updating security stack..."
	@if "$(SSH_CIDR)"=="" ( \
		aws cloudformation update-stack \
			--stack-name $(SECURITY_STACK) \
			--template-body file://$(SECURITY_TEMPLATE) \
			--parameters ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
			--region $(REGION) \
			--capabilities CAPABILITY_NAMED_IAM \
	) else ( \
		aws cloudformation update-stack \
			--stack-name $(SECURITY_STACK) \
			--template-body file://$(SECURITY_TEMPLATE) \
			--parameters \
				ParameterKey=Environment,ParameterValue=$(ENVIRONMENT) \
				ParameterKey=AllowedSSHCidr,ParameterValue=$(SSH_CIDR) \
			--region $(REGION) \
			--capabilities CAPABILITY_NAMED_IAM \
	)
	@echo "==> Waiting for security stack update..."
	aws cloudformation wait stack-update-complete --stack-name $(SECURITY_STACK) --region $(REGION)
	@echo "[OK] Security stack updated"

update: update-application ## Alias for update-application

##@ Deletion
delete-application: ## Delete application stack
	@echo "==> Deleting application stack..."
	aws cloudformation delete-stack --stack-name $(APPLICATION_STACK) --region $(REGION)
	@echo "==> Waiting for application stack deletion..."
	aws cloudformation wait stack-delete-complete --stack-name $(APPLICATION_STACK) --region $(REGION)
	@echo "[OK] Application stack deleted"

delete-security: ## Delete security stack
	@echo "==> Deleting security stack..."
	aws cloudformation delete-stack --stack-name $(SECURITY_STACK) --region $(REGION)
	@echo "==> Waiting for security stack deletion..."
	aws cloudformation wait stack-delete-complete --stack-name $(SECURITY_STACK) --region $(REGION)
	@echo "[OK] Security stack deleted"

delete-storage: ## Delete storage stack (WARNING: Deletes S3 and DynamoDB data!)
	@echo "WARNING: This will delete all data in S3 and DynamoDB!"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
	@timeout /t 5 > nul 2>&1
	@echo "==> Emptying S3 bucket before deletion..."
	@aws s3 rm s3://$(S3_BUCKET_NAME) --recursive --region $(REGION) 2> nul || echo "Bucket already empty or doesn't exist"
	@echo "==> Deleting storage stack..."
	aws cloudformation delete-stack --stack-name $(STORAGE_STACK) --region $(REGION)
	@echo "==> Waiting for storage stack deletion..."
	aws cloudformation wait stack-delete-complete --stack-name $(STORAGE_STACK) --region $(REGION)
	@echo "[OK] Storage stack deleted"

delete-network: ## Delete network stack
	@echo "==> Deleting network stack..."
	aws cloudformation delete-stack --stack-name $(NETWORK_STACK) --region $(REGION)
	@echo "==> Waiting for network stack deletion..."
	aws cloudformation wait stack-delete-complete --stack-name $(NETWORK_STACK) --region $(REGION)
	@echo "[OK] Network stack deleted"

delete-all: delete-application delete-security delete-storage delete-network ## Delete all stacks in reverse order
	@echo "[OK] All stacks deleted"

delete: delete-all ## Alias for delete-all

##@ Status & Information
status: ## Show status of all stacks
	@echo "==> Stack Status:"
	@echo ""
	@echo "Network Stack:"
	@aws cloudformation describe-stacks --stack-name $(NETWORK_STACK) --region $(REGION) --query "Stacks[0].StackStatus" --output text 2> nul || echo "Not deployed"
	@echo ""
	@echo "Storage Stack:"
	@aws cloudformation describe-stacks --stack-name $(STORAGE_STACK) --region $(REGION) --query "Stacks[0].StackStatus" --output text 2> nul || echo "Not deployed"
	@echo ""
	@echo "Security Stack:"
	@aws cloudformation describe-stacks --stack-name $(SECURITY_STACK) --region $(REGION) --query "Stacks[0].StackStatus" --output text 2> nul || echo "Not deployed"
	@echo ""
	@echo "Application Stack:"
	@aws cloudformation describe-stacks --stack-name $(APPLICATION_STACK) --region $(REGION) --query "Stacks[0].StackStatus" --output text 2> nul || echo "Not deployed"
	@echo ""
	@echo "Application URL:"
	@aws cloudformation describe-stacks --stack-name $(APPLICATION_STACK) --region $(REGION) --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerURL'].OutputValue" --output text 2> nul || echo "Not available"

get-api-key: ## Retrieve the API key from Secrets Manager
	@echo "==> Retrieving API key..."
	@aws secretsmanager get-secret-value --secret-id zennlogic/$(ENVIRONMENT)/api-key --region $(REGION) --query SecretString --output text 2> nul | jq -r .api_key || echo "API key not found"

logs: ## Tail application logs from CloudWatch
	@echo "==> Tailing API logs (Ctrl+C to exit)..."
	aws logs tail /aws/ec2/zennlogic/$(ENVIRONMENT)/api --follow --region $(REGION)

describe-network: ## Show network stack outputs
	@aws cloudformation describe-stacks --stack-name $(NETWORK_STACK) --region $(REGION) --query "Stacks[0].Outputs" --output table

describe-storage: ## Show storage stack outputs
	@aws cloudformation describe-stacks --stack-name $(STORAGE_STACK) --region $(REGION) --query "Stacks[0].Outputs" --output table

describe-security: ## Show security stack outputs
	@aws cloudformation describe-stacks --stack-name $(SECURITY_STACK) --region $(REGION) --query "Stacks[0].Outputs" --output table

describe-application: ## Show application stack outputs
	@aws cloudformation describe-stacks --stack-name $(APPLICATION_STACK) --region $(REGION) --query "Stacks[0].Outputs" --output table

##@ Development
test: ## Run tests
	uv run pytest tests/ -v

test-cov: ## Run tests with coverage
	uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

lint: ## Run linting checks
	uv run ruff check .

format: ## Format code
	uv run ruff format .

format-check: ## Check code formatting without making changes
	uv run ruff format --check .

typecheck: ## Run type checking
	uv run mypy src/

check: lint format-check typecheck ## Run all code quality checks

fix: format lint ## Auto-fix formatting and linting issues

##@ Quick Commands
quick-deploy: ## Quick deploy to dev environment with minimal instances
	@$(MAKE) deploy-all ENVIRONMENT=dev MIN_INSTANCES=1 MAX_INSTANCES=2 DESIRED_INSTANCES=1

prod-deploy: ## Deploy to production with recommended settings
	@$(MAKE) deploy-all ENVIRONMENT=prod MIN_INSTANCES=2 MAX_INSTANCES=4 DESIRED_INSTANCES=2

scale-up: ## Scale application to maximum instances
	@$(MAKE) update-application DESIRED_INSTANCES=$(MAX_INSTANCES)
	@echo "[OK] Scaled up to $(MAX_INSTANCES) instances"

scale-down: ## Scale application to minimum instances
	@$(MAKE) update-application DESIRED_INSTANCES=$(MIN_INSTANCES)
	@echo "[OK] Scaled down to $(MIN_INSTANCES) instances"

##@ Examples
examples: ## Show usage examples
	@echo ""
	@echo "==> Common Usage Examples:"
	@echo ""
	@echo "1. Deploy everything to production:"
	@echo "   make deploy ENVIRONMENT=prod S3_BUCKET_NAME=my-prod-bucket KEY_NAME=my-key"
	@echo ""
	@echo "2. Deploy to dev with minimal resources:"
	@echo "   make quick-deploy S3_BUCKET_NAME=my-dev-bucket"
	@echo ""
	@echo "3. Update just the application code:"
	@echo "   make update-application ENVIRONMENT=prod"
	@echo ""
	@echo "4. Enable SSH access:"
	@echo "   make deploy SSH_CIDR=1.2.3.4/32 S3_BUCKET_NAME=my-bucket"
	@echo ""
	@echo "5. Scale up instances:"
	@echo "   make scale-up ENVIRONMENT=prod"
	@echo ""
	@echo "6. Get your API key:"
	@echo "   make get-api-key ENVIRONMENT=prod"
	@echo ""
	@echo "7. Delete everything:"
	@echo "   make delete-all ENVIRONMENT=prod"
	@echo ""
	@echo "8. Run development checks:"
	@echo "   make check"
	@echo ""
