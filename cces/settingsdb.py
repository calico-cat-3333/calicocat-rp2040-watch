import json
import os

from .log import log, ERROR
from .utils import path_exist, is_file
from . import hal

_settings = {}
SETTINGS_FILE = '/settings.json'

def load_settings():
    log('load settings from file')
    if not path_exist(SETTINGS_FILE):
        log('/settings.json not existed, create it')
        save_settings()
        return
    try:
        with open(SETTINGS_FILE, 'r') as f:
            _read = json.load(f)
        _settings.update(_read)
        log('setting load success')
    except Exception as e:
        log('faild to load settings from file: ', e, level=ERROR, exc=e)

def get(key, default=None):
    return _settings.setdefault(key, default)

def put(key, value):
    _settings[key] = value

def remove(key):
    if _settings.pop(key, None) == None:
        log('settings', key, 'not exist or is None')

def save_settings():
    log('save settings to file')
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(_settings, f, separators=(',', ':'))
        log('settings save success')
    except Exception as e:
        log('faild to save settings to file:', e, level=ERROR, exc=e)

def start():
    load_settings()
    hal.dispdev.set_brightness(get('display_brightness', 100))
    hal.buzzer.set_volume(get('sound_volume', 100))