import logging
import threading
import time

from pynput import keyboard

from database import create_table_if_not_exists, insert_data_into_table
from app_stats import AppStats

# Initialize global variables
keystroke_counter = 0
erase_keys_counter = 0
erase_keys_percentage = 0
press_press_intervals = []
press_release_intervals = []
word_lengths = []
word_counter = 0
last_press_time = 0
last_timestamp = time.time()

# Initialize AppStats
app_stats = AppStats()


# Set up a timer to run the insert_data_into_table function every minute
def insert_data_timer():
    threading.Timer(5.0, insert_data_timer).start()
    current_time = time.time()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
    global keystroke_counter, erase_keys_counter, erase_keys_percentage, press_press_intervals, press_release_intervals, word_lengths, word_counter
    active_apps_count, current_app, penultimate_app, current_app_foreground_time, current_app_average_processes, current_app_stddev_processes = app_stats.update()
    insert_data_into_table(timestamp, keystroke_counter, erase_keys_counter, erase_keys_percentage,
                           press_press_intervals, press_release_intervals, word_lengths, active_apps_count,
                           current_app, penultimate_app, current_app_foreground_time, current_app_average_processes,
                           current_app_stddev_processes)  # <-- added the missing argument here
    # Reset the counters and intervals
    keystroke_counter = 0
    erase_keys_counter = 0
    erase_keys_percentage = 0
    press_press_intervals = []
    press_release_intervals = []
    word_lengths = []
    word_counter = 0


# Update the global variables based on the keyboard event
def on_keyboard_event(key):
    global keystroke_counter, erase_keys_counter, erase_keys_percentage, press_press_intervals, press_release_intervals, word_lengths, word_counter, last_press_time, last_timestamp
    current_time = time.time()
    keystroke_counter += 1
    if key == keyboard.Key.backspace:
        erase_keys_counter += 1
        erase_keys_percentage = round((erase_keys_counter / keystroke_counter) * 100, 2)
    elif key == keyboard.Key.space:
        word_lengths.append(word_counter)
        word_counter = 0
    elif isinstance(key, keyboard._win32.KeyCode):
        if last_press_time == 0:
            last_press_time = current_time
        else:
            press_press_intervals.append(current_time - last_press_time)
            last_press_time = current_time
        word_counter += 1
    elif isinstance(key, keyboard._win32.Key):
        press_release_intervals.append(current_time - last_press_time)
        last_press_time = 0
    # Check if it's time to insert data into the database
    if current_time - last_timestamp > 60:
        last_timestamp = current_time
        insert_data_timer()


if __name__ == '__main__':
    # Create the database table if it doesn't exist
    create_table_if_not_exists()

    # Set up the keyboard listener
    listener = keyboard.Listener(on_press=on_keyboard_event)
    listener.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
