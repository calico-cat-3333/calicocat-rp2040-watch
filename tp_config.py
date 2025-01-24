import cst816s
import board

def config():
    return cst816s.CST816S(board.i2c1, board.tp_int, board.tp_rst)
