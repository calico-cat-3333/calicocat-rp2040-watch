from .device import Device
# 假装这里有 IMU

class IMU(Device):
    def __init__(self):
        pass

    def reset(self):
        pass

    def config(self):
        pass

    def get_accel_xyz(self):
        return [0,0,1]

    def get_gyro_xyz(self):
        return [0,0,0]

    def get_step(self):
        return 33

    def clear_step(self):
        pass