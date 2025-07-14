# 🔐 IAM Configuration for Lambda Function

This module defines the IAM (Identity and Access Management) setup required for the Lambda function to securely interact with various AWS services such as **Kinesis**, **S3**, and **CloudWatch Logs**.

All IAM resources are defined in `modules/lambda/iam.tf`.

---

## 📌 Overview

The Lambda function in our ride prediction pipeline consumes events from Kinesis, performs inference using a model stored in S3, and publishes predictions to another Kinesis stream. It also logs to CloudWatch.

To enable secure access, we configure:

- An IAM **role** that Lambda can assume
- IAM **policies** to interact with Kinesis, S3, and CloudWatch
- Attachments that bind policies to the role

---

## ✅ IAM Role

This IAM role allows Lambda (and optionally Kinesis) to assume it using AWS Security Token Service (STS).

```hcl
resource "aws_iam_role" "iam_lambda" {
  name = "iam_${var.lambda_function_name}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "kinesis.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
```

---

## 📦 Kinesis Access Policy

Grants Lambda full access to list, read from, and write to Kinesis streams.

```hcl
resource "aws_iam_policy" "allow_kinesis_processing" {
  name        = "allow_kinesis_processing_${var.lambda_function_name}"
  path        = "/"
  description = "IAM policy for Kinesis access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "kinesis:ListShards",
        "kinesis:ListStreams",
        "kinesis:*"
      ],
      "Resource": "arn:aws:kinesis:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "stream:GetRecord",
        "stream:GetShardIterator",
        "stream:DescribeStream",
        "stream:*"
      ],
      "Resource": "arn:aws:stream:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}
```

---

## 🔗 Attach Kinesis Policy to Role

```hcl
resource "aws_iam_role_policy_attachment" "kinesis_processing" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.allow_kinesis_processing.arn
}
```

---

## 📝 Inline Policy for Output Stream

Allows Lambda to send predictions to the output stream.

```hcl
resource "aws_iam_role_policy" "inline_lambda_policy" {
  name       = "LambdaInlinePolicy"
  role       = aws_iam_role.iam_lambda.id
  depends_on = [aws_iam_role.iam_lambda]
  policy     = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:PutRecords",
        "kinesis:PutRecord"
      ],
      "Resource": "${var.output_stream_arn}"
    }
  ]
}
EOF
}
```

---

## 📊 IAM Policy for CloudWatch Logging

Allows Lambda to write logs to AWS CloudWatch.

```hcl
resource "aws_iam_policy" "allow_logging" {
  name        = "allow_logging_${var.lambda_function_name}"
  path        = "/"
  description = "IAM policy for CloudWatch logging"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}
```

---

## 🔗 Attach CloudWatch Policy to Role

```hcl
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.allow_logging.arn
}
```

---

## 🪣 IAM Policy for S3 Access

Grants Lambda access to read models and interact with the S3 bucket.

```hcl
resource "aws_iam_policy" "lambda_s3_role_policy" {
  name = "lambda_s3_policy_${var.lambda_function_name}"
  description = "IAM Policy for S3 access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "s3:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::${var.model_bucket}",
        "arn:aws:s3:::${var.model_bucket}/*"
      ]
    },
    {
      "Action": [
        "autoscaling:Describe*",
        "cloudwatch:*",
        "logs:*",
        "sns:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
```

---

## 🔗 Attach S3 Policy to Role

```hcl
resource "aws_iam_role_policy_attachment" "iam-policy-attach" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_role_policy.arn
}
```

---
