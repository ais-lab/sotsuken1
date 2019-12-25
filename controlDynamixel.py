# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:39:43 2019

@author: kojima
"""
import cv2
from dynamixel_sdk import *
from dynamixel_sdk import Protocol2PacketHandler as P2PH                    # Uses Dynamixel SDK library
from dynamixel_sdk import PortHandler
from dynamixel_sdk import PacketHandler

# Control table address
AX_TORQUE_ENABLE       = 24                          # Control table address is different in Dynamixel model
AX_GOAL_POSITION       = 30
AX_PRESENT_POSITION    = 36
AX_MOVING_SPEE         = 32
AX_MOVING              = 46
# Protocol version
PROTOCOL_VERSION            = 1                             # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                             # Dynamixel ID: 1
BAUDRATE                    = 1000000
DEVICENAME                  = "COM3"                # Check which port is being used on your controller
                                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 0                       # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1023                        # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)

ESC_ASCII_VALUE             = 0x1b

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

flag = 0


# Initialize PortHandler Structs
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)
cap = cv2.VideoCapture(0) #cameraの設定

class DXL():

    def __init__(self):

        # Open port
        if portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            quit()


        # Set port baudrate
        if portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            quit()

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, AX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")



    def moveDXL(self):
        global flag
        # Read moving state
        dxl_moving_state, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, AX_MOVING)
        # Write goal position
        if dxl_moving_state == 0:
            if flag == 1:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, AX_GOAL_POSITION, DXL_MINIMUM_POSITION_VALUE)
                flag=0
            else:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, AX_GOAL_POSITION, DXL_MAXIMUM_POSITION_VALUE)
                flag = 1



################## Main Loop ################################################

if __name__ == "__main__":
    
    dx = DXL()

    try:
        while True:
            ret, frame = cap.read()#　カメラの読み込み
            img = frame
            print("press ESC to quit!")
            cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Camera',img)
            if cv2.waitKey(1) & 0xff == 27:
                break
            
            dx.moveDXL()# dynamixelを動かすメソッド

##############################################################################

    finally:
        # Close port
        cap.release()
        cv2.destroyAllWindows()
        portHandler.closePort()


