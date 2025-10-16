from typing import List
from models.records import Record
from config.settings import settings
class RecordFilter:
    def filter_records(self, records: List[Record], threshold: float = None) -> List[Record]:
        if threshold is None:
            threshold = settings.default_threshold

        filtered = []
        for record in records:
            if self._should_include(record, threshold):
                filtered.append(record)
        return filtered

    @staticmethod
    def _should_include(record: Record, threshold: float) -> bool:
        if settings.filter_mode == "ALL":
            return record.get_numeric_value() is not None

        return record.is_valid(threshold)


# Singleton instance
record_filter = RecordFilter()