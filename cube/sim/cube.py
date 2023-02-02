import matplotlib.pyplot as plt
import numpy as np
import time

class Cube:
    def __init__(self, order):
        self.order = order
        self.color = {"y": "#ffe600", "w": "#fffffb", "o": "#f15a20", "r": "#ed1941", "b": "#2a5caa", "g": "#65c294"}
        
        self.faces_up = np.zeros((self.order, self.order), dtype = int)
        self.faces_down = np.zeros((self.order, self.order), dtype = int)
        self.faces_left = np.zeros((self.order, self.order), dtype = int)
        self.faces_right = np.zeros((self.order, self.order), dtype = int)
        self.faces_front = np.zeros((self.order, self.order), dtype = int)
        self.faces_back = np.zeros((self.order, self.order), dtype = int)
        
        # creat a canvas
        self.ax = plt.figure().add_subplot(projection = '3d')
        # prepare some axis points
        self.n_voxels = np.ones((self.order + 2, self.order + 2, self.order + 2), dtype = bool)
        self.order = np.array(self.n_voxels.shape) * 2
        # generate gap
        self.body = np.zeros(self.order - 1, dtype = self.n_voxels.dtype)
        self.body[::2, ::2, ::2] = self.n_voxels
        self.facecolors = np.full(self.body.shape, '#afb4db')
        
        self.x, self.y, self.z = np.indices(np.array(self.body.shape) + 1).astype(float) // 2
        
        self.body[0, 0, :] = 0
        self.body[0, -1, :] = 0
        self.body[-1, 0, :] = 0
        self.body[-1, -1, :] = 0
        
        self.x[1::2, :, :] += 0.95
        self.y[:, 1::2, :] += 0.95
        self.z[:, :, 1::2] += 0.95
        
        self.x[0, :, :] += 0.94
        self.y[:, 0, :] += 0.94
        self.z[:, :, 0] += 0.94

        self.x[-1, :, :] -= 0.94
        self.y[:, -1, :] -= 0.94
        self.z[:, :, -1] -= 0.94

        self.body[0, 0, :] = 0
        self.body[0, -1, :] = 0
        self.body[-1, 0, :] = 0
        self.body[-1, -1, :] = 0

        self.body[:, 0, 0] = 0
        self.body[:, 0, -1] = 0
        self.body[:, -1, 0] = 0
        self.body[:, -1, -1] = 0

        self.body[0, :, 0] = 0
        self.body[0, :, -1] = 0
        self.body[-1, :, 0] = 0
        self.body[-1, :, -1] = 0
        
        self.facecolors[:, :, -1] = self.color["y"]  # up:    yellow
        self.facecolors[:, :, 0]  = self.color["w"]  # down:  white
        self.facecolors[:, 0, :]  = self.color["o"]  # left:  orange
        self.facecolors[:, -1, :] = self.color["r"]  # right: red
        self.facecolors[0, :, :]  = self.color["b"]  # front: blue
        self.facecolors[-1, :, :] = self.color["g"]  # back:  green
        
        
    def _show(self):
        self.ax.voxels(self.x, self.y, self.z, self.body, facecolors = self.facecolors)
        plt.ioff
        plt.axis("off")
        plt.show()

if __name__ == '__main__':
    cube = Cube(3)
    cube._show()
