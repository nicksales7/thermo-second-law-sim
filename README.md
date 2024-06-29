# gas-second-law
A simulation of the second law of thermodynamics using gas particles with elastic collisions in a closed system.

# Features
- Collisions between gas molecules behave elastically (i.e no net loss of kinetic energy due to collision).
- Gas molecules begin in a fixed corner of the closed system (start at very low entropy -> end with very high entropy).

# TODO
- Implement proper physics for gas molecule collision.
- Calculate the systems entropy using Boltzmann entropy.
- Use matplotlib to visualize the increase in entropy.
- Possibly add calculation to determine the systems complexity (low entropy, low complexity -> medium entropy, high complexity -> high entropy, low complexity).
- Optimize, shit is slow af.

# Usage
```python
pip install matplotlib numpy pygame
python main.py
```
