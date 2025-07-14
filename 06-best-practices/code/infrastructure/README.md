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

**`infrastructure/main.tf`**
```hcl
# ride_events
module "source_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name = "${var.source_stream_name}-${var.project_id}"
  tags = var.project_id
}
```

**`infrastructure/variables.tf`**
```hcl
variable "source_stream_name" {
  description = ""
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
### 🚀 Destroy the resource
```bash
terraform destroy
```
This command will destroy the resource

---

### 🔹 Step 4: Add Kinesis Output Stream

In addition to the input stream, a second **Kinesis stream** was created for publishing ride prediction events.

**`infrastructure/main.tf`**
```hcl
# ride_predictions
module "output_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name = "${var.output_stream_name}-${var.project_id}"
  tags = var.project_id
}
```

**`infrastructure//variables.tf`**
```hcl
variable "output_stream_name" {
  description = ""
}
```

---

### 🔹 Step 5: Add S3 Module for Model Storage

A new Terraform module was added to manage the **S3 bucket** that stores ML model artifacts.

**`infrastructure/main.tf`**
```hcl
module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.model_bucket}-${var.project_id}"
}
```

**`infrastructure/variables.tf`**
```hcl
ariable "model_bucket" {
  description = "s3_bucket"
}

```
---
---

### 🔹 Step 6: Add and Configure ECR with Image Dependency for Lambda

#### 🚀 Why ECR is Important in MLOps

ECR (Elastic Container Registry) is used to store Docker images in AWS.  
In this pipeline, the **Lambda function** that will run ML predictions is based on a **custom Docker image** — and that image must be available **before** Lambda is created.

Normally, Terraform isn't responsible for building and pushing Docker images — that's a job for a CI/CD pipeline. But because Lambda needs a valid `image_uri` at creation time, we're including this image provisioning step **within Terraform** just for this workshop.

---

### 🏗️ Real-World Context: Two-Repos Approach

In professional teams, infrastructure and application code are usually separated into:

- **Infrastructure repo**: stable components like VPCs, ECR, databases, etc.
- **Service/App repo**: application-level infrastructure like Lambda or ECS tasks

CI/CD pipelines then ensure that infrastructure is deployed before application services rely on them. For example:

> 🔁 “If ECR has been provisioned by infra CI, then app CI can deploy Lambda using the image URI.”

But for this **mono-repository workshop**, we're doing everything together — so we must **simulate those dependencies inside Terraform**.

---

## 🧱 ECR Module Breakdown

We added a new module to:

- Create an ECR repository
- Build and push a Docker image
- Output the `image_uri` for use in Lambda configuration

---

### 📦 Create ECR Repository

**`modules/ecr/main.tf`**
```hcl
resource "aws_ecr_repository" "repo" {
  name = var.ecr_repo_name
}
```

This creates a named container registry in AWS.

---

### 🔄 Build and Push Docker Image

Terraform is not designed to push images — but we use a workaround.

#### ✅ `null_resource` with `local-exec`

We use a **special Terraform resource** called `null_resource`, combined with `provisioner "local-exec"` to run custom shell commands *on your machine* during provisioning.

```hcl
resource "null_resource" "ecr_image" {
  triggers = {
    python_file = md5(file(var.lambda_function_local_path))
    docker_file = md5(file(var.docker_image_local_path))
  }

  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
      cd ../
      docker build -t ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag} .
      docker push ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag}
    EOF
  }
}
```

##### 🧠 What this does:

1. **Authenticates** Docker with AWS ECR  
2. **Builds** the image from your local Dockerfile and Lambda code  
3. **Pushes** it to the ECR repo  

It runs only when the Dockerfile or Lambda code changes (thanks to the `triggers` block).

---

### 📥 Fetch the Image with `data` Source

After pushing the image, we use a `data` block to read the image metadata.  
This ensures the Lambda function (created later) gets a valid URI.

```hcl
data "aws_ecr_image" "lambda_image" {
  depends_on = [null_resource.ecr_image]
  repository_name = var.ecr_repo_name
  image_tag       = var.ecr_image_tag
}
```

This guarantees the Lambda won’t configure until the Docker image exists.

---

### 📤 Output the Image URI

To pass the image to the Lambda module later, expose it via:

```hcl
output "image_uri" {
  value = "${aws_ecr_repository.repo.repository_url}:${data.aws_ecr_image.lambda_image.image_tag}"
}
```

---

## 🔗 Infrastructure Integration

In `infrastructure/main.tf`, the ECR module is configured like this:

```hcl
module "ecr_image" {
  source                     = "./modules/ecr"
  ecr_repo_name              = "${var.ecr_repo_name}_${var.project_id}"
  account_id                 = local.account_id
  lambda_function_local_path = var.lambda_function_local_path
  docker_image_local_path    = var.docker_image_local_path
}
```

---

## 🧪 Managing Environment Configurations with `.tfvars`

As the number of variables grows, it becomes hard to pass them all on the CLI.  
To solve this, we use **`.tfvars` files** for different environments (e.g., staging, production).

Folder structure:
```
vars/
├── stg.tfvars
├── prod.tfvars
```

We can run Terraform with config varibles file:

```bash
terraform plan -var-file=vars/stg.tfvars
terraform apply -var-file=vars/stg.tfvars
```

Terraform will skip any unchanged resources, only applying new updates (as previously streams, and s3 were created, so will not created again.)


🎉 That completes the ECR setup. With this in place, you're ready to connect Lambda and build the full pipeline!

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

## ✅ What's Next?

- Add and configure AWS Lambda function to run ML inference  
- Pull the model from S3 and Docker image from ECR  
- Stream results into the new output Kinesis stream  
- Set up CloudWatch for monitoring and debugging  


---
