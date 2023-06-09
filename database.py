import logging
import psycopg2
import statistics

logging.basicConfig(filename='error.log', level=logging.ERROR)

DB_HOST = "localhost"
DB_NAME = "radar_security"
DB_USER = "postgres"
DB_PASS = "12345678"


def connect_to_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def create_table_if_not_exists():
    print("Creating table if not exists...")
    # Create a new table if it doesn't exist
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS typing_stats (
                    timestamp TIMESTAMP NOT NULL,
                    keystroke_counter INTEGER,
                    erase_keys_counter INTEGER,
                    erase_keys_percentage REAL,
                    press_press_average_interval REAL,
                    press_press_stddev_interval REAL,
                    press_release_average_interval REAL,
                    press_release_stddev_interval REAL,
                    word_counter INTEGER,
                    word_average_length REAL,
                    word_stddev_length REAL,
                    active_apps_average REAL,
                    current_app TEXT,
                    penultimate_app TEXT,
                    current_app_foreground_time INTEGER,
                    current_app_average_processes REAL,
                    current_app_stddev_processes REAL,
                    cpu_percent REAL,
                    ram_percent REAL,
                    bytes_sent INTEGER,
                    bytes_received INTEGER
                );
            """)
            conn.commit()


def insert_data_into_table(timestamp, keystroke_counter, erase_keys_counter, erase_keys_percentage,
                           press_press_intervals, press_release_intervals, word_lengths, active_apps_count,
                           current_app, penultimate_app, current_app_foreground_time, current_app_average_processes,
                           current_app_stddev_processes, cpu_percent, ram_percent, bytes_sent, bytes_received):
    print("Inside insert_data_into_table() function...")
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            word_counter = len(word_lengths)
            word_average_length = statistics.mean(word_lengths) if word_counter > 0 else 0
            word_stddev_length = statistics.stdev(word_lengths) if word_counter > 1 else 0
            press_press_average_interval = statistics.mean(press_press_intervals) if len(
                press_press_intervals) > 0 else 0
            press_press_stddev_interval = statistics.stdev(press_press_intervals) if len(
                press_press_intervals) > 1 else 0
            press_release_average_interval = statistics.mean(press_release_intervals) if len(
                press_release_intervals) > 0 else 0
            press_release_stddev_interval = statistics.stdev(press_release_intervals) if len(
                press_release_intervals) > 1 else 0
            print("trying to Insert the data into the database")

            # Insert the data into the database
            try:
                print("inside the try block")

                cur.execute("""
    INSERT INTO typing_stats (
        timestamp,
        keystroke_counter,
        erase_keys_counter,
        erase_keys_percentage,
        press_press_average_interval,
        press_press_stddev_interval,
        press_release_average_interval,
        press_release_stddev_interval,
        word_counter,
        word_average_length,
        word_stddev_length,
        active_apps_average,
        current_app,
        penultimate_app,
        current_app_foreground_time,
        current_app_average_processes,
        current_app_stddev_processes,
        cpu_percent,
        ram_percent,
        bytes_sent,
        bytes_received
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
""", (
                    timestamp,
                    keystroke_counter,
                    erase_keys_counter,
                    erase_keys_percentage,
                    press_press_average_interval,
                    press_press_stddev_interval,
                    press_release_average_interval,
                    press_release_stddev_interval,
                    word_counter,
                    word_average_length,
                    word_stddev_length,
                    active_apps_count,
                    current_app,
                    penultimate_app,
                    current_app_foreground_time,
                    current_app_average_processes,
                    current_app_stddev_processes,
                    cpu_percent,
                    ram_percent,
                    bytes_sent,
                    bytes_received
                ))
                print("after the insertion")
                conn.commit()
            except Exception as e:
                logging.error(f"Error occurred while inserting data into database: {e}")
