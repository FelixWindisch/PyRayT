from Vector import Vec3
import enum


class Camera:
    def post_process(self, color):
        try:
            for p in self.post_process_stack:
                color = p.post_process(color)
            return color
        except:
            return color

    def __init__(self, position, rotation, resolution, perspective, trace_stack, post_process_stack):
        self.position = position
        self.rotation = rotation
        self.resolution = resolution
        self.perspective = perspective
        self.viewDir = Vec3(0, 0, 1)
        self.post_process_stack = post_process_stack
        self.trace_stack = trace_stack


