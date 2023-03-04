terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  backend "s3" {
    bucket   = "terraform-state-igti-geovani"
    key      = "job_glue_states.tfstate"
    region   = "us-east-2"
    
  }
}

provider "aws" {
  region = "us-east-2"
}