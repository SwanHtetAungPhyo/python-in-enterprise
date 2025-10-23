import json
from pathlib import Path
from typing import List, Dict, Any
from models.records import Record
from config.settings import settings


class DataLoader:
    def __init__(self):
        self._cache = {}

    def load_records(self, file_path: Path = None) -> List[Record]:
        """Load records from JSON file."""
        if file_path is None:
            file_path = settings.data_path

        try:
            with open(file_path, 'r', encoding=settings.encoding) as f:
                raw_data = json.load(f)
            return self._parse_records(raw_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_fallback_data()

    def _parse_records(self, raw_data: List[Dict[str, Any]]) -> List[Record]:
        """Parse raw JSON data into Record objects."""
        records = []
        for item in raw_data:
            status = item.get('status', item.get('STATUS', 'unknown'))
            value = item.get('value', 0)
            records.append(Record(status=status, value=value))
        return records

    def _get_fallback_data(self) -> List[Record]:
        """Provide fallback data when file loading fails."""
        return [
            Record(status="ok", value="3"),
            Record(status="bad", value="x"),
            Record(status="ok", value=7)
        ]