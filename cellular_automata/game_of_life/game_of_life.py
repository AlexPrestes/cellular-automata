import numpy as np
import taichi as ti


@ti.data_oriented
class CellularAutomata:
    def __init__(self, width=1600, height=900):
        self.size = (width, height)
        self.current_state = ti.field(ti.int32, shape=self.size)
        self.next_state = ti.field(ti.int32, shape=self.size)
        self.current_state.fill(0)
        self.next_state.fill(0)
    
    @ti.func
    def count_neighbors(self, x, y):
        neighbors = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                #if (i >= 0 and i < self.size[0]) and (j >= 0 and j < self.size[1]):
                neighbors += self.current_state[i, j]
        return neighbors

    @ti.func
    def rules_cell(self, x, y):
        neighbors = self.count_neighbors(x, y)

        if self.current_state[x, y] == 1:
            neighbors -= 1
            if neighbors == 2 or neighbors == 3:
                self.next_state[x, y] = 1
            else:
                self.next_state[x, y] = 0
        else:
            if neighbors == 3:
                self.next_state[x, y] = 1
            else:
                self.next_state[x, y] = 0

    @ti.kernel
    def step(self):
        for x, y in self.current_state:
            self.rules_cell(x, y)