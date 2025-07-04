# Deployment
# MLOps Zoomcamp — Deployments Module

This README summarizes the Deployments module of the MLOps Zoomcamp. It explains different deployment strategies, how web services function, and how to serve models using MLflow.

### Quick recap:

We've learned how to rewrite our training into a workflow. Now we'll study how to deploy the resulting model.
## 🚀 Model Deployment Strategies

- There are primarily two kinds of deployments:
    1. Batch (offline) - runs regularly
    2. Online - Up & running all the time with two sub-options:
        1. Web service
        2. Streaming

### 1️⃣ Batch (Offline) Deployment
- A batch mode "scores" data based on a pre-trained model on a regular interval (e.g. hourly, daily, monthly)
- This is used for use cases where the activities it supports are not happening in real time but can be batched
- It **pulls data from a database**, scores it, and generates predictions.
- Typical workflow: `Database → Scoring Job (Model) → Predictions → Reports`
- Example scenarios:
  - A daily job pulls data from **yesterday**.
  - An hourly job pulls data from the **previous hour**.
- Common use cases:
  - Marketing analytics
  - Customer churn analysis
  - Scheduled reporting

### 2️⃣ Online Deployment (Web Service)
- The duration prediction we've been exploring is a perfect use case for a prediction that can be returned by making a call to a "Ride Duration Prediction Service"
- This relationship produces a 1:1 relationship between the client ```(BackendService)``` and the server ```(DurationPredictionService)```  to process the client requests.
- The model is deployed as a **web service** that runs continuously to handle real-time requests.
- Suitable for scenarios where **instant predictions** are required.
- Example: Taxi ride duration prediction service  
  `User → Backend → Duration Model → Immediate Response`
- Often implemented using:
  - **Flask**: Handles routing and prediction logic.
  - **Gunicorn**: Runs multiple Flask worker processes to handle concurrent requests efficiently.

#### ⚙️ How Flask and Gunicorn Work
- **Flask** is a lightweight Python web framework that defines routes and handles incoming HTTP requests for predictions.
- **Gunicorn** is a production-grade WSGI server that runs multiple worker processes to handle requests in parallel.
- Together they provide a scalable and efficient web service: `Client Request → Gunicorn → Flask App → Model Inference → Response`

### 3️⃣ [Streaming Deployment](./Streaming)
- Involves a **producer-consumer architecture** where data continuously flows through the system.
- In the streaming use case, the concept builds on web service by decoupling the client from the server and establishing a many:many relationship between ```Producers``` and ```Consumers```
- Producers create events, and consumers have to react to these events. Usually it's a one-to-many or a many-to-many relationship between producers and consumers.
- Different from web services — data is not requested on demand, but consumed as it arrives.
- Example: `Producer (e.g., sensor, app) → Stream (e.g., Kafka, Kinesis) → Consumer (Model Scoring)`
- Common use cases:
  - if a ride starts, then a ride duration predictor will keep updating, there's also a tip predictor.
  - Real-time fraud detection
  - Event-driven predictions

---

## 🌟 Serving Models with MLflow
- Models are trained and registered in the **MLflow Model Registry**.
- We can load the model directly from the registry or from a local path / S3 location.
- Typical process:
  1. Train the model and log it to MLflow.
  2. Download the model (and preprocessor if needed, e.g., `dv`).
  3. Serve the model using `mlflow.pyfunc` for prediction.

- To simplify deployment, we trained the model as a pipeline so we no longer need to handle the **Dictionary Vectorizer (dv)** separately during inference.

- **What if the MLflow server is down?**
  - If the server is down, web services depending on it will fail to load the model.
  - A common mitigation is to load the model from a **local file system** or a **cloud storage location (e.g., S3)** to ensure continued service availability.

