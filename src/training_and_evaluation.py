import argparse
import pandas as pd
from get_data import read_params

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score

import json
import os
import joblib

def get_data(config_path):
    config = read_params(config_path)
    data_path = config["split_data"]["train_path"]
    df_train = pd.read_csv(data_path, sep=",", encoding='utf-8')
    data_path = config["split_data"]["test_path"]
    df_test = pd.read_csv(data_path, sep=",", encoding='utf-8')
    return df_train, df_test

def eval_metrics(actual, predicted):
    accuracy_score = accuracy_score(actual, predicted)
    return accuracy_score

def model_train(config_path):
    config = read_params(config_path=config_path)
    df_train, df_test = get_data(config_path=config_path)
    C = config["estimators"]["model-1"]["params"]["C"]
    pipe = Pipeline([
                 ('vect', CountVectorizer()),
                 ('tfidf', TfidfTransformer()),
                 ('clf', LinearSVC(C=C))
    ])
    pipe.fit(df_train["text"],df_train["label"])
    prediction = pipe.predict(df_test["text"])
    accuracy_score = eval_metrics(df_test["label"], prediction)

    ##########################################
    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "accuracy_score": accuracy_score
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
            "C": C
        }
        json.dump(params, params_file, indent=4)

    model_dir = config["model-dir"]
    os.makedirs(model_dir, exists_ok=True)
    model_path = os.model.join(model_dir, "model-1.joblib")
    joblib.dump(pipe, open(model_path, "wb"))

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    model_train(config_path=parsed_args.config)
