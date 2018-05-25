import pynamixel.io as pynamixel
import pynamixel.ports as ports
import time

portname = ports.list_ports()[0]
baud = 1000000
ids = [1,2,3,4,5]
angles = [0,0,0,0,0]


print("Connecting to port: " + port)

dxl_io = pynamixel.Dxl_IO(port=portname, baudrate=baud, protocol=1)
dxl_io.chain.set_goal_position(dict(zip(ids,angles)))
time.sleep(0.1)
print("The current angles are: "+ str(dxl_io.chain.get_present_position(ids)))


