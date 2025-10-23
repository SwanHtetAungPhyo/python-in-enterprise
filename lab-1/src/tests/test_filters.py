import unittest
from unittest.mock import patch
from core.filters import RecordFilter
from models.records import Record
from config.settings import Settings


class TestRecordFilter(unittest.TestCase):
    
    def setUp(self):
        self.filter = RecordFilter()

    def test_filter_records_with_ok_status_above_threshold(self):
        """Test filtering records with OK status above threshold."""
        records = [
            Record(status="ok", value=10),
            Record(status="ok", value=5),
            Record(status="bad", value=15),
            Record(status="ok", value=20)
        ]
        
        filtered = self.filter.filter_records(records, threshold=8)
        
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].value, 10)
        self.assertEqual(filtered[1].value, 20)

    def test_filter_records_with_case_insensitive_status(self):
        """Test filtering with case-insensitive status matching."""
        records = [
            Record(status="OK", value=10),
            Record(status="ok", value=15),
            Record(status="Bad", value=20),
            Record(status="ERROR", value=25)
        ]
        
        filtered = self.filter.filter_records(records, threshold=5)
        
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.normalize_status() == "ok" for r in filtered))

    @patch('core.filters.settings')
    def test_filter_records_with_all_mode(self, mock_settings):
        """Test filtering in ALL mode includes all records with valid numeric values."""
        mock_settings.filter_mode = "ALL"
        
        records = [
            Record(status="ok", value=10),
            Record(status="bad", value=15),
            Record(status="error", value=20),
            Record(status="ok", value=None)
        ]
        
        filtered = self.filter.filter_records(records, threshold=5)
        
        self.assertEqual(len(filtered), 3)  # Excludes None value

    @patch('core.filters.settings')
    def test_filter_records_uses_default_threshold(self, mock_settings):
        """Test filtering uses default threshold when none provided."""
        mock_settings.default_threshold = 12
        mock_settings.filter_mode = "OK"
        
        records = [
            Record(status="ok", value=10),
            Record(status="ok", value=15),
            Record(status="ok", value=20)
        ]
        
        filtered = self.filter.filter_records(records)
        
        self.assertEqual(len(filtered), 2)  # Only values >= 12

    def test_filter_records_with_invalid_values(self):
        """Test filtering excludes records with invalid numeric values."""
        records = [
            Record(status="ok", value=10),
            Record(status="ok", value="invalid"),
            Record(status="ok", value=None),
            Record(status="ok", value=20)
        ]
        
        filtered = self.filter.filter_records(records, threshold=5)
        
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].value, 10)
        self.assertEqual(filtered[1].value, 20)

    def test_should_include_with_valid_ok_record(self):
        """Test _should_include method with valid OK record."""
        record = Record(status="ok", value=15)
        
        result = RecordFilter._should_include(record, threshold=10)
        
        self.assertTrue(result)

    def test_should_include_with_below_threshold(self):
        """Test _should_include method with record below threshold."""
        record = Record(status="ok", value=5)
        
        result = RecordFilter._should_include(record, threshold=10)
        
        self.assertFalse(result)

    def test_should_include_with_bad_status(self):
        """Test _should_include method with bad status."""
        record = Record(status="bad", value=15)
        
        result = RecordFilter._should_include(record, threshold=10)
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()