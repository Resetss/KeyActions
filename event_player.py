import time
import json
import os

from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from PyQt5.QtCore import QThread, pyqtSignal

from event_manager import EventManager

class EventPlayer(QThread):

    event_signal = pyqtSignal(str)

    def __init__(self, filename, play_count, initial_delay_seconds=0, intermediate_delay_seconds=0, recordings_path='data'):
        super().__init__()

        self.recordings = []

        if filename.endswith(".rec"):
            # Load a single recording file
            file_path = os.path.join(recordings_path, filename)
            with open(file_path) as json_file:
                self.recordings.append(('file', json.load(json_file)))
        else:
            # Load a sequence file
            file_path = os.path.join(recordings_path, filename)
            with open(file_path) as seq_file:
                sequence = json.load(seq_file)
                for event in sequence:
                    if event["type"] == "file":
                        recording_path = os.path.join(recordings_path, event["filename"])
                        with open(recording_path) as json_file:
                            self.recordings.append(('file', json.load(json_file)))
                    elif event["type"] == "delay":
                        self.recordings.append(('delay', event["delay"]))

        self.play_count = play_count
        self.initial_delay_seconds = initial_delay_seconds
        self.intermediate_delay_seconds = intermediate_delay_seconds
        self.stop_event_player = False

    def run(self):
        """Starts the event playing process."""
        mouse = MouseController()
        keyboard = KeyboardController()

        for item_type, content in self.recordings:
            if item_type == 'file':
                self.play_recording(content, mouse, keyboard)
            elif item_type == 'delay':
                self.handle_delay(content, "Next sequence in")

        self.event_signal.emit("End Playing")

    def play_recording(self, events, mouse, keyboard):
        """Handles the playback of a recording."""
        self.handle_initial_delay()

        self.event_signal.emit(f"Start Playing: Recording")

        for current_play in range(self.play_count):
            self.event_signal.emit(f"Play {current_play + 1} out of {self.play_count}")

            for index, event in enumerate(events):
                if self.stop_event_player:
                    return

                self.handle_event(event, index, events, mouse, keyboard)

            if self.intermediate_delay_seconds > 0 and current_play + 1 != self.play_count:
                self.handle_delay(self.intermediate_delay_seconds, "Next play in")

    def handle_event(self, event, index, events, mouse, keyboard):
        """Processes a single event."""
        action = event['action']
        event_time = event['time']

        pause_time = self.calculate_pause_time(index, event_time, events)

        if action in ["pressed_key", "released_key"]:
            self.handle_key_event(event, action, keyboard)
        elif action in ["pressed", "released"]:
            self.handle_mouse_button_event(event, action, mouse)
        elif action == "scroll":
            self.handle_scroll_event(event, index, events, mouse)

        time.sleep(pause_time)

    def handle_initial_delay(self):
        """Handles the initial delay before the first playback."""
        if self.initial_delay_seconds > 0:
            self.handle_delay(self.initial_delay_seconds, "Playing starts in")

    def handle_delay(self, delay_seconds, message_prefix):
        """Handles a countdown delay with a given prefix message."""
        for i in range(delay_seconds, 0, -1):
            self.event_signal.emit(f"{message_prefix} {i} seconds...")
            time.sleep(1)

    def calculate_pause_time(self, index, current_time, events):
        """Calculates the pause time between two events."""
        try:
            next_event_time = events[index + 1]['time']
            return next_event_time - current_time
        except IndexError:
            return 1

    def handle_key_event(self, event, action, keyboard):
        """Handles keyboard events."""
        key_name = event['key']
        if EventManager.is_key_valid(key_name):
            key = EventManager.get_key(key_name)
            self.emit_key_event(event)
            if action == "pressed_key":
                keyboard.press(key)
            else:
                keyboard.release(key)
        else:
            self.event_signal.emit(f"Invalid key: {key_name}")

    def handle_mouse_button_event(self, event, action, mouse):
        """Handles mouse button events."""
        button_name = event['button']
        if EventManager.is_button_valid(button_name):
            button = EventManager.get_button(button_name)
            self.emit_mouse_event(event)
            mouse.position = (event['x'], event['y'])
            if action == "pressed":
                mouse.press(button)
            elif action == "released":
                mouse.release(button)
        else:
            self.event_signal.emit(f"Invalid button: {button_name}")

    def handle_scroll_event(self, event, index, events, mouse):
        """Handles mouse scroll events."""
        move_for_scroll = True
        x, y = event['x'], event['y']
        if index > 0 and (events[index - 1]['action'] in ["pressed", "released"]):
            if x == events[index - 1]['x'] and y == events[index - 1]['y']:
                move_for_scroll = False
        self.emit_scroll_event(event)
        mouse.position = (x, y)
        if move_for_scroll:
            time.sleep(0.1)
        mouse.scroll(event['horizontal_direction'], event['vertical_direction'])

    def emit_mouse_event(self, event):
        """Emits a signal for mouse events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | X: {event['x']}, Y: {event['y']} | Time: {time_formatted}")

    def emit_key_event(self, event):
        """Emits a signal for keyboard events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | Key: {event['key']} | Time: {time_formatted}")

    def emit_scroll_event(self, event):         
        """Emits a signal for scroll events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | dx: {event['vertical_direction']}, dy: {event['horizontal_direction']} | Time: {time_formatted}")

    def stop(self):
        """Stops the event player."""
        self.stop_event_player = True
