import os
from Texture import Texture
import MipMap


class Cubemap:

    def __init__(self, left, right, up, down, front, back):
        self.left = Texture(left)
        self.right = Texture(right)
        self.up = Texture(up)
        self.down = Texture(down)
        self.front = Texture(front)
        self.back = Texture(back)

    def __init__(self, folder):
        self.left = Texture(os.getcwd() + "/" + folder + "/" + "Left.jpg")
        self.right = Texture(os.getcwd() + "/" + folder + "/" + "Right.jpg")
        self.up = Texture(os.getcwd() + "/" + folder + "/" + "Up.jpg")
        self.down = Texture(os.getcwd() + "/" + folder + "/" + "Down.jpg")
        self.front = Texture(os.getcwd() + "/" + folder + "/" + "Front.jpg")
        self.back = Texture(os.getcwd() + "/" + folder + "/" + "Back.jpg")

    def sample(self, vector):
        abs_x = abs(vector.x)
        abs_y = abs(vector.y)
        abs_z = abs(vector.z)
        if vector.x > 0 and abs_x >= abs_y and abs_x >= abs_z:
            max_axis = abs_x
            u, v = -vector.y, vector.z
            side = self.right
        elif vector.x < 0 and abs_x >= abs_y and abs_x >= abs_z:
            max_axis = abs_x
            u, v = -vector.y, -vector.z
            side = self.left
        elif vector.y > 0 and abs_y >= abs_x and abs_y >= abs_z:
            max_axis = abs_y
            u, v = -vector.x, vector.z
            side = self.down
        elif vector.y < 0 and abs_y >= abs_x and abs_y >= abs_z:
            max_axis = abs_y
            u, v = vector.x, vector.z
            side = self.up
        elif vector.z > 0 and abs_z >= abs_x and abs_z >= abs_y:
            max_axis = abs_z
            u, v = -vector.y, -vector.x
            side = self.front
        elif vector.z < 0 and abs_z >= abs_x and abs_z >= abs_y:
            max_axis = abs_z
            u, v = -vector.y, vector.x
            side = self.back
        u = 0.5 * (u / max_axis + 1)
        v = 0.5 * (v / max_axis + 1)

        sample_color = side.sample(u, v)
        return sample_color

    def mip_map(self, mips):
        self.right = MipMap.mip_map(self.right, mips)
        self.left = MipMap.mip_map(self.left, mips)
        self.front = MipMap.mip_map(self.front, mips)
        self.back = MipMap.mip_map(self.back, mips)
        self.up = MipMap.mip_map(self.up, mips)
        self.down = MipMap.mip_map(self.down, mips)
        return self
