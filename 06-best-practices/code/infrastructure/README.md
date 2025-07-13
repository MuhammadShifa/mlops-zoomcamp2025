# Infrastructure with Terraform

In this module, we explore one of the most critical skills in MLOps:  
**Infrastructure as Code (IaC)** — using **Terraform**.

---

## 📘 What is Infrastructure as Code (IaC)?

**Infrastructure as Code (IaC)** refers to the practice of provisioning and managing infrastructure through code instead of manual configuration.

- Enables cloud resources to be created and managed programmatically  
- Supports automation and reproducibility  
- Makes infrastructure version-controlled and consistent

---

## 🛠️ What is Terraform?

**Terraform** is an open-source tool by HashiCorp that facilitates Infrastructure as Code using a declarative configuration language called **HCL (HashiCorp Configuration Language)**.

- Provisions infrastructure across multiple cloud providers (AWS, GCP, Azure, etc.)  
- Manages compute, storage, and networking components  
- Supports modular, reusable configurations with state tracking

---

## 📊 Architecture Diagram — Real-time Ride Prediction Pipeline

```
                                            +----------------------------+
                                            |  S3 Bucket: Model Artifacts|
                                            +----------------------------+
                                                          | 
                                                          | Get Model
                                                          v
+--------------------+     +-----------------+     +--------------+                               +-------------------------+
| Kinesis Stream     | --> |  CW Event       |--->|   AWS Lambda  | ---publish prediction event-->|   Kinesis Stream        |
| Input (Ride Events)|     | Lambda Trigger  |     +--------------+                               | Output(ride Predictions)| 
+--------------------+     +-----------------+            ^                                       +-------------------------+   
                                                          |         
                                                          | Get Image                                         
                                                    +-------------+           
                                                    |    ECR      |
                                                    +-------------+

        
```

> ☁️ This architecture lives inside the AWS Cloud.  
> 🔁 It supports **event-driven inference** for real-time ride predictions using **Kinesis**, **Lambda**, **ECR**, and **S3**.

---

## 📁 Project Structure

```
module6/
└── infrastructure/
    ├── main.tf            # Backend + AWS provider
    ├── variables.tf       # Global variables
    └── modules/
        └── kinesis/
            ├── main.tf    # Kinesis stream definition
            └── variables.tf
```

---

## 🧭 Step-by-Step Progress

### 🔹 Step 1: Configure Remote State with S3

Terraform state is used to track resource changes. A remote S3 bucket is configured to store this state securely.

**`infrastructure/main.tf`**
```hcl
terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket  = "tf-state-mlops-zoomcamp2025"
    key     = "mlops-zoomcamp-stg.tfstate"
    region  = "ap-south-1"
    encrypt = true
  }
}
```

> ✅ The S3 bucket `tf-state-mlops-zoomcamp2025` was created manually via the AWS console.

---

### 🔹 Step 2: Set Up the AWS Provider

**`infrastructure/main.tf`**
```hcl
provider "aws" {
  region = var.aws_region
}
```

**`infrastructure/variables.tf`**
```hcl
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-south-1"
}
```

---

### 🔹 Step 3: Create a Terraform Module for Kinesis

A reusable module for creating a Kinesis stream:

**`modules/kinesis/main.tf`**
```hcl
resource "aws_kinesis_stream" "ride_events" {
  name             = var.stream_name
  shard_count      = 1
  retention_period = 24
}
```

**`modules/kinesis/variables.tf`**
```hcl
variable "stream_name" {
  description = "Name of the Kinesis stream"
  type        = string
}
```

---

## 💻 Running Terraform

Navigate to the `infrastructure` directory and run the following commands:

### ✅ Initialize Terraform
```bash
terraform init
```

If multiple AWS profiles are used:
```bash
terraform init --profile <your-profile-name>
```

---

### 🔍 Preview the Execution Plan
```bash
terraform plan -var="stream_name=ride-events-stg"
```

---

### 🚀 Apply the Plan
```bash
terraform apply -var="stream_name=ride-events-stg"
```

After approval, the Kinesis stream `ride-events-stg` will be created.

---

## 📌 Summary of Concepts Learned

| Concept                 | Description                                                  |
|------------------------|--------------------------------------------------------------|
| Infrastructure as Code | Define and manage infra through code                        |
| Terraform              | Declarative, multi-cloud infrastructure tool                 |
| Backend                | Stores Terraform state remotely (S3 in this case)            |
| Provider               | Specifies the cloud platform and region                      |
| Module                 | Reusable and isolated Terraform logic                        |
| Resource               | Any AWS entity defined and provisioned via Terraform         |

---

## 🔜 What’s Next?

- Expand with Lambda, ECR, and S3 modules  
- Wire services together for live predictions  
- Configure CloudWatch for monitoring  
- Deploy ML models into Lambda using Docker

---
