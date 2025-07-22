// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "Waveshare RP2040-Touch-LCD-1.28"
// Modified from MPY origin to reduce flash storage to accommodate larger program flash requirement
// of lvgl and its bindings. Developers should review this setting when adding additional features 
#define MICROPY_HW_FLASH_STORAGE_BYTES          (5 * 512 * 1024)
