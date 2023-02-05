import matplotlib.pyplot as plt
import numpy as np

class Cube:
    def __init__(self, order:int):
        self.order = order
        self.color = {"y": "#ffe600", "w": "#fffffb", "o": "#f15a20", "r": "#ed1941", "b": "#2a5caa", "g": "#65c294", "bc": "#afb4db"}
        self.face_color = {"y": 0, "w": 1, "r": 2, "o": 3, "b": 4, "g": 5}
        self.face_up    = np.zeros((self.order, self.order), dtype = int)
        self.face_down  = np.zeros((self.order, self.order), dtype = int)
        self.face_left  = np.zeros((self.order, self.order), dtype = int)
        self.face_right = np.zeros((self.order, self.order), dtype = int)
        self.face_front = np.zeros((self.order, self.order), dtype = int)
        self.face_back  = np.zeros((self.order, self.order), dtype = int)
        
        for i in range(self.order):
            for j in range(self.order):
                self.face_up[i, j]    = self.face_color["y"]
                self.face_down[i, j]  = self.face_color["w"]
                self.face_right[i, j] = self.face_color["r"]
                self.face_left[i, j]  = self.face_color["o"]
                self.face_front[i, j] = self.face_color["b"]
                self.face_back[i, j]  = self.face_color["g"]
                
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
        
        self.colors_up    = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.colors_down  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.colors_left  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.colors_right = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.colors_front = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        self.colors_back  = np.full((self.order * 2 + 3, self.order * 2 + 3), self.color["bc"])
        
        # self.face_down[0,0] = self.face_color["g"]

        self.rotate("F", 1, 1)
        # self.rotate("U", 1, -1)
        # self.rotate("R", 1, -1)

        # creat a canvas
        self.ax = plt.figure().add_subplot(projection = '3d')
        plt.ioff()
        plt.axis("off")
        self.__show() 
    
    def __mat_circ_shift(self, mat, rshift, cshift):
        """
        - mat: input matrix
        - rshift: row shift step, if rshift > 0, down shift, else up shift
        - cshift: col shift step, if cshift > 0, right shift, else left shift
        """
        h, w = mat.shape
        if rshift > 0:
            mat = np.vstack((mat[(h - rshift):, :], mat[:(h - rshift), :]))
        else:
            rshift = -rshift
            mat = np.vstack((mat[rshift:, :], mat[:rshift, :]))
        
        if cshift > 0:
            mat = np.hstack((mat[:, (w - cshift):],mat[:, :(w - cshift)]))
        else:
            cshift = -cshift
            mat = np.hstack((mat[:, cshift:],mat[:, :cshift]))
        
        return mat
        
    def __fill_color(self): 
        x = 0
        y = 0
        for i in range(self.order * 2 + 3 - 1):
            x = (i // 2) - 1
            for j in range(self.order * 2 + 3 - 1):
                y = (j // 2) - 1
                if self.face_up[x, y] == self.face_color["y"]:
                    self.colors_up[i, j] = self.color["y"]
                elif self.face_up[x, y] == self.face_color["w"]:
                    self.colors_up[i, j] = self.color["w"]
                elif self.face_up[x, y] == self.face_color["r"]:
                    self.colors_up[i, j] = self.color["r"]
                elif self.face_up[x, y] == self.face_color["o"]:
                    self.colors_up[i, j] = self.color["o"]
                elif self.face_up[x, y] == self.face_color["b"]:
                    self.colors_up[i, j] = self.color["b"]
                elif self.face_up[x, y] == self.face_color["g"]:
                    self.colors_up[i, j] = self.color["g"]
                else:
                    return
                    
                if self.face_down[x, y] == self.face_color["y"]:
                    self.colors_down[i, j] = self.color["y"]
                elif self.face_down[x, y] == self.face_color["w"]:
                    self.colors_down[i, j] = self.color["w"]
                elif self.face_down[x, y] == self.face_color["r"]:
                    self.colors_down[i, j] = self.color["r"]
                elif self.face_down[x, y] == self.face_color["o"]:
                    self.colors_down[i, j] = self.color["o"]
                elif self.face_down[x, y] == self.face_color["b"]:
                    self.colors_down[i, j] = self.color["b"]
                elif self.face_down[x, y] == self.face_color["g"]:
                    self.colors_down[i, j] = self.color["g"]
                else:
                    return
                
                if self.face_left[x, y] == self.face_color["y"]:
                    self.colors_left[i, j] = self.color["y"]
                elif self.face_left[x, y] == self.face_color["w"]:
                    self.colors_left[i, j] = self.color["w"]
                elif self.face_left[x, y] == self.face_color["r"]:
                    self.colors_left[i, j] = self.color["r"]
                elif self.face_left[x, y] == self.face_color["o"]:
                    self.colors_left[i, j] = self.color["o"]
                elif self.face_left[x, y] == self.face_color["b"]:
                    self.colors_left[i, j] = self.color["b"]
                elif self.face_left[x, y] == self.face_color["g"]:
                    self.colors_left[i, j] = self.color["g"]
                else:
                    return
                
                if self.face_right[x, y] == self.face_color["y"]:
                    self.colors_right[i, j] = self.color["y"]
                elif self.face_right[x, y] == self.face_color["w"]:
                    self.colors_right[i, j] = self.color["w"]
                elif self.face_right[x, y] == self.face_color["r"]:
                    self.colors_right[i, j] = self.color["r"]
                elif self.face_right[x, y] == self.face_color["o"]:
                    self.colors_right[i, j] = self.color["o"]
                elif self.face_right[x, y] == self.face_color["b"]:
                    self.colors_right[i, j] = self.color["b"]
                elif self.face_right[x, y] == self.face_color["g"]:
                    self.colors_right[i, j] = self.color["g"]
                else:
                    return

                if self.face_front[x, y] == self.face_color["y"]:
                    self.colors_front[i, j] = self.color["y"]
                elif self.face_front[x, y] == self.face_color["w"]:
                    self.colors_front[i, j] = self.color["w"]
                elif self.face_front[x, y] == self.face_color["r"]:
                    self.colors_front[i, j] = self.color["r"]
                elif self.face_front[x, y] == self.face_color["o"]:
                    self.colors_front[i, j] = self.color["o"]
                elif self.face_front[x, y] == self.face_color["b"]:
                    self.colors_front[i, j] = self.color["b"]
                elif self.face_front[x, y] == self.face_color["g"]:
                    self.colors_front[i, j] = self.color["g"]
                else:
                    return
                
                if self.face_back[x, y] == self.face_color["y"]:
                    self.colors_back[i, j] = self.color["y"]
                elif self.face_back[x, y] == self.face_color["w"]:
                    self.colors_back[i, j] = self.color["w"]
                elif self.face_back[x, y] == self.face_color["r"]:
                    self.colors_back[i, j] = self.color["r"]
                elif self.face_back[x, y] == self.face_color["o"]:
                    self.colors_back[i, j] = self.color["o"]
                elif self.face_back[x, y] == self.face_color["b"]:
                    self.colors_back[i, j] = self.color["b"]
                elif self.face_back[x, y] == self.face_color["g"]:
                    self.colors_back[i, j] = self.color["g"]
                else:
                    return
                
        self.facecolors[:, :, -1] = self.colors_up 
        self.facecolors[:, :, 0]  = self.colors_down
        self.facecolors[:, 0, :]  = self.colors_right
        self.facecolors[:, -1, :] = self.colors_left
        self.facecolors[0, :, :]  = self.colors_front
        self.facecolors[-1, :, :] = self.colors_back
        
    def __show(self):
        self.__fill_color()
        self.ax.voxels(self.x, self.y, self.z, self.body, facecolors = self.facecolors)
        plt.show()
        
    def rotate(self, ref: str, layer: int, step: int):
        """
        - ref:   ["F", "U", "R"], reference face
        - layer: [1, n], n is a interger number, cube layer
        - step:  [-n, +n], n is a integer number, rotate (n * 90) degrees, -n: clockwise, n: counterclockwise
        ---
        - Front: orange
        - Back:  red
        - Right: green
        - Left:  blue
        - Up:    yellow
        - Down:  white
        """
        if layer > self.order:
            layer = self.order
        elif layer < 1:
            layer = 1
        
        layer_face = np.zeros((4, self.order), dtype = int)
        n = abs(step) % 4
        if step < 0:
            n = -n
        # np.flipud() ,旋转会数组倒序
        if ref == "F":
            layer_face[0, :] = self.face_up[:, layer - 1]
            layer_face[1, :] = self.face_back[layer - 1, :]
            layer_face[2, :] = self.face_down[:, layer - 1]
            layer_face[3, :] = self.face_front[layer - 1, :]
            
            layer_face = self.__mat_circ_shift(layer_face, -n, 0);
            
            self.face_up[:, layer - 1]    = np.flip(layer_face[0, :])
            self.face_back[layer - 1, :]  = np.flip(layer_face[1, :])
            self.face_down[:, layer - 1]  = np.flip(layer_face[2, :])
            self.face_front[layer - 1, :] = np.flip(layer_face[3, :])
            
            if layer == 1:
                self.face_right = np.rot90(self.face_right, n)
            elif layer == self.order:
                self.face_left = np.rot90(self.face_left, n)
        elif ref == "U":
            layer_face[0, :] = self.face_left[:, self.order - layer]
            layer_face[1, :] = self.face_front[:, self.order - layer]
            layer_face[2, :] = self.face_right[:, self.order - layer]
            layer_face[3, :] = self.face_back[:, self.order - layer]
            
            layer_face = self.__mat_circ_shift(layer_face, n, 0)
            
            self.face_left[:, self.order - layer]  = np.flip(layer_face[0, :])
            self.face_front[:, self.order - layer] = np.flip(layer_face[1, :])
            self.face_right[:, self.order - layer] = np.flip(layer_face[2, :])
            self.face_back[:, self.order - layer]  = np.flip(layer_face[3, :])
            
            if layer == 1:
                self.face_up = np.rot90(self.face_up, n)
            elif layer == self.order:
                self.face_down = np.rot90(self.face_down, n)
        elif ref == "R": 
            layer_face[0, :] = self.face_up[self.order - layer, :]
            layer_face[1, :] = self.face_left[:, self.order - layer]
            layer_face[2, :] = self.face_down[self.order - layer, :]
            layer_face[3, :] = self.face_right[:, self.order - layer]
            
            layer_face = self.__mat_circ_shift(layer_face, -n, 0)
            self.face_up[self.order - layer, :]    = np.flip(layer_face[0, :])
            self.face_left[self.order - layer, :]  = np.flip(layer_face[1, :])
            self.face_down[self.order - layer, :]  = np.flip(layer_face[2, :])
            self.face_right[self.order - layer, :] = np.flip(layer_face[3, :])
            
            if layer == 1:
                self.face_back = np.rot90(self.face_back, n)
            elif layer == self.order:
                self.face_front = np.rot90(self.face_front, n)
        else:
            return
        
        # self.__show()
    
if __name__ == '__main__':
    import time
    cube = Cube(3)
    