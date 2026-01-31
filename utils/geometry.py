import math
import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle at point b given points a, b, and c.
    Points are expected to be [x, y] or [x, y, z] lists/tuples.
    We only use x and y for 2D angle calculation.
    """
    a = np.array([a[0], a[1]])
    b = np.array([b[0], b[1]])
    c = np.array([c[0], c[1]])

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle
