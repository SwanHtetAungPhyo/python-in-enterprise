from pathlib import Path
from typing import Dict, Any

from utils import logger


class Settings:
    def __init__(self):
        self.data_path = Path("data/sample.json")
        self.encoding = 'utf-8'
        self.default_threshold = 0
        self.filter_mode = 'OK'

    def update_from_file(self, config_path: Path)-> None:
        if config_path.exists():
            try:
                import json
                with open(config_path,'r',encoding=self.encoding) as f:
                    data = json.load(f)
                self.__dict__.update(data)
            except Exception:
                logger.error(f"Failed to load config file: {config_path}")
                pass

    def update_from_args(self, args: Dict[str, Any]) -> None:
        if 'data_path' in args:
            self.data_path = Path(args['data_path'])
        if 'threshold' in args:
            self.default_threshold = args['threshold']
        if 'filter_mode' in args:
            self.filter_mode = args['filter_mode']


settings = Settings()