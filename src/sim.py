import pygame as py
import numpy as np
from typing import List, Dict, Tuple
from src.molecule import Molecule, MoleculePhysics

class Simulation:
    def __init__(self, number_of_molecules: int = 100, iterations: int = 100000) -> None:
        py.init()
        py.display.set_caption("Gas Simulation")
        self.screen: py.Surface = py.display.set_mode((800, 600))
        self.molecules: List[Molecule] = [Molecule(number) for number in range(number_of_molecules)]
        self.physics: MoleculePhysics = MoleculePhysics()
        self.iterations: int = iterations
        self.entropy: np.ndarray = np.zeros(iterations)
        self.positions: np.ndarray = np.zeros((number_of_molecules, 2))
        self.velocities: np.ndarray = np.zeros((number_of_molecules, 2))
        self.quadrants: Dict[int, Dict[int, Tuple[float, float]]] = {i: {} for i in range(8)}

    def get_quadrant(self, pos_x: float, pos_y: float) -> int:
        if pos_x < 200:
            return 0 if pos_y < 300 else 4
        elif pos_x < 400:
            return 1 if pos_y < 300 else 5
        elif pos_x < 600:
            return 2 if pos_y < 300 else 6
        else:
            return 3 if pos_y < 300 else 7

    def update_quadrant(self, old_quad: int, new_quad: int, number: int, pos: Tuple[float, float]) -> None:
        if old_quad != new_quad:
            self.quadrants[old_quad].pop(number, None)
            self.quadrants[new_quad][number] = pos

    def assign_quadrant(self, pos_x: float, pos_y: float, number: int) -> None:
        quadrant: int = self.get_quadrant(pos_x, pos_y)
        self.quadrants[quadrant][number] = (pos_x, pos_y)

    def get_quadrant_molecules(self, molecule_quadrant: int) -> Dict[int, Tuple[float, float]]:
        nearby: Dict[int, Tuple[float, float]] = self.quadrants[molecule_quadrant].copy()
        # TODO: Add logic later to implement nearby molecules in neighboring quadrants
        return nearby

    def run(self) -> None:
        for loop_count in range(self.iterations):
            py.time.delay(10)
            if not self.handle_events():
                break
            self.draw()
            py.display.update()
            self.update()

        py.quit()

    def handle_events(self) -> bool:
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        return True

    def update(self) -> None:
        collisions: List[Tuple[int, int]] = []
        for i, molecule in enumerate(self.molecules):
            molecule.move_molecule()
            pos_x, pos_y = molecule.get_position()
            self.positions[i] = [pos_x, pos_y]
            self.velocities[i] = molecule.get_velocity()
            self.assign_quadrant(pos_x, pos_y, molecule.number)
            quadrant: int = self.get_quadrant(pos_x, pos_y)
            nearby: Dict[int, Tuple[float, float]] = self.get_quadrant_molecules(quadrant)
            collisions.extend(molecule.detect_collision(nearby))

        for collision in collisions:
            mol1, mol2 = self.molecules[collision[0]], self.molecules[collision[1]]
            v1, v2 = mol1.get_velocity(), mol2.get_velocity()
            unit: List[float] = self.physics.unit_vector(mol1.get_position(), mol2.get_position())
            if unit == [0, 0]:
                print(f"Skipping collision between {mol1.number} and {mol2.number} due to zero magnitude.")
                continue
            parallel: Tuple[List[float], List[float]] = self.physics.parallel_components(v1, v2, unit)
            if parallel == ([0, 0], [0, 0]):
                print(f"Skipping parallel components calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            perpendicular: Tuple[List[float], List[float]] = self.physics.perpendicular_components(v1, v2, parallel)
            if perpendicular == ([0, 0], [0, 0]):
                print(f"Skipping perpendicular components calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            final: Tuple[List[float], List[float]] = self.physics.final_velocity(parallel, perpendicular)
            if final == ([0, 0], [0, 0]):
                print(f"Skipping final velocity calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            mol1.resolve_collision(final[0])
            mol2.resolve_collision(final[1])

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        for pos_x, pos_y in self.positions:
            if isinstance(pos_x, (int, float)) and isinstance(pos_y, (int, float)):
                py.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 3)
            else:
                print(f"Invalid position: {pos_x}, {pos_y}")
        py.display.flip()
