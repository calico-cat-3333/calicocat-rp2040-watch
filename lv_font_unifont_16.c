/*******************************************************************************
 * Size: 16 px
 * Bpp: 1
 * Opts: --bpp 1 --size 16 --no-compress --font unifont-15.0.06.ttf --range 32-127,176,8226 --format lvgl -o lv_font_unifont_16.c
 ******************************************************************************/

#ifdef LV_LVGL_H_INCLUDE_SIMPLE
#include "lvgl.h"
#else
#include "lvgl/lvgl.h"
#endif

#ifndef LV_FONT_UNIFONT_16
#define LV_FONT_UNIFONT_16 1
#endif

#if LV_FONT_UNIFONT_16

/*-----------------
 *    BITMAPS
 *----------------*/

/*Store the image of the glyphs*/
static LV_ATTRIBUTE_LARGE_CONST const uint8_t glyph_bitmap[] = {
    /* U+0020 " " */
    0x0,

    /* U+0021 "!" */
    0xfe, 0x40,

    /* U+0022 "\"" */
    0x8c, 0x63, 0x10,

    /* U+0023 "#" */
    0x24, 0x92, 0x7f, 0x49, 0x2f, 0xe4, 0x92, 0x40,

    /* U+0024 "$" */
    0x10, 0xfa, 0x4c, 0x87, 0x3, 0x85, 0x49, 0x7c,
    0x20,

    /* U+0025 "%" */
    0x63, 0x28, 0x23, 0x41, 0x6, 0xb, 0x29, 0x91,
    0x18,

    /* U+0026 "&" */
    0x38, 0x88, 0x1, 0x41, 0xa, 0x62, 0xc2, 0x8c,
    0xe4,

    /* U+0027 "'" */
    0xf0,

    /* U+0028 "(" */
    0x2a, 0x49, 0x24, 0x91, 0x10,

    /* U+0029 ")" */
    0x88, 0x12, 0x49, 0x21, 0x40,

    /* U+002A "*" */
    0x11, 0x25, 0x51, 0xc5, 0x52, 0x44, 0x0,

    /* U+002B "+" */
    0x10, 0x20, 0x47, 0xf1, 0x2, 0x4, 0x0,

    /* U+002C "," */
    0xd6,

    /* U+002D "-" */
    0xf0,

    /* U+002E "." */
    0xc0,

    /* U+002F "/" */
    0x4, 0x0, 0x84, 0x0, 0x80, 0x10, 0x2, 0x0,

    /* U+0030 "0" */
    0x31, 0x28, 0x63, 0x96, 0x9c, 0x61, 0x48, 0xc0,

    /* U+0031 "1" */
    0x23, 0x28, 0x42, 0x10, 0x84, 0x27, 0xc0,

    /* U+0032 "2" */
    0x7a, 0x10, 0x41, 0x18, 0x84, 0x20, 0x83, 0xf0,

    /* U+0033 "3" */
    0x7a, 0x10, 0x41, 0x3c, 0x10, 0x61, 0x1, 0xe0,

    /* U+0034 "4" */
    0x8, 0x62, 0x92, 0x8a, 0x2f, 0xc2, 0x8, 0x20,

    /* U+0035 "5" */
    0xfe, 0x8, 0x20, 0xf8, 0x10, 0x41, 0x85, 0xe0,

    /* U+0036 "6" */
    0x39, 0x8, 0x20, 0xfa, 0x18, 0x61, 0x85, 0xe0,

    /* U+0037 "7" */
    0xfc, 0x10, 0x42, 0x8, 0x21, 0x4, 0x10, 0x40,

    /* U+0038 "8" */
    0x7a, 0x18, 0x61, 0x7a, 0x18, 0x61, 0x85, 0xe0,

    /* U+0039 "9" */
    0x7a, 0x18, 0x61, 0x7c, 0x10, 0x41, 0x9, 0xc0,

    /* U+003A ":" */
    0xc0, 0xc0,

    /* U+003B ";" */
    0xc0, 0x35, 0x80,

    /* U+003C "<" */
    0x8, 0x88, 0x88, 0x20, 0x82, 0x8,

    /* U+003D "=" */
    0xfc, 0x0, 0x0, 0xfc,

    /* U+003E ">" */
    0x82, 0x8, 0x20, 0x88, 0x88, 0x80,

    /* U+003F "?" */
    0x7a, 0x10, 0x41, 0x8, 0x40, 0x0, 0x0, 0x40,

    /* U+0040 "@" */
    0x39, 0x19, 0x6b, 0xa6, 0x9a, 0x67, 0x40, 0xf0,

    /* U+0041 "A" */
    0x31, 0x20, 0x21, 0x87, 0xf8, 0x61, 0x86, 0x10,

    /* U+0042 "B" */
    0xfa, 0x18, 0x61, 0xfa, 0x18, 0x61, 0x87, 0xe0,

    /* U+0043 "C" */
    0x7a, 0x18, 0x20, 0x82, 0x8, 0x21, 0x1, 0xe0,

    /* U+0044 "D" */
    0xf2, 0x28, 0x61, 0x86, 0x18, 0x61, 0x8b, 0xc0,

    /* U+0045 "E" */
    0xfe, 0x8, 0x20, 0xfa, 0x8, 0x20, 0x83, 0xf0,

    /* U+0046 "F" */
    0xfe, 0x8, 0x20, 0xfa, 0x8, 0x20, 0x82, 0x0,

    /* U+0047 "G" */
    0x7a, 0x18, 0x20, 0x82, 0x78, 0x61, 0x8d, 0xd0,

    /* U+0048 "H" */
    0x86, 0x18, 0x61, 0xfe, 0x18, 0x61, 0x86, 0x10,

    /* U+0049 "I" */
    0xf9, 0x8, 0x42, 0x10, 0x84, 0x27, 0xc0,

    /* U+004A "J" */
    0x3e, 0x10, 0x20, 0x40, 0x81, 0x2, 0x44, 0x10,
    0xe0,

    /* U+004B "K" */
    0x86, 0x29, 0x28, 0xc3, 0xa, 0x24, 0x8a, 0x10,

    /* U+004C "L" */
    0x82, 0x8, 0x20, 0x82, 0x8, 0x20, 0x83, 0xf0,

    /* U+004D "M" */
    0x86, 0x1c, 0xf1, 0xb6, 0x18, 0x61, 0x86, 0x10,

    /* U+004E "N" */
    0x87, 0x1c, 0x69, 0xa6, 0x59, 0x63, 0x86, 0x10,

    /* U+004F "O" */
    0x7a, 0x18, 0x61, 0x86, 0x18, 0x61, 0x85, 0xe0,

    /* U+0050 "P" */
    0xfa, 0x18, 0x61, 0xfa, 0x8, 0x20, 0x82, 0x0,

    /* U+0051 "Q" */
    0x79, 0xa, 0x14, 0x28, 0x50, 0xa1, 0x5a, 0xcc,
    0xf0, 0x18,

    /* U+0052 "R" */
    0xfa, 0x18, 0x61, 0xfa, 0x48, 0xa2, 0x8a, 0x10,

    /* U+0053 "S" */
    0x7a, 0x18, 0x20, 0x60, 0x70, 0x61, 0x1, 0xe0,

    /* U+0054 "T" */
    0xfe, 0x20, 0x40, 0x81, 0x2, 0x4, 0x8, 0x10,
    0x20,

    /* U+0055 "U" */
    0x86, 0x18, 0x61, 0x86, 0x18, 0x61, 0x85, 0xe0,

    /* U+0056 "V" */
    0x83, 0x6, 0xa, 0x24, 0x48, 0x8a, 0x0, 0x0,
    0x20,

    /* U+0057 "W" */
    0x86, 0x18, 0x61, 0xb6, 0x1c, 0xe1, 0x86, 0x10,

    /* U+0058 "X" */
    0x84, 0x4, 0x80, 0x30, 0x4, 0x80, 0x2, 0x10,

    /* U+0059 "Y" */
    0x82, 0x1, 0x10, 0x2, 0x82, 0x4, 0x8, 0x10,
    0x20,

    /* U+005A "Z" */
    0xfc, 0x10, 0x42, 0x10, 0x84, 0x20, 0x83, 0xf0,

    /* U+005B "[" */
    0xf2, 0x49, 0x24, 0x92, 0x70,

    /* U+005C "\\" */
    0x80, 0x4, 0x8, 0x0, 0x40, 0x2, 0x0, 0x10,

    /* U+005D "]" */
    0xe4, 0x92, 0x49, 0x24, 0xf0,

    /* U+005E "^" */
    0x31, 0x28, 0x40,

    /* U+005F "_" */
    0xfe,

    /* U+0060 "`" */
    0x88, 0x80,

    /* U+0061 "a" */
    0x7a, 0x10, 0x5f, 0x86, 0x18, 0xdd,

    /* U+0062 "b" */
    0x82, 0x8, 0x2e, 0xc6, 0x18, 0x61, 0x87, 0x1b,
    0x80,

    /* U+0063 "c" */
    0x7a, 0x18, 0x20, 0x82, 0x8, 0x5e,

    /* U+0064 "d" */
    0x4, 0x10, 0x5d, 0x8e, 0x18, 0x61, 0x86, 0x37,
    0x40,

    /* U+0065 "e" */
    0x7a, 0x18, 0x7f, 0x82, 0x8, 0x5e,

    /* U+0066 "f" */
    0x19, 0x8, 0x4f, 0x90, 0x84, 0x21, 0x8,

    /* U+0067 "g" */
    0x76, 0x28, 0xa2, 0x71, 0x7, 0xa1, 0x1, 0xe0,

    /* U+0068 "h" */
    0x82, 0x8, 0x2e, 0xc6, 0x18, 0x61, 0x86, 0x18,
    0x40,

    /* U+0069 "i" */
    0x20, 0x0, 0xc2, 0x10, 0x84, 0x21, 0x3e,

    /* U+006A "j" */
    0x8, 0x0, 0x30, 0x84, 0x21, 0x8, 0x43, 0x26,
    0x0,

    /* U+006B "k" */
    0x82, 0x8, 0x22, 0x92, 0x8c, 0x28, 0x92, 0x28,
    0x40,

    /* U+006C "l" */
    0x61, 0x8, 0x42, 0x10, 0x84, 0x21, 0x3e,

    /* U+006D "m" */
    0xed, 0x26, 0x4c, 0x99, 0x32, 0x64, 0xc9,

    /* U+006E "n" */
    0xbb, 0x18, 0x61, 0x86, 0x18, 0x61,

    /* U+006F "o" */
    0x7a, 0x18, 0x61, 0x86, 0x18, 0x5e,

    /* U+0070 "p" */
    0xbb, 0x18, 0x61, 0x86, 0x1c, 0x6e, 0x82, 0x0,

    /* U+0071 "q" */
    0x76, 0x38, 0x61, 0x86, 0x18, 0xdd, 0x4, 0x10,

    /* U+0072 "r" */
    0xbb, 0x18, 0x20, 0x82, 0x8, 0x20,

    /* U+0073 "s" */
    0x7a, 0x10, 0x18, 0x18, 0x8, 0x5e,

    /* U+0074 "t" */
    0x21, 0x9, 0xf2, 0x10, 0x84, 0x20, 0xc0,

    /* U+0075 "u" */
    0x86, 0x18, 0x61, 0x86, 0x18, 0xdd,

    /* U+0076 "v" */
    0x86, 0x18, 0x52, 0x49, 0x20, 0xc,

    /* U+0077 "w" */
    0x83, 0x26, 0x4c, 0x99, 0x32, 0x64, 0xb6,

    /* U+0078 "x" */
    0x84, 0x4, 0x8c, 0x1, 0x20, 0x21,

    /* U+0079 "y" */
    0x86, 0x18, 0x61, 0x85, 0x33, 0x41, 0x5, 0xe0,

    /* U+007A "z" */
    0xfc, 0x10, 0x84, 0x21, 0x8, 0x3f,

    /* U+007B "{" */
    0x34, 0x42, 0x44, 0x84, 0x24, 0x40, 0x30,

    /* U+007C "|" */
    0xff, 0xfc,

    /* U+007D "}" */
    0xc2, 0x4, 0x2, 0x12, 0x44, 0x24, 0xc0,

    /* U+007E "~" */
    0x63, 0x26, 0x30,

    /* U+007F "" */
    0xaa, 0xaa, 0x0, 0x1, 0x80, 0x0, 0x0, 0x1,
    0x80, 0x0, 0x73, 0xd1, 0xca, 0x10, 0x4b, 0xd1,
    0xca, 0x10, 0x73, 0xdf, 0x80, 0x0, 0x0, 0x1,
    0x80, 0x0, 0x0, 0x1, 0x80, 0x0, 0x55, 0x55,

    /* U+00B0 "°" */
    0x69, 0x6,

    /* U+2022 "•" */
    0x77, 0xff, 0xf7, 0x0
};


