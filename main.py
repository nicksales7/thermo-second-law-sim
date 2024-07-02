import sys
from sim import Simulation

def parse_args(molecules=100, iterations=10000) -> tuple:
    mol = molecules
    iter = iterations
    args = sys.argv[1:]
    
    for i in range(len(args)):
        if args[i].startswith("MOL="):
            try:
                mol = int(args[i].split("=")[1])
            except ValueError:
                print("Invalid value for MOL. Using default value.")
        elif args[i].startswith("ITER="):
            try:
                iter = int(args[i].split("=")[1])
            except ValueError:
                print("Invalid value for ITER. Using default value.")
    
    return mol, iter

if __name__ == "__main__":
    mol_count, iter_count = parse_args()
    simulation = Simulation(mol_count, iter_count)
    simulation.run()
