# CCES 文档索引

## 用户文档

了解如何 CCES 及内置应用的使用说明。

[CCES 系统使用](cces_useage.md)

[连接 Gadgetbridge](gadgetbridge_useage.md)

[内置应用使用说明](apps.md)

[应用管理说明](appmanagement.md)

## 开发文档

Todo.

### 编译 lv_micropython

[RP2040-Touch-LCD-1.28](compile.md#RP2040-Touch-LCD-1.28)

[Linux 模拟器](compile.md#Linux-模拟器)

### 系统 API

`cces.`

- [`acitvity` - Activity](activity.md)

- [`appmgr` - AppManager](appmgr.md)

- [`daiyl_scheduler` - 每日任务](dailytask.md)

- [`drvs` - 硬件驱动程序]() - Todo.

- [`gadgetbridge` - Gadgetbridge 服务](gadgetbridge_api.md)

- [`hal` - 硬件抽象层](hal.md)

- [`log` - 日志系统](log.md)

- [`notification` - 通知](notification.md)

- [`powermanager` - 电源管理](powermanager.md)

- [`settingsdb` - 设置存储](settingsdb.md)

- [`task_scheduler` - 任务调度器](task_scheduler.md)

- [`utils` - 实用函数](utils.md)

Todo.

### [编写扩展应用](create_app.md)

### 移植 CCES 到其他设备

Todo.

基本上，完成 lv_micropython 的编译，并编写对应的硬件驱动，即可完成移植的大部分工作。