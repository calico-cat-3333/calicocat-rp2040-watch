# Gadgetbridge 服务

解析 Gadgetbridge 通信协议数据，与 Gadgetbridge 应用通信。

这里使用了 Bangle.js 的通信协议，可以参考：

[http://www.espruino.com/Gadgetbridge](http://www.espruino.com/Gadgetbridge)

[https://github.com/Freeyourgadget/Gadgetbridge/blob/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java](https://github.com/Freeyourgadget/Gadgetbridge/blob/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java)

[https://codeberg.org/Freeyourgadget/Gadgetbridge/src/branch/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java](https://codeberg.org/Freeyourgadget/Gadgetbridge/src/branch/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java)

[https://github.com/wasp-os/wasp-os/blob/master/wasp/gadgetbridge.py](https://github.com/wasp-os/wasp-os/blob/master/wasp/gadgetbridge.py)

## weather_data = \{\}

字典，储存接收到的天气数据，可能为空。

如果非空，则字典的键和描述分别对应：

| 键 | 描述 |
|-|-|
| temp | 当前温度（开尔文）|
| hi | 最高温度（开尔文）|
| low | 最低温度（开尔文）|
| hum | 湿度（%）|
| rain | 降雨率（%）|
| uv | 紫外线指数 |
| code | 天气代码，遵循 openweathermap 的标准，参考 [https://openweathermap.org/weather-conditions](https://openweathermap.org/weather-conditions)
| txt | 天气文本 |
| wind | 风速（km/h）|
| wdir | 风向，以正南方为 0 顺时针旋转的度数 |
| loc | 位置 |
| time | 更新时间，unix 时间戳 |

## music_info = \{\}

字典，储存接收到的音乐信息，可能为空。

如果非空，则字典的键和描述分别对应：

| 键 | 描述 |
|-|-|
| artist | 艺术家 |
| album | 专辑名 |
| track | 轨道名 |
| dur | 时长（s） |
| c | 专辑数 |
| n | 轨道数 |

## music_state = \{\}

字典，储存接收到的音乐状态，可能为空。

如果非空，则字典的键和描述分别对应：

| 键 | 描述 |
|-|-|
| state | 状态，"play"/"pause" |
| position | 当前位置（s）|
| shuffle | 随机 |
| repeat | 重复 |

## send_msg(msg_type, text)

发送信息到手机，手机接收到后会弹出 toast 提示。

参数 msg_type 为字符串，仅可为 `"info"`/`"warn"`/`"error"` 表示信息等级。

参数 text 为信息内容字符串。

## music_ctrl(cmd)

发送音乐控制指令。

参数 cmd 为字符串，表示控制指令，指令可以是：`'play'`, `'pause'`, `'next'`, `'previous'`, `'volumeup'`, `'volumedown'` 分别表示播放、暂停、下一曲、上一曲、音量加、音量减。

## find_phone(s)

发送查找手机指令。

参数 s 为布尔类型，表示是否开启查找手机。如果为 `True` 则手机将响铃，为 `False` 将令正在响铃的手机停止响铃。