import pygame
import random

class Window: 
    def __init__(self) -> None:  
        # Initialize Pygame
        pygame.init()
        
        # Create gas molecules
        self.molecules = [Gas() for _ in range(1000)]
        
        # Set up display
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Gas Simulation")

    
    def game_loop(self, running=True) -> None:
        # Loop
        while running:
            pygame.time.delay(10)
            self.screen.fill((255, 255, 255)) # Clears screen

            for gas in self.molecules:
                pos_x, pos_y = gas.get_position()
                pygame.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 3)
                gas.move_molecule()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

class Gas:
    def __init__(self) -> None:
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        self.x = 800 
        self.y = 600 

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def move_molecule(self, width=800, height=600) -> tuple[float, float]:
        # Change in y and change in x
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Keep within boundaries
        if self.x <= 0 or self.x >= width:
            self.velocity_x = -self.velocity_x
        if self.y <= 0 or self.y >= height:
            self.velocity_y = -self.velocity_y

        return self.x, self.y

if __name__ == "__main__":
    window = Window()
    window.game_loop()
