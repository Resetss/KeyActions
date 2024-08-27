import os
import time
import json

from pynput import mouse, keyboard

from PyQt5.QtCore import QThread, pyqtSignal

from settings_manager import SettingsManager

class EventRecorder(QThread):
    finished = pyqtSignal()
    event_signal = pyqtSignal(str)

    def __init__(self, recording_name, record_mouse=False, initial_delay_seconds=0, recordings_path='data'):
        super().__init__()

        self.recording_name = recording_name
        self.record_mouse = record_mouse
        self.initial_delay_seconds = initial_delay_seconds
        self.recordings_path = recordings_path
        self.recording_events = []

        self.is_recording = True

    def run(self):
        """Starts the event recording process."""
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        mouse_listener = mouse.Listener(on_click=self.on_mouse_click, on_scroll=self.on_mouse_scroll, on_move=self.on_mouse_move)

        if self.initial_delay_seconds > 0:
            self.handle_initial_delay()

        self.event_signal.emit("Recording started.")
        keyboard_listener.start()
        mouse_listener.start()

        while self.is_recording:
            time.sleep(0.001)

        if keyboard_listener.running:
            keyboard_listener.stop()

        if mouse_listener.running:
            mouse_listener.stop()

        self.event_signal.emit("Recording finished.")
        self.save_recording()
        self.finished.emit()

    def handle_initial_delay(self):
        """Handles the initial delay before recording starts."""
        for i in range(self.initial_delay_seconds, 0, -1):
            self.event_signal.emit(f"Recording starts in {i} seconds...")
            time.sleep(1)

    def on_key_press(self, key):
        """Handles keyboard key press events."""
        if self.is_recording:
            event = {'action': 'pressed_key', 'key': str(key).replace("'", ""), 'time': time.time()}
            self.emit_key_event(event)
            self.recording_events.append(event)

    def on_key_release(self, key):
        """Handles keyboard key release events."""
        if self.is_recording:
            event = {'action': 'released_key', 'key': str(key).replace("'", ""), 'time': time.time()}
            self.emit_key_event(event)
            self.recording_events.append(event)

    def on_mouse_move(self, x, y):
        """Handles mouse movement events."""
        if self.record_mouse and self.is_recording:
            self.record_mouse_event('moved', x, y)

    def on_mouse_click(self, x, y, button, pressed):
        """Handles mouse click events."""
        if self.is_recording:
            action = 'pressed' if pressed else 'released'
            event = {
                'action': action, 
                'button': str(button), 
                'x': x, 'y': y, 
                'time': time.time()
            }
            self.emit_mouse_event(event)
            self.recording_events.append(event)

    def on_mouse_scroll(self, x, y, dx, dy):
        """Handles mouse scroll events."""
        if self.is_recording:
            event = {
                'action': 'scroll',
                'vertical_direction': int(dy),
                'horizontal_direction': int(dx),
                'x': x,
                'y': y,
                'time': time.time()
            }
            self.emit_scroll_event(event)
            self.recording_events.append(event)

    def record_mouse_event(self, action, x, y):
        """Records mouse movement event with a threshold to avoid frequent updates."""
        if len(self.recording_events) >= 1:
            last_event = self.recording_events[-1]
            if last_event['action'] != action or (time.time() - last_event['time'] > 0.02):
                event = {
                    'action': action, 
                    'x': x, 
                    'y': y, 
                    'time': time.time()
                }
                self.emit_mouse_event(event)
                self.recording_events.append(event)
        else:
            event = {
                'action': action, 
                'x': x, 
                'y': y, 
                'time': time.time()
            }
            self.emit_mouse_event(event)
            self.recording_events.append(event)

    def emit_mouse_event(self, event):
        """Emits a signal for mouse events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | X: {event['x']}, Y: {event['y']} | Time: {time_formatted}")

    def emit_scroll_event(self, event):
        """Emits a signal for scroll events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | dx: {event['vertical_direction']}, dy: {event['horizontal_direction']} | Time: {time_formatted}")

    def emit_key_event(self, event):
        """Emits a signal for key events."""
        time_formatted = time.strftime('%H:%M:%S', time.localtime(event['time']))
        self.event_signal.emit(f"Action: {event['action']} | Key: {event['key']} | Time: {time_formatted}")

    def save_recording(self):
        """Saves the recorded events to a file."""
        recording_path = SettingsManager.get_recordings_folder()
        full_path = os.path.join(recording_path, f'{self.recording_name}.json')
        with open(full_path, 'w') as outfile:
            json.dump(self.recording_events, outfile)

    def stop(self):
        """Stops the recording process."""
        self.is_recording = False
