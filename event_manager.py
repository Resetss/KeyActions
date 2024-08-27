from pynput.keyboard import Key
from pynput.mouse import Button

class EventManager:
    SPECIAL_KEYS = {
        "Key.space": Key.space,
        "Key.shift": Key.shift, 
        "Key.tab": Key.tab, 
        "Key.caps_lock": Key.caps_lock,
        "Key.ctrl": Key.ctrl, 
        "Key.alt": Key.alt, 
        "Key.cmd": Key.cmd, 
        "Key.cmd_r": Key.cmd_r,
        "Key.alt_r": Key.alt_r, 
        "Key.ctrl_l": Key.ctrl_l, 
        "Key.ctrl_r": Key.ctrl_r,
        "Key.shift_r": Key.shift_r, 
        "Key.enter": Key.enter, 
        "Key.backspace": Key.backspace,
        "Key.f1": Key.f1,
        "Key.f2": Key.f2,
        "Key.f3": Key.f3,
        "Key.f4": Key.f4,
        "Key.f5": Key.f5, 
        "Key.f6": Key.f6,
        "Key.f7": Key.f7,
        "Key.f8": Key.f8,
        "Key.f9": Key.f9,
        "Key.f10": Key.f10,
        "Key.f11": Key.f11,
        "Key.f12": Key.f12,
        "Key.f13": Key.f13,
        "Key.f14": Key.f14, 
        "Key.f15": Key.f15, 
        "Key.f16": Key.f16,
        "Key.f17": Key.f17, 
        "Key.f18": Key.f18, 
        "Key.f19": Key.f19, 
        "Key.media_volume_up": Key.media_volume_up, 
        "Key.media_volume_down": Key.media_volume_down,
        "Key.media_volume_mute": Key.media_volume_mute, 
        "Key.media_play_pause": Key.media_play_pause,
        "Key.right": Key.right, 
        "Key.down": Key.down,
        "Key.left": Key.left, 
        "Key.up": Key.up, 
        "Key.page_up": Key.page_up, 
        "Key.page_down": Key.page_down,
        "Key.home": Key.home, 
        "Key.end": Key.end, 
        "Key.delete": Key.delete 
    }

    BUTTONS = {
        "Button.left": Button.left,
        "Button.right": Button.right,
        "Button.middle": Button.middle
    }

    @classmethod
    def get_key(cls, key_name):
        if key_name in cls.SPECIAL_KEYS:
            return cls.SPECIAL_KEYS[key_name]
        elif len(key_name) == 1:
            return key_name
        else:
            raise ValueError(f"Key '{key_name}' not recognized.")

    @classmethod
    def is_key_valid(cls, key_name):
        return key_name in cls.SPECIAL_KEYS or len(key_name) == 1
    
    @classmethod
    def get_button(cls, button_name):
        if button_name in cls.BUTTONS:
            return cls.BUTTONS[button_name]
        else:
            raise ValueError(f"Button '{button_name}' not recognized.")

    @classmethod
    def is_button_valid(cls, button_name):
        return button_name in cls.BUTTONS