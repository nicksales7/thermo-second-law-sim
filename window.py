import pygame
from gas import Gas
from quadrant import QuadrantSystem
from physics import Physics

class Window:
    def __init__(self, num_mol=100) -> None:
        # Initialize Pygame
        pygame.init()

        # Create gas molecules
        self.molecules = [Gas(number) for number in range(num_mol)]
        self.quadrant = QuadrantSystem()

        # Set up display
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Gas Simulation")

        self.test = Physics()

    def game_loop(self, running=True) -> None:
        # Loop
        while running:
            pygame.time.delay(10)
            self.screen.fill((255, 255, 255)) # Clears screen
            # Physics update
            collisions = []
            for gas in self.molecules:
                gas.move_molecule()
                pos_x, pos_y = gas.get_position()
                self.quadrant.assign_quadrant(pos_x, pos_y, gas.number)

                quadrant = self.quadrant.get_quadrant(pos_x, pos_y)
                nearby = self.quadrant.get_nearby_molecules(quadrant)
                collisions.extend(gas.detect_collision(nearby))

            # Collisions resolution
            for collision in collisions:
                mol1, mol2 = self.molecules[collision[0]], self.molecules[collision[1]]
                v1 = [mol1.velocity_x, mol1.velocity_y]
                v2 = [mol2.velocity_x, mol2.velocity_y]
                unit = self.test.unit_vector(mol1.get_position(), mol2.get_position())
                para = self.test.parallel_components(v1, v2, unit)
                perp = self.test.perpendicular_components(v1, v2, unit)
                final = self.test.final_velocity(para, perp)
                mol1.resolve_collision(final[0])
                mol2.resolve_collision(final[1])
            
            # Rendering
            for gas in self.molecules:
                pos_x, pos_y = gas.get_position()
                if isinstance(pos_x, (int, float)) and isinstance(pos_y, (int, float)):
                    pygame.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 3)
                else:
                    print(f"Invalid position for molecule {gas.number}: {pos_x}, {pos_y}")


            pygame.display.update()


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
