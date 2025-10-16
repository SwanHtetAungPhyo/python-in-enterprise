from typing import List
from models.records import Record, AnalysisResult
class StatisticsCalculator:
    @staticmethod
    def calculate_statistics(records: List[Record]) -> AnalysisResult:
        """Calculate statistics for valid records."""
        if not records:
            return AnalysisResult(count=0, total=0.0, average=0.0)

        valid_values = []
        for record in records:
            numeric_value = record.get_numeric_value()
            if numeric_value is not None:
                valid_values.append(numeric_value)

        if not valid_values:
            return AnalysisResult(count=0, total=0.0, average=0.0)

        total = sum(valid_values)
        average = total / len(valid_values)

        return AnalysisResult(
            count=len(valid_values),
            total=total,
            average=average
        )


calculator = StatisticsCalculator()