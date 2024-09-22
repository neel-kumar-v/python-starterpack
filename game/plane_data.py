from dataclasses import dataclass
from enum import Enum
import math

@dataclass
class Vector:
    x: float
    y: float

    def deserialize(blob: object) -> "Vector":
        try:
            pos = Vector(blob["x"], blob["y"])
        except:
            print("Failed to validate position json")
            raise

        return pos
    
    def __add__(self, o):
        if o is None:
            return None
        return Vector(self.x + o.x, self.y + o.y)
    def __sub__(self, o):
        if o is None:
            return None
        return Vector(self.x - o.x, self.y - o.y)
    def __rmul__(self, lhs):
        return self * lhs
    def __mul__(self, o):
        if o is None:
            return None
        return Vector(o*self.x, o*self.y)
    def __eq__(self, o):
        if o is None:
            return False
        return self.x == o.x and self.y == o.y
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def dot(self, o):
        if o is None:
            return None
        return self.x*o.x+self.y*o.y
    def norm(self):
        return (self.x**2 + self.y**2)**.5
    def distance(self, o):
        if o is None:
            return -1
        return ((self.x-o.x)**2 + (self.y-o.y)**2)**.5
    
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
    radius: float

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
