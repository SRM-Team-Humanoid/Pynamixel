#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, ctypes
import protocol1_0, protocol2_0
from dynamixel_sdk import *

class Dxl_IO(object):
    # Initializer for Dynamixel I/O object
    def __init__(self, baudrate=1000000, port='/dev/ttyUSB0', protocol = 1.0):
        self.baudrate = baudrate
        self.portHandler = PortHandler(port)
        self.protocol = protocol
        self.packetHandler = PacketHandler(float(self.protocol))
        if self.protocol == 1.0:
            chain = protocol1_0.Chain(port=self.port, portHandler=self.portHandler, packetHandler=self.packetHandler)
        elif self.protocol == 2.0:
            chain = protocol2_0.Chain(port=self.port, portHandler=self.portHandler, packetHandler=self.packetHandler)
        self.connect()

    # Open the Port and set the baudrate
    def connect(self):
        if not self.portHandler.openPort():
            print("Failed to open the port!")
            quit()
        if  not self.portHandler.setBaudRate(self.baudrate):
            print("Failed to change the baudrate!")
            quit()

    # Close the Port
    def disconnect(self):
        portHandler.closePort(self.port)
