# SettingsDB 设置存储

管理系统设置。内部使用字典存储设置，并使用 json 文件持久保存。

## load_settings()

从文件加载设置，开机时会自动执行一次。

## get(key, default=None)

获取某个设置项，如果设置项不存在，则返回默认值，并将默认值加入设置存储。

参数 key 为字符串，是设置项的键。

参数 default 是如果还没有这个键，则返回这个默认值，并将该默认值加入设置存储。

## put(key, value)

设置某个设置项。

参数 key 为字符串，是设置项的键。

参数 value 是该设置项的值。

## remove(key)

删除某个设置项。

参数 key 为字符串，是设置项的键。

## save_settings()

保存设置项到 json 文件。