/*---------------------
 *  GLYPH DESCRIPTION
 *--------------------*/

static const lv_font_fmt_txt_glyph_dsc_t glyph_dsc[] = {
    {.bitmap_index = 0, .adv_w = 0, .box_w = 0, .box_h = 0, .ofs_x = 0, .ofs_y = 0} /* id = 0 reserved */,
    {.bitmap_index = 0, .adv_w = 128, .box_w = 1, .box_h = 1, .ofs_x = 0, .ofs_y = 0},
    {.bitmap_index = 1, .adv_w = 128, .box_w = 1, .box_h = 10, .ofs_x = 4, .ofs_y = 0},
    {.bitmap_index = 3, .adv_w = 128, .box_w = 5, .box_h = 4, .ofs_x = 2, .ofs_y = 8},
    {.bitmap_index = 6, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 14, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 23, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 32, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 41, .adv_w = 128, .box_w = 1, .box_h = 4, .ofs_x = 4, .ofs_y = 8},
    {.bitmap_index = 42, .adv_w = 128, .box_w = 3, .box_h = 12, .ofs_x = 3, .ofs_y = -1},
    {.bitmap_index = 47, .adv_w = 128, .box_w = 3, .box_h = 12, .ofs_x = 2, .ofs_y = -1},
    {.bitmap_index = 52, .adv_w = 128, .box_w = 7, .box_h = 7, .ofs_x = 1, .ofs_y = 1},
    {.bitmap_index = 59, .adv_w = 128, .box_w = 7, .box_h = 7, .ofs_x = 1, .ofs_y = 1},
    {.bitmap_index = 66, .adv_w = 128, .box_w = 2, .box_h = 4, .ofs_x = 3, .ofs_y = -2},
    {.bitmap_index = 67, .adv_w = 128, .box_w = 4, .box_h = 1, .ofs_x = 2, .ofs_y = 4},
    {.bitmap_index = 68, .adv_w = 128, .box_w = 2, .box_h = 1, .ofs_x = 3, .ofs_y = 0},
    {.bitmap_index = 69, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 77, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 85, .adv_w = 128, .box_w = 5, .box_h = 10, .ofs_x = 2, .ofs_y = 0},
    {.bitmap_index = 92, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 100, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 108, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 116, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 124, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 132, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 140, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 148, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 156, .adv_w = 128, .box_w = 2, .box_h = 5, .ofs_x = 3, .ofs_y = 3},
    {.bitmap_index = 158, .adv_w = 128, .box_w = 2, .box_h = 9, .ofs_x = 3, .ofs_y = -1},
    {.bitmap_index = 161, .adv_w = 128, .box_w = 5, .box_h = 9, .ofs_x = 2, .ofs_y = 0},
    {.bitmap_index = 167, .adv_w = 128, .box_w = 6, .box_h = 5, .ofs_x = 1, .ofs_y = 2},
    {.bitmap_index = 171, .adv_w = 128, .box_w = 5, .box_h = 9, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 177, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 185, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 193, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 201, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 209, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 217, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 225, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 233, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 241, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 249, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 257, .adv_w = 128, .box_w = 5, .box_h = 10, .ofs_x = 2, .ofs_y = 0},
    {.bitmap_index = 264, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 273, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 281, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 289, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 297, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 305, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 313, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 321, .adv_w = 128, .box_w = 7, .box_h = 11, .ofs_x = 1, .ofs_y = -1},
    {.bitmap_index = 331, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 339, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 347, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 356, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 364, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 373, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 381, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 389, .adv_w = 128, .box_w = 7, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 398, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 406, .adv_w = 128, .box_w = 3, .box_h = 12, .ofs_x = 4, .ofs_y = -1},
    {.bitmap_index = 411, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 419, .adv_w = 128, .box_w = 3, .box_h = 12, .ofs_x = 1, .ofs_y = -1},
    {.bitmap_index = 424, .adv_w = 128, .box_w = 6, .box_h = 3, .ofs_x = 1, .ofs_y = 9},
    {.bitmap_index = 427, .adv_w = 128, .box_w = 7, .box_h = 1, .ofs_x = 1, .ofs_y = -1},
    {.bitmap_index = 428, .adv_w = 128, .box_w = 3, .box_h = 3, .ofs_x = 2, .ofs_y = 10},
    {.bitmap_index = 430, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 436, .adv_w = 128, .box_w = 6, .box_h = 11, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 445, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 451, .adv_w = 128, .box_w = 6, .box_h = 11, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 460, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 466, .adv_w = 128, .box_w = 5, .box_h = 11, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 473, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = -2},
    {.bitmap_index = 481, .adv_w = 128, .box_w = 6, .box_h = 11, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 490, .adv_w = 128, .box_w = 5, .box_h = 11, .ofs_x = 2, .ofs_y = 0},
    {.bitmap_index = 497, .adv_w = 128, .box_w = 5, .box_h = 13, .ofs_x = 1, .ofs_y = -2},
    {.bitmap_index = 506, .adv_w = 128, .box_w = 6, .box_h = 11, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 515, .adv_w = 128, .box_w = 5, .box_h = 11, .ofs_x = 2, .ofs_y = 0},
    {.bitmap_index = 522, .adv_w = 128, .box_w = 7, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 529, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 535, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 541, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = -2},
    {.bitmap_index = 549, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = -2},
    {.bitmap_index = 557, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 563, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 569, .adv_w = 128, .box_w = 5, .box_h = 10, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 576, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 582, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 588, .adv_w = 128, .box_w = 7, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 595, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 601, .adv_w = 128, .box_w = 6, .box_h = 10, .ofs_x = 1, .ofs_y = -2},
    {.bitmap_index = 609, .adv_w = 128, .box_w = 6, .box_h = 8, .ofs_x = 1, .ofs_y = 0},
    {.bitmap_index = 615, .adv_w = 128, .box_w = 4, .box_h = 13, .ofs_x = 2, .ofs_y = -2},
    {.bitmap_index = 622, .adv_w = 128, .box_w = 1, .box_h = 14, .ofs_x = 4, .ofs_y = -2},
    {.bitmap_index = 624, .adv_w = 128, .box_w = 4, .box_h = 13, .ofs_x = 2, .ofs_y = -2},
    {.bitmap_index = 631, .adv_w = 128, .box_w = 7, .box_h = 3, .ofs_x = 1, .ofs_y = 8},
    {.bitmap_index = 634, .adv_w = 256, .box_w = 16, .box_h = 16, .ofs_x = 0, .ofs_y = -2},
    {.bitmap_index = 666, .adv_w = 128, .box_w = 4, .box_h = 4, .ofs_x = 2, .ofs_y = 6},
    {.bitmap_index = 668, .adv_w = 128, .box_w = 5, .box_h = 5, .ofs_x = 1, .ofs_y = 2}
};

