import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from cli.main import parse_arguments, main


class TestCLI(unittest.TestCase):
    
    def test_parse_arguments_with_all_options(self):
        """Test argument parsing with all command line options."""
        test_args = ['--file', 'test.json', '--thres', '5.5', '--all']
        
        with patch.object(sys, 'argv', ['main.py'] + test_args):
            args = parse_arguments()
            
            self.assertEqual(args.file, 'test.json')
            self.assertEqual(args.thres, 5.5)
            self.assertTrue(args.all)

    def test_parse_arguments_with_minimal_options(self):
        """Test argument parsing with minimal options."""
        test_args = ['--file', 'data.json']
        
        with patch.object(sys, 'argv', ['main.py'] + test_args):
            args = parse_arguments()
            
            self.assertEqual(args.file, 'data.json')
            self.assertIsNone(args.thres)
            self.assertFalse(args.all)

    def test_parse_arguments_with_no_options(self):
        """Test argument parsing with no options."""
        with patch.object(sys, 'argv', ['main.py']):
            args = parse_arguments()
            
            self.assertIsNone(args.file)
            self.assertIsNone(args.thres)
            self.assertFalse(args.all)

    @patch('cli.main.DataLoader')
    @patch('cli.main.record_filter')
    @patch('cli.main.calculator')
    @patch('cli.main.settings')
    @patch('cli.main.dt')
    def test_main_function_integration(self, mock_dt, mock_settings, mock_calculator, mock_filter, mock_loader_class):
        """Test main function integration with mocked dependencies."""
        # Setup mocks
        mock_dt.datetime.now.return_value.strftime.return_value = "2024/01/01-12:00:00"
        
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_records.return_value = [MagicMock()]
        
        mock_filter.filter_records.return_value = [MagicMock()]
        
        mock_result = MagicMock()
        mock_result.format_summary.return_value = "[2024/01/01-12:00:00] ok_count=5 total_value=100.00 avg=20.00"
        mock_calculator.calculate_statistics.return_value = mock_result
        
        # Test with command line arguments
        test_args = ['--file', 'test.json', '--thres', '10', '--all']
        
        with patch.object(sys, 'argv', ['main.py'] + test_args):
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Verify settings were updated
                self.assertEqual(mock_settings.data_path, 'test.json')
                self.assertEqual(mock_settings.default_threshold, 10)
                self.assertEqual(mock_settings.filter_mode, 'ALL')
                
                # Verify function calls
                mock_loader.load_records.assert_called_once()
                mock_filter.filter_records.assert_called_once()
                mock_calculator.calculate_statistics.assert_called_once()
                
                # Verify output
                mock_print.assert_called_once_with("[2024/01/01-12:00:00] ok_count=5 total_value=100.00 avg=20.00")
                
                # Verify return value
                self.assertEqual(result, mock_result)

    @patch('cli.main.DataLoader')
    @patch('cli.main.record_filter')
    @patch('cli.main.calculator')
    @patch('cli.main.settings')
    @patch('cli.main.dt')
    def test_main_function_with_no_args(self, mock_dt, mock_settings, mock_calculator, mock_filter, mock_loader_class):
        """Test main function with no command line arguments."""
        # Setup mocks
        mock_dt.datetime.now.return_value.strftime.return_value = "2024/01/01-12:00:00"
        
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_records.return_value = []
        
        mock_filter.filter_records.return_value = []
        
        mock_result = MagicMock()
        mock_result.format_summary.return_value = "[2024/01/01-12:00:00] ok_count=0 total_value=0.00 avg=0.00"
        mock_calculator.calculate_statistics.return_value = mock_result
        
        with patch.object(sys, 'argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Verify settings were not modified
                # (settings should retain their default values)
                
                # Verify function calls
                mock_loader.load_records.assert_called_once()
                mock_filter.filter_records.assert_called_once()
                mock_calculator.calculate_statistics.assert_called_once()
                
                # Verify output
                mock_print.assert_called_once_with("[2024/01/01-12:00:00] ok_count=0 total_value=0.00 avg=0.00")

    @patch('cli.main.DataLoader')
    @patch('cli.main.record_filter')
    @patch('cli.main.calculator')
    @patch('cli.main.settings')
    @patch('cli.main.dt')
    def test_main_function_partial_args(self, mock_dt, mock_settings, mock_calculator, mock_filter, mock_loader_class):
        """Test main function with partial command line arguments."""
        # Setup mocks
        mock_dt.datetime.now.return_value.strftime.return_value = "2024/01/01-12:00:00"
        
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_records.return_value = [MagicMock()]
        
        mock_filter.filter_records.return_value = [MagicMock()]
        
        mock_result = MagicMock()
        mock_result.format_summary.return_value = "[2024/01/01-12:00:00] ok_count=3 total_value=75.50 avg=25.17"
        mock_calculator.calculate_statistics.return_value = mock_result
        
        # Test with only threshold argument
        test_args = ['--thres', '7.5']
        
        with patch.object(sys, 'argv', ['main.py'] + test_args):
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Verify only threshold was updated
                self.assertEqual(mock_settings.default_threshold, 7.5)
                # file and filter_mode should not be modified
                
                # Verify output
                mock_print.assert_called_once_with("[2024/01/01-12:00:00] ok_count=3 total_value=75.50 avg=25.17")


if __name__ == '__main__':
    unittest.main()