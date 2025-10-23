import unittest
from models.records import Record, AnalysisResult


class TestRecord(unittest.TestCase):
    
    def test_normalize_status(self):
        """Test status normalization to lowercase."""
        record = Record(status="OK", value=10)
        self.assertEqual(record.normalize_status(), "ok")
        
        record = Record(status="Bad", value=5)
        self.assertEqual(record.normalize_status(), "bad")
        
        record = Record(status="ERROR", value=0)
        self.assertEqual(record.normalize_status(), "error")

    def test_get_numeric_value_with_numbers(self):
        """Test numeric value extraction from int and float."""
        record = Record(status="ok", value=42)
        self.assertEqual(record.get_numeric_value(), 42.0)
        
        record = Record(status="ok", value=3.14)
        self.assertEqual(record.get_numeric_value(), 3.14)

    def test_get_numeric_value_with_strings(self):
        """Test numeric value extraction from string numbers."""
        record = Record(status="ok", value="123")
        self.assertEqual(record.get_numeric_value(), 123.0)
        
        record = Record(status="ok", value="45.67")
        self.assertEqual(record.get_numeric_value(), 45.67)

    def test_get_numeric_value_with_invalid_data(self):
        """Test numeric value extraction with invalid data."""
        record = Record(status="ok", value="invalid")
        self.assertIsNone(record.get_numeric_value())
        
        record = Record(status="ok", value=None)
        self.assertIsNone(record.get_numeric_value())

    def test_is_valid_with_ok_status(self):
        """Test record validation with OK status."""
        record = Record(status="ok", value=10)
        self.assertTrue(record.is_valid(5))
        self.assertFalse(record.is_valid(15))

    def test_is_valid_with_bad_status(self):
        """Test record validation with bad status."""
        record = Record(status="bad", value=10)
        self.assertFalse(record.is_valid(5))

    def test_is_valid_with_null_value(self):
        """Test record validation with null values."""
        record = Record(status="ok", value=None)
        self.assertFalse(record.is_valid(0))


class TestAnalysisResult(unittest.TestCase):
    
    def test_format_summary(self):
        """Test analysis result formatting."""
        result = AnalysisResult(count=5, total=100.0, average=20.0)
        timestamp = "2024/01/01-12:00:00"
        expected = "[2024/01/01-12:00:00] ok_count=5 total_value=100.00 avg=20.00"
        self.assertEqual(result.format_summary(timestamp), expected)

    def test_format_summary_with_decimals(self):
        """Test analysis result formatting with decimal values."""
        result = AnalysisResult(count=3, total=33.33, average=11.11)
        timestamp = "2024/01/01-12:00:00"
        expected = "[2024/01/01-12:00:00] ok_count=3 total_value=33.33 avg=11.11"
        self.assertEqual(result.format_summary(timestamp), expected)


if __name__ == '__main__':
    unittest.main()