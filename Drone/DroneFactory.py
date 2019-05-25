from Drone import Drone
from SmartDrone import SmartDrone


class DroneFactory:
    @staticmethod
    def create_drone(typ):
        target_class = typ
        return globals()[target_class]
