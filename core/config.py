from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config"


def load_config(name: str):

    config_path = CONFIG_DIR / f"{name}.yaml"

    with open(config_path, encoding="utf-8") as config:

        data = yaml.safe_load(config)

        filtered_config = {}

        if data is not None:

            for key, value in data.items():

                if not key.startswith("_"):

                    filtered_config[key] = value

        return filtered_config
    