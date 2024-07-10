import os
import time
import json

from PyQt5.QtCore import QThread, pyqtSignal
from pynput import mouse, keyboard

class EventRecorder(QThread):

    finished = pyqtSignal()
    
    event_signal = pyqtSignal(str)

    def __init__(self, name_of_recording, record_mouse=False, delay=0, recordings_path='data'):
        super().__init__()
        self.name_of_recording = name_of_recording
        self.record_mouse = record_mouse
        self.delay = delay
        self.storage = []
        self.recording = True
        self.recordings_path = recordings_path

        # Create the listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move)

    def run(self):
        if self.delay > 0:
            for i in range(self.delay, 0, -1):
                self.event_signal.emit(f"Recording starts in {i} seconds...")
                time.sleep(1)

        self.start_time = time.time()

        self.event_signal.emit("Recording started.")
        self.keyboard_listener.start()
        self.mouse_listener.start()

        while self.recording:
            time.sleep(0.001)

        if self.keyboard_listener.running:
            self.keyboard_listener.stop()

        if self.mouse_listener.running:
            self.mouse_listener.stop()

        self.event_signal.emit("Recording finished.")

        # Serialize the data to a JSON file
        file_path = os.path.join(self.recordings_path, f'{self.name_of_recording}.json')
        with open(file_path, 'w') as outfile:
            json.dump(self.storage, outfile)

        self.finished.emit()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.event_signal.emit("End Recording")
            self.recording = False
            return False
        json_object = {'action': 'pressed_key', 'key': str(key).replace("'", ""), '_time': time.time()}
        self.emit_key_event(json_object)
        self.storage.append(json_object)

    def on_release(self, key):
        json_object = {'action': 'released_key', 'key': str(key).replace("'", ""), '_time': time.time()}
        self.emit_key_event(json_object)
        self.storage.append(json_object)

    def on_move(self, x, y):
        if self.record_mouse:
            if len(self.storage) >= 1:
                if self.storage[-1]['action'] != "moved":
                    json_object = {'action': 'moved', 'x': x, 'y': y, '_time': time.time()}
                    self.emit_mouse_event(json_object)
                    self.storage.append(json_object)
                elif self.storage[-1]['action'] == "moved" and time.time() - self.storage[-1]['_time'] > 0.02:
                    json_object = {'action': 'moved', 'x': x, 'y': y, '_time': time.time()}
                    self.emit_mouse_event(json_object)
                    self.storage.append(json_object)
            else:
                json_object = {'action': 'moved', 'x': x, 'y': y, '_time': time.time()}
                self.emit_mouse_event(json_object)
                self.storage.append(json_object)
                
    def on_click(self, x, y, button, pressed):
        json_object = {'action': 'pressed' if pressed else 'released', 'button': str(button), 'x': x, 'y': y, '_time': time.time()}
        self.emit_mouse_event(json_object)
        self.storage.append(json_object)

    def on_scroll(self, x, y, dx, dy):
        json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x': x, 'y': y, '_time': time.time()}
        self.emit_mouse_event(json_object)
        self.storage.append(json_object)

    def emit_mouse_event(self, obj):
        #To Do add condition for dealing with onscroll events 
        time_data = time.localtime(obj['_time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | X: {obj['x']}, Y: {obj['y']} | Time: {time_formatted}")

    def emit_key_event(self, obj):
        time_data = time.localtime(obj['_time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | Key: {obj['key']} | Time: {time_formatted}") 

    def stop(self):
        self.recording = False
