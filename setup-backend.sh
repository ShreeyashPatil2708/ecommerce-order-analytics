#!/bin/bash

REGION="ap-south-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "🚀 Setting up Terraform backend..."
echo "Account ID: $ACCOUNT_ID"
echo "Region: $REGION"

# Create S3 bucket for Terraform state
BUCKET_NAME="terraform-state-ecommerce-${ACCOUNT_ID}"
echo "Creating bucket: $BUCKET_NAME"

aws s3 mb s3://${BUCKET_NAME} --region ${REGION} 2>/dev/null || echo "Bucket might already exist"

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket ${BUCKET_NAME} \
    --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
    --bucket ${BUCKET_NAME} \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'

# Create DynamoDB table for state locking
echo "Creating DynamoDB table for state locking..."
aws dynamodb create-table \
    --table-name terraform-state-lock \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region ${REGION} 2>/dev/null || echo "Table might already exist"

echo "✅ Terraform backend setup complete!"
echo ""
echo "📝 Update your terraform/main.tf with:"
echo "   bucket = \"${BUCKET_NAME}\""