/*---------------------
 *  CHARACTER MAPPING
 *--------------------*/

static const uint16_t unicode_list_1[] = {
    0x0, 0x1f72
};

/*Collect the unicode lists and glyph_id offsets*/
static const lv_font_fmt_txt_cmap_t cmaps[] =
{
    {
        .range_start = 32, .range_length = 96, .glyph_id_start = 1,
        .unicode_list = NULL, .glyph_id_ofs_list = NULL, .list_length = 0, .type = LV_FONT_FMT_TXT_CMAP_FORMAT0_TINY
    },
    {
        .range_start = 176, .range_length = 8051, .glyph_id_start = 97,
        .unicode_list = unicode_list_1, .glyph_id_ofs_list = NULL, .list_length = 2, .type = LV_FONT_FMT_TXT_CMAP_SPARSE_TINY
    }
};



/*--------------------
 *  ALL CUSTOM DATA
 *--------------------*/

#if LVGL_VERSION_MAJOR == 8
/*Store all the custom data of the font*/
static  lv_font_fmt_txt_glyph_cache_t cache;
#endif

#if LVGL_VERSION_MAJOR >= 8
static const lv_font_fmt_txt_dsc_t font_dsc = {
#else
static lv_font_fmt_txt_dsc_t font_dsc = {
#endif
    .glyph_bitmap = glyph_bitmap,
    .glyph_dsc = glyph_dsc,
    .cmaps = cmaps,
    .kern_dsc = NULL,
    .kern_scale = 0,
    .cmap_num = 2,
    .bpp = 1,
    .kern_classes = 0,
    .bitmap_format = 0,
#if LVGL_VERSION_MAJOR == 8
    .cache = &cache
#endif
};

extern const lv_font_t lv_font_unifont_zh_16;


/*-----------------
 *  PUBLIC FONT
 *----------------*/

/*Initialize a public general font descriptor*/
#if LVGL_VERSION_MAJOR >= 8
const lv_font_t lv_font_unifont_16 = {
#else
lv_font_t lv_font_unifont_16 = {
#endif
    .get_glyph_dsc = lv_font_get_glyph_dsc_fmt_txt,    /*Function pointer to get glyph's data*/
    .get_glyph_bitmap = lv_font_get_bitmap_fmt_txt,    /*Function pointer to get glyph's bitmap*/
    .line_height = 16,          /*The maximum line height required by the font*/
    .base_line = 2,             /*Baseline measured from the bottom of the line*/
#if !(LVGL_VERSION_MAJOR == 6 && LVGL_VERSION_MINOR == 0)
    .subpx = LV_FONT_SUBPX_NONE,
#endif
#if LV_VERSION_CHECK(7, 4, 0) || LVGL_VERSION_MAJOR >= 8
    .underline_position = -1,
    .underline_thickness = 1,
#endif
    .dsc = &font_dsc,          /*The custom font data. Will be accessed by `get_glyph_bitmap/dsc` */
#if LV_VERSION_CHECK(8, 2, 0) || LVGL_VERSION_MAJOR >= 9
    .fallback = &lv_font_unifont_zh_16,
#endif
    .user_data = NULL,
};



#endif /*#if LV_FONT_UNIFONT_16*/

