import sys
import pickle
import pandas as pd


def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    return dv, model

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    return df

def prepare_dictionaries(df):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    dicts = df[categorical].to_dict(orient='records')
    
    return dicts


def apply_model(input_file, year, month, output_file):
    print(f"reading the data from {input_file}...")
    df = read_data(input_file)

    dicts = prepare_dictionaries(df)
    
    print(f"loading the model from local path")
    dv, model = load_model()
    
    X_val = dv.transform(dicts)
    
    print("applying the model ...")
    y_pred = model.predict(X_val)
    # print(f"Q1: standard deviation of prediction: {round(y_pred.std(), 2)}")
    print("Q5: Mean predicted duration:", round(y_pred.mean(), 2))


    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    print(f"saving the results to {output_file}")
    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

def run():
    year = int(sys.argv[1])  # 2021
    month = int(sys.argv[2])  # 3
    taxi_type = 'yellow' # 'green'

    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    output_file = f"output/{taxi_type}_{year:04d}-{month:02d}.parquet"

    apply_model(input_file=input_file,
                year= year, 
                month= month, 
                output_file=output_file)


if __name__ == "__main__":
    run()

# Run the script from terminal
# python managed_script.py 2021 2 
