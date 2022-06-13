import pandas as pd
import argparse
from get_data import read_params
import numpy as np

def get_data(config_path):
    config = read_params(config_path=config_path)
    data_path = config["load_data"]["raw_dataset_csv"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    return df

def pre_processing(config_path):
    config = read_params(config_path=config_path)
    df = get_data(config_path=config_path)
    df["text"] = df["title"] + "---" + df["text"]
    df = df.drop(["title", "Unnamed: 0"], axis=1)
    df["label"] = np.where(df["label"].str.contains("REAL"), 1, 0)
    df.to_csv(config["pre_processing"]["pre-processed_csv"], index=False, sep=",")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    pre_processing(config_path=parsed_args.config)