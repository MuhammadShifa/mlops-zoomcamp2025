import normal_predict

ride = {
    "PULocationID": 10,
    "DOLocationID": 50,
    "trip_distance": 40
}

features = normal_predict.prepare_features(ride)
pred = normal_predict.predict(features)
print(pred)
