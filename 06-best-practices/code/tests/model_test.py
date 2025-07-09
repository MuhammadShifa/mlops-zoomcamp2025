import model


def test_base64_decode():
    input_base64 = "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ=="
    actual_results = model.base64_decode(input_base64)
    
    expected_results = {
            "ride": {
                "PULocationID": 130,
                "DOLocationID": 205,
                "trip_distance": 3.66
            }, 
            "ride_id": 256
    }

    assert actual_results == expected_results

def test_prepare_features():

    model_service = model.ModelService(None)
    ride = {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66,
            }

    actual_features = model_service.prepare_features(ride)

    expected_features = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }

    assert actual_features == expected_features


# Creates a fake (mock) model that always returns the prediction 10.0.
# This is useful for testing, so you don’t use a real model.class ModelMock:

class ModelMock():
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(10.0)
    # Creates a ModelService instance and gives it the fake model (model_mock) to use.
    # Now, any prediction made through model_service will use that mock.
    
    model_service = model.ModelService(model_mock) # we don't want the actually model tbe use from s3, test should be independent as possible
    features = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction
    
    
def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = 'Test123'
    
    event = {
        "Records": [
            {
            "kinesis": {
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
                },
            }]
        }

    model_service = model.ModelService(model_mock, model_version= model_version) # we don't want the actually model tbe use from s3, test should be independent as possible
    

    actual_prediction = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'ride_duration_prediction_model',
                'version': model_version,
                'prediction': {
                    'ride_duration': 10.0,
                    'ride_id': 256,
                },
            }
        ]
    }

    assert actual_prediction == expected_predictions
