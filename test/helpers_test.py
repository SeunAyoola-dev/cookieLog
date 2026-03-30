import unittest
from helpers import parse_date, parse_file, build_arg_parser
import argparse
from parameterized import parameterized
from unittest.mock import patch

class ParseDateTest(unittest.TestCase):
    def test_parse_valid_date(self):
        valid_date = "2018-12-09"
        self.assertEqual(
            valid_date,
            parse_date(valid_date)
        )

    @parameterized.expand([
        ("letters_appended", "2018-12-09s"),
        ("letters_prepended", "s2018-12-09"),
        ("no_dashes", "20181209"),
        ("wrong_separator", "2018/12/09"),
        ("short_year", "18-12-09"),
        ("single_digit_month", "2018-9-09"),
        ("single_digit_day", "2018-12-9"),
        ("extra_dashes", "2018-12-09-"),
        ("empty_string", ""),
        ("completely_non_numeric", "abcd-ef-gh"),
    ])
    def test_parse_invalid_date(self, name, invalid_date):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_date(invalid_date)

class TestParseFile(unittest.TestCase):

    def test_valid_file_returns_path(self):
        with patch("builtins.open"):
            result = parse_file("cookie_log.csv")
        self.assertEqual(result, "cookie_log.csv")

    def test_raises_on_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(argparse.ArgumentTypeError):
                parse_file("nonexistent.csv")

    def test_raises_on_directory(self):
        with patch("builtins.open", side_effect=IsADirectoryError):
            with self.assertRaises(argparse.ArgumentTypeError):
                parse_file("/some/directory/")

class TestBuildArgParser(unittest.TestCase):

    def setUp(self):
        self.parser = build_arg_parser()

    def test_valid_args_parse_correctly(self):
        with patch("builtins.open"):
            args = self.parser.parse_args(["-f", "cookie_log.csv", "-d", "2018-12-09"])
            self.assertEqual(args.f, "cookie_log.csv")
            self.assertEqual(args.d, "2018-12-09")
#
    def test_missing_f_flag_exits(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["-d", "2018-12-09"])

    def test_missing_d_flag_exits(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["-f", "cookie_log.csv"])

    def test_missing_both_flags_exits(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_invalid_date_format_exits(self):
        with patch("builtins.open"):
            with self.assertRaises(SystemExit):
                self.parser.parse_args(["-f", "cookie_log.csv", "-d", "09-12-2018"])

    def test_nonexistent_file_exits(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(SystemExit):
                self.parser.parse_args(["-f", "missing.csv", "-d", "2018-12-09"])
