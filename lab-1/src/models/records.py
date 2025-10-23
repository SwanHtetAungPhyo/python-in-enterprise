from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class Record:
    status: str
    value: Union[int, float, str]
    def normalize_status(self)-> str:
        return self.status.lower()

    def get_numeric_value(self)-> Optional[float]:
        try:
            if isinstance(self.value, (int, float)):
                return float(self.value)
            elif isinstance(self.value, str):
                return float(self.value)
        except (ValueError, TypeError):
            return None
        return None

    def is_valid(self, threshold: float = 0) -> bool:
        numeric_value = self.get_numeric_value()
        if numeric_value is None:
            return False
        return self.normalize_status() == "ok" and numeric_value >= threshold


@dataclass
class AnalysisResult:
    count: int
    total: float
    average: float

    def format_summary(self, timestamp: str) -> str:
        return f"[{timestamp}] ok_count={self.count} total_value={self.total:.2f} avg={self.average:.2f}"