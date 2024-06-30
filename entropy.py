import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

class Entropy():
    def __init__(self) -> None:        
        self.k_B = 1.380649e-23  # Boltzmann constant in J/K
        self.k_B_scaled = 1.380649 # Scaled Boltzmann constant for larger numbers

    def calculate_entropy(self, positions, velocities, num_bins=10):
        if not positions or not velocities:
            return 0

        # Normalize
        positions = (positions - np.mean(positions, axis=0)) / np.std(positions, axis=0)
        velocities = (velocities - np.mean(velocities, axis=0)) / np.std(velocities, axis=0)

        phase_space = np.hstack((positions, velocities)) 

        # Dynamic bin size
        bin_edges = [np.linspace(np.min(phase_space[:,i]), np.max(phase_space[:,i]), num_bins+1) for i in range(phase_space.shape[1])]

        hist, _ = np.histogramdd(phase_space, bins=bin_edges)
        probabilities = hist / np.sum(hist)
        non_zero_probs = probabilities[probabilities > 0]
        entropy = -self.k_B_scaled * np.sum(non_zero_probs * np.log(non_zero_probs))
        
        return entropy

    def plot_entropy(self, time, entropy): # TODO: too lazy rn
       plt.switch_backend('TkAgg')
       x_points = np.array([0, time])
       y_points = np.array([0, entropy])

       plt.plot(x_points, y_points)
       plt.show()
