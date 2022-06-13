import argparse
import pandas as pd
from get_data import read_params
import argparse
from nltk.corpus import 

def get_data(config_path):
    config = read_params(config_path)
    data_path = config["load_data"]["raw_dataset_csv"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    return df

def processing(config_path):
    config = read_params(config_path=config_path)
    df = get_data(config_path=config_path)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    processing(config_path=parsed_args.config)