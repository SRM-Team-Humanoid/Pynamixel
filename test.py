from dynamixel import Dynamixel
from ports import *

ser = list_port()[0]
baud = 1000000
print(ser)

dxl = Dynamixel(port=ser, baudrate=baud, protocol=1)
dxl.connect()
# dxl.set_op_mode([4,6], 3)
print dxl.read_angle([4,6])
dxl.disconnect()