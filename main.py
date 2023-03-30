import threading
import time

from pynput import keyboard

from database import create_table_if_not_exists, insert_data_into_table
from app_stats import AppStats
from logger import (
    reset_counters,  # Add this line
    on_press as logger_on_press,
    on_release as logger_on_release, get_logger_data,
)

# Initialize AppStats
app_stats = AppStats()


def on_press(key):
    global keystroke_counter, erase_keys_counter, press_press_intervals, press_release_intervals, word_lengths, word_counter, last_press_time
    logger_on_press(key)  # Call the on_press function from logger.py


def on_release(key):
    global keystroke_counter, erase_keys_counter, press_press_intervals, press_release_intervals, word_lengths, word_counter, last_press_time
    logger_on_release(key)


# Set up a timer to run the insert_data_into_table function every minute
def insert_data_timer():
    threading.Timer(5, insert_data_timer).start()
    current_time = time.time()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
    active_apps_count, current_app, penultimate_app, current_app_foreground_time, current_app_average_processes, current_app_stddev_processes = app_stats.update()

    # Get data from logger.py
    keystroke_counter, erase_keys_counter, press_press_intervals, press_release_intervals, word_lengths, word_counter = get_logger_data()

    # Calculate erase_keys_percentage
    erase_keys_percentage = (erase_keys_counter / keystroke_counter) * 100 if keystroke_counter > 0 else 0

    print(f"keyboard{keystroke_counter}")
    insert_data_into_table(timestamp, keystroke_counter, erase_keys_counter, erase_keys_percentage,
                           press_press_intervals, press_release_intervals, word_lengths, active_apps_count,
                           current_app, penultimate_app, current_app_foreground_time, current_app_average_processes,
                           current_app_stddev_processes)

    # Reset the counters in logger.py
    reset_counters()


if __name__ == '__main__':
    print("Starting the main script...")
    # Create the database table if it doesn't exist
    create_table_if_not_exists()

    # Set up the keyboard listener
    listener = keyboard.Listener(on_press=on_press,
                                 on_release=on_release)  # Update the listener to include both on_press and on_release
    listener.start()

    # Call the insert_data_timer() function to start the timer
    insert_data_timer()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
