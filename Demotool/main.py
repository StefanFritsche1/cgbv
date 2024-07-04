import glfw
from OpenGL.GL import *
import numpy as np
import glm
from shader import Shader
from camera import Camera
from object import Object3D  # Stelle sicher, dass dieses Modul die richtigen Methoden hat.
from raycaster import Raycaster  # Dieses Modul müsstest du noch definieren.

# Initialisiere GLFW
def initialize_window():
    if not glfw.init():
        raise Exception("GLFW can not be initialized!")
    
    window = glfw.create_window(800, 600, "3D World", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can not be created!")
    
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, frame_buffer_size_callback)
    return window

def frame_buffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def main():
    window = initialize_window()
    shader = Shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
    camera = Camera()
    objects = [Object3D(), Object3D(), Object3D()]  # Erstelle spezifische Objekte hier.

    # Hauptrender-Schleife
    while not glfw.window_should_close(window):
        process_input(window, camera)
        
        # Rendering commands
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader.use()
        shader.set_mat4("view", camera.get_view_matrix())
        shader.set_mat4("projection", camera.projection)

        # Zeichne jedes Objekt
        for obj in objects:
            obj.draw(shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

def process_input(window, camera):
    # Implementiere Kamerabewegungen und andere Steuerungen.
    pass

if __name__ == "__main__":
    main()


# main.py
import numpy as np

# Beispieldaten für einen Würfel und eine Pyramide
cube_vertices = np.array([
    # Positionen        # Farben
    -0.5, -0.5, -0.5,   1.0, 0.0, 0.0,
     0.5, -0.5, -0.5,   0.0, 1.0, 0.0,
     0.5,  0.5, -0.5,   0.0, 0.0, 1.0,
    -0.5,  0.5, -0.5,   1.0, 1.0, 0.0,
    -0.5, -0.5,  0.5,   1.0, 0.0, 1.0,
     0.5, -0.5,  0.5,   0.0, 1.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 1.0, 1.0,
    -0.5,  0.5,  0.5,   0.0, 0.0, 0.0,
], dtype=np.float32)

cube_indices = np.array([
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    4, 5, 1, 1, 0, 4,
    6, 7, 3, 3, 2, 6,
    5, 6, 2, 2, 1, 5,
    7, 4, 0, 0, 3, 7
], dtype=np.uint32)

shader = Shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")  # Define the shader variable
objects = [Object3D(cube_vertices, cube_indices, np.array([1.0, 0.0, 0.0], dtype=np.float32))]

# Setze dies im Hauptprogramm ein, um die Objekte zu rendern
for obj in objects:
    obj.draw(shader)
