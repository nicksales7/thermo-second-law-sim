import math 
import random 

class Gas:
    def __init__(self, number) -> None:
        # Assign a number to the molecule
        self.number = number

        # Initialize position
        self.x = 800.0
        self.y = 600.0

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
                if distance <= 3:
                    collisions.append((self.number, number))
        return collisions

    def resolve_collision(self):
        # temporary to see if molecules detect collision
        self.velocity_x = -self.velocity_x
        self.velocity_y = -self.velocity_y

    def move_molecule(self, width=800, height=600) -> tuple:
        # Change in y and change in x
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Keep within boundaries
        if self.x <= 0 or self.x >= width:
            self.velocity_x = -self.velocity_x
        if self.y <= 0 or self.y >= height:
            self.velocity_y = -self.velocity_y

        return self.x, self.y
