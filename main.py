import sys
from src.sim import Simulation
from typing import Tuple, List

def parse_args(molecules: int = 100, iterations: int = 10000) -> Tuple[int, int]:
    mol: int = molecules
    iter: int = iterations
    args: List[str] = sys.argv[1:]
    
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
    mol_count: int
    iter_count: int
    mol_count, iter_count = parse_args()
    simulation: Simulation = Simulation(mol_count, iter_count)
    simulation.run()
