from pynamixel.protocol1_0 import Dxl_IO
import pynamixel.ports as ports
import time

port = ports.list_ports()[0]
baud = 1000000
ids = [1,2,3,4,5]
angles = [0,0,0,0,0]


print("Connecting to port: " + port)

dxl_io = Dxl_IO(port = port, baudrate = baud)
dxl_io.set_goal_position(dict(zip(ids,angles)))
time.sleep(0.1)
print("The current angles are: "+ str(dxl_io.get_present_position(ids)))


