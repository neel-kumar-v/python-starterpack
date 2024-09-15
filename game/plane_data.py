from dataclasses import dataclass
from enum import Enum


@dataclass
class Position:
    x: float
    y: float

    def deserialize(blob: object) -> "Position":
        try:
            pos = Position(blob["x"], blob["y"])
        except:
            print("Failed to validate position json")
            raise

        return pos

class PlaneType(Enum):
    STANDARD = "STANDARD"
    FLYING_FORTRESS = "FLYING_FORTRESS"
    THUNDERBIRD = "THUNDERBIRD"
    SCRAPYARD_RESCUE = "SCRAPYARD_RESCUE"
    PIGEON = "PIGEON"

@dataclass
class PlaneStats:
    speed: float
    turn_speed: float
    max_health: int
    attack_spread_angle: float
    attack_range: float

    def deserialize(blob: object) -> "PlaneStats":
        try:
            plane = PlaneStats(
                blob["speed"],
                blob["turnSpeed"],
                blob["health"],
                blob["attackSpreadAngle"],
                blob["attackRange"],
            )
        except:
            print("Failed to validate plane stats json")
            raise

        return plane
