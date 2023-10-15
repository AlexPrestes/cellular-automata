import numpy as np
import taichi as ti


@ti.data_oriented
class CellularAutomata:
    def __init__(self, width=1600, height=900):
        self.size = (width, height)
        self.current_state = ti.Vector.field(3, ti.f32, shape=self.size)
        self.next_state = ti.Vector.field(3, ti.f32, shape=self.size)
        self.color_background = ti.Vector( (0, 0, 0), ti.f32)
        self.current_state.fill( self.color_background )
        self.next_state.fill( self.color_background )
    
    @ti.func
    def count_neighbors(self, x: ti.i32, y: ti.i32):
        neighbors: ti.i32 = 0
        color_means = ti.Vector( (0, 0, 0), ti.f32)
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if any(self.current_state[i, j] != self.color_background):
                    neighbors += 1
                    color_means += self.current_state[i, j]
        if neighbors != 0:
            color_means /= neighbors
        return neighbors, color_means

    @ti.func
    def rules_cell(self, x: ti.i32, y: ti.i32):
        neighbors, color = self.count_neighbors(x, y)

        if any(self.current_state[x, y] != self.color_background):
            neighbors -= 1
            if neighbors == 2 or neighbors == 3:
                self.next_state[x, y] = color
            else:
                self.next_state[x, y] = self.color_background
        else:
            if neighbors == 3:
                self.next_state[x, y] = color
            else:
                self.next_state[x, y] = self.color_background
        

    @ti.kernel
    def step(self):
        for x, y in self.current_state:
            self.rules_cell(x, y)