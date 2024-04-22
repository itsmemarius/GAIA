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
POSITION_MAX = 1000
POSITION_MIN = 0
FORCE_MAX = 100
FORCE_MIN = 20
SPEED_MAX = 100
SPEED_MIN = 1

MESSAGE_DELAY = 0.2



class Gripper:
    def __init__(self, port='/dev/tty.usbserial-AB0NVDQJ', baudrate=115200):
        self.client = ModbusSerialClient(
            port=port,
            timeout=1,
            baudrate=baudrate,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        self.connect()

    def connect(self):
        if not self.client.connect():
            raise ConnectionError("Failed to connect to the gripper")

    def set_speed(self, speed):
        # Ensure speed is within valid range
        if not SPEED_MIN <= speed <= SPEED_MAX:
            raise ValueError("Speed must be between 0 and 100")

        self.client.write_register(address=WRITE_ADDRESS_SPEED, count=1, slave=2, value=speed)
        time.sleep(MESSAGE_DELAY)
        self._validate_register_update(READ_ADDRESS_SPEED, speed)

    def set_force(self, force):
        # Ensure force is within valid range
        if not FORCE_MIN <= force <= FORCE_MAX:
            raise ValueError("Force must be between 20 and 100")

        self.client.write_register(address=WRITE_ADDRESS_FORCE, count=1, slave=2, value=force)
        time.sleep(MESSAGE_DELAY)
        self._validate_register_update(READ_ADDRESS_FORCE, force)


    def set_position(self, position):
        # Ensure position is within valid range
        if not POSITION_MIN <= position <= POSITION_MAX:
            raise ValueError("Position must be between 0 and 1000")
        self.client.write_register(address=WRITE_ADDRESS_POSITION, count=1, slave=2, value=position) #this is position from 0 to 1000
        time.sleep(MESSAGE_DELAY)
        self._validate_register_update(READ_ADDRESS_CURRENT_POSITION, position)

    def get_position(self):
        # Ensure position is within valid range
        
        self.client.read_holding_registers(address=READ_ADDRESS_CURRENT_POSITION, count=1, slave=2) #this is position from 0 to 1000
        time.sleep(MESSAGE_DELAY)

    def get_gripper_state(self):
        try:
            response = self.client.read_holding_registers(address=ADDRESS_GRIPPER_STATE, count=1, slave=2)
            if response.isError():
                raise ModbusIOException("Modbus communication error")
            state_value = response.registers[0]
            if state_value == 0:
                return "In motion"
            elif state_value == 1:
                return "Reach position"
            elif state_value == 2:
                return "Object caught"
            elif state_value == 3:
                return "Object dropped"
            else:
                return "Unknown state"

        except ModbusIOException as e:
            raise ConnectionError(f"Modbus communication error: {e}")
        
    def get_initialization_state(self):
        try:
            response = self.client.read_holding_registers(address=READ_ADDRESS_INIT_STATE, count=1, slave=2)
            if response.isError():
                raise ModbusIOException("Modbus communication error")
                
            state_value = response.registers[0]
            if state_value == 0:
                return "Not initialized"
            elif state_value == 1:
                return "Initialized"
            else:
                return "Unknown state"

        except ModbusIOException as e:
            raise ConnectionError(f"Modbus communication error: {e}")

    def disconnect(self):
        self.client.close()

    def grab_object_and_wait(self, position=POSITION_MIN, timeout=10):
        self.set_position(position)

        start_time = time.time()
        while True:
            try:
                gripper_state = self.get_gripper_state()
                if gripper_state == "Object caught":
                    return
                elif time.time() - start_time > timeout:
                    raise TimeoutError("Timeout occurred while waiting for the gripper to reach the desired state")

                time.sleep(0.1)
            except ConnectionError as e:
                print(f"Connection error: {e}")
                return
            
    def release_object_and_wait(self, position=POSITION_MAX, timeout=10):
        self.set_position(position)

        start_time = time.time()
        while True:
            try:
                gripper_position = self.get_position()
                if gripper_position == POSITION_MAX:
                    return
                elif time.time() - start_time > timeout:
                    raise TimeoutError("Timeout occurred while waiting for the gripper to reach the desired state")

                time.sleep(0.1)
            except ConnectionError as e:
                print(f"Connection error: {e}")
                return

    def _validate_register_update(self, address, expected_value, timeout=10):
        start_time = time.time()
        while True:
            try:
                response = self.client.read_holding_registers(address, count=1, slave=2)
                if not response.isError() and response.registers[0] == expected_value:
                    return True
                elif (time.time() - start_time > timeout and 
                      self.get_gripper_state() != "Object caught" and 
                      self.get_gripper_state() != "Object dropped"):
                    raise TimeoutError("Timeout occurred while waiting for register update")
            except ModbusIOException as e:
                raise ConnectionError(f"Modbus communication error: {e}")
            
            time.sleep(MESSAGE_DELAY)  # Sleep for a short duration before retrying
        
        

# Exemplu
# gripper = Gripper()
# gripper.set_speed(50)
# gripper.set_force(80)
# gripper.set_position(500)
# gripper.disconnect()