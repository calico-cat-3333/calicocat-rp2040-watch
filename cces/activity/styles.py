import lvgl as lv

transparent_button = None

def start():
    global transparent_button
    transparent_button = lv.style_t()
    transparent_button.init()
    transparent_button.set_bg_opa(0)
    transparent_button.set_bg_color(lv.color_hex(0xFFFFFF))
    transparent_button.set_shadow_width(0)
    transparent_button.set_shadow_spread(0)
    transparent_button.set_text_color(lv.color_hex(0x000000))
