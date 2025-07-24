# CalicoCat's Extendable Smartwatch system

暂简称为 CCES

我的毕业设计项目-基于 RP2040 的智能穿戴设备 的软件部分代码。

整体使用 Micropython + LVGL 开发。

硬件使用了 RP2040-Touch-LCD-1.28 开发板 + 自制扩展板（扩展板设计文件见 hardware 文件夹）。

外壳使用 FreeCAD 设计，设计文件见 case 文件夹。

设计时尽可能考虑了可扩展性和可移植性，未来也可能往别的设备上移植。

[视频展示](https://www.bilibili.com/video/BV1XT8wznE5z)

## 安装体验

克隆此储存库。

### RP2040-Touch-LCD-1.28 真机（带扩展板）

1. 首先需要安装带有中文字体、GC9A01 驱动支持的 lv_micropython。预构建的文件可以在 Release 中获取，编译教程见文档。

2. 将得到的 uf2 文件刷入开发板，连接硬件，并将本储存库的 apps/ 文件夹和 main.py rst.py a.png 复制到开发板中，apps/ 文件夹中的文件为可选的应用，可以根据需要增删。

3. 在开发板上执行 e104ble_setup.py 对蓝牙模块进行配置（这个配置是长期生效的，只需要执行一次）

4. 重启设备，即可体验。

注意：我使用 Thonny 复制文件或进行编程时，可能需要关闭“连接时重置设备”选项。

### RP2040-Touch-LCD-1.28 真机（不带扩展板）

是的，即使没有扩展板也可以体验系统，基本步骤与带扩展板的版本相同，只是：

第二步中，需要先将 main-noextboard.py 重命名成 main.py 再复制到开发板中（或者将开发板中的 main.py 的内容改成和本储存库的 main-noextboard.py 相同。然后将 drvs_linux 文件夹中的 dummyble.py 和 dummphr.py 复制到开发板中。

不需要执行第三步。

然后重启设备即可开始体验。

注意：不带扩展板将无法使用蜂鸣器、蓝牙等功能，心率测量接口将返回随机数，系统不会关闭屏幕。

### 模拟器

需要 linux 操作系统。

使用带有中文字体等扩展的 lv_micropython unix port, 预构建的文件可以从 Release 中获取，编译教程见文档。

将 micropython 可执行文件放在本储存库的文件夹中，执行：

```
./lvmpy_linux.sh testmain_linux.py
```

模拟器不具备全部的真机功能，目前：

心率测量接口将返回随机数。

蜂鸣器通过发送通知实现。

蓝牙部分蓝牙收发通过发送通知和模拟器中的 SimuCtrl 应用实现。

电池及充电状态的显示是固定的。

会模拟关闭屏幕，模拟关闭屏幕时显示将不会更新，日志输出中将包含提示模拟关闭/打开屏幕的内容。

等等。

## 文档

功能和使用介绍：[查看文档](docs/README.md#用户文档)

编译 lv_micropython、扩展应用开发、移植等相关内容：[查看文档](docs/README.md#开发文档)

## Todo

- [ ] 完善文档

- [ ] 重构 HAL

- [ ] 完善 powermanager

- [ ] 完善血氧饱和度算法

- [ ] 编写更多扩展应用

- [ ] 向更多设备移植：RP2350 ESP32 + ST7735 ST7789 等等