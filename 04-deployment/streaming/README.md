
# Model Deployment through Streaming

This project demonstrates deploying a machine learning model using **AWS Lambda** and **Amazon Kinesis** for real-time streaming predictions.

---

## Scenario

We aim to:
- Create IAM roles and permissions
- Create a Lambda function
- Create Kinesis streams for input and output
- Connect Lambda to Kinesis as a trigger
- Send and process records through the stream
- Read predictions from the output stream

Link
- [Tutorial: Using Amazon Lambda with Amazon Kinesis](https://docs.amazonaws.cn/en_us/lambda/latest/dg/with-kinesis-example.html)

---

## Steps

### Login & Setup

- Login to AWS Console.
- SSH into an EC2 instance (used to run AWS CLI commands).

### Create Lambda Function

- Name: `ride-duration-prediction-test`
- Deploy the Lambda function.

### Create IAM Role

- Create a role named: `lambda-kinesis-role`
- Attach policies for Lambda to access Kinesis

### Create Input Kinesis Streams

- Input stream: `ride_events`
- Attached the role created

### Connect Lambda to Kinesis

- Set up an event source mapping to trigger Lambda from `ride_events`.

---

## ✅ Send Data to Kinesis

From the EC2 shell, run:

```bash
KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
  --stream-name ${KINESIS_STREAM_INPUT} \
  --partition-key 1 \
  --data fileb://<(echo -n 'Final test record')
```

✅ Check CloudWatch logs to confirm encoded data:

```json
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49664824644643310713708959161081702737227201669809307650",
                "data": "RmluYWwgdGVzdCByZWNvcmQ=",
                "approximateArrivalTimestamp": 1751536173
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49664824644643310713708959161081702737227201669809307650",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::259959202267:role/lambda-kinesis-role",
            "awsRegion": "ap-south-1",
            "eventSourceARN": "arn:aws:kinesis:ap-south-1:259959202267:stream/ride_events"
        }
    ]
}
```

---

### Update Lambda Code to Decode and Print Data

Decoding base64
```python
base64.b64decode(encoded_data).decode('utf-8')
```

Example snippet:

```python
for record in event['Records']:
    encoded_data = record['kinesis']['data']
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    print(decoded_data)
```
#### Test Event
```Json
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49664824644643310713708959161081702737227201669809307650",
                "data": "RmluYWwgdGVzdCByZWNvcmQ=",
                "approximateArrivalTimestamp": 1751536173
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49664824644643310713708959161081702737227201669809307650",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::259959202267:role/lambda-kinesis-role",
            "awsRegion": "ap-south-1",
            "eventSourceARN": "arn:aws:kinesis:ap-south-1:259959202267:stream/ride_events"
        }
    ]
}
```
Check the execution results, we will have decoded data

---

#### Record example
```json
{
    "ride": {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    }, 
    "ride_id": 123
}
```

Sending this Record to Kinesis

```bash
aws kinesis put-record \
  --stream-name ${KINESIS_STREAM_INPUT} \
  --partition-key 1 \
  --data fileb://<(echo -n '{"ride": {"PULocationID": 130, "DOLocationID": 205, "trip_distance": 3.66}, "ride_id": 156}')
```

✅ Example CloudWatch output:

```json
"data": "eyJyaWRlIjogeyJQVUxvY2F0aW9uSUQiOiAxMzAsICJET0xvY2F0aW9uSUQiOiAyMDUsICJ0cmlwX2Rpc3RhbmNlIjogMy42Nn0sICJyaWRlX2lkIjogMTU2fQ=="
```
#### Test event
```json
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49630081666084879290581185630324770398608704880802529282",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
                "approximateArrivalTimestamp": 1654161514.132
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49630081666084879290581185630324770398608704880802529282",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::XXXXXXXXX:role/lambda-kinesis-role",
            "awsRegion": "eu-west-1",
            "eventSourceARN": "arn:aws:kinesis:eu-west-1:XXXXXXXXX:stream/ride_events"
        }
    ]
}
```
---

## ✅ Reading Data from Output Stream

#### Create Output Kinesis Stream
- Output stream: `ride_prediction`
- Create the `write` policy to Kinesis Stream
- Attach the write policy to `lambda-kinesis-role`

### Update Lambda Code to Send data to Output Stream

- Updated code to call `PutRecord` on the `ride_predictions` stream.
- Ensure a policy is attached to `lambda-kinesis-role` that allows:
  - `kinesis:PutRecord`
  - `kinesis:PutRecords`
  on `ride_predictions` stream.


### Read Data from Output Kinesis Stream

```bash
KINESIS_STREAM_OUTPUT='ride_prediction'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
  get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${KINESIS_STREAM_OUTPUT} \
    --query 'ShardIterator' \
    --output text)

# Read encoded data
echo $SHARD_ITERATOR

# pretty-print JSON
echo $SHARD_ITERATOR | jq

# Get records in a RESULT
RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

# Decode and pretty-print JSON
echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode | jq
```

---

## ✅ Configuring Model Prediction with Trained Model locally

- Brought the Lambda code to the local system for testing.
- Created and tested a script locally.
- Exported environment variables:

```bash
export PREDICTIONS_STREAM_NAME="ride_prediction"
export RUN_ID="e1efc53e9bd149078b0c12aeaa6365df"
export TEST_RUN="True"
```

- Run the local test:

```bash
python test.py
```

➡ **Result:** Everything worked as expected.

---

## 🐳 Dockerizing the Model

- Created a virtual environment:

```bash
pipenv install boto3 mlflow==2.22.0 numpy==1.21.5 scikit-learn==1.0.2 --python=3.9
```

- Created a `Dockerfile`.
- Used a base image from [**AWS ECR Public Gallery**](https://gallery.ecr.aws/lambda/python).

- Built the Docker image:

```bash
docker build -t stream-model-duration:v1 .
```

- Ran the Docker image:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_prediction" \
    -e RUN_ID="55b250328b3343f0a08b8a97a15707bf" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    stream-model-duration:v1
```

- **URL for testing:**

```
http://localhost:8080/2015-03-31/functions/function/invocations
```

- Run the docker testing script:

```bash
python test_docker.py
```

### 🚀 Publishing Docker Image to AWS ECR

- Created a repository:

```bash
aws ecr create-repository --repository-name duration-prediction-model
```
output:/
Note the `repositoryUri` from Json output

- Logged in to ECR:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
```

- Tagged and pushed the image:

```bash
REMOTE_URI="noted_repositoryUri"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}
LOCAL_IMAGE="stream-model-duration:v1"

docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}
```

✅ Confirmed:

```bash
echo $REMOTE_IMAGE
# ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/duration-prediction-model:v1
```

---

### 🔑 Using Image in Lambda

- Created a new Lambda function **from container image** using the ECR REMOTE_IMAGE URL.
- Name: `ride-duration-prediction`
- Delete the old Lambda function `ride-duration-prediction-test`
- Created a policy for **S3 read access**:
  - Actions: `Get*`, `List*`
  - Resource: Specific bucket and object ARNs.

- Set environment variables for Lambda Configuration:

```
PREDICTIONS_STREAM_NAME
RUN_ID
```

### Testing in Lambda

- Created a **test event** in Lambda console.
- Sent data through **bash command** and test event JSON.
- Monitored results in **CloudWatch / Watchdog**.
- Increased Lambda **RAM memory** and **timeout** as needed.

---

✅ **Conclusion:** Successfully deployed and tested model streaming via Docker + Lambda + Kinesis + S3 integration.

---
