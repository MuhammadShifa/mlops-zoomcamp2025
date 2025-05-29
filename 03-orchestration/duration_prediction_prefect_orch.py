import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
import mlflow
import mlflow.sklearn
import pickle
from pathlib import Path
from prefect import flow, task
import argparse

@task
def read_data(year: int, month: int):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    df = pd.read_parquet(url)
    print(f"[Q3] Number of records loaded: {len(df)}")
    return df

@task
def prepare_data(df):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    print(f"[Q4] Records after filtering: {len(df)}")
    return df

@task
def train_model(df):
    categorical = ['PULocationID', 'DOLocationID']
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    y_train = df['duration'].values

    model = LinearRegression()
    model.fit(X_train, y_train)

    print(f"[Q5] Model intercept: {model.intercept_:.2f}")
    return dv, model

@task
def log_model(dv, model):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("nyc-taxi-hw3")

    with mlflow.start_run() as run:
        mlflow.log_param("model_type", "LinearRegression")

        with open("dict_vectorizer.pkl", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("dict_vectorizer.pkl")

        mlflow.sklearn.log_model(model, artifact_path="model")

        run_id = run.info.run_id
        print("[Q6] Model logged to MLflow")
        print(f"MLflow Run ID: {run_id}")

        with open("run_id.txt", "w") as f:
            f.write(run_id)

@flow
def main(year: int, month: int):
    df_raw = read_data(year, month)
    df_prepared = prepare_data(df_raw)
    dv, model = train_model(df_prepared)
    log_model(dv, model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True, help="Year of the data")
    parser.add_argument("--month", type=int, required=True, help="Month of the data")
    args = parser.parse_args()

    main(args.year, args.month)