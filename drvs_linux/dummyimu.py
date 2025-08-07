from cces.drvs import Device
# 假装这里有 IMU

class IMU(Device):
    def __init__(self):
        self.dummy_step = 33

    def reset(self):
        pass

    def config(self):
        pass

    def get_accel_xyz(self):
        return [0,0,1]

    def get_gyro_xyz(self):
        return [0,0,0]

    def get_step(self):
        return self.dummy_step

    def clear_step(self):
        self.dummy_step = 0