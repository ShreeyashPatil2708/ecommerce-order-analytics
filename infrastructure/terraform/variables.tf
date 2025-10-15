variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "ecommerce"
}

variable "recipient_email" {
  description = "Email to receive reports"
  type        = string
  # CHANGE THIS to your verified email!
  default     = "patilshreeyash2708@gmail.com"
}

variable "sender_email" {
  description = "SES verified sender email"
  type        = string
  # CHANGE THIS to your verified email!
  default     = "patilshreeyash2708@gmail.com"
}

variable "owner" {
  description = "Owner name"
  type        = string
  default     = "Shreeaysh"
}