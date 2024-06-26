import pygame
import random

class Window: 
    def __init__(self) -> None:  
        pygame.init()
        self.screen = pygame.display.set_mode((300, 200))
        color = (255, 255, 255)
        self.screen.fill(color)
        pygame.display.set_caption("Gas Entropy")
        pygame.display.flip() 
    
    def game_loop(self, running=True) -> None:
        gas = Gas()
        pos_x, pos_y = gas.get_position()

        while running:
            pygame.time.delay(10)

            self.screen.fill((255, 255, 255)) # Clears screen
            pygame.draw.circle(self.screen, (0, 0, 0), (int(pos_x), int(pos_y)), 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pos_x, pos_y = gas.move_circle(pos_x, pos_y) # Move circle

        pygame.quit()

class Gas:
    def __init__(self) -> None:
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)

    def get_position(self) -> tuple[int, int]:
        return random.randint(0, 300), random.randint(0, 200)

    def move_circle(self, x, y, width=300, height=200) -> tuple[int, int]:
        # Change in y and change in x
        x += self.velocity_x
        y += self.velocity_y

        if x <= 0 or x >= width:
            self.velocity_x = -self.velocity_x
        if y <= 0 or y >= height:
            self.velocity_y = -self.velocity_y

        return x, y


if __name__ == "__main__":
    window = Window()
    window.game_loop()


