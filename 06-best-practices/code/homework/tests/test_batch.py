from batch import prepare_data
from data_utils import get_sample_dataframe


def test_prepare_data_filters_and_transforms():

    df = get_sample_dataframe()

    categorical = ['PULocationID', 'DOLocationID']
    actual = prepare_data(df, categorical)

    # Should retain 2 rows
    assert len(actual) == 2

    # Optional: check that PULocationID is string
    assert actual['PULocationID'].dtype == 'object'
