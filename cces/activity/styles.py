import lvgl as lv

# 部分通用 style 目前有：
# 透明背景按钮及其按下后样式

transparent_button = None
white_button = None

def start():
    global transparent_button
    transparent_button = lv.style_t()
    transparent_button.init()
    transparent_button.set_bg_opa(0)
    transparent_button.set_bg_color(lv.color_hex(0xFFFFFF))
    transparent_button.set_shadow_width(0)
    transparent_button.set_shadow_spread(0)
    transparent_button.set_text_color(lv.color_hex(0x000000))

    global white_button
    white_button = lv.style_t()
    white_button.init()
    white_button.set_bg_opa(255)
    white_button.set_bg_color(lv.color_hex(0xFFFFFF))
    white_button.set_shadow_width(0)
    white_button.set_shadow_spread(0)
    white_button.set_text_color(lv.color_hex(0x000000))
