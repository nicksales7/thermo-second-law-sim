# gas-second-law
A simulation of the second law of thermodynamics using gas particles with elastic collisions in a closed system.

# Features
- Collisions between gas molecules behave elastically (i.e. no net loss of kinetic energy due to collision).
- Gas molecules begin in a fixed corner (randomized 49x49 pixel box) of the closed system (start at very low entropy -> increase entropy over time).

# TODO
- Use matplotlib to visualize the increase in entropy.
- Possibly add a calculation to determine the systems complexity (https://scottaaronson.blog/?p=762)
- Optimize, shit is slow af xd.

# Usage
```python
pip install matplotlib numpy pygame
```
```bash
# value is number of molecules and iterations in the sim, default is 100 and 10000 respectively
python main.py MOL=<value> ITER=<value> 
```
