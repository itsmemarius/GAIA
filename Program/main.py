from gripper_package import *
import time

gripper = Gripper()

gripper.set_force(50)
gripper.set_speed(50)

time.sleep(3)
gripper.set_position(1000)

    

