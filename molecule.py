import numpy as np
import matplotlib.pyplot as plt
import math 
import random 

class Molecule:
    def __init__(self, number) -> None:
        self.number = number
        self.x, self.y = random.randint(750, 799), random.randint(550, 599)
        self.initial_velocity_x, self.initial_velocity_y = random.uniform(-1, 1), random.uniform(-1, 1)
        self.velocity_x, self.velocity_y = self.initial_velocity_x, self.initial_velocity_y

    def get_position(self) -> tuple:
        return self.x, self.y

    def get_velocity(self) -> tuple:
        return self.velocity_x, self.velocity_y

    def calculate_distance(self, m1, m2) -> float:
        return math.sqrt((m2[0] - m1[0])**2 + (m2[1] - m1[1])**2)

    def detect_collision(self, nearby_molecules) -> list:
        collisions = [(self.number, number) for number, pos in nearby_molecules.items() if number != self.number and self.calculate_distance(self.get_position(), pos) < 3]
        return collisions

    def resolve_collision(self, vel) -> None:
        self.velocity_x, self.velocity_y = vel[0], vel[1]
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
        self.k_B = 1.380649e-23  # Boltzmann constant in J/K
        self.k_B_scaled = 1.380649 # Scaled Boltzmann constant for larger numbers

    def unit_vector(self, v1, v2) -> list:
        v2_sub_v1 = np.subtract(v2, v1) 
        magnitude = np.linalg.norm(v2_sub_v1)
        if magnitude == 0:
            return [0, 0] 
        return (v2_sub_v1 / magnitude).tolist()

    def parallel_components(self, v1, v2, unit_vec) -> tuple:
        v1_dot_unit, v2_dot_unit = np.dot(v1, unit_vec), np.dot(v2, unit_vec)
        if np.isnan(v1_dot_unit) or np.isnan(v2_dot_unit):
            return [0, 0], [0, 0]
        return (np.multiply(v1_dot_unit, unit_vec)).tolist(), (np.multiply(v2_dot_unit, unit_vec)).tolist()

    def perpendicular_components(self, v1, v2, parallel) -> tuple:
        perp1, perp2 = np.subtract(v1, parallel[0]), np.subtract(v2, parallel[1])
        if np.isnan(perp1).any() or np.isnan(perp2).any():
            return [0, 0], [0, 0]
        return perp1.tolist(), perp2.tolist()

    def final_velocity(self, parallel, perpendicular) -> tuple:
        final1, final2 = np.add(perpendicular[0], parallel[1]), np.add(perpendicular[1], parallel[0])
        if np.isnan(final1).any() or np.isnan(final2).any():
            return [0, 0], [0, 0]
        return final1.tolist(), final2.tolist()

    def calculate_entropy(self, positions, velocities, num_bins=10):
        # Normalize
        positions, velocities = (positions - np.mean(positions, axis=0)) / np.std(positions, axis=0), (velocities - np.mean(velocities, axis=0)) / np.std(velocities, axis=0)
        phase_space = np.hstack((positions, velocities)) 

        # Dynamic bin size
        bin_edges = [np.linspace(np.min(phase_space[:,i]), np.max(phase_space[:,i]), num_bins+1) for i in range(phase_space.shape[1])]

        hist, _ = np.histogramdd(phase_space, bins=bin_edges)
        probabilities = hist / np.sum(hist)
        non_zero_probs = probabilities[probabilities > 0]
        entropy = -self.k_B_scaled * np.sum(non_zero_probs * np.log(non_zero_probs))
        
        return entropy

"""
    def plot_entropy(self, iterations, entropy): # TODO: too lazy rn
       x, y = np.array([0, iterations]), np.array([0, entropy.max()])
       
       plt.xlabel("Iterations")
       plt.ylabel("Boltzmann Entropy")
        
       plt.plot(x, y)
       plt.show()
"""
