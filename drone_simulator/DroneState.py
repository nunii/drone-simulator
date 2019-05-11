from enum import Enum


class DroneState(Enum):
    EMERGENCY_LAND = 0
    LAND = 1
    GROUND = -1
    TAKE_OFF = 2
    HOVER = 3
    SCAN = 4
    FLY_SLOW = 5
    FLY_FAST = 6
    BRAKE = 7
    RTH = 8
    LOW_BAT = 9
    MINOR_BUMP = 10
    MAJOR_BUMP = 11
    REVERSE = 12
    EMERGENCY = 20
