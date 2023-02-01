import matplotlib.pyplot as plt
import numpy as np

class Cube:
    def __init__(self, size):
        self.face_num = size
        self.ax = plt.figure().add_subplot(projection = '3d')
        # prepare some axis points
        self.n_voxels = np.ones((self.face_num + 2, self.face_num + 2, self.face_num + 2), dtype = bool)
        self.size = np.array(self.n_voxels.shape) * 2
        # generate gap
        self.filled_2 = np.zeros(self.size - 1, dtype = self.n_voxels.dtype)
        self.filled_2[::2, ::2, ::2] = self.n_voxels
        
        self.x, self.y, self.z = np.indices(np.array(self.filled_2.shape) + 1).astype(float) // 2  # 3x6x6x8，其中x,y,z均为6x6x8
        
        self.filled_2[0, 0, :] = 0
        self.filled_2[0, -1, :] = 0
        self.filled_2[-1, 0, :] = 0
        self.filled_2[-1, -1, :] = 0
        
        self.x[1::2, :, :] += 0.95
        self.y[:, 1::2, :] += 0.95
        self.z[:, :, 1::2] += 0.95
        
        self.x[0, :, :] += 0.94
        self.y[:, 0, :] += 0.94
        self.z[:, :, 0] += 0.94

        self.x[-1, :, :] -= 0.94
        self.y[:, -1, :] -= 0.94
        self.z[:, :, -1] -= 0.94

        self.filled_2[0, 0, :] = 0
        self.filled_2[0, -1, :] = 0
        self.filled_2[-1, 0, :] = 0
        self.filled_2[-1, -1, :] = 0

        self.filled_2[:, 0, 0] = 0
        self.filled_2[:, 0, -1] = 0
        self.filled_2[:, -1, 0] = 0
        self.filled_2[:, -1, -1] = 0

        self.filled_2[0, :, 0] = 0
        self.filled_2[0, :, -1] = 0
        self.filled_2[-1, :, 0] = 0
        self.filled_2[-1, :, -1] = 0
        
        self.color_map = np.array(['#ffd400', "#fffffb", "#f47920", "#d71345", "#145b7d", "#45b97c"])
        self.facecolors = np.full(self.filled_2.shape, '#77787b')  # 设一个灰色的基调
        
        self.facecolors[:, :, -1] = self.color_map[0]  # up:    yellow
        self.facecolors[:, :, 0]  = self.color_map[1]  # down:  white
        self.facecolors[:, 0, :]  = self.color_map[2]  # left:  orange
        self.facecolors[:, -1, :] = self.color_map[3]  # right: red
        self.facecolors[0, :, :]  = self.color_map[4]  # front: blue
        self.facecolors[-1, :, :] = self.color_map[5]  # back:  green
        
    
    def _show(self):
        self.ax.voxels(self.x, self.y, self.z, self.filled_2, facecolors = self.facecolors)
        plt.axis("off")
        plt.show()

if __name__ == '__main__':
    cube = Cube(3)
    cube._show()
