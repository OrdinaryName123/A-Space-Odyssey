from characters import *
import math
import random
from items import *

# 3. **game_data.py**: Stores and manages game data like character stats, inventory, and progress.
"""
**Group 3: Game Mechanics (Morgan, Darsh, Ziyi)**
- Implement core game mechanics (movement, inventory, puzzles).
- Design and implement additional gameplay features.
- Focus on playability and enjoyment.
"""

pathfinder = Spaceship("Pathfinder", 1, 500, 500, 500, 500, 500, random.randint(0, 50), 5000, 0, random.randint(100, 500), 1500, [Astral_Bow, Quantum_Quiver])

#pathfinder.attack(Abyssal_Asteroid)