terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      created_by  = "dennis_vriend"
      deployed_by = "Terraform/Tofu"
      environment = "dev"
      project = "study-ecs-loki-cluster-deployment-monolithic"
    }
  }
}
