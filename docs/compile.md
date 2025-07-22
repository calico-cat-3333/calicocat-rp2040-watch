# 编译 lv_micropython

我们需要修改 lv_micropython 以扩展 Flash 容量、添加中文字体、添加 GC9A01 驱动（仅限 RP2040-Touch-LCD-1.28）

## RP2040-Touch-LCD-1.28

1. 克隆此储存库、 lv_micropython 和 修改过的 gc9a01_mpy 储存库。

```
git clone https://github.com/calico-cat-3333/calicocat-rp2040-watch.git
cd calicocat-rp2040-watch/build_lv_micropython/
git clone https://github.com/lvgl/lv_micropython.git
git clone https://github.com/calico-cat-3333/gc9a01_mpy_lv.git
cd lv_micropython
git submodule update --init --recursive user_modules/lv_binding_micropython
cd ..
```

2. 添加 RP2040-Touch-lcd-1.28 开发板定义。

```
cp -a RP2040-TOUCH-LCD-128 lv_micropython/ports/rp2/board
```

3. 添加中文字体文件

```
cp font/*.c lv_micropython/user_modules/lv_binding_micropython/lvgl/src/font
```

4. 使用这里提供的 lv_conf.h 或按照后文修改 lv_conf.h

```
cp lv_conf.h lv_micropython/user_modules/lv_binding_micropython/lv_conf.h
```

5. 添加冻结 CCES

```
echo 'include("$(MPY_DIR)/../../manifest.py")' >> lv_micropython/ports/rp2/boards/mainifest.py
```

6. 编译

```
cd lv_micropython
make -C ports/rp2 BOARD=PICO submodules
make -j -C mpy-cross
make -j -C ports/rp2 BOARD=RP2040-TOUCH-LCD-128 USER_C_MODULES=../../../bind.cmake
```

然后即可在 lv_micropython/ports/rp2/build-RP2040_TOUCH_LCD128 中获取 firmware.uf2

## Linux 模拟器

如果你已经配置并编译了 RP2040-Touch-LCD-1.28 版本的，则完成第一步后，可以直接跳到第五步。

1. 安装依赖

```
sudo apt-get install build-essential libreadline-dev libffi-dev git pkg-config libsdl2-2.0-0 libsdl2-dev python3 parallel
```

2. 克隆此储存库和 lv_micropython储存库。

```
git clone https://github.com/calico-cat-3333/calicocat-rp2040-watch.git
cd calicocat-rp2040-watch/build_lv_micropython/
git clone https://github.com/lvgl/lv_micropython.git
cd lv_micropython
git submodule update --init --recursive user_modules/lv_binding_micropython
cd ..
```

3. 添加中文字体文件

```
cp font/*.c lv_micropython/user_modules/lv_binding_micropython/lvgl/src/font
```

4. 使用这里提供的 lv_conf.h 或按照后文修改 lv_conf.h

```
cp lv_conf.h lv_micropython/user_modules/lv_binding_micropython/lv_conf.h
```

5. 修改 lv_micropython/user_modules/lv_binding_micropython/lv_conf.h，将 `#define LV_COLOR_16_SWAP 1` 修改为 `#define LV_COLOR_16_SWAP 0`

6. 编译

```
cd lv_micropython
make -C mpy-cross
make -C ports/unix submodules
make -C ports/unix VARIANT=lvgl
```

然后即可在 lv_micropython/ports/unix/build-lvgl 中获取 micropython 可执行文件。

## lv_conf.h 中修改了什么？

声明字体：将 `#define LV_FONT_CUSTOM_DECLARE` 行修改为

```
#define LV_FONT_CUSTOM_DECLARE LV_FONT_DECLARE(lv_font_unifont_zh_16) LV_FONT_DECLARE(lv_font_unifont_16) LV_FONT_DECLARE(lv_font_chinese_calendar) LV_FONT_DECLARE(lv_font_extra_symbols) LV_FONT_DECLARE(lv_font_number72) LV_FONT_DECLARE(lv_font_number90)
```

开启交换字节序：在 `#define LV_COLOR_DEPTH 16` 后添加 `#define LV_COLOR_16_SWAP 1` （仅限 RP2040-Touch-LCD-1.28 或其他使用了 GC9A01 屏幕的平台）

修改默认字体：将 `#define LV_FONT_DEFAULT &lv_font_montserrat_14` 修改为 `#define LV_FONT_DEFAULT &lv_font_unifont_zh_16`

启用压缩字体支持：将 `#define LV_USE_FONT_COMPRESSED 0` 修改为 `#define LV_USE_FONT_COMPRESSED 1`

启用中文日历支持：在 `#define LV_USE_CALENDAR_HEADER_DROPDOWN 1` 后添加 `#define LV_USE_CALENDAR_CHINESE 1`

