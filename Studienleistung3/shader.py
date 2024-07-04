# shader.py
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

class Shader:
    def __init__(self, vertex_path, fragment_path):
        # Read vertex shader file
        with open(vertex_path, 'r') as file:
            vertex_src = file.read()
        
        # Read fragment shader file
        with open(fragment_path, 'r') as file:
            fragment_src = file.read()
        
        # Compile vertex shader
        vertex_shader = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
        
        # Compile fragment shader
        fragment_shader = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
        
        # Create shader program
        self.program = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)
    
    def use(self):
        glUseProgram(self.program)
    
    def set_mat4(self, name, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, glm.value_ptr(mat))
    
    def set_vec3(self, name, vec):
        glUniform3fv(glGetUniformLocation(self.program, name), 1, glm.value_ptr(glm.vec3(vec)))

# Example of how to use the Shader class with absolute paths
if __name__ == "__main__":
    shader = Shader(
        r"C:\Users\stefa\Documents\GitHub\cgbv\Studienleistung3\shaders\vertex_shader.glsl",
        r"C:\Users\stefa\Documents\GitHub\cgbv\Studienleistung3\shaders\fragment_shader.glsl"
    )
    shader.use()
