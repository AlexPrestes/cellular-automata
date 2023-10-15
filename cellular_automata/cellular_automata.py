import numpy as np
import taichi as ti


@ti.data_oriented
class CellularAutomata:
    def __init__(self, width=1600, height=900, scaled=1):
        self.size = (width, height)
        self.scaled = scaled
        self.ws, self.hs = width//scaled, height//scaled
        self.current_state = ti.field(ti.int32, shape=(self.ws, self.hs))
        self.next_state = ti.field(ti.int32, shape=(self.ws, self.hs))
        self.set_current_state()
    
    def set_current_state(self):
        cs = np.zeros((self.ws, self.hs), dtype=np.int32)
        cs[self.ws//2-1:self.ws//2+1, :] = 1
        cs[:, self.hs//2-1:self.hs//2+1] = 1
        self.current_state.from_numpy(cs)
    
    @ti.func
    def count_neighbors(self, x, y):
        neighbors = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i >= 0 and i < self.ws) and (j >= 0 and j < self.hs):
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


if __name__ == '__main__':
    app = CellularAutomata(1000, 1000, 2)
    #app.set_current_state_image('./cellular_automata/test_automata.png')
    #app.make_video(t=30, fps=45)
    app.run()