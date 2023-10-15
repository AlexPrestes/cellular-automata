import numpy as np
import taichi as ti

from game_of_life import CellularAutomata


@ti.data_oriented
class App:
    def __init__(self, width=1600, height=900):
        ti.init(arch=ti.cuda)
        self.res = (width, height)
        self.window = ti.ui.Window('pygame', self.res)
        self.canvas = self.window.get_canvas()
        self.ca = CellularAutomata(width, height)
        self.frame = ti.Vector.field(3, ti.f32, shape=self.res)
        self.radius_draw = 20
        self.paused = False
        self.color_select = ti.Vector( (1,1,0), ti.f32 )
    
    def events(self):
        if self.window.get_event( ti.ui.PRESS ):
            if self.window.event.key == ti.ui.SPACE:
                self.paused = not self.paused
            
            if self.window.event.key in ['r', 'R']:
                self.reset()
            
            if self.window.event.key in ['q', 'Q']:
                exit()
            
            if self.window.event.key == ti.ui.LEFT:
                self.color_select = (1, 1, 0)
            
            if self.window.event.key == ti.ui.RIGHT:
                self.color_select = (0, 1, 0)
            
            if self.window.event.key == ti.ui.UP:
                self.color_select = (1, 0, 0)
            
            if self.window.event.key == ti.ui.DOWN:
                self.color_select = (0, 0, 1)

        if self.window.is_pressed(ti.ui.RMB):
            x, y = self.real_pos_mouse()
            self.erase(x, y)

        if self.window.is_pressed(ti.ui.LMB):
            x, y = self.real_pos_mouse()
            self.draw(x, y, self.color_select)
        
    
    def real_pos_mouse(self):
        x, y = self.window.get_cursor_pos()
        return int(self.res[0]*x), int(self.res[1]*y)
    
    @ti.func
    def pos_shape_square(self, x: ti.i32, y: ti.i32) -> bool:
        res = False
        if (x >= 0 and x < self.res[0]) and (y >= 0 and y < self.res[1]):
            res = True
        return res
    
    @ti.func
    def pos_shape_sphere(self, x: ti.i32, y: ti.i32, xc: ti.i32, yc: ti.i32) -> bool:
        res = False
        if (x >= 0 and x < self.res[0]) and (y >= 0 and y < self.res[1]) and ((x-xc)**2 + (y-yc)**2 <= self.radius_draw**2):
            res = True
        return res
    
    @ti.kernel
    def draw(self, x: ti.i32, y: ti.i32, color: ti.math.vec3):
        for i in range(x-self.radius_draw, x+self.radius_draw+1):
            for j in range(y-self.radius_draw, y+self.radius_draw+1):
                if self.pos_shape_sphere(i, j, x, y) and ti.random(float) <= 0.05:
                    self.ca.current_state[i, j] = color
    
    @ti.kernel
    def erase(self, x: ti.i32, y: ti.i32):
        for i in range(x-self.radius_draw, x+self.radius_draw+1):
            for j in range(y-self.radius_draw, y+self.radius_draw+1):
                if self.pos_shape_sphere(i, j, x, y):
                    self.ca.current_state[i, j] = self.ca.color_background
    
    def reset(self):
        self.ca.current_state.fill(self.ca.color_background)
    
    def update(self):
        if not self.paused:
            self.ca.step()
            self.ca.current_state.copy_from(self.ca.next_state)
        self.frame.copy_from(self.ca.current_state)
    

    def draw_mouse_contour(self):
        x, y = self.real_pos_mouse()
        for i in range(-self.radius_draw, self.radius_draw+1):
            self.frame[i+x, y+self.radius_draw] = (1, 1, 1)
            self.frame[i+x, y-self.radius_draw] = (1, 1, 1)
            self.frame[x+self.radius_draw, i+y] = (1, 1, 1)
            self.frame[x-self.radius_draw, i+y] = (1, 1, 1)

    def run(self):
        while self.window.running:
            self.events()
            self.update()
            #self.draw_mouse_contour()
            self.canvas.set_image(self.ca.current_state)
            self.window.show()


if __name__ == '__main__':
    app = App()
    app.run()