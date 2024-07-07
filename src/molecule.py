import numpy as np
import matplotlib.pyplot as plt
import math
import random
from typing import List, Tuple, Dict

class Molecule:
    def __init__(self, number: int) -> None:
        self.number: int = number
        self.x: float = random.randint(750, 799)
        self.y: float = random.randint(550, 599)
        self.initial_velocity_x: float = random.uniform(-1, 1)
        self.initial_velocity_y: float = random.uniform(-1, 1)
        self.velocity_x: float = self.initial_velocity_x
        self.velocity_y: float = self.initial_velocity_y

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_velocity(self) -> Tuple[float, float]:
        return self.velocity_x, self.velocity_y

    def calculate_distance(self, m1: Tuple[float, float], m2: Tuple[float, float]) -> float:
        return math.sqrt((m2[0] - m1[0])**2 + (m2[1] - m1[1])**2)

    def detect_collision(self, nearby_molecules: Dict[int, Tuple[float, float]]) -> List[Tuple[int, int]]:
        return [
            (self.number, number)
            for number, pos in nearby_molecules.items()
            if number != self.number and self.calculate_distance(self.get_position(), pos) < 3
        ]

    def resolve_collision(self, vel: List[float]) -> None:
        self.velocity_x, self.velocity_y = vel
        self.move_molecule()

    def move_molecule(self, width: int = 800, height: int = 600) -> None:
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x <= 1 or self.x >= width - 1:
            self.velocity_x = -self.velocity_x
            self.x = max(1, min(self.x, width - 1))

        if self.y <= 1 or self.y >= height - 1:
            self.velocity_y = -self.velocity_y
            self.y = max(1, min(self.y, height - 1))

class MoleculePhysics:
    def __init__(self) -> None:
        self.k_B: float = 1.380649e-23  # Boltzmann constant in J/K
        self.k_B_scaled: float = 1.380649  # Scaled Boltzmann constant for larger numbers

    def unit_vector(self, v1: Tuple[float, float], v2: Tuple[float, float]) -> List[float]:
        v2_sub_v1: np.ndarray = np.subtract(v2, v1)
        magnitude = np.linalg.norm(v2_sub_v1)  
        if magnitude == 0:
            return [0, 0]
        return (v2_sub_v1 / magnitude).tolist()

    def parallel_components(self, v1: Tuple[float, float], v2: Tuple[float, float], unit_vec: List[float]) -> Tuple[List[float], List[float]]:
        v1_dot_unit: float = np.dot(v1, unit_vec)
        v2_dot_unit: float = np.dot(v2, unit_vec)
        if np.isnan(v1_dot_unit) or np.isnan(v2_dot_unit):
            return [0, 0], [0, 0]
        return (
            (np.multiply(v1_dot_unit, unit_vec)).tolist(),
            (np.multiply(v2_dot_unit, unit_vec)).tolist()
        )

    def perpendicular_components(self, v1: Tuple[float, float], v2: Tuple[float, float], parallel: Tuple[List[float], List[float]]) -> Tuple[List[float], List[float]]:
        perp1: np.ndarray = np.subtract(v1, parallel[0])
        perp2: np.ndarray = np.subtract(v2, parallel[1])
        if np.isnan(perp1).any() or np.isnan(perp2).any():
            return [0, 0], [0, 0]
        return perp1.tolist(), perp2.tolist()

    def final_velocity(self, parallel: Tuple[List[float], List[float]], perpendicular: Tuple[List[float], List[float]]) -> Tuple[List[float], List[float]]:
        final1: np.ndarray = np.add(perpendicular[0], parallel[1])
        final2: np.ndarray = np.add(perpendicular[1], parallel[0])
        if np.isnan(final1).any() or np.isnan(final2).any():
            return [0, 0], [0, 0]
        return final1.tolist(), final2.tolist()

    def calculate_entropy(self, positions, velocities, num_bins: int = 10) -> float:          
        positions = (positions - np.mean(positions, axis=0)) / np.std(positions, axis=0)
        velocities = (velocities - np.mean(velocities, axis=0)) / np.std(velocities, axis=0)
        phase_space: np.ndarray = np.hstack((positions, velocities))

        bin_edges: List[np.ndarray] = [np.linspace(np.min(phase_space[:, i]), np.max(phase_space[:, i]), num_bins + 1) for i in range(phase_space.shape[1])]

        hist, _ = np.histogramdd(phase_space, bins=bin_edges) 
        probabilities: np.ndarray = hist / np.sum(hist)
        non_zero_probs: np.ndarray = probabilities[probabilities > 0]
        entropy: float = -self.k_B_scaled * np.sum(non_zero_probs * np.log(non_zero_probs))

        return entropy
