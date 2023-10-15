import numpy as np
import taichi as ti

from .cellular_automata import CellularAutomata


@ti.data_oriented
class App:
    def __init__(self, width=1600, height=900):
        ti.init(arch=ti.cuda)
        self.res = (width, height)
        self.window = ti.ui.Window('pygame', self.res)
        self.canvas = self.window.get_canvas()
        self.frame = ti.Vector.field(3, ti.f32, self.res)
        self.ca = CellularAutomata(width, height, 1)
        self.copy_frame_to_current_state()
        self.radius_draw = 10
        self.paused = False
    
    def events(self):
        if self.window.get_event( ti.ui.PRESS ):
            if self.window.event.key == ti.ui.SPACE:
                self.paused = not self.paused
            
            if self.window.event.key in ['r', 'R']:
                self.reset()

        if self.window.is_pressed(ti.ui.RMB):
            x, y = self.real_pos_mouse()
            self.erase(x, y)
            self.copy_frame_to_current_state()

        if self.window.is_pressed(ti.ui.LMB):
            x, y = self.real_pos_mouse()
            self.draw(x, y)
            self.copy_frame_to_current_state()
        
    
    def real_pos_mouse(self):
        x, y = self.window.get_cursor_pos()
        return int(self.res[0]*x), int(self.res[1]*y)
    
    @ti.func
    def pos_shape(self, x: ti.i32, y: ti.i32, xc: ti.i32, yc: ti.i32) -> bool:
        res = False
        if (x >= 0 and x < self.res[0]) and (y >= 0 and y < self.res[1]):
            res = True
        return res
    
    @ti.kernel
    def draw(self, x: ti.i32, y: ti.i32):
        for i in range(x-self.radius_draw, x+self.radius_draw+1):
            for j in range(y-self.radius_draw, y+self.radius_draw+1):
                if self.pos_shape(i, j, x, y):
                    self.frame[i, j] = (1, 1, 0)
    
    @ti.kernel
    def erase(self, x: ti.i32, y: ti.i32):
        for i in range(x-self.radius_draw, x+self.radius_draw+1):
            for j in range(y-self.radius_draw, y+self.radius_draw+1):
                if self.pos_shape(i, j, x, y):
                    self.frame[i, j] = (0, 0, 0)
    
    @ti.kernel
    def copy_frame_to_current_state(self):
        for x, y in self.frame:
            if self.frame[x, y][0] == 1:
                self.ca.current_state[x, y] = 1
            else:
                self.ca.current_state[x, y] = 0
    
    @ti.kernel
    def copy_current_state_to_frame(self):
        for x, y in self.ca.current_state:
            if self.ca.current_state[x, y]:
                self.frame[x, y] = (1, 1, 0)
            else:
                self.frame[x, y] = (0, 0, 0)
    
    def reset(self):
        self.ca.current_state.from_numpy(np.zeros((self.res[0], self.res[1]), dtype=np.int32))
    
    def update(self):
        if not self.paused:
            self.ca.step()
            self.ca.current_state.copy_from(self.ca.next_state)
        self.copy_current_state_to_frame()
    
    def draw_mouse_contour(self):
        x, y = self.real_pos_mouse()
        for i in range(x-self.radius_draw, x+self.radius_draw+1):
            for j in range(y-self.radius_draw, y+self.radius_draw+1):
                if (x >= 0 and x < self.res[0]) \
                    and (y >= 0 and y < self.res[1]) \
                    and (i == x-self.radius_draw or i == x+self.radius_draw) \
                    and (j == y-self.radius_draw or j == y+self.radius_draw):
                    self.frame[i, j] = (1, 0, 0)

    def run(self):
        while self.window.running:
            self.events()
            self.draw_mouse_contour()
            self.canvas.set_image(self.frame)
            self.update()
            self.window.show()


if __name__ == '__main__':
    app = App()
    app.run()