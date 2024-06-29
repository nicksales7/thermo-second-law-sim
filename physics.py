import numpy
import math

class Physics:
    def __init__(self) -> None: 
        pass

    def unit_vector(self, r1, r2) -> tuple:
        # The unit vector along the line of collision
        # r1/r2 = init pos (vector) of molecule 1/2 
        # unit vec = (r2 - r1) / (||r2 - r1||)
        r2_sub_r1 = numpy.subtract(r2, r1)
        magnitude = math.sqrt((r2_sub_r1[0] ** 2) + (r2_sub_r1[1] ** 2)) 
        return r2_sub_r1[0] / magnitude, r2_sub_r1[1] / magnitude 
