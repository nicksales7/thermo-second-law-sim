import numpy as np

class Physics:
    def __init__(self) -> None: 
        pass

    def unit_vector(self, v1, v2) -> list:
        # The unit vector along the line of collision
        # r1/r2 = init pos (vector) of molecule 1/2 
        # unit vec = (r2 - r1) / (||r2 - r1||)
        v2_sub_v1 = np.subtract(v2, v1)
        magnitude = np.linalg.norm(v2_sub_v1) 
        return (v2_sub_v1 / magnitude).tolist()

    def parallel_components(self, v1, v2, unit_vec) -> tuple:
        v1_dot_unit = np.dot(v1, unit_vec)
        v2_dot_unit = np.dot(v2, unit_vec)
        return (np.multiply(v1_dot_unit, unit_vec)).tolist(), (np.multiply(v2_dot_unit, unit_vec)).tolist()

    def perpendicular_components(self, v1, v2, para) -> tuple:
        return (np.subtract(v1, para[0])).tolist(), (np.subtract(v2, para[1])).tolist()

    def final_velocity(self, para, perp) -> tuple:
        return (np.add(perp[0], para[1])).tolist(), (np.add(perp[1], para[0])).tolist()
