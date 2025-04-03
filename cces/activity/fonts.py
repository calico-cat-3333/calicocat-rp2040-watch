import lvgl as lv

class SYMBOL:
    CLOCK = ''
    RELOAD = ''
    SUN = ''
    MOON = ''
    MAN = ''
    WOMAN = ''
    ACCESSIBILITY = ''
    BELL_DISABLE = ''
    TEMP_HIGH = ''
    TEMP_LOW = ''
    HEART_RATE = ''
    HEART = ''
    CALCULATOR = ''
    CALENDAR = '' # calendar
    WALK = '' # walk
    USER_CONFIG = '' # user_cofig
    SHOE_PRINT = '' # shoe print
    WEIGHT = '' # weight
    RAIN = '' # rain
    HEAVY_RAIN = '' # heavy rain
    SNOW = ''
    WIND = '' # wind
    SMOG = '' # smog
    CLOUD = ''
    COUNTDOWN = ''
    GPS = '' #GPS
    PHONE = ''
    CHIP = ''
    CLOUD_BOLT = '' # cloud bolt
    TORNADO = '🌪'
    STOPWATCH = '' # stopwatch

number_72 = None
extra_symbols = None

def start():
    global extra_symbols
    global number_72

    extra_symbols = lv.binfont_create('S:fonts/extra_symbols.bin')
    extra_symbols.fallback = lv.font_unifont_zh_16
    number_72 = lv.binfont_create('S:fonts/number_72.bin')