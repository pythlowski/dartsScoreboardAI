import numpy as np
import random
from darts.dart import Dart

BOARD_SIZE = 1000
SECTOR_ANGLE = 18

BULL = 0.018676
OUTER_BULL = 0.046765
TRIPLE_RING = (0.291176, 0.314706)
DOUBLE_RING = (0.476471, 0.5)

MULTIPLIERS = {
    (0, BULL): lambda x: Dart(25, 2),
    (BULL, OUTER_BULL): lambda x: Dart(25, 1),
    TRIPLE_RING: lambda x: Dart(x, 3),
    DOUBLE_RING: lambda x: Dart(x, 2),
    (0.5, float(np.inf)): lambda x: Dart(0, 1)
}

NUMBERS = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
# [351, 360) u [0,9) -> 6, [9,27) -> 13, [27,45) -> 4, [45,63) -> 18, ..., [81,99) -> 20, ...


def dart_from_polar(distance: float, angle: float) -> Dart:
    sector = NUMBERS[int((angle+9) % 360 / SECTOR_ANGLE)]

    for range_multipliers, dart in MULTIPLIERS.items():
        if range_multipliers[0] <= distance/BOARD_SIZE < range_multipliers[1]:
            return dart(sector)
    return Dart(sector, 1)


def middle(lower: float, greater: float) -> float:
    assert greater > lower
    return greater - (greater - lower)/2


def center_of_target(target_dart: Dart) -> (float, float):
    distance = None
    if target_dart.sector == 25 and target_dart.multiplier == 2:
        distance = 0
    elif target_dart.sector == 25:
        distance = BOARD_SIZE * middle(BULL, OUTER_BULL)
    elif target_dart.multiplier == 1:
        distance = BOARD_SIZE * middle(TRIPLE_RING[1], DOUBLE_RING[0])
    elif target_dart.multiplier == 2:
        distance = BOARD_SIZE * middle(DOUBLE_RING[0], DOUBLE_RING[1])
    elif target_dart.multiplier == 3:
        distance = BOARD_SIZE * middle(TRIPLE_RING[0], TRIPLE_RING[1])

    angle = SECTOR_ANGLE * NUMBERS.index(target_dart.sector) if target_dart.sector <= 20 else 0

    return distance, angle


def cartesian_to_polar(x: float, y: float) -> (float, float):
    distance = np.sqrt(x ** 2 + y ** 2)
    angle = 180 * np.arctan2(y, x) / np.pi
    return distance, angle


def polar_to_cartesian(distance: float, angle: float) -> (float, float):
    angle_radian = np.pi * angle / 180
    x = distance * np.cos(angle_radian)
    y = distance * np.sin(angle_radian)
    return x, y


def apply_throw_error(target_x: float, target_y: float, sigma) -> (float, float):
    [error_x, error_y] = [BOARD_SIZE * BULL * random.gauss(0, sigma) for i in range(2)]
    return target_x + error_x, target_y + error_y


def simulate_throw(target_dart, sigma=1.1):
    center_distance, center_angle = center_of_target(target_dart)
    center_x, center_y = polar_to_cartesian(center_distance, center_angle)
    throw_x, throw_y = apply_throw_error(center_x, center_y, sigma)
    throw_distance, throw_angle = cartesian_to_polar(throw_x, throw_y)
    return dart_from_polar(throw_distance, throw_angle)







