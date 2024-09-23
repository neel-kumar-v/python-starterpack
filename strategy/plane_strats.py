import random
import math
from game.plane_data import Vector
import strategy.utils as u
from game.base_strategy import BaseStrategy
from game.plane import Plane, PlaneType

def all_scrapyard() -> dict[PlaneType, int]:
    return {
        # PlaneType.STANDARD: 10,
        # PlaneType.FLYING_FORTRESS: 1,
        # PlaneType.THUNDERBIRD: 1,
        PlaneType.SCRAPYARD_RESCUE: 10,
        # PlaneType.PIGEON: 10,
    }
def all_pigeons() -> dict[PlaneType, int]:
    return {
        # PlaneType.STANDARD: 5,
        # PlaneType.FLYING_FORTRESS: 1,
        # PlaneType.THUNDERBIRD: 1,
        # PlaneType.SCRAPYARD_RESCUE: 1,
        PlaneType.PIGEON: 100,
    }
def all_thunder() -> dict[PlaneType, int]:
    return {
        # PlaneType.STANDARD: 10,
        # PlaneType.FLYING_FORTRESS: 1,
        PlaneType.THUNDERBIRD: 5,
        # PlaneType.SCRAPYARD_RESCUE: 1,
        # PlaneType.PIGEON: 100,
    }

def all_standard() -> dict[PlaneType, int]:
    return {
        PlaneType.STANDARD: 5,
        # PlaneType.FLYING_FORTRESS: 1,
        # PlaneType.THUNDERBIRD: 1,
        # PlaneType.SCRAPYARD_RESCUE: 1,
        # PlaneType.PIGEON: 100,
    }

def all_fortress() -> dict[PlaneType, int]:
    return {
        # PlaneType.STANDARD: 5,
        PlaneType.FLYING_FORTRESS: 3,
        # PlaneType.THUNDERBIRD: 1,
        # PlaneType.SCRAPYARD_RESCUE: 1,
        PlaneType.PIGEON: 10,
    }