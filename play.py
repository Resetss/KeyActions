import time
import json
import os

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from PyQt5.QtCore import QThread, pyqtSignal

from pynput import keyboard

class EventPlayer(QThread):
    event_signal = pyqtSignal(str)

    def __init__(self, name_of_recording, number_of_plays, delay=0, recordings_path='data'):
        super().__init__()
        self.name_of_recording = name_of_recording
        self.number_of_plays = number_of_plays
        self.delay = delay
        self.recordings_path = recordings_path
        self._stop_flag = False

    def run(self):
        # TODO Load settings for key input here. 

        file_path = os.path.join(self.recordings_path, self.name_of_recording)
        with open(file_path) as json_file:
            data = json.load(json_file)

        special_keys = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_l": Key.ctrl_l, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

        mouse = MouseController()
        keyboardController = KeyboardController()

        # Event Listener for stopping play
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()        

        if self.delay > 0:
            for i in range(self.delay, 0, -1):
                self.event_signal.emit(f"Playing starts in {i} seconds...")
                time.sleep(1)

        self.event_signal.emit(f"Start Playing: {self.name_of_recording}")

        for current_play in range(self.number_of_plays):
            if self._stop_flag:
                break

            self.event_signal.emit(f"Play {current_play} out of {self.number_of_plays}")

            for index, obj in enumerate(data):
                action, _time = obj['action'], obj['_time']
                try:
                    next_movement = data[index+1]['_time']
                    pause_time = next_movement - _time
                except IndexError:
                    pause_time = 1

                if action in ["pressed_key", "released_key"]:
                    key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
                    self.emit_key(obj)
                    if action == "pressed_key":
                        keyboardController.press(key)
                    else:
                        keyboardController.release(key)
                    time.sleep(pause_time)

                else:
                    move_for_scroll = True
                    x, y = obj['x'], obj['y']
                    if action == "scroll" and index > 0 and (data[index - 1]['action'] in ["pressed", "released"]):
                        if x == data[index - 1]['x'] and y == data[index - 1]['y']:
                            move_for_scroll = False
                    self.emit_mouse(obj)
                    mouse.position = (x, y)
                    if action in ["pressed", "released", "scroll"] and move_for_scroll:
                        time.sleep(0.1)
                    if action == "pressed":
                        mouse.press(Button.left if obj['button'] == "Button.left" else Button.right)
                    elif action == "released":
                        mouse.release(Button.left if obj['button'] == "Button.left" else Button.right)
                    elif action == "scroll":
                        horizontal_direction, vertical_direction = obj['horizontal_direction'], obj['vertical_direction']
                        mouse.scroll(horizontal_direction, vertical_direction)
                    time.sleep(pause_time)

        self.event_signal.emit("End Playing")
    
    def emit_mouse(self, obj):
        time_data = time.localtime(obj['_time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | X: {obj['x']}, Y: {obj['y']} | Time: {time_formatted}")

    def emit_key(self, obj):
        time_data = time.localtime(obj['_time'])
        time_formatted = time.strftime('%H:%M:%S', time_data)
        self.event_signal.emit(f"Action: {obj['action']} | Key: {obj['key']} | Time: {time_formatted}") 

    def stop(self):
        self._stop_flag = True
        
    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
