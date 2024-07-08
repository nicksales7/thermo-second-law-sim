88# thermo-second-law-sim
A simulation of the second law of thermodynamics using gas molecules with elastic collisions in a closed system.

# Features
- Collisions between gas molecules behave elastically (i.e. no net loss of kinetic energy due to collision).
  - Collisions are detected by dividing the window into 8 quadrants and checking for nearby molecules within the current quadrant. Do they detect collisions on quadrant boundaries? Of course not, I'm lazy.
- Gas molecules begin in the bottom right corner (randomized in a 49x49 pixel box) of the window (start at very low entropy -> increase entropy over time).
- Calculates entropy by using the Boltzmann-Plank measure of entropy. (i.e. quantifying system disorder using S = (k_B)(ln)(W), where k_B is the Boltzmann constant and W denotes microstate multiplicity)

--- 
- A plot of the increase in entropy starting from t = 0. (lol not yet)

# TODO
- Use matplotlib to visualize the increase in entropy.
- Possibly add a calculation to determine the complexity of the system (https://scottaaronson.blog/?p=762)
- Optimize, shit is slow af.

# Usage
```python
pip install matplotlib numpy pygame
```
```bash
# value is the number of molecules and iterations in the sim, default is 100 and 10000 respectively
python main.py MOL=<value> ITER=<value> 
```
