from dataclasses import dataclass
import re
import yaml
from pathlib import Path

path = Path(__file__).parent

class Config:

    def __init__(self, config_file) -> None:
        self.config_file = path.joinpath(config_file)

    def get(self, conf_item=None):
        with open(self.config_file) as f:
            conf = yaml.safe_load(f)

        if conf_item:
            return conf[conf_item]
        else:
            return conf

configuration = Config('config.yaml')