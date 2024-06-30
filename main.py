import sys
from sim import Simulation

def parse_args(default=100):
    for arg in sys.argv[1:]:
        if arg.startswith("MOL="):
            try:
                return int(arg.split("=")[1])
            except ValueError:
                print("Invalid value for MOL. Using default value.")
                return default
    return default

if __name__ == "__main__":
    number_of_molecules = parse_args()
    simulation = Simulation(number_of_molecules)
    simulation.run()
