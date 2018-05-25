#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, ctypes
import protocol1_0, protocol2_0
import dynamixel_functions as dxl

class Dxl_IO(object):
    def __init__(self, baudrate=1000000, port='/dev/ttyUSB0', protocol = 1):
        self.baudrate = baudrate
        self.port = dxl.portHandler(port.encode('utf-8'))
        self.protocol = protocol
        if self.protocol == 1:
            chain = protocol1_0.Chain(port = self.port)
        elif self.protocol == 2:
            chain = protocol2_0.Chain(port = self.port)
        dxl.packetHandler()
        self.connect()

    def connect(self):
        if dxl.openPort(self.port):
            dxl.setBaudRate(self.port, self.baudrate)
        else:
            print("Failed to open the port!")
            quit()

    def disconnect(self):
        dxl.closePort(self.port)


