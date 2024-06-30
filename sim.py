import pygame as py
from molecule import Molecule, Molecule_Physics

class Simulation:
    def __init__(self, number_of_molecules=100) -> None:
        py.init()
        self.screen = py.display.set_mode((800, 600))
        py.display.set_caption("Gas Simulation")
        self.molecules, self.physics = [Molecule(number) for number in range(number_of_molecules)], Molecule_Physics()
        self.quadrants = {
            0: {},  # Quad 1: 0-199x, 0-299y
            1: {},  # Quad 2: 200-399x, 0-299y 
            2: {},  # Quad 3: 400-599x, 0-299y
            3: {},  # Quad 4: 600-799x, 0-299y
            4: {},  # Quad 5: 0-199x, 300-599y
            5: {},  # Quad 6: 200-399x, 300-599y
            6: {},  # Quad 7: 400-599x, 300-599y
            7: {}   # Quad 8: 600-799x, 300-599y
}

    def get_quadrant(self, pos_x, pos_y) -> int:
        if pos_x < 200:
            return 0 if pos_y < 300 else 4
        elif pos_x < 400:
            return 1 if pos_y < 300 else 5
        elif pos_x < 600:
            return 2 if pos_y < 300 else 6
        else:
            return 3 if pos_y < 300 else 7

    def update_quadrant(self, old_quad, new_quad, number, pos) -> None:
        if old_quad != new_quad:
            self.quadrants[old_quad].pop(number, None)
            self.quadrants[new_quad][number] = pos

    def assign_quadrant(self, pos_x, pos_y, number) -> None:  
        quadrant = self.get_quadrant(pos_x, pos_y)
        self.quadrants[quadrant][number] = (pos_x, pos_y)
  
    def get_quadrant_molecules(self, molecule_quadrant) -> dict:
        nearby = self.quadrants[molecule_quadrant].copy()
        # TODO: Add logic later to implement nearby molecules in neighboring quadrants
        return nearby

    def run(self, running=True) -> None:
        while running:
            py.time.delay(10)
            if not self.handle_events(): running = False
            else:
                self.update()            
                self.draw()
                py.display.update()
        py.quit()
        
    def handle_events(self) -> bool: 
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        return True

    def update(self) -> None:
        collisions = []
        for molecule in self.molecules:
            molecule.move_molecule()
            pos_x, pos_y = molecule.get_position()
            self.assign_quadrant(pos_x, pos_y, molecule.number)
            quadrant = self.get_quadrant(pos_x, pos_y)
            nearby = self.get_quadrant_molecules(quadrant)
            collisions.extend(molecule.detect_collision(nearby))

        for collision in collisions:
            mol1, mol2 = self.molecules[collision[0]], self.molecules[collision[1]]
            v1 = [mol1.velocity_x, mol1.velocity_y]
            v2 = [mol2.velocity_x, mol2.velocity_y]
            unit = self.physics.unit_vector(mol1.get_position(), mol2.get_position())
            if unit == [0, 0]:
                print(f"Skipping collision between {mol1.number} and {mol2.number} due to zero magnitude.")
                continue  
            parallel = self.physics.parallel_components(v1, v2, unit)
            if parallel == ([0, 0], [0, 0]):
                print(f"Skipping parallel components calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            perpendicular = self.physics.perpendicular_components(v1, v2, parallel)
            if perpendicular == ([0, 0], [0, 0]):
                print(f"Skipping perpendicular components calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            final = self.physics.final_velocity(parallel, perpendicular)
            if final == ([0, 0], [0, 0]):
                print(f"Skipping final velocity calculation for molecules {mol1.number} and {mol2.number} due to NaN values.")
                continue
            mol1.resolve_collision(final[0])
            mol2.resolve_collision(final[1])

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        for molecule in self.molecules:
            pos_x, pos_y = molecule.get_position()
            if isinstance(pos_x, (int, float)) and isinstance(pos_y, (int, float)):
                py.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 4)
            else:
                print(f"Invalid position for molecule {molecule.number}: {pos_x}, {pos_y}")
        py.display.flip()
