import json
import os
import sys

from .log import log, ERROR
from .utils import path_exist, is_file
from . import hal

# 设置存储，储存系统设置项目

_settings = {}
SETTINGS_FILE = '/settings.json'
if sys.platform != 'rp2':
    SETTINGS_FILE = 'settings.json'


def load_settings():
    # 从文件加载设置
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
    # 获取某个设置项，如果设置项不存在，则返回默认值，并将默认值加入设置存储
    return _settings.setdefault(key, default)

def put(key, value):
    # 设置某个设置项
    _settings[key] = value

def remove(key):
    # 删除某个设置项
    if _settings.pop(key, None) == None:
        log('settings', key, 'not exist or is None')

def save_settings():
    # 保存设置项到文件
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