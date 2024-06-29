import numpy as np

class Physics:
    def __init__(self) -> None: 
        pass

    def unit_vector(self, v1, v2) -> list:
        v2_sub_v1 = np.subtract(v2, v1)
        magnitude = np.linalg.norm(v2_sub_v1) 
        if magnitude == 0:
            return [0, 0] 
        return (v2_sub_v1 / magnitude).tolist()

    def parallel_components(self, v1, v2, unit_vec) -> tuple:
        v1_dot_unit = np.dot(v1, unit_vec)
        v2_dot_unit = np.dot(v2, unit_vec)
        if np.isnan(v1_dot_unit) or np.isnan(v2_dot_unit):
            return [0, 0], [0, 0]
        return (np.multiply(v1_dot_unit, unit_vec)).tolist(), (np.multiply(v2_dot_unit, unit_vec)).tolist()

    def perpendicular_components(self, v1, v2, para) -> tuple:
        perp1 = np.subtract(v1, para[0])
        perp2 = np.subtract(v2, para[1])
        if np.isnan(perp1).any() or np.isnan(perp2).any():
            return [0, 0], [0, 0]
        return perp1.tolist(), perp2.tolist()

    def final_velocity(self, para, perp) -> tuple:
        final1 = np.add(perp[0], para[1])
        final2 = np.add(perp[1], para[0])
        if np.isnan(final1).any() or np.isnan(final2).any():
            return [0, 0], [0, 0]
        return final1.tolist(), final2.tolist()
