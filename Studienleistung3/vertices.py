import numpy as np

vertices_cube = np.array([
    # positions       # colors
    -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
     0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
     0.5,  0.5, -0.5,  0.0, 0.0, 1.0,
     0.5,  0.5, -0.5,  0.0, 0.0, 1.0,
    -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,
    -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
    # more vertices ...
], dtype=np.float32)

vertices_pyramid = np.array([
    # positions       # colors
    # base
    -0.5, 0.0, -0.5,  1.0, 0.0, 0.0,
     0.5, 0.0, -0.5,  0.0, 1.0, 0.0,
     0.5, 0.0,  0.5,  0.0, 0.0, 1.0,
     0.5, 0.0,  0.5,  0.0, 0.0, 1.0,
    -0.5, 0.0,  0.5,  1.0, 0.0, 0.0,
    -0.5, 0.0, -0.5,  1.0, 0.0, 0.0,
    # sides
    -0.5, 0.0, -0.5,  1.0, 0.0, 0.0,
     0.5, 0.0, -0.5,  0.0, 1.0, 0.0,
     0.0, 0.5,  0.0,  0.0, 0.0, 1.0,
     0.5, 0.0, -0.5,  0.0, 1.0, 0.0,
     0.5, 0.0,  0.5,  0.0, 0.0, 1.0,
     0.0, 0.5,  0.0,  0.0, 0.0, 1.0,
     0.5, 0.0,  0.5,  0.0, 0.0, 1.0,
    -0.5, 0.0,  0.5,  1.0, 0.0, 0.0,
     0.0, 0.5,  0.0,  0.0, 0.0, 1.0,
    -0.5, 0.0,  0.5,  1.0, 0.0, 0.0,
    -0.5, 0.0, -0.5,  1.0, 0.0, 0.0,
     0.0, 0.5,  0.0,  0.0, 0.0, 1.0
], dtype=np.float32)

import numpy as np

def create_sphere(radius, sector_count, stack_count):
    vertices = []
    for i in range(stack_count + 1):
        stack_angle = np.pi / 2 - i * np.pi / stack_count
        xy = radius * np.cos(stack_angle)
        z = radius * np.sin(stack_angle)

        for j in range(sector_count + 1):
            sector_angle = j * 2 * np.pi / sector_count
            x = xy * np.cos(sector_angle)
            y = xy * np.sin(sector_angle)
            vertices.extend([x, y, z])

            # Adding color (random for example purposes)
            vertices.extend([np.random.rand(), np.random.rand(), np.random.rand()])

    vertices = np.array(vertices, dtype=np.float32)
    return vertices

def create_sphere_indices(sector_count, stack_count):
    indices = []
    for i in range(stack_count):
        for j in range(sector_count):
            first = i * (sector_count + 1) + j
            second = first + sector_count + 1

            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])

    indices = np.array(indices, dtype=np.uint32)
    return indices

# Define sphere parameters
radius = 0.5
sector_count = 36
stack_count = 18

vertices_sphere = create_sphere(radius, sector_count, stack_count)
indices_sphere = create_sphere_indices(sector_count, stack_count)

# Example usage in an OpenGL setup (in the main.py script)
# Create and bind VBO, VAO, EBO as needed using vertices_sphere and indices_sphere
