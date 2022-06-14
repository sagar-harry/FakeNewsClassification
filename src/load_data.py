# Read the data from data source
# Save it in data/raw

from get_data import read_params, get_data
import argparse


def load_and_save(config_path):
    config = read_params(config_path=config_path)
    df = get_data(config_path=config_path)
    new_cols = [col.strip() for col in df.columns]
    df.to_csv(config["load_data"]["raw_dataset_csv"],
              sep=",", columns=new_cols, index=False)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = load_and_save(parsed_args.config)
