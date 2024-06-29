class QuadrantSystem:
    def __init__(self) -> None:
        self.quadrants = {
            0: {},  # Quad 1: 0-399x, 0-299y
            1: {},  # Quad 2: 400-799x, 0-299y
            2: {},  # Quad 3: 0-399x, 300-599y
            3: {},  # Quad 4: 400-799x, 300-599y
}

    def get_quadrant(self, pos_x, pos_y) -> int:
        if pos_x < 400:
            return 0 if pos_y < 300 else 2
        else:
            return 1 if pos_y < 300 else 3

    def update_quadrant(self, old_quad, new_quad, number, pos) -> None:
        if old_quad != new_quad:
            self.quadrants[old_quad].pop(number, None)
            self.quadrants[new_quad][number] = pos

    def assign_quadrant(self, pos_x, pos_y, number) -> None:  
        quadrant = self.get_quadrant(pos_x, pos_y)
        self.quadrants[quadrant][number] = (pos_x, pos_y)
   
    def get_nearby_molecules(self, quadrant) -> dict:
        nearby = self.quadrants[quadrant].copy()
        # TODO: Add logic later to implement nearby molecules ine neighboring quadrants 
        return nearby
