import sys
import pickle

import pandas as pd


def read_data(filename, categorical, storage_options=None):
    df = pd.read_parquet(filename, storage_options=storage_options)
    return prepare_data(df, categorical)


def prepare_data(df, categorical):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


def save_data(df_result, output_file, storage_options=None):
    df_result.to_parquet(
        output_file, engine='pyarrow', index=False, storage_options=storage_options
    )


def main(year, month, storage_options=None):
    input_file = f's3://nyc-duration/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file_path = (
        f's3://nyc-duration/taxi_type=yellow_year={year:04d}_month={month:02d}.parquet'
    )

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(input_file, categorical, storage_options)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(df_result, output_file_path, storage_options)


if __name__ == "__main__":
    input_year = int(sys.argv[1])
    input_month = int(sys.argv[2])

    # Optional: check if running under integration test with S3/LocalStack
    use_localstack = True  # Set False if not testing
    if use_localstack:
        storage_opts = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}
    else:
        storage_opts = None

    main(input_year, input_month, storage_opts)
