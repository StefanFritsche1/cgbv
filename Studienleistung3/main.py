import glfw
from OpenGL.GL import *
import numpy as np
import glm
from shader import Shader
from camera import Camera
from object import Object3D
from raycaster import Raycaster
import vertices

def main():
    # Initialize GLFW
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "3D World", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    # Initialize OpenGL context
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Set up camera
    camera = Camera()
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_scroll_callback(window, camera.scroll_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Create shader program
    shader = Shader(
        r"C:\Users\stefa\Documents\GitHub\cgbv\Studienleistung3\shaders\vertex_shader.glsl",
        r"C:\Users\stefa\Documents\GitHub\cgbv\Studienleistung3\shaders\fragment_shader.glsl"
    )

    # Create objects
    object1 = Object3D(vertices=vertices.vertices_cube, indices=None, color=glm.vec3(1.0, 0.0, 0.0), position=glm.vec3(-1.0, 0.0, -3.0), radius=0.5)
    object2 = Object3D(vertices=vertices.vertices_pyramid, indices=None, color=glm.vec3(0.0, 1.0, 0.0), position=glm.vec3(1.0, 0.0, -3.0), radius=0.5)
    object3 = Object3D(vertices=vertices.vertices_sphere, indices=vertices.indices_sphere, color=glm.vec3(0.0, 0.0, 1.0), position=glm.vec3(0.0, 0.0, -5.0), radius=0.5)

    objects = [object1, object2, object3]

    # Raycaster for object selection
    raycaster = Raycaster()

    glfw.set_mouse_button_callback(window, lambda win, button, action, mods: mouse_button_callback(win, button, action, mods, camera, raycaster, objects))

    # Main render loop
    while not glfw.window_should_close(window):
        # Process input
        process_input(window, camera)

        # Update camera
        view = camera.get_view_matrix()
        projection = glm.perspective(glm.radians(camera.zoom), 800/600, 0.1, 100.0)

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render objects
        shader.use()
        # An den entsprechenden Stellen sicherstellen, dass die Camera-Klasse korrekt verwendet wird:
        shader.set_mat4("projection", camera.projection)
        shader.set_mat4("view", camera.get_view_matrix())


        for obj in objects:
            model = glm.mat4(1.0)
            model = glm.translate(model, obj.position)
            shader.set_mat4("model", model)
            shader.set_vec3("objectColor", obj.color)
            obj.draw(shader)

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

def mouse_button_callback(window, button, action, mods, camera, raycaster, objects):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        xpos, ypos = glfw.get_cursor_pos(window)
        raycaster.check_intersections(camera, objects, xpos, ypos, 800, 600)

def process_input(window, camera):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard("FORWARD", 0.1)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard("BACKWARD", 0.1)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard("LEFT", 0.1)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard("RIGHT", 0.1)

if __name__ == "__main__":
    main()
