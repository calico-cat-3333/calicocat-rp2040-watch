# `utils` - 实用函数

几个 Micropython 没有官方实现的常用函数。

## path_exist(path)

判断路径是否存在。

参数 path 为路径字符串。

## is_file(path)

判断路径是文件还是文件夹。

参数 path 为路径字符串。

如果是文件，则返回 True 否则返回 False

注意：此函数不会预先判断路径是否存在。