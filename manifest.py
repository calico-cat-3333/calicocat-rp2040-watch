# 使用方法：
# 在 lv_micropython/ports/rp2/boards/manifest.py 中添加：
# include('path/to/this/manifest.py')
package('cces_drvs')
module('board.py', base_path='lib')
module('extboard.py', base_path='lib')
module('pcf8574.py', base_path='lib')
module('cst816s.py', base_path='lib')