# 🚀 CI/CD Pipeline for MLOps Zoomcamp


This section explains the **CI/CD pipeline** setup for our MLOps Zoomcamp(06-best-practices module), using **GitHub Actions** to automate testing, infrastructure provisioning, Docker image creation, and deployment.

---

### 📌 What is CI/CD?

CI/CD stands for:

- **CI (Continuous Integration)**  
  Automatically builds, tests, and validates code when changes are made. It helps detect errors early in the development lifecycle.

- **CD (Continuous Delivery)**  
  Automates the delivery of applications and infrastructure changes. It ensures that new versions are deployed reliably and safely.

Together, **CI/CD** is a critical DevOps practice to shorten the software development lifecycle and improve code quality through automation.

---

### 🎯 CI/CD Pipeline Goals

The purpose of this pipeline is to:

1. **Automatically run tests** on new code and infrastructure changes.
2. **Define infrastructure** using Terraform.
3. **Build and push Docker images** for a Lambda service.
4. **Update AWS Lambda** to use the new container image.
5. **Repeat all of this on every commit or PR merge**, without manual steps.

We use **GitHub Actions** to orchestrate this process, which provides pre-configured virtual machines for running our CI/CD jobs.

---

### 📁 Pipeline Overview

We split our automation into **two workflows**:

#### 🧪 Continuous Integration (CI)

- **Trigger:**  
  Runs on **pull requests** created from feature branches.

- **Jobs in CI Workflow:**
  - ✅ **Run Unit Tests**  
    Ensure Python functions work correctly using pytest or similar.
  - ✅ **Run Integration Tests**  
    Test how different parts of the system work together.
  - ✅ **Terraform Plan**  
    Validate any infrastructure changes before applying them, by running `terraform plan` on the Terraform code.

#### 🚢 Continuous Delivery (CD)

- **Trigger:**  
  Runs **after a pull request is merged** into the `main` or `develop` branch.

- **Jobs in CD Workflow:**

  1. **Define Infrastructure**
     - Use `Terraform Apply` to provision or update infrastructure such as S3 buckets, Lambda functions, IAM roles, etc.

  2. **Build and Push Docker Image**
     - Package the Lambda function as a Docker image.
     - Tag and push the image to **Amazon ECR (Elastic Container Registry)**.

  3. **Deploy**
     - Update the Lambda function configuration to use the **new image version**.
     - Enable multi-environment support (e.g., dev, staging, prod) via environment variables or separate infrastructure definitions.

---

### 🔧 Why GitHub Actions?

We chose **GitHub Actions** because it:

- Is **natively integrated with GitHub**.
- Provides **ready-to-use VMs** for automation.
- Has a wide ecosystem of actions for Terraform, Docker, AWS, etc.
- Supports **multi-job workflows** and **environment-specific secrets**.

---

### 📁 CI/CD Workflow Directory

Workflows must be defined inside the `.github/workflows/` directory at the root of the repository.

In our project:

- `ci-tests.yml` → Continuous Integration (CI) workflow
- `cd-deploy.yml` → Continuous Deployment (CD) workflow

---

## 🚨 Workflow Trigger

We configure GitHub Actions to trigger the CI workflow when a **pull request is opened or updated** on the `main` branch, **only if** changes are made inside the MLOps code folder.

```yaml
on:
  pull_request:
    branches:
      - 'main'
    paths:
      - '06-best-practices/code/**'
```

This ensures the workflow runs only when meaningful changes are introduced.


### 🔐 Environment Variables

We define AWS credentials and region using GitHub Secrets in the environment block:

```yaml
env:
  AWS_DEFAULT_REGION: 'eu-west-1'
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

These secrets must be configured under **Settings → Secrets and variables → Actions** in your GitHub repository.

### 🧪 CI Jobs

Our `ci-tests.yml` contains two jobs:

- `test`: runs unit tests, linter, and integration tests
- `tf-plan`: validates Terraform infrastructure changes


#### ✅ `test` Job

This job performs code checkout, dependency installation, testing, linting, and integration testing.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9.12

      - name: Install dependencies
        working-directory: "06-best-practices/code"
        run: pip install pipenv && pipenv install --dev

      - name: Run Unit tests
        working-directory: "06-best-practices/code"
        run: pipenv run pytest tests/

      - name: Lint
        working-directory: "06-best-practices/code"
        run: pipenv run pylint --recursive=y .

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ env.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ env.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_DEFAULT_REGION }}
      
      - name: Install Docker Compose Plugin
        run: |
          sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          sudo chmod +x /usr/local/bin/docker-compose
      
      - name: Integration Test
        working-directory: '06-best-practices/code/integration-test'
        run: |
          . run.sh
```

#### 🛠️ `tf-plan` Job

This job performs infrastructure validation using Terraform:

```yaml
tf-plan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ env.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ env.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_DEFAULT_REGION }}

    - uses: hashicorp/setup-terraform@v2

    - name: TF plan
      id: plan
      working-directory: '06-best-practices/code/infrastructure'
      run: |
        terraform init -backend-config="key=mlops-zoomcamp-prod.tfstate" --reconfigure && terraform plan --var-file vars/prod.tfvars```

```

✅ This setup ensures every pull request goes through automated testing and Terraform validation before merging to `main`, improving code quality and infrastructure stability.

---
### ✅ Summary

By implementing CI/CD, we ensure that:

- Code is always tested before being merged.
- Infrastructure changes are validated before applying.
- Deployments are automated, consistent, and reliable.
- The entire pipeline is triggered automatically based on Git events (PRs and merges).
