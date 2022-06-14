from get_data import read_params
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split


def get_data(config_path):
    config = read_params(config_path=config_path)
    data_path = config["pre_processing"]["pre-processed_csv"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    return df


def train_test_split_data(config_path):
    config = read_params(config_path=config_path)
    df = get_data(config_path=config_path)
    x_train, x_test, y_train, y_test = train_test_split(df["text"], df["label"],
                                                        test_size=config["split_data"]["test_size"], random_state=config["split_data"]["random_state"])
    df_train = pd.DataFrame({"text": x_train.values, "label": y_train})
    df_test = pd.DataFrame({"text": x_test.values, "label": y_test})
    df_train.reset_index(inplace=True)
    df_test.reset_index(inplace=True)
    df_train.drop("index", axis=1, inplace=True)
    df_test.drop("index", axis=1, inplace=True)
    df_train.to_csv(config["split_data"]["train_path"])
    df_test.to_csv(config["split_data"]["test_path"])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_test_split_data(config_path=parsed_args.config)
