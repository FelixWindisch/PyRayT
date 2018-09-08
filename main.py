import sys
import pygame
from Window import Window
from StopWatch import StopWatch
from Material import*
import Example


def init_scene(scene_to_render):
    # Set the scene variable in other modules, so it doesn't have to be passed through method calls
    Material.scene = scene_to_render
    Raytracing.scene = scene_to_render


def render(scene):
    init_scene(scene)
    stop_watch = StopWatch()
    stop_watch.start()
    window = Window(scene.camera.resolution.x, scene.camera.resolution.y)
    #foreach Pixel on Screen
    for x in range(0, scene.camera.resolution.x):
        for y in range(0, scene.camera.resolution.y):
            prime_ray = Raytracing.generate_prime_ray(x, y, scene.camera)
            color = Raytracing.trace(prime_ray, scene.camera.trace_stack, 0).clamp()
            color = scene.camera.post_process(color)
            window.set_pixel(x, y, color)
        pygame.display.flip()
        print(x)
    stop_watch.stop()

# Pick the scene to render
render(Example.caustics)
# Pick the scene to render

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()



