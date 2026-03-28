import unittest
import io
import sys
import os
from main import main
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

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_cookie_log.csv"
        with open(self.test_file, "w") as f:
            f.write(SAMPLE_LOG)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_full_flow_single_winner(self):
        test_args = ["main.py", "-f", self.test_file, "-d", "2018-12-09"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                main()
                self.assertEqual(
                    mock_stdout.getvalue(),
                    "AtY0laUfhglK3lC7\n"
                )

    def test_full_flow_multiple_winners(self):
        with open(self.test_file, "w") as f:
            f.write("cookie,timestamp\n")
            f.write("AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n")
            f.write("SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n")
            f.write("SAZuXPGUrfbcn5UA,2018-12-09T11:00:00+00:00\n")
            f.write("AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n")
            f.write("SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n")

        test_args = ["main.py", "-f", self.test_file, "-d", "2018-12-09"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue().strip().split('\n')
                self.assertCountEqual(output, ["AtY0laUfhglK3lC7", "SAZuXPGUrfbcn5UA"])

    def test_full_flow_no_cookies_for_date(self):
        test_args = ["main.py", "-f", self.test_file, "-d", "2018-12-10"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                main()
                self.assertEqual(mock_stdout.getvalue(), "")

    def test_invalid_date_format_exits(self):
        test_args = ["main.py", "-f", self.test_file, "-d", "09-12-2018"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):
                main()

    def test_file_not_found_exits(self):
        test_args = ["main.py", "-f", "nonexistent.csv", "-d", "2018-12-09"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):
                main()
