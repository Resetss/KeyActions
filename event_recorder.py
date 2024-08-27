import os
import time
import json

from settings_manager import SettingsManager

from PyQt5.QtCore import QThread, pyqtSignal
from pynput import mouse, keyboard

class EventRecorder(QThread):

    finished = pyqtSignal()
    
    event_signal = pyqtSignal(str)

    def __init__(self, name_of_recording, record_mouse=False, initial_delay=0, recordings_path='data'):
        super().__init__()

        self.name_of_recording = name_of_recording
        self.record_mouse = record_mouse
        self.delay = initial_delay
        self.recording_data = [] 

        self.recording = True

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move)

        if self.delay > 0:
            for i in range(self.delay, 0, -1):
                self.event_signal.emit(f"Recording starts in {i} seconds...")
                time.sleep(1)

        self.event_signal.emit("Recording started.")
        keyboard_listener.start()
        mouse_listener.start()

        while self.recording:
            time.sleep(0.001)

        if keyboard_listener.running:
            keyboard_listener.stop()

        if mouse_listener.running:
            mouse_listener.stop()

        self.event_signal.emit("Recording finished.")

        recording_path = SettingsManager.get_recordings_folder()
        full_path = os.path.join(recording_path, f'{self.name_of_recording}.json')
        with open(full_path, 'w') as outfile:
            json.dump(self.recording_data, outfile)

        self.finished.emit()

    def on_press(self, key):
        if self.recording:
            json_object = {'action': 'pressed_key', 'key': str(key).replace("'", ""), 'time': time.time()}
            self.emit_key_event(json_object)
            self.recording_data.append(json_object)

    def on_release(self, key):
        if self.recording:
            json_object = {'action': 'released_key', 'key': str(key).replace("'", ""), 'time': time.time()}
            self.emit_key_event(json_object)
            self.recording_data.append(json_object)

    def on_move(self, x, y):
        if self.record_mouse:
            if self.recording:
                if len(self.recording_data) >= 1:
                    if self.recording_data[-1]['action'] != "moved":
                        json_object = {'action': 'moved', 'x': x, 'y': y, 'time': time.time()}
                        self.emit_mouse_event(json_object)
                        self.recording_data.append(json_object)
                    elif self.recording_data[-1]['action'] == "moved" and time.time() - self.recording_data[-1]['time'] > 0.02:
                        json_object = {'action': 'moved', 'x': x, 'y': y, 'time': time.time()}
                        self.emit_mouse_event(json_object)
                        self.recording_data.append(json_object)
                else:
                    json_object = {'action': 'moved', 'x': x, 'y': y, 'time': time.time()}
                    self.emit_mouse_event(json_object)
                    self.recording_data.append(json_object)
                    
    def on_click(self, x, y, button, pressed):
        if self.recording:
            json_object = {'action': 'pressed' if pressed else 'released', 'button': str(button), 'x': x, 'y': y, 'time': time.time()}
            self.emit_mouse_event(json_object)
            self.recording_data.append(json_object)

    def on_scroll(self, x, y, dx, dy):
        if self.recording:
            json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x': x, 'y': y, 'time': time.time()}
            self.emit_scroll_event(json_object)
            self.recording_data.append(json_object)

    def emit_mouse_event(self, obj): 
        time_data = time.localtime(obj['time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | X: {obj['x']}, Y: {obj['y']} | Time: {time_formatted}")

    def emit_scroll_event(self, obj):         
        time_data = time.localtime(obj['time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | dx: {obj['vertical_direction']}, dy: {obj['horizontal_direction']} | Time: {time_formatted}")

    def emit_key_event(self, obj):
        time_data = time.localtime(obj['time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | Key: {obj['key']} | Time: {time_formatted}") 

    def stop(self):
        self.recording = False
