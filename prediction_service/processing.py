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


def process_input(title, content):
    config = read_params("params.yaml")
    cv1 = joblib.load(os.path.join(
        config["processing"], "count-vectorizer.pkl"))
    tfidf1 = joblib.load(os.path.join(
        config["processing"], "tfidf-vectorizer.pkl"))
    text_data = title + "---" + content
    cv_output = cv1.transform([text_data])
    tfidf_output = tfidf1.transform(cv_output)
    return tfidf_output.toarray()
