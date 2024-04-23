import serial
import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time


#-----CONSTANTS-----
WRITE_ADDRESS_POSITION = 0x0103
WRITE_ADDRESS_FORCE = 0x0101
WRITE_ADDRESS_SPEED = 0x0104

READ_ADDRESS_CURRENT_POSITION = 0x0202
READ_ADDRESS_FORCE = 0x0101
READ_ADDRESS_SPEED = 0x0104
READ_ADDRESS_INIT_STATE= 0x0200
ADDRESS_GRIPPER_STATE = 0x0201

MESSAGE_DELAY = 0.2

client = ModbusSerialClient(
            port="/dev/tty.usbserial-AB0NVDQJ",
            timeout=1,
            baudrate=115200,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

client.connect()

register_into = client.read_holding_registers(ADDRESS_GRIPPER_STATE, count=1, slave=2, value=0x01)
print(register_into.registers[0])
