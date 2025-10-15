# ========================================
# DATA PROCESSOR LAMBDA
# ========================================

resource "aws_lambda_function" "data_processor" {
  filename         = "${path.module}/../../lambda-packages/data-processor.zip"
  function_name    = "${var.project_name}-data-processor-${var.environment}"
  role            = aws_iam_role.lambda_processor.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/../../lambda-packages/data-processor.zip")
  runtime         = "python3.11"
  timeout         = 60
  memory_size     = 256

  environment {
    variables = {
      PROCESSED_BUCKET = aws_s3_bucket.processed_data.id
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_processor_basic,
    aws_cloudwatch_log_group.data_processor
  ]
}

resource "aws_lambda_permission" "allow_eventbridge_processor" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_processor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_upload.arn
}

# ========================================
# REPORT GENERATOR LAMBDA
# ========================================

resource "aws_lambda_function" "report_generator" {
  filename         = "${path.module}/../../lambda-packages/report-generator.zip"
  function_name    = "${var.project_name}-report-generator-${var.environment}"
  role            = aws_iam_role.lambda_report.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/../../lambda-packages/report-generator.zip")
  runtime         = "python3.11"
  timeout         = 300
  memory_size     = 256

  environment {
    variables = {
      PROCESSED_BUCKET = aws_s3_bucket.processed_data.id
      REPORTS_BUCKET   = aws_s3_bucket.reports.id
      RECIPIENT_EMAIL  = join(",", var.recipient_emails)
      SENDER_EMAIL     = var.sender_email
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_report_basic,
    aws_cloudwatch_log_group.report_generator
  ]
}

resource "aws_lambda_permission" "allow_eventbridge_report" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.report_generator.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_report.arn
}

# ========================================
# CLOUDWATCH LOG GROUPS
# ========================================

resource "aws_cloudwatch_log_group" "data_processor" {
  name              = "/aws/lambda/${var.project_name}-data-processor-${var.environment}"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "report_generator" {
  name              = "/aws/lambda/${var.project_name}-report-generator-${var.environment}"
  retention_in_days = 7
}
