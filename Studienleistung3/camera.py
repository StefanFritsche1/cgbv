import glm

class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0, 0.0, 3.0)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.world_up = glm.vec3(0.0, 1.0, 0.0)

        self.yaw = -90.0  # Yaw is initialized to -90 degrees
        self.pitch = 0.0
        self.speed = 2.5
        self.mouse_sensitivity = 0.1
        self.zoom = 45.0

        self.update_camera_vectors()

        # Projection matrix
        self.projection = glm.perspective(glm.radians(self.zoom), 800 / 600, 0.1, 100.0)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, deltaTime):
        velocity = self.speed * deltaTime
        if direction == 'FORWARD':
            self.position += self.front * velocity
        if direction == 'BACKWARD':
            self.position -= self.front * velocity
        if direction == 'LEFT':
            self.position -= self.right * velocity
        if direction == 'RIGHT':
            self.position += self.right * velocity

    def update_camera_vectors(self):
        front = glm.vec3(
            glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def mouse_callback(self, window, xpos, ypos):
        # Implement mouse movement callback logic
        pass

    def scroll_callback(self, window, xoffset, yoffset):
        # Implement mouse scroll callback logic for zooming
        self.zoom -= yoffset
        if self.zoom < 1.0:
            self.zoom = 1.0
        elif self.zoom > 45.0:
            self.zoom = 45.0
        self.projection = glm.perspective(glm.radians(self.zoom), 800 / 600, 0.1, 100.0)
