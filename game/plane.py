from dataclasses import dataclass, field

from game.plane_data import PlaneStats, PlaneType, Vector

@dataclass
class Plane:
    id: str
    team: str
    type: PlaneType
    position: Vector
    angle: float
    health: int
    stats: PlaneStats
    target: Vector

    def deserialize(blob: object) -> "Plane":
        try:
            plane = Plane(
                blob["id"],
                blob["team"],
                PlaneType[blob["type"]],
                Vector.deserialize(blob["position"]),
                blob["angle"],
                blob["health"],
                blob["stats"],
                Vector(0, 0)
            )
        except:
            print("Failed to validate plane json")
            raise

        return plane
