// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "RP2040 Device with 8MB Flash"
// Modified from MPY origin to reduce flash storage to accommodate larger program flash requirement
// of lvgl and its bindings. Developers should review this setting when adding additional features
#define MICROPY_HW_FLASH_STORAGE_BYTES          (PICO_FLASH_SIZE_BYTES - (3 * 512 * 1024))
