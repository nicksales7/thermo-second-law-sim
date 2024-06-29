import pygame
from gas import Gas
from quadrant import QuadrantSystem

class Window:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()

        # Create gas molecules
        self.molecules = [Gas(number) for number in range(100)]
        self.quadrant = QuadrantSystem()

        # Set up display
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Gas Simulation")

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
                self.molecules[collision[0]].resolve_collision()
                self.molecules[collision[1]].resolve_collision()

            # Rendering
            for gas in self.molecules:
                pos_x, pos_y = gas.get_position()
                pygame.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 3)


            pygame.display.update()


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
