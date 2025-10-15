output "raw_data_bucket" {
  description = "Raw data S3 bucket name"
  value       = aws_s3_bucket.raw_data.id
}

output "processed_data_bucket" {
  description = "Processed data S3 bucket name"
  value       = aws_s3_bucket.processed_data.id
}

output "reports_bucket" {
  description = "Reports S3 bucket name"
  value       = aws_s3_bucket.reports.id
}

output "data_processor_lambda" {
  description = "Data processor Lambda function name"
  value       = aws_lambda_function.data_processor.function_name
}

output "report_generator_lambda" {
  description = "Report generator Lambda function name"
  value       = aws_lambda_function.report_generator.function_name
}

output "eventbridge_s3_rule" {
  description = "EventBridge rule for S3 uploads"
  value       = aws_cloudwatch_event_rule.s3_upload.name
}

output "eventbridge_daily_rule" {
  description = "EventBridge rule for daily reports"
  value       = aws_cloudwatch_event_rule.daily_report.name
}