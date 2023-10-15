import numpy as np
import taichi as ti
from enum import Enum


class StateMatter(Enum):
    SOLID: int = 0
    LIQUID: int = 1
    GAS: int = 2


class Particle:
    def __init__(self, color, gravity, state_of_matter):
        super().__init__()
        self.color: ti.math.vec3 = color
        self.gravity: bool = gravity
        self.state_of_matter: StateMatter = state_of_matter
    
    def move(self, current_field: ti.field, next_field: ti.field):
        pass
    

    def swap(self, xi: ti.i32, yi: ti.i32, xj: ti.i32, yj: ti.i32):
        pass


class Air(Particle):
    def __init__(self):
        super().__init__(
            color=(1, 1, 1),
            gravity=False,
            state_of_matter=StateMatter.GAS
        )


class Rock(Particle):
    def __init__(self):
        super().__init__(
            color=(0.2, 0.2, 0.2),
            gravity=False,
            state_of_matter=StateMatter.SOLID
        )


class Sand(Particle):
    def __init__(self):
        super().__init__(
            color=(1, 1, 0),
            gravity=True,
            state_of_matter=StateMatter.SOLID
        )


class Water(Particle):
    def __init__(self):
        super().__init__(
            color=(0, 0, 1),
            gravity=True,
            state_of_matter=StateMatter.LIQUID
        )