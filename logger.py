import time

from pynput import keyboard

# Initialize the global variables
keystroke_counter = 0
erase_keys_counter = 0
press_press_intervals = []
press_release_intervals = []
word_lengths = []
last_press_time = 0
word_counter = 0
window_start_time = time.time()
last_release_time = 0
print(window_start_time)


def on_keyboard_event(key, event):
    global keystroke_counter, erase_keys_counter, press_press_intervals, press_release_intervals, word_lengths, last_press_time, word_counter, window_start_time, last_release_time

    if event == 'press':
        # Update the keystroke counter
        keystroke_counter += 1

        if key == keyboard.Key.backspace:
            # Handle erase keys
            erase_keys_counter += 1
            if word_lengths and word_lengths[-1] > 0:
                word_lengths[-1] -= 1
                if word_lengths[-1] == 0:
                    word_lengths.pop()
                    word_counter -= 1
        elif key == keyboard.Key.enter:
            if press_press_intervals:
                last_press_time = press_press_intervals[-1]
            else:
                last_press_time = 0

            # Start a new word length count
            word_lengths.append(0)
            word_counter += 1
        elif key == keyboard.Key.space:
            # End the previous word and start a new one
            if word_lengths:
                word_lengths[-1] = max(0, word_lengths[-1])
            word_lengths.append(1)
            word_counter += 1
        else:
            # This is a letter or symbol, so we count it as part of the current word
            if not word_lengths:
                word_lengths.append(0)
                word_counter += 1
            word_lengths[-1] += 1

        # Calculate the press-press interval
        current_timestamp = time.time()
        if last_press_time != 0:
            press_press_intervals.append(current_timestamp - last_press_time)
        last_press_time = current_timestamp
    elif event == 'release':
        # Calculate the press-release interval
        current_timestamp = time.time()
        if last_release_time != 0:
            press_release_intervals.append(current_timestamp - last_release_time)
        last_release_time = current_timestamp

    # Debugging output
    print(f"Event: {event}, Key: {key}")
    print(f"Word Counter: {word_counter}")
    print(f"Word Lengths: {word_lengths}")
    print(f"Press-Press Intervals: {press_press_intervals}")
    print(f"Press-Release Intervals: {press_release_intervals}")
    print(f"Keystroke Counter: {keystroke_counter}")
    print(f"Erase Keys Counter: {erase_keys_counter}\n")


def on_press(key):
    on_keyboard_event(key, 'press')


def on_release(key):
    on_keyboard_event(key, 'release')
