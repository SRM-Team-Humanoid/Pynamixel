#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, ctypes
from reg1_0 import *
from ports import *
from constants import *
from dynamixel_sdk import *


#Daisy chain IO class for protocol 1
class Chain(object):
    def __init__(self, port, port_handler, packet_handler):
        self.port = port
        self.protocol = 1
        self.mx_res = MX_RESOLUTION # MX-28 Resolution
        self.fsr_res = FSR_RESOLUTION #FSR Resolution
        self.port_handler = port_handler
        self.packet_handler = packet_handler
        self.group_sync_write = GroupSyncWrite(self.port_handler, self.packet_handler, ADDR_GOAL_POS, LEN_GOAL_POSITION)
        # self.groupspeed = dxl.groupSyncWrite(self.port, self.protocol, ADDR_MOV_SPEED, LEN_MOV_SPEED)
        # self.groupread = dxl.groupSyncRead(self.port, self.protocol, ADDR_PRES_POS, LEN_PRESENT_POSITION)

    # Check for errors in the last comm
    def check_comm_error(self, id, dxl_comm_result, dxl_error):
        if dxl_comm_result != COMM_SUCCESS:
            print("[id: %d, %s]" %(id, self.packet_handler.getTxRxResult(dxl_comm_result)))
            return False
        elif dxl_error != 0:
            print("[id: %d, %s]" %(id, self.packet_handler.getRxPacketError(dxl_error)))
            return False
        return True

    # Enable/Disable the torque of dyanmixel
    def set_torque_status(self, ids, value):
        for id in ids:
            dxl.write1ByteTxRx(self.port, self.protocol, id, ADDR_TORQUE_ENABLE, value)
            self.check_result(id)
            self.check_error(id)

    # Convert bits to degrees
    def to_degree(self, value):
        angle = int(value*self.mx_res)
        return angle

    # Convert degrees to bits
    def from_degree(self, angle):
        degree = int(float(angle)/self.mx_res)
        return degree

    # Set the moving speed of the dynamixel motors
    def set_moving_speed(self, speed_dict):
        for id, speed in speed_dict.items():
            self.packet_handler.write2ByteTxRx(self.port_handler, id, speed,  ADDR_MOV_SPEED)
            self.check_comm_error(id)

    # Check if dynamixel is moving
    def is_moving(self, id_list):
        moving = {}
        for id in id_list:
            value = self.packet_handler.read1ByteRx(self.port_handler, id, ADDR_MOVING)
            moving[id] = value
        return moving

    # Set the goal position for the dynamixels in the chain
    def set_goal_position(self, angle_dict):
        #self.set_torque_status(write_dict.keys(),1)
        for id, angle in angle_dict.items():
            # Get position from angle
            goal_position = self.from_degree(angle + 180)
            # generate list of byte values from position values
            param_goal_psosition = [DXL_LOBYTE(DXL_LOWORD(goal_position)), DXL_HIBYTE(DXL_LOWORD(goal_position)), DXL_LOBYTE(DXL_HIWORD(goal_position)), DXL_HIBYTE(DXL_HIWORD(goal_position))]
            # Add dxl goal position value to the Syncwrite storage
            addparam_result = self.group_sync_write.addParam(id, param_goal_position))
            if addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % (id))
                quit()
        # Syncwrite goal position
        self.group_sync_write.txPacket()
        # Clear syncwrite parameter storage
        self.group_sync_write.clearParam()

    # Get the present dynamixel positions
    def get_present_position(self, ids):
        positions = []
        for id in ids:
            present_position = self.packet_handler.read2ByteTxRx(self.port_handler, id, ADDR_PRES_POS)
            # if not self.check_result() and not self.check_error():
            present_position = self.to_degree(present_position)-180
            positions.append(present_position)
        return dict(zip(ids,positions))

    # Convert fsr readings to newtons
    def to_newton(self, value):
        newton = float(value)*self.fsr_res
        return newton

    # Read FSR values
    def get_fsr_readings(self, foot):
        id_dict = {'left':111,'right':112}
        id = id_dict[foot]
        #fsr_reading = {'1':0, '2':0, '3':0, '4':0, 'x':0, 'y':0}
        fsr_reading = {}
        fsr_reg1 = {'1':ADDR_FSR_1, '2':ADDR_FSR_2, '3':ADDR_FSR_3, '4':ADDR_FSR_4}
        fsr_reg2 = {'x':ADDR_FSR_X, 'y':ADDR_FSR_Y}

        for reg in fsr_reg1.keys():
            fsr_reading[reg] = self.to_newton(self.packet_handler.read2ByteTxRx(self.port_handler, id, fsr_reg1[reg]))
            self.check_comm_error(id)
        for reg in fsr_reg2.keys():
            fsr_reading[reg] = self.packet_handler.read1ByteTxRx(self.port_handler, id, fsr_reg2[reg])
            self.check_comm_error(id)
        return fsr_reading
