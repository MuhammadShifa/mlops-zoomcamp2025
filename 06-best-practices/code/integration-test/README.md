# 🚀 Integration Testing for Model Streaming Service

This module focuses on **Integration Testing** of our ML model service. Unlike unit tests that isolate individual components, integration tests ensure that various parts of the system work together as expected — especially when Docker, environment variables, model loading, and external services are involved.

---

## 📁 Folder Structure

```bash
integration-test/
├── test_docker_test.py     # Integration test script
├── run.sh                  # Automation script to build, run and test
├── docker-compose.yml      # Docker Compose file to simplify container setup
└── model/                  # Locally downloaded model from S3
```

---

## ✅ Steps Performed

1. 📂 **Created `integration-test` Directory**  
   A new folder `integration-test` was created, and the `test_docker.py` file was added using the same code from the unit testing module.

2. ☁️ **Downloaded Model from S3**  
   To avoid runtime dependency on S3, we downloaded the model manually with:

   ```bash
   aws s3 cp --recursive s3://mlartifact-s3/1/55b250328b3343f0a08b8a97a15707bf/artifacts/model/ model
   ```

   Check the size of the model directory:

   ```bash
   ls -lh model
   ```

3. 🔧 **Refactored Code to Remove S3 Dependency**  
   The service code was updated to load the model from a local path (`/app/model`) instead of fetching from S3 at runtime. This makes integration tests faster, more reliable, and independent of cloud connectivity.

4. ✅ **Build Docker Image**

```bash
docker build -t stream-model-duration:v2 .
```

5. ✅ **Run Docker Container**
    
   The container was run with the model directory mounted into it:

   ```bash
   docker run -it --rm \
     -p 8080:8080 \
     -e PREDICTIONS_STREAM_NAME="ride_predictions" \
     -e RUN_ID="Test123" \
     -e MODEL_LOCATION="/app/model" \
     -e TEST_RUN="True" \
     -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
     -v $(pwd)/model:/app/model \
     stream-model-duration:v2
   ```

6. 🧪 **Run Docker Test**  
   We tested the running container using:

   ```bash
   pipenv run python test_docker_test.py
   ```

   All tests passed successfully.

7. ⚙️ **Created Automation Script: `run.sh`**  
   To streamline the process, we created a shell script to automate:

   - Docker image build  
   - Container run via Docker Compose  
   - Test execution  
   - Clean-up

   Make the script executable:

   ```bash
   chmod +x integration-test/run.sh
   ```

   Run it with:

   ```bash
   ./integration-test/run.sh
   ```
## 🧠 Summary

This integration test ensures our full streaming service works end-to-end inside a container, independent of external cloud services, and is reproducible locally with Docker.

---

## 🔁 Integration Test with Kinesis (Testing Cloud Services with LocalStack)

In the earlier integration test, we validated the model and container behavior but **did not test the Kinesis part**. This section focuses on testing **AWS Kinesis integration using LocalStack**, a local AWS cloud emulator.

---

### 🧱 Setting Up LocalStack via Docker Compose
Before starting integration with Kinesis, we updated the `docker-compose.yml` file to include a new service for [**LocalStack**](https://docs.localstack.cloud/aws/getting-started/installation/#docker-compose), which emulates AWS services locally. We configured it to enable the Kinesis service.

We use Docker Compose to start only the required `kinesis` service from `docker-compose.yaml`.

To start just the Kinesis service and test how it works:

```bash
docker-compose up kinesis
```

> 🔹 This will pull the necessary image from Docker Hub and start only the `kinesis` container.

---

### 🔍 Verifying Local Kinesis Setup with AWS CLI

Initially, there are no Kinesis streams:

```bash
aws kinesis list-streams
```

**Output:**
```json
{
  "StreamNames": [],
  "StreamSummaries": []
}
```

But this command points to real AWS. To point to LocalStack instead:

```bash
aws --endpoint-url=http://localhost:4566 kinesis list-streams
```

**Output:**
```json
{
  "StreamNames": []
}
```

---

### ⚙️ Creating a Stream in LocalStack

To create a new Kinesis stream:

```bash
aws --endpoint-url=http://localhost:4566 \
  kinesis create-stream \
  --stream-name ride_predictions \
  --shard-count 1
```

Verify it again:

```bash
aws --endpoint-url=http://localhost:4566 kinesis list-streams
```

**Output:**
```json
{
  "StreamNames": ["ride_predictions"]
}
```

> ✅ This confirms that the stream exists only in LocalStack, not in actual AWS.

---

### 🛠 Updating Code to Use LocalStack

To redirect the app to LocalStack instead of AWS:

- Define a new environment variable in `docker-compose.yml`:
  
```yaml
KINESIS_ENDPOINT_URL=http://kinesis:4566/
```

- Update `model.py` and create a method like `create_kinesis_client()` that uses this endpoint.
- Modify the Docker service definition and scripts to use the updated variable.

---

### 🔄 Updating `run.sh` and `test_kinesis.py`

We:

- Added the stream creation command to `run.sh`
- Created `test_kinesis.py` to validate the Kinesis stream behavior
- Updated `run.sh` to execute this test after starting services

Run everything with:

```bash
./integration-test/run.sh
```

> 🐳 The Docker container **must stay running** during Kinesis testing.

---

### 📡 Exploring Kinesis Stream

Get the `shardId` (usually `shardId-000000000000`):

```bash
SHARD='shardId-000000000000'
```

Get a shard iterator:

```bash
aws --endpoint-url=http://localhost:4566 kinesis get-shard-iterator \
  --shard-id ${SHARD} \
  --shard-iterator-type TRIM_HORIZON \
  --stream-name 'ride_predictions' \
  --query 'ShardIterator' \
  --output text
```

Use the iterator to fetch records:

```bash
aws --endpoint-url=http://localhost:4566 kinesis get-records --shard-iterator <output-from-above>
```

If the data is encoded, decode it:

```bash
echo "<base64-string>" | base64 -d
```

> This gives the prediction message sent through the local Kinesis stream.

---

### 🧪 Automating Kinesis Test

We added a new file `test_kinesis.py` to automate the above steps.  
`run.sh` was updated to:

- Build and run containers
- Create the stream
- Run both `test_docker_test.py` and `test_kinesis.py`

---

## ✅ Summary of Testing Types

1. **Unit Testing**  
   Run from `code` directory:
   ```bash
   pipenv run pytest ./tests
   ```

2. **Integration Testing (Model + Kinesis + Container)**  
   Run from project root:
   ```bash
   ./integration-test/run.sh
   ```

---

All components — model, environment variables, container, and Kinesis — are now **fully tested locally** with automation using LocalStack. 🚀



### Reference:
- [Bash Shebange](https://linuxize.com/post/bash-shebang/)
- [Docker Compose](https://docs.docker.com/compose/)


