Week 2 of MLOps Zoomcamp

Link to Course: https://github.com/DataTalksClub/mlops-zoomcamp

# Introduction to MLflow, ML experiments and model registry.

# 📘 Introduction to MLflow

**MLflow** is an open-source platform designed to manage the end-to-end machine learning lifecycle. It simplifies tracking experiments, packaging code into reproducible runs, and managing and deploying models.

## 📌 Important Concepts

- **ML Experiment**: The entire process of training and evaluating a machine learning model.
- **Experiment Run**: A single trial or execution of the ML experiment (with specific parameters, metrics, etc.).
- **Run Artifact**: Any file or output generated during the experiment run (e.g., model files, plots, metrics).
- **Experiment Metadata**: Contextual information about the run, such as:
  - Source code version
  - User name
  - Timestamp
  - Git commit hash
  - Notes and tags

---

## 🚀 Why MLflow?

Machine learning projects often involve:
- Multiple experiments with different hyperparameters
- Difficulties in tracking results
- Challenges in reproducing models

MLflow addresses these issues by providing a unified interface for:

- **Experiment Tracking**: Log parameters, metrics, and artifacts (e.g., models, plots) during training runs.
- **Model Management**: Save and version models using a consistent format.
- **Model Registry**: Organize models in different stages like Staging or Production.
- **Reproducibility**: Package code and environment with MLflow Projects.

---

## 🧩 MLflow Components

| Component          | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **MLflow Tracking** | Log parameters, metrics, tags, and artifacts for each experiment run       |
| **MLflow Models**   | Deployable, standardized format to package ML models                       |
| **MLflow Registry** | Central model store with versioning, stage transitions, and annotations    |
| **MLflow Projects** | Package data science code in a standard format for reproducibility(out of scope for this course)         |



## 🛠️ Getting Started

Install and run MLflow locally:
```bash
pip install mlflow
mlflow ui
```
---

## 📊 Experiment Tracking

**Experiment Tracking** is the process of keeping track of all relevant information associated with an ML experiment. This is essential for understanding what was done, reproducing results, and improving performance over time.

During an ML experiment, we typically log the following:

- **📄 Source Code**: The scripts, notebooks, and functions used for model training.
- **🌍 Environment**: The dependencies, packages, and their versions (e.g., Python, NumPy, Scikit-learn).
- **🗂️ Data**: The input dataset used during the training run.
- **🤖 Model**: The trained machine learning model and its architecture.
- **⚙️ Hyperparameters**: Settings like learning rate, batch size, number of estimators, etc.
- **📈 Metrics**: Evaluation results such as RMSE, accuracy, precision, etc.
- **📦 Artifacts**: Additional files such as plots, serialized models, or configuration files.

---

### 🧪 How It Works

Each experiment consists of **runs**. A *run* is one attempt at training a model.

You can log everything using MLflow like this:

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("alpha", 0.01)
    mlflow.log_metric("rmse", 2.56)
    mlflow.log_artifact("model.pkl")
```

---

## 🖥️ MLflow UI

MLflow provides a web-based User Interface (UI) to visualize and compare all your experiment runs. It makes it easier to analyze metrics, parameters, models, and artifacts in one place.

### 🚀 Running MLflow UI Locally

To launch the MLflow UI locally, run the following command:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
````
This command starts a local server and opens the MLflow dashboard at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 💾 Backend Store

The `--backend-store-uri` argument specifies the storage for the experiment metadata and tracking results. In this case:

- `sqlite:///mlflow.db` uses a SQLite database named `mlflow.db` in the current directory.
- This allows experiments and their logs to persist across different sessions.

You can also link this backend in your Python code using:

```python
import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
```

In addition to the backend URI, we can also add an artifact root directory where we store the artifacts for runs, this is done by adding a `--default-artifact-root` paramater:

```
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

### 📡 MLflow Tracking Client API

MLflow provides a Python API to interact programmatically with the tracking server.

This is useful when you want to:

- Log metrics, parameters, and artifacts
- Set experiment names
- Start and end runs
- Retrieve run information programmatically

In addition to the UI, an interface that is introduced in the course and used to automate processes is the Tracking API. Initialized through:
```python
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
```

the `client` is an object that allows managing experiments, runs, models and model registries (cf. Interacting with MLflow through the Tracking Client). 

## Creating new Experiments:

We create an experiment in the top left corner of the UI. (In this instance `nyc-new-brand-experiment_first`).

Using the Python API we use `client.create_experiment("nyc-new-brand-experiment_first")`.

## Tracking Single Experiment Runs with Mlflow in a Jupyter notebook or Python file:

In order to track experiment runs, we first initialize the mlflow experiment using the code:

```python
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-new-brand-experiment_first")
```
Or
```python
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("nyc-new-brand-experiment_first")
```

where we set the tracking URI and the current experiment name. In case the experiment does not exist, it will be automatically created.

We can then track a run, we'll use this simple code snippet as a starting point:

```python
alpha = 0.01

