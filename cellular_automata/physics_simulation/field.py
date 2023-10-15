import taichi as ti
from .particles import Particle

ti.init(arch=ti.cuda)

class Field:
    def __init__(self) -> None:
        self.field = ti.Struct.field(Particle, shape=(1600, 900))