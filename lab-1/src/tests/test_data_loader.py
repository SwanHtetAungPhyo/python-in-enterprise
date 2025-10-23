import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from data_io.data_loader import DataLoader
from models.records import Record


class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        self.loader = DataLoader()

    def test_load_records_from_valid_json(self):
        """Test loading records from valid JSON file."""
        test_data = [
            {"status": "ok", "value": 10},
            {"status": "bad", "value": 20},
            {"STATUS": "OK", "value": "30"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = Path(f.name)
        
        try:
            records = self.loader.load_records(temp_path)
            
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0].status, "ok")
            self.assertEqual(records[0].value, 10)
            self.assertEqual(records[1].status, "bad")
            self.assertEqual(records[1].value, 20)
            self.assertEqual(records[2].status, "OK")
            self.assertEqual(records[2].value, "30")
        finally:
            temp_path.unlink()

    def test_load_records_with_missing_fields(self):
        """Test loading records with missing status or value fields."""
        test_data = [
            {"status": "ok", "value": 10},
            {"value": 20},  # Missing status
            {"status": "bad"},  # Missing value
            {}  # Missing both
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = Path(f.name)
        
        try:
            records = self.loader.load_records(temp_path)
            
            self.assertEqual(len(records), 4)
            self.assertEqual(records[0].status, "ok")
            self.assertEqual(records[1].status, "unknown")  # Default status
            self.assertEqual(records[1].value, 20)
            self.assertEqual(records[2].status, "bad")
            self.assertEqual(records[2].value, 0)  # Default value
            self.assertEqual(records[3].status, "unknown")
            self.assertEqual(records[3].value, 0)
        finally:
            temp_path.unlink()

    @patch('config.settings.settings')
    def test_load_records_uses_default_path(self, mock_settings):
        """Test loading records uses settings default path when none provided."""
        mock_settings.data_path = Path("test_file.json")
        mock_settings.encoding = 'utf-8'
        
        test_data = [{"status": "ok", "value": 42}]
        
        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            records = self.loader.load_records()
            
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].status, "ok")
            self.assertEqual(records[0].value, 42)

    def test_load_records_file_not_found_returns_fallback(self):
        """Test loading records returns fallback data when file not found."""
        non_existent_path = Path("non_existent_file.json")
        
        records = self.loader.load_records(non_existent_path)
        
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0].status, "ok")
        self.assertEqual(records[0].value, "3")
        self.assertEqual(records[1].status, "bad")
        self.assertEqual(records[1].value, "x")
        self.assertEqual(records[2].status, "ok")
        self.assertEqual(records[2].value, 7)

    def test_load_records_invalid_json_returns_fallback(self):
        """Test loading records returns fallback data when JSON is invalid."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = Path(f.name)
        
        try:
            records = self.loader.load_records(temp_path)
            
            # Should return fallback data
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0].status, "ok")
            self.assertEqual(records[1].status, "bad")
            self.assertEqual(records[2].status, "ok")
        finally:
            temp_path.unlink()

    def test_parse_records_with_various_formats(self):
        """Test parsing records with various data formats."""
        raw_data = [
            {"status": "ok", "value": 10},
            {"STATUS": "BAD", "value": "20"},
            {"status": "error", "value": 30.5},
            {"status": "ok", "value": None}
        ]
        
        records = self.loader._parse_records(raw_data)
        
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0].status, "ok")
        self.assertEqual(records[0].value, 10)
        self.assertEqual(records[1].status, "BAD")
        self.assertEqual(records[1].value, "20")
        self.assertEqual(records[2].status, "error")
        self.assertEqual(records[2].value, 30.5)
        self.assertEqual(records[3].status, "ok")
        self.assertIsNone(records[3].value)

    def test_get_fallback_data(self):
        """Test fallback data structure."""
        fallback_records = self.loader._get_fallback_data()
        
        self.assertEqual(len(fallback_records), 3)
        self.assertIsInstance(fallback_records[0], Record)
        self.assertIsInstance(fallback_records[1], Record)
        self.assertIsInstance(fallback_records[2], Record)


if __name__ == '__main__':
    unittest.main()