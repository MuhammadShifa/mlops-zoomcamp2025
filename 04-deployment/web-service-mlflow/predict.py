import pickle
import mlflow
from mlflow.tracking import MlflowClient

from flask import Flask, request, jsonify

# this will never work if mlflow server is down
# MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

RUN_ID = 'f12de8218f6d4711a2902c7d4581aac2'

# if server is down, directly point to the location locally s3 etc.
logged_model = f'/home/mshifa/workspace/zoomcamp/repo_clone/mlops-zoomcamp2025/mlartifacts/496409895171607791/{RUN_ID}/artifacts/model'
# logged_model = f'runs:/{RUN_ID}/model' # if mlflow tracking server is available
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)