lr = Lasso(alpha)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_val)

mean_squared_error(y_val, y_pred, squared=False)
```
We initialize the run using
```python
with mlflow.start_run():
```
and wrapping the whole run inside it.
```python
with mlflow.start_run():
    
    mlflow.set_tag("developer", "moshifa")
    mlflow.log_param("tain data path","./data/green_tripdata_2021-01.parquet")
    mlflow.log_param("val data path", "./data/green_tripdata_2021-02.parquet")
    
    alpha = 0.01
    mlflow.log_param("alpha", alpha)

    lr = Lasso(alpha)
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_val)

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    mlflow.log_metric("rmse", rmse)
```

We track the relevant information using  three mlflow commands:
+ `set_tag` for Metadata tags
+ `log_param` for logging model parameters
+ `log_metric` for logging model metrics

In this instance, we may set as Metadata tags the author name, the model parameters as the training and validation data paths and alpha, and set the metric as RMSE:

In the MLflow UI, within the `nyc-new-brand-experiment_first` we now have a run logged with our logged parameters, tag, and metric.

Notebook is [here](./notebooks/duration_prediction/ipynb)
## Hyperparameter Optimizaiton Tracking:

By wrapping the `hyperopt` Optimization objective inside a `with mlflow.start_run()` block, we can track every optimization run that was ran by `hyperopt`. We then log the parameters passed by `hyperopt` as well as the metric as follows:

```python


import xgboost as xgb

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

train = xgb.DMatrix(X_train, label=y_train)
valid = xgb.DMatrix(X_val, label=y_val)
def objective(params):
    with mlflow.start_run():
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(params)
        booster = xgb.train(
            params=params,
            dtrain=train,
            num_boost_round=100,
            evals=[(valid, 'validation')],
            early_stopping_rounds=50
        )
        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

    return {'loss': rmse, 'status': STATUS_OK}
search_space = {
    'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
    'learning_rate': hp.loguniform('learning_rate', -3, 0),
    'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
    'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
    'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
    'objective': 'reg:linear',
    'seed': 42
}

best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=50,
    trials=Trials()
)

```

In this block, we defined the search space and the objective than ran the optimizer. We wrap the training and validation block inside `with mlflow.start_run()` and log the used parameters using `log_params` and validation RMSE using `log_metric`.

In the UI we can see each run of the optimizer and compare their metrics and parameters. We can also see how different parameters affect the RMSE using Parallel Coordinates Plot, Scatter Plot (1 parameter at a time) and Contour Plot.

## Autolog in MLflow: 

Autologging in MLflow simplifies experiment tracking by automatically logging parameters, metrics, artifacts, and more — without explicitly specifying them.

Instead of logging manually, MLflow’s `autolog()` function captures all essential data during model training, making it easier to manage and reproduce experiments.
 There are two ways to use Autologging; 
 #### 🔹 Enable Global Autologging

```python
mlflow.autolog()
```

#### 🔹 Enable Framework-Specific Autologging

You can also enable autologging for specific ML frameworks. For example, for XGBoost:

```python
import mlflow.xgboost

