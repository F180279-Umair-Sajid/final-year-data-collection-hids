import unittest
from unittest.mock import patch
from io import StringIO
import psycopg2
from database import create_table_if_not_exists, insert_data_into_table


class TestTypingStats(unittest.TestCase):
    def setUp(self):
        self.mock_conn = psycopg2.connect(database='test_db')

    def tearDown(self):
        self.mock_conn.close()

    def test_create_table_if_not_exists(self):
        with patch('psycopg2.connect', return_value=self.mock_conn):
            create_table_if_not_exists()
            with self.mock_conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='typing_stats')")
                result = cur.fetchone()[0]
                self.assertTrue(result)

    def test_insert_data_into_table(self):
        with patch('psycopg2.connect', return_value=self.mock_conn):
            insert_data_into_table(
                timestamp='2022-01-01 12:00:00',
                keystroke_counter=100,
                erase_keys_counter=10,
                erase_keys_percentage=10.0,
                press_press_intervals=[0.1, 0.2, 0.3],
                press_release_intervals=[0.4, 0.5, 0.6],
                word_lengths=[3, 4, 5],
                active_apps_count=2,
                current_app='app1',
                penultimate_app='app2',
                current_app_foreground_time=60,
                current_app_average_processes=2.0,
                current_app_stddev_processes=1.0,
                cpu_percent=10.0,
                ram_percent=20.0,
                bytes_sent=1000,
                bytes_received=2000
            )
            with self.mock_conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM typing_stats")
                result = cur.fetchone()[0]
                self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
