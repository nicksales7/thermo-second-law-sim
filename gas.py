import math 
import random 

class Gas:
    def __init__(self, number) -> None:
        # Assign a number to the molecule
        self.number = number

        # Initialize position in small localized corner
        self.x = random.randint(750, 799) 
        self.y = random.randint(550, 599)

        # Initialize initial random velocity
        self.initial_velocity_x = random.uniform(-1, 1)
        self.initial_velocity_y = random.uniform(-1, 1)

        # Set current velocity
        self.velocity_x = self.initial_velocity_x
        self.velocity_y = self.initial_velocity_y

    def get_position(self) -> tuple:
        return self.x, self.y

    def calculate_distance(self, m1, m2) -> float:
        return math.sqrt((m2[0] - m1[0])**2 + (m2[1] - m1[1])**2)

    def detect_collision(self, nearby_molecules) -> list:
        collisions = []
        for number, pos in nearby_molecules.items():
            if number != self.number:
                distance = self.calculate_distance(self.get_position(), pos)
                if distance <= 2:
                    collisions.append((self.number, number))
        return collisions

    def resolve_collision(self, vel, width=800, height=600) -> None:
        self.velocity_x = vel[0]
        self.velocity_y = vel[1]
        self.move_molecule() 

    def move_molecule(self, width=800, height=600) -> None:
        # Change in y and change in x
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Keep within boundaries
        if self.x <= 0 or self.x >= width:
            self.velocity_x = -self.velocity_x
            self.x = max(0, min(self.x, width))
        if self.y <= 0 or self.y >= height:
            self.velocity_y = -self.velocity_y
            self.y = max(0, min(self.y, height))

