import argparse
import pandas as pd
from get_data import read_params

from processing_input import processing_input

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
    model_accuracy_score = accuracy_score(actual, predicted)
    return model_accuracy_score


def model_train(config_path):
    config = read_params(config_path=config_path)
    df_train, df_test = get_data(config_path=config_path)
    df_train, df_test = processing_input(df_train=df_train, df_test=df_test)

    C = config["estimators"]["model-1"]["params"]["C"]

    clf = LinearSVC(C=C)
    clf.fit(df_train.iloc[:, :-1], df_train.iloc[:, -1])

    prediction = clf.predict(df_test.iloc[:, :-1])
    model_accuracy_score = eval_metrics(df_test["label"], prediction)
    model_dir = config["model-dir"]
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model-1.joblib")
    joblib.dump(clf, open(model_path, "wb"))


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    model_train(config_path=parsed_args.config)
