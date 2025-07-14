## 🧪 Unit Testing and Dockerizing the Streaming Module

### 📚 Overview

This README explains the process of:

- Structuring unit tests for a streaming service
- Making code more testable
- Running and debugging tests
- Building and running Docker containers for the updated module

The unit testing work is based on the [**streaming**](../04-deployment/streaming) module from the [**Deployment**](../04-deployment/) module of the MLOps Zoomcamp.

---

### 🧱 Project Structure

```bash
.
├── code/                    # Source code copied from streaming module
│   ├── lambda_function.py.py
│   ├── model.py.py
│   └── test_docker.py
│   ├── Dockerfile

├── test/                    # Unit tests for the above code
│   └── model_test.py
└── README.md
```

---

### ✅ What is Unit Testing?

Unit testing is the process of testing **individual pieces of code (units)** like functions or classes to make sure they behave as expected.

#### 🔍 Why do we unit test?

- To catch bugs early
- To make code modular and independent
- To support safe refactoring
- To improve reliability

---

### 🧪 Writing a Simple Unit Test


Let’s say we have the following model serivce class required model in `model.py`
We then wrap this with a service class in `service.py`:

```python
class ModelService:
    def __init__(self, model):
        self.model = model

    def predict(self, features):
        return self.model.predict(features)
```

We then wrap this with a mock class in `model_test.py`:

```python
class ModelMock():
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n
```

#### ✅ A simple unit test:

```python
from model import ModelService

def test_predict():
    model_mock = ModelMock(10.0)
    # Creates a ModelService instance and gives it the fake model (model_mock) to use.
    # Now, any prediction made through model_service will use that mock.

    model_service = model.ModelService(model_mock) # we don't want the actually model tbe use from s3, test should be independent as possible
    features = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction

```

#### 🔍 Explanation:

- We use a **mock model** that always returns `10.0`
- This isolates the `ModelService` and avoids dependencies on real ML models
- `assert` ensures the result is what we expect

---

### 🧪 Running the Tests

Make sure you have `pytest` installed:

```bash
pipenv install --dev pytest
```
In your project root, run:

```bash
pipenv run pytest test
```

---

### 🐳 Dockerizing the Updated Code

Once you’ve tested and debugged your code, you can containerize it for deployment.

#### ✅ Build Docker Image

```bash
docker build -t stream-model-duration:v2 .
```

#### ✅ Run Docker Container

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```

> The `-e` flags set environment variables inside the container.

---

### 🧠 Key Learnings

- Unit testing helps isolate and validate parts of your code
- Mocking makes testing easier by replacing real models or APIs
- Docker allows you to package and run your tested code in a consistent environment
- Keeping code modular and independent improves testability

---

### 📌 Best Practices for Unit Testing in MLOps

| Practice            | Benefit                                 |
|---------------------|------------------------------------------|
| Use mocks           | Avoid relying on real models or APIs     |
| One assert per test | Makes failures clearer                   |
| Keep tests fast     | Encourages frequent testing              |
| Name tests clearly  | Improves readability                     |
| Automate with CI    | Ensures reliability over time            |

---

### 🛠 Tools Used

- `pytest` for unit testing
- `Docker` for containerization
- AWS environment variables for Kinesis stream simulation

---

## 🔗 Integration Testing

In addition to unit testing, we implemented **integration testing** to validate the end-to-end functionality of the streaming service inside Docker containers.

Key steps include:

- Downloading the trained model from S3
- Refactoring the code to load the model locally
- Mounting the model into the container at runtime
- Running the service and validating predictions through tests
- Automating the entire process with a shell script

📁 You can find the detailed steps and commands in the [integration-test/README.md](integration-test/README.md).

---

## 🧼 Linting and Formatting

To maintain clean, consistent, and production-ready Python code, we adopted best practices around **linting** and **formatting**.

- **Linting** helps catch common errors and enforce code style by analyzing code statically.
- **Formatting** tools automatically structure code to follow standardized conventions like PEP8.

We used tools like `pylint`, `black`, and `isort`, and centralized configuration in `pyproject.toml` for easier project management.

🔗 [Read full guide on linting and formatting →](linting_and_formatting.md)

---

## 🔒 Git Pre-commit Hooks

To ensure consistent code quality and prevent accidental commits with formatting or linting issues, we’ve integrated **Git pre-commit hooks** using the [`pre-commit`](https://pre-commit.com/) framework.

These hooks automatically run tools like `isort`, `black`, `pylint`, and `pytest` **before every commit**, making our workflow more reliable and automated.

🔗 [Read full guide on pre-commit hooks →](pre_commit_hooks.md)

---
## 🧱 Makefiles and `make`

To automate repetitive tasks like testing, linting, building Docker images, running integration tests, and publishing, we use **Makefiles** with the `make` tool.

This acts as a lightweight orchestrator for our development and deployment workflow. It ensures tasks run in the right order with a single command, helping us maintain consistency across local development and CI/CD pipelines.

🛠️ With just one command, you can:

- Run tests: `make test`
- Check code quality: `make quality_checks`
- Build Docker images: `make build`
- Run integration tests: `make integration_test`
- Publish models: `make publish`

🔗 [Read full guide on Makefiles and `make` →](./make_and_makefiles.md)

---

## ☁️ Infrastructure as a Code with Terraform

To provision and manage cloud resources like Kinesis, S3, Lambda, ECR, and IAM, we use **Terraform** — an Infrastructure as Code (IaC) tool.

Terraform enables us to declaratively define infrastructure using version-controlled code, allowing automated, consistent, and repeatable deployments across environments.

🛠️ With just a few commands, we can:

- Initialize Terraform: `terraform init`
- Preview planned changes: `terraform plan`
- Apply infrastructure updates: `terraform apply`
- Tear down infrastructure: `terraform destroy`

🔗 [Read full guide on Terraform and cloud infrastructure setup →](./infrastructure/README.md)


---

Happy Testing & Best-Practices!! 🚀
---
