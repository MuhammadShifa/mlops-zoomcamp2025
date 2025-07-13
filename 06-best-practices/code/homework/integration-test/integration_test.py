import os

import pandas as pd
from data_utils import get_sample_dataframe


def save_data(df, output_file, options):
    df.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options,
    )


df_input = get_sample_dataframe()

# 2. Define S3 paths
input_file_path = "s3://nyc-duration/yellow_tripdata_2023-01.parquet"
output_file_path = "s3://nyc-duration/taxi_type=yellow_year=2023_month=01.parquet"

# 3. LocalStack S3 config
storage_options = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}

# 4. Save input file to S3
save_data(df_input, input_file_path, storage_options)

# 5. Run batch.py
os.system("python batch_q6.py 2023 1")

# 6. Read output file from S3 and verify result
df_output = pd.read_parquet(output_file_path, storage_options=storage_options)
print("Output dataframe:")
print(df_output)

print("Sum of predicted durations:", round(df_output['predicted_duration'].sum(), 2))
