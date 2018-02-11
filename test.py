from dynamixel import Dynamixel
from ports import *

ser = list_port()[0]
baud = 1000000
print(ser)

dxl = Dynamixel(port=ser, baudrate=baud)
dxl.connect()
dxl.set_op_mode([4,6], 3)
dxl.write({4:180, 6:180})
dxl.disconnect()