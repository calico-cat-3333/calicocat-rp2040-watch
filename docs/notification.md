## `notification` - 通知

负责通知中心 UI 和管理通知。

## send(title, text, nid=None, *, popup=False)

发送一条通知，返回通知 id。

参数 title 和 text 为字符串，分别为通知标题和正文。

参数 nid 为通知 id 对于 Gadgetbridge 发送的通知，通知 id 将由 Gadgetbridge 制定，否则应该留空为 None，随后将自动生成新通知 id 并作为该函数的返回值。

参数 popup 为布尔类型，表示该通知是否会弹出，如果为 True 则收到通知后，将弹出该通知覆盖当前窗口。

## remove(nid, need_refresh=True)

删除一条通知。

参数 nid 为通知 id, 如果不是有效通知 id 则不会做任何事。

参数 need_refresh 为布尔类型，表示是否需要请求刷新通知中心 UI.

## clear_all(need_refresh=True)

清空通知中心中的全部通知。

参数 need_refresh 为布尔类型，表示是否需要请求刷新通知中心 UI.