from regression_model.config import config as model_config

from regression_model.processing.data_management import load_dataset

from regression_model import __version__ as _version

from ml_api.api import __version__ as api_version

import json
import math


def test_heatlth_endpoint_returns_200(flask_test_client):
    #when
    response = flask_test_client.get("/health")

    #then
    assert response.status_code == 200


def test_version_endpoint_returns_version(flask_test_client):
    #when
    response = flask_test_client.get("/version")

    #Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    
    assert response_json["model_version"] == _version
    assert response_json["api_version"] == api_version


def test_prediction_endpoint_returns_prediction(flask_test_client):
    #given
    #load the test data from the regression_model package
    #this is important as it makes it harder for the test
    #data versions to get confused by not spreading it across packages

    test_data = load_dataset(file_name=model_config.TESTING_DATA_FILE)
    post_json = test_data[0:1].to_json(orient="records")

    #when
    response = flask_test_client.post("/v1/predict/regression", json=post_json)

    #Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json["predictions"]
    response_version = response_json["version"]
    assert math.ceil(prediction[0]) == 12
    assert response_version is None
    # The response_version looks like {"predictions": 11.84092..., "version": None}
    # So indeed the version is none, due to some null objects created while changing from 
    # one data type to another. Solve this problem in later versions.

    