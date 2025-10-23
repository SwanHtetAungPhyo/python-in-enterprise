import unittest
from core.calculator import StatisticsCalculator
from models.records import Record


class TestStatisticsCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = StatisticsCalculator()

    def test_calculate_statistics_with_valid_records(self):
        """Test statistics calculation with valid numeric records."""
        records = [
            Record(status="ok", value=10),
            Record(status="ok", value=20),
            Record(status="ok", value=30)
        ]
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 3)
        self.assertEqual(result.total, 60.0)
        self.assertEqual(result.average, 20.0)

    def test_calculate_statistics_with_mixed_records(self):
        """Test statistics calculation with mixed valid/invalid records."""
        records = [
            Record(status="ok", value=10),
            Record(status="ok", value="invalid"),
            Record(status="ok", value=20),
            Record(status="ok", value=None)
        ]
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 2)
        self.assertEqual(result.total, 30.0)
        self.assertEqual(result.average, 15.0)

    def test_calculate_statistics_with_string_numbers(self):
        """Test statistics calculation with string numeric values."""
        records = [
            Record(status="ok", value="15"),
            Record(status="ok", value="25.5"),
            Record(status="ok", value=10)
        ]
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 3)
        self.assertEqual(result.total, 50.5)
        self.assertAlmostEqual(result.average, 16.833333333333332)

    def test_calculate_statistics_with_empty_list(self):
        """Test statistics calculation with empty record list."""
        records = []
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 0)
        self.assertEqual(result.total, 0.0)
        self.assertEqual(result.average, 0.0)

    def test_calculate_statistics_with_no_valid_values(self):
        """Test statistics calculation when no records have valid numeric values."""
        records = [
            Record(status="ok", value="invalid"),
            Record(status="ok", value=None),
            Record(status="ok", value="not_a_number")
        ]
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 0)
        self.assertEqual(result.total, 0.0)
        self.assertEqual(result.average, 0.0)

    def test_calculate_statistics_with_float_values(self):
        """Test statistics calculation with float values."""
        records = [
            Record(status="ok", value=1.5),
            Record(status="ok", value=2.5),
            Record(status="ok", value=3.0)
        ]
        result = self.calculator.calculate_statistics(records)
        
        self.assertEqual(result.count, 3)
        self.assertEqual(result.total, 7.0)
        self.assertAlmostEqual(result.average, 2.333333333333333)


if __name__ == '__main__':
    unittest.main()