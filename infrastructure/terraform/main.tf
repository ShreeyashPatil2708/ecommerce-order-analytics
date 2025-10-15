terraform {
  required_version = ">= 1.6"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }

  # ✅ UPDATED with your bucket name
  backend "s3" {
    bucket         = "terraform-state-ecommerce-160885275231"
    key            = "pipeline/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ECommerceAnalytics"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
    }
  }
}

# Get AWS account info
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Random suffix for globally unique bucket names
resource "random_id" "suffix" {
  byte_length = 4
}

# ========================================
# S3 BUCKETS
# ========================================

# Raw Data Bucket (incoming CSV files)
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-data-${var.environment}-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_versioning" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "raw_data" {
  bucket                  = aws_s3_bucket.raw_data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Processed Data Bucket
resource "aws_s3_bucket" "processed_data" {
  bucket = "${var.project_name}-processed-${var.environment}-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_versioning" "processed_data" {
  bucket = aws_s3_bucket.processed_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "processed_data" {
  bucket = aws_s3_bucket.processed_data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "processed_data" {
  bucket                  = aws_s3_bucket.processed_data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Reports Bucket
resource "aws_s3_bucket" "reports" {
  bucket = "${var.project_name}-reports-${var.environment}-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ========================================
# EVENTBRIDGE RULE FOR S3 EVENTS
# ========================================

resource "aws_cloudwatch_event_rule" "s3_upload" {
  name        = "${var.project_name}-s3-upload-${var.environment}"
  description = "Trigger Lambda when CSV uploaded to S3"

  event_pattern = jsonencode({
    source      = ["aws.s3"]
    detail-type = ["Object Created"]
    detail = {
      bucket = {
        name = [aws_s3_bucket.raw_data.id]
      }
      object = {
        key = [{
          prefix = "incoming/"
        }]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "lambda_processor" {
  rule      = aws_cloudwatch_event_rule.s3_upload.name
  target_id = "DataProcessorLambda"
  arn       = aws_lambda_function.data_processor.arn
}

# ========================================
# EVENTBRIDGE RULE FOR DAILY REPORT
# ========================================

resource "aws_cloudwatch_event_rule" "daily_report" {
  name                = "${var.project_name}-daily-report-${var.environment}"
  description         = "Trigger report generation daily at 7 AM IST"
  schedule_expression = "cron(30 1 * * ? *)"  # 7:00 AM IST = 1:30 AM UTC
}

resource "aws_cloudwatch_event_target" "lambda_report" {
  rule      = aws_cloudwatch_event_rule.daily_report.name
  target_id = "ReportGeneratorLambda"
  arn       = aws_lambda_function.report_generator.arn
}

# ========================================
# S3 EVENT NOTIFICATION
# ========================================

resource "aws_s3_bucket_notification" "raw_data_events" {
  bucket      = aws_s3_bucket.raw_data.id
  eventbridge = true
}
