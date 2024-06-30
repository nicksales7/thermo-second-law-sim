import numpy as np
import math 
import random 

class Molecule:
    def __init__(self, number) -> None:
        self.number = number
        self.x = random.randint(750, 799) 
        self.y = random.randint(550, 599)
        self.initial_velocity_x = random.uniform(-1, 1)
        self.initial_velocity_y = random.uniform(-1, 1)
        self.velocity_x = self.initial_velocity_x
        self.velocity_y = self.initial_velocity_y
   
    def get_position(self) -> tuple:
        return float(self.x), float(self.y)

    def calculate_distance(self, m1, m2) -> float:
        return math.sqrt((m2[0] - m1[0])**2 + (m2[1] - m1[1])**2)

    def detect_collision(self, nearby_molecules) -> list:
        collisions = []
        for number, pos in nearby_molecules.items():
            if number != self.number:
                distance = self.calculate_distance(self.get_position(), pos)
                if distance <= 4:
                    collisions.append((self.number, number))
        return collisions

    def resolve_collision(self, vel) -> None:
        self.velocity_x = vel[0]
        self.velocity_y = vel[1]
        self.move_molecule() 

    def move_molecule(self, width=800, height=600) -> None:
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x <= 0 or self.x >= width:
            self.velocity_x = -self.velocity_x
            self.x = max(0, min(self.x, width))
        if self.y <= 0 or self.y >= height:
            self.velocity_y = -self.velocity_y
            self.y = max(0, min(self.y, height))

class Molecule_Physics():
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

    def perpendicular_components(self, v1, v2, parallel) -> tuple:
        perp1 = np.subtract(v1, parallel[0])
        perp2 = np.subtract(v2, parallel[1])
        if np.isnan(perp1).any() or np.isnan(perp2).any():
            return [0, 0], [0, 0]
        return perp1.tolist(), perp2.tolist()

    def final_velocity(self, parallel, perpendicular) -> tuple:
        final1 = np.add(perpendicular[0], parallel[1])
        final2 = np.add(perpendicular[1], parallel[0])
        if np.isnan(final1).any() or np.isnan(final2).any():
            return [0, 0], [0, 0]
        return final1.tolist(), final2.tolist()
