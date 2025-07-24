watch-baseboard-v1-old.epro 进行了打样测试，并发现错误，需要飞两根线用 10 千欧电阻上拉 BLE_MOD 和 BLE_WKP 解决。

watch-baseboard-v1.epro 是正确的版本，修正了上述错误，但是未经打样验证。

扩展板和开发板之间通过 12Pin SH 1.0 端子线连接，开发板端使用连接器，扩展板端直接焊线。

电池采用 40350 圆形锂电池。

![](../docs/assets/hardware_assimble.jpg)