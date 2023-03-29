import time
import unittest
from time import time

import HtmlTestRunner
from pynput import keyboard

import logger
from logger import on_keyboard_event


class TestKeyboardEvent(unittest.TestCase):

    def setUp(self):
        self.keystroke_counter = 0
        self.erase_keys_counter = 0
        self.press_press_intervals = []
        self.press_release_intervals = []
        self.word_lengths = []
        self.last_press_time = 0
        self.word_counter = 0
        self.window_start_time = time()

    def test_on_keyboard_event(self):
        event = keyboard.KeyCode.from_char('a')
        on_keyboard_event(event)
        self.assertEqual(logger.keystroke_counter, 1)
        self.assertEqual(logger.word_lengths, [1])
        self.assertEqual(logger.word_counter, 1)

        event = keyboard.KeyCode.from_char('b')
        on_keyboard_event(event)
        self.assertEqual(logger.keystroke_counter, 2)
        self.assertEqual(logger.word_lengths, [2])
        self.assertEqual(logger.word_counter, 1)

        event = keyboard.KeyCode.from_char(' ')
        on_keyboard_event(event)
        self.assertEqual(logger.keystroke_counter, 3)
        self.assertEqual(logger.word_lengths, [3])
        self.assertEqual(logger.word_counter, 1)

        event = keyboard.KeyCode.from_char('c')
        on_keyboard_event(event)
        self.assertEqual(logger.keystroke_counter, 4)


if __name__ == '__main__':
    # Create a test suite and add the test case
    suite = unittest.TestSuite()
    suite.addTest(TestKeyboardEvent('test_keyboard_event'))

    # Configure the HTMLTestRunner options
    runner = HtmlTestRunner(output='test-reports', report_title='Keyboard Test Report')

    # Run the test suite with the HTMLTestRunner
    runner.run(suite)