mlflow.xgboost.autolog()
```
Both must be done before running the experiments.

#### What Autolog Logs

When `mlflow.autolog()` is enabled, MLflow automatically tracks a wide range of training-related details:

- **Parameters**  
  All hyperparameters used during model training are recorded automatically.

- **Metrics**  
  Evaluation metrics such as accuracy, RMSE, F1-score, etc., are captured for easy comparison.

- **Artifacts**  
  MLflow saves several useful files:
  - `conda.yaml`: Defines the Conda environment used for reproducibility.
  - `requirements.txt`: Lists Python dependencies for pip-based environments.
  - `MLmodel`: Metadata describing how to load and use the model.
  
  **Model Binary**: The trained model file (e.g., `.pkl`, `.onnx`, etc.) is stored automatically.

- **Tags**  
  Metadata such as the username, source code version, Git commit hash, and more are added for traceability.

- **Environment Info**  
  Includes details such as:
  - Python version  
  - ML library versions (e.g., scikit-learn, XGBoost)

---

## Saving Models:

We may use MLflow to log whole models for storage (see Model Registry later), to do this we add a line to our `with mlflow.start_run()` block:

```python
mlflow.<framework>.log_model(model, artifact_path="models_mlflow")
```

where we replace the `<framework>` wih our model's framework (ex: `sklearn`, `xgboost`...etc).
The `artifact_path` defines where in the `artifact_uri` the model is stored.

We now have our model inside our `models_mlflow` directory in the experiment folder. (Using Autologging would store more data on parameters as well as the model. i.e: This is redundant when using the autologger)

## Saving Artifacts with the Model:

Sometimes we may want to save some artifacts with the model, for example in our case we may want to save the `DictVectorizer` object with the model for inference (subsequently testing as well). In that case we save the artifact as:
```python
mlflow.log_artifact("vectorizer.pkl", artifact_path="extra_artifacts")
```

Where `vectorizer.pkl` is the vectorizer stored in a Pickle file and `extra_artifacts` the folder within the artifacts of the model where the file is stored.

## Loading Models:

We can use the model to make predictions with multiple ways depending on what we need:
+ We may load the model as a Spark UDF (User Defined Function) for use with Spark Dataframes
+ We may load the model as a MLflow PyFuncModel structure, to then use to predict data in a Pandas DataFrame, NumPy Array or SciPy Sparse Array. The obtained interface is general for all models from all frameworks
+ We may load the model as is, i.e: load the XGBoost model as an XGBoost model and treat it as such

The first two methods are explained briefly in the MLflow artifacts page for each run, for the latter we may use (XGBoost example):
```python
logged_model = 'runs:/9245396b47c94513bbf9a119b100aa47/models' # Model UUID from the MLflow Artifact page for the run

xgboost_model = mlflow.xgboost.load_model(logged_model)
```
the resultant `xgboost_model` is an XGBoost `Booster` object which behaves like any XGBoost model. We can predict as normal and even use XGBoost Booster functions such as `get_fscore` for feature importance.


## Model Registry:

Just as MLflow helps us store, compare and deal with ML experiment runs. It also allows us to store Models and categoerize them. While it may be possible to store models in a folder structure manually, doing this is cumbersome and leaves us open to errors. MLflow deals with this using the Model Registry, where models may be stored and labeled depending on their status within the project.

### Storing Models in the Registry:

In order to register models using the UI, we select the run whose model we want to register and then select "Register Model". There we may either create a new model registry or register the model into an existing registry. We can view the registry and the models therein by selecting the "Models" tab in the top and selecting the registry we want.

### Promoting and Demoting Models in the registry:

Models in the registry are labeled either as Staging, Production or Archive. Promoting and demoting a model can be done by selecting the model in the registry and selecting the stage of the model in the drop down "Stage" Menu at the top.

## Interacting with MLflow through the Tracking Client:

In order to automate the process of registering/promoting/demoting models, we use the Tracking Client API initialized as described above:

```python
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
```

we can then use the client to interface with the MLflow backend as with the UI.

### Selecting runs:

We can search for runs by ascending order of metric score using the API by:

```python
from mlflow.entities import ViewType

runs = client.search_runs(
    experiment_ids='1',    # Experiment ID we want
    filter_string="metrics.rmse < 7",
    run_view_type=ViewType.ACTIVE_ONLY,
    max_results=5,
    order_by=["metrics.rmse ASC"]
)
```
We can then get information about the selected runs from the resulting `runs` enumerator:
```python
for run in runs:
    print(f"run id: {run.info.run_id}, rmse: {run.data.metrics['rmse']:.4f}")
```

### Interacting with the Model Registry:

We can add a run model to a registry using:
```python
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

run_id = "9245396b47c94513bbf9a119b100aa47"
model_uri = f"runs:/{run_id}/models"
mlflow.register_model(model_uri=model_uri, name="nyc-taxi-regressor")
```

we can get the models  in a model registry:
```python
model_name = "nyc-taxi-regressor"
latest_versions = client.get_latest_versions(name=model_name)

for version in latest_versions:
    print(f"version: {version.version}, stage: {version.current_stage}")
```

promote a model to staging:
```python
model_version = 4
new_stage = "Staging"
client.transition_model_version_stage(
    name=model_name,
    version=model_version,
    stage=new_stage,
    archive_existing_versions=False
)
```

update the description of a model:
```python
from datetime import datetime

date = datetime.today().date()
client.update_model_version(
    name=model_name,
    version=model_version,
    description=f"The model version {model_version} was transitioned to {new_stage} on {date}"
)
```

these can then be used to automate the promotion of packages into production or the archival of older models.
