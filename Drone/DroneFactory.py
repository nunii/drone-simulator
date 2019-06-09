from Drone import Drone
from SmartDrone import SmartDrone
from SmartDroneV2 import SmartDroneV2


class DroneFactory:
    @staticmethod
    def create_drone(typ):
        target_class = typ
        return globals()[target_class]
