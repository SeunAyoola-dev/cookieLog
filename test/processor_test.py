import unittest
import io
from processor import process, parse_input_file, find_most_active_cookies
from unittest.mock import patch, mock_open

SAMPLE_LOG = (
    "cookie,timestamp\n"
    "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
    "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
    "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
    "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
    "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
    "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n"
    "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n"
    "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00\n"
)

SAMPLE_LOG_WITH_ERROR = (
    "cookie,timestamp\n"
    "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
    "SAZuXPGUrfbcn5UA,invalid\n"
    "5UAVanZf6UtGyKVS,\n"
    "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
)

SAMPLE_LOG_WITH_MULTIPLE_ACTIVE_COOKIES = (
    "cookie,timestamp\n"
    "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
    "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
    "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
    "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
    "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
    "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
    "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n"
    "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n"
    "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00\n"
)

def mock_file_open(content):
    return mock_open(read_data=content)

class parse_input_file_test(unittest.TestCase):
    def setUp(self):
        self.target_date = "2018-12-09"
        self.none_date = "2020-12-09"
        self.file_path = "dummy.csv"

    def test_counts_most_frequent_cookies(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG)):
            counts = parse_input_file(self.file_path, self.target_date)

        self.assertEqual(
        {
            "AtY0laUfhglK3lC7": 2,
            "SAZuXPGUrfbcn5UA": 1,
            "5UAVanZf6UtGyKVS": 1
            },
            counts
        )

    def test_returns_empty_dict_for_empty_date(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG)):
            counts = parse_input_file(self.file_path, self.none_date)

        self.assertEqual(counts, {})

    def test_skip_malformed_line(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG_WITH_ERROR)):
            counts = parse_input_file(self.file_path, self.target_date)

        self.assertEqual(
            {
                "AtY0laUfhglK3lC7": 1,
                "5UAVanZf6UtGyKVS": 1
            },
            counts
        )
class find_most_active_cookie_test(unittest.TestCase):
    def setUp(self):
        self.target_date = "2018-12-09"

    def test_returns_empty_list_if_no_cookie(self):
        active_cookies = find_most_active_cookies({})
        self.assertEqual(
            [],
            active_cookies
        )

    def test_returns_most_active_cookie(self):
        count = {
            "AtY0laUfhglK3lC7": 2,
            "SAZuXPGUrfbcn5UA": 1,
            "5UAVanZf6UtGyKVS": 1
            }
        active_cookies = find_most_active_cookies(count)
        self.assertEqual(
            ["AtY0laUfhglK3lC7"],
            active_cookies
        )

    def test_returns_most_active_cookies(self):
        count = {
            "AtY0laUfhglK3lC7": 2,
            "SAZuXPGUrfbcn5UA": 2,
        }
        active_cookies = find_most_active_cookies(count)
        self.assertEqual(
            ["AtY0laUfhglK3lC7", "SAZuXPGUrfbcn5UA"],
            active_cookies
        )

class process_test(unittest.TestCase):
    def setUp(self):
        self.target_date = "2018-12-09"
        self.none_date = "2020-12-09"
        self.file_path = "dummy.csv"

    def test_prints_nothing_if_no_cookie(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG)):
            with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                process(self.file_path, self.none_date)
                self.assertEqual(
                    '',
                    mock_stdout.getvalue()
                )

    def test_prints_most_active_cookie(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG)):
            with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                process(self.file_path, self.target_date)
                self.assertEqual(
                    'AtY0laUfhglK3lC7\n',
                    mock_stdout.getvalue()  # It's important to remember about '\n'
                )

    def test_prints_most_active_cookies(self):
        with patch("builtins.open", mock_file_open(SAMPLE_LOG_WITH_MULTIPLE_ACTIVE_COOKIES)):
            with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                process(self.file_path, self.target_date)
                self.assertEqual(
                    mock_stdout.getvalue(),
                    'AtY0laUfhglK3lC7\nSAZuXPGUrfbcn5UA\n'
                )