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

---

## 🧠 Summary

This integration test ensures our full streaming service works end-to-end inside a container, independent of external cloud services, and is reproducible locally with Docker.
