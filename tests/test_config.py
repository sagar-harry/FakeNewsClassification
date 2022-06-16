import pytest
from prediction_service import prediction
import json

input_data = {
    "incorrect_values":
    {"title": "123", 
    "content": "Donald trup resigns as president of USA"},

    "correct_value":
    {"title":"Breaking news!!",
    "content": "Donald trup resigns as president of USA"},

    "incorrect_input":
    {"title": "",
    "content": ""}
}

TARGET_VALUES_FORM = {
    "response": [1, 0]
}

TARGET_VALUES_API = {
    "response": ["REAL NEWS", "FAKE NEWS"]
}

TARGET_VALUES_INCORRECT_API = {
    "response": ["Text is empty"]
}



def test_api_response_correct_input(data=input_data["correct_value"]):
    res = prediction.api_response(data)
    print("Sagar"*100)
    print(res)
    assert res["response"] in TARGET_VALUES_API["response"]

def test_form_response_correct_input(data=input_data["correct_value"]):
    res = prediction.predict(data["title"], data["content"])
    assert res in TARGET_VALUES_FORM["response"]

def test_api_response_incorrect_input(data=input_data["incorrect_input"]):
    res = prediction.api_response(data)
    assert res["error"] in TARGET_VALUES_INCORRECT_API["response"]

def test_form_response_incorrect_input(data=input_data["incorrect_input"]):
    with pytest.raises(prediction.NotAValidValue):
        res = prediction.predict(data["title"], data["content"])