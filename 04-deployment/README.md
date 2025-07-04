# MLOps Zoomcamp — Deployments Module

This README summarizes the Deployments module of the MLOps Zoomcamp. It explains different deployment strategies, how web services function, and how to serve models using MLflow.

### Quick recap:

We've learned how to rewrite our training into a workflow. Now we'll study how to deploy the resulting model.
## Model Deployment Strategies

- There are primarily two kinds of deployments:
    1. Batch (offline) - runs regularly
    2. Online - Up & running all the time with two sub-options:
        1. Web service
        2. Streaming

### [Batch (Offline) Deployment](./batch)
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

### [Online Deployment (Web Service)](./web-service)
- The duration prediction we've been exploring is a perfect use case for a prediction that can be returned by making a call to a "Ride Duration Prediction Service"
- This relationship produces a 1:1 relationship between the client ```(BackendService)``` and the server ```(DurationPredictionService)```  to process the client requests.
- The model is deployed as a **web service** that runs continuously to handle real-time requests.
- Suitable for scenarios where **instant predictions** are required.
- Example: Taxi ride duration prediction service  
  `User → Backend → Duration Model → Immediate Response`
- Often implemented using:
  - **Flask**: Handles routing and prediction logic.
  - **Gunicorn**: Runs multiple Flask worker processes to handle concurrent requests efficiently.

### [Streaming Deployment](./streaming)
- Involves a **producer-consumer architecture** where data continuously flows through the system.
- In the streaming use case, the concept builds on web service by decoupling the client from the server and establishing a many:many relationship between ```Producers``` and ```Consumers```
- Producers create events, and consumers have to react to these events. Usually it's a one-to-many or a many-to-many relationship between producers and consumers.
- Different from web services — data is not requested on demand, but consumed as it arrives.
- Example: `Producer (e.g., sensor, app) → Stream (e.g., Kafka, Kinesis) → Consumer (Model Scoring)`
- Common use cases:
  - if a ride starts, then a ride duration predictor will keep updating, there's also a tip predictor.
  - Real-time fraud detection
  - Event-driven predictions
A seperate README.md is provided for streaming [here](./streaming/README.md)
---
## [Deploying model as a web-service](web-service)
#### Steps

- Save the trained model
- Create a virtual environment
- Create a script for prediction
- Put the script into a Flask app
- Package the app to Docker image

#### Save the trained model
Here we are taking the same model, saved as a binary file, that was trained in previous model and put that in newly created web-service directory for this week.

#### Create a virtual environment
We need to have exact same version of Scikit-learn library that was used to create the model as well as same Python version in order to avoid any compatibility issue.

Go to the virtual environment in EC2 server or local conda envrironment where the model was trained and run the following command.
```bash
pip freeze | grep scikit-learn
python --version
```

With pipenv create a new virtual environment.
```bash
pipenv install scikit-learn==1.0.2 flask --python=3.9
```
Activate the environment.
```bash
pipenv shell
```

#### Create a script for prediction

First we create a script that loads the saved model, preprocesses the input data and generates prediction.

[Predict script without flask](./web-service/normal_predict.py)\
[Test script to test predict script](./web-service/normal_test.py)

The idea is to create a working script that can take input in original format and generate the prediction result.

#### Put the script into a Flask app

Note: Rename the files from predict_without_flask.py to predict.py and test_without_flask.py to test.py and make a flask application from these files.
Now that we have the working predict.py script ready, we can build a web-service around it so that we can expose it to an HTTP endpoint.

Note: Current flask set up is for the development environment. Install gunicorn and configure in order to solve the following production environment type warning.
```bash
pipenv install gunicorn
gunicorn --bind=0.0.0.0:9696 predict:app
```
```
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
```
Note: our Flask application is ready to dockerized


#### Package the app to Docker
- Create Dockerfile with necessary content.
- Run the following command to build docker image
```bash
docker build -t ride-duration-prediction-service:v1 .
```
- Run the following command to run the image
```
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
```
This will deploy the webserive on localhost and we can run the test.py script again to test.
The model was directly used from the local path, in next step we will load the model from Mlflow model registry.


## [Serving Models with MLflow](./web-service-mlflow)
- Models are trained and registered in the **MLflow Model Registry**.
- We can load the model directly from the registry or from a local path or S3 location.
- Typical process:
  1. Train the model and log it to MLflow.
  2. Download the model (and preprocessor if needed, e.g., `dv`).
  3. Serve the model using `mlflow.pyfunc` for prediction.

- To simplify deployment, we trained the model as a pipeline so we no longer need to handle the **Dictionary Vectorizer (dv)** separately during inference.

- **What if the MLflow server is down?**
  - If the server is down, web services depending on it will fail to load the model.
  - A common mitigation is to load the model from a **local file system** or a **cloud storage location (e.g., S3)** to ensure continued service availability.


