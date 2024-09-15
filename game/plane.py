from dataclasses import dataclass

from game.plane_data import PlaneStats, PlaneType, Position

@dataclass
class Plane:
    id: str
    team: str
    type: PlaneType
    position: Position
    angle: float
    health: int
    stats: PlaneStats

    def deserialize(blob: object) -> "Plane":
        try:
            plane = Plane(
                blob["id"],
                blob["team"],
                PlaneType[blob["type"]],
                Position.deserialize(blob["position"]),
                blob["angle"],
                blob["health"],
                blob["stats"]
            )
        except:
            print("Failed to validate plane json")
            raise

        return plane
