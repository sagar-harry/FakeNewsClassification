import os
import joblib
from zlib import DEF_BUF_SIZE
import numpy as np
import yaml
import pandas as pd
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def processing_input(df_train, df_test):
    config = read_params("params.yaml")
    cv1 = CountVectorizer(max_features=500000)
    tfidf1 = TfidfTransformer()
    df_train_cv = cv1.fit_transform(df_train.text)
    df_train_tfidf = tfidf1.fit_transform(df_train_cv)

    df_test_cv = cv1.transform(df_test.text)
    df_test_tfidf = tfidf1.transform(df_test_cv)

    joblib.dump(cv1, config["processing"]["count-vectorizer"])
    joblib.dump(tfidf1, config["processing"]["tfidf-transformer"])

    df_train_processed = pd.DataFrame(df_train_tfidf.toarray())
    df_test_processed = pd.DataFrame(df_test_tfidf.toarray())
    df_train_processed["label"] = df_train.label
    df_test_processed["label"] = df_test.label

    return df_train_processed, df_test_processed
