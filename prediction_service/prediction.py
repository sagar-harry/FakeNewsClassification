import yaml
import joblib
import numpy as np
import os
import json

params_path = "params.yaml"
webapp_root = "webapp"


class NotAString(Exception):
    def __init__(self, message="Either or both title and text are not a string"):
        self.message = message
        super().__init__(self.message)


class NotAValidValue(Exception):
    def __init__(self, message="Text is empty"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(title, content):
    if validate_input(title=title, content=content):
        config = read_params(params_path)
        model_dir_path = config["prediction"]["final-model"]
        model = joblib.load(model_dir_path)
        prediction = model.predict([title+"---"+content])
        return prediction[0]
    else: return -1


def validate_input(title, content):
    if (title.isnumeric() or content.isnumeric()):
        raise NotAString
    elif (len(content) == 0):
        raise NotAValidValue
    else: return True


def api_response(request):
    try:
        title, content = request.json.values()
        response = "FAKE NEWS"
        model_output = predict(title, content)
        if model_output == 1:
            response = "REAL NEWS"
        elif model_output == -1:
            response = "Not a valid input"
        response_ = {"response": response}
        return response_
    except Exception as e:
        return {"error": str(e)}
