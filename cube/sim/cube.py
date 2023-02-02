import matplotlib.pyplot as plt
import numpy as np
import time

class Cube:
    def __init__(self, order:int):
        self.order = order
        self.color = {"y": "#ffe600", "w": "#fffffb", "o": "#f15a20", "r": "#ed1941", "b": "#2a5caa", "g": "#65c294", "bc": "#afb4db"}
        
        # prepare some axis points
        self.n_voxels = np.ones((self.order + 2, self.order + 2, self.order + 2), dtype = bool)
        self.size = np.array(self.n_voxels.shape) * 2
        # generate gap
        self.body = np.zeros(self.size - 1, dtype = self.n_voxels.dtype)
        self.body[::2, ::2, ::2] = self.n_voxels
        self.facecolors = np.full(self.body.shape, self.color["bc"])
        
        self.x, self.y, self.z = np.indices(np.array(self.body.shape) + 1).astype(float) // 2
        
        self.x[1::2, :, :] += 0.950
        self.y[:, 1::2, :] += 0.950
        self.z[:, :, 1::2] += 0.950
        
        self.x[0, :, :] += 0.945
        self.y[:, 0, :] += 0.945
        self.z[:, :, 0] += 0.945

        self.x[-1, :, :] -= 0.945
        self.y[:, -1, :] -= 0.945
        self.z[:, :, -1] -= 0.945

        self.body[0, 0, :]   = 0
        self.body[0, -1, :]  = 0
        self.body[-1, 0, :]  = 0
        self.body[-1, -1, :] = 0

        self.body[:, 0, 0]   = 0
        self.body[:, 0, -1]  = 0
        self.body[:, -1, 0]  = 0
        self.body[:, -1, -1] = 0

        self.body[0, :, 0]   = 0
        self.body[0, :, -1]  = 0
        self.body[-1, :, 0]  = 0
        self.body[-1, :, -1] = 0
        
        self.faces_up    = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.faces_down  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.faces_left  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.faces_right = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.faces_front = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.faces_back  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        
        # for i in range(self.order * 2 + 3):
        #     # i //= 2
        
        self.faces_up[:, :]    = self.color["y"]
        self.faces_down[:, :]  = self.color["w"]
        self.faces_right[:, :] = self.color["o"]
        self.faces_left[:, :]  = self.color["r"]
        self.faces_front[:, :] = self.color["b"]
        self.faces_back[:, :]  = self.color["g"]
        
        self._fill_color()
        
        # creat a canvas
        self.ax = plt.figure().add_subplot(projection = '3d')
    
    def _fill_color(self):
        self.facecolors[:, :, -1] = self.faces_up    # up:    yellow
        self.facecolors[:, :, 0]  = self.faces_down  # down:  white
        self.facecolors[:, 0, :]  = self.faces_right # right: orange
        self.facecolors[:, -1, :] = self.faces_left  # left:  red
        self.facecolors[0, :, :]  = self.faces_front # front: blue
        self.facecolors[-1, :, :] = self.faces_down  # back:  green
        
    def _show(self):
        self.ax.voxels(self.x, self.y, self.z, self.body, facecolors = self.facecolors)
        plt.ioff
        plt.axis("off")
        plt.show()
        
if __name__ == '__main__':
    cube = Cube(2)
    cube._show()
