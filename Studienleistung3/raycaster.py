# raycaster.py
import glm

class Raycaster:
    def __init__(self):
        pass

    def cast_ray(self, camera, screen_x, screen_y, window_width, window_height):
        x = (2.0 * screen_x) / window_width - 1.0
        y = 1.0 - (2.0 * screen_y) / window_height
        z = 1.0
        ray_nds = glm.vec3(x, y, z)

        ray_clip = glm.vec4(ray_nds.x, ray_nds.y, -1.0, 1.0)

        ray_eye = glm.inverse(camera.projection) * ray_clip
        ray_eye = glm.vec4(ray_eye.x, ray_eye.y, -1.0, 0.0)

        ray_wor = glm.vec3(glm.inverse(camera.view) * ray_eye)
        ray_wor = glm.normalize(ray_wor)

        return ray_wor

    def intersect_sphere(self, ray_origin, ray_direction, sphere_center, sphere_radius):
        oc = ray_origin - sphere_center
        a = glm.dot(ray_direction, ray_direction)
        b = 2.0 * glm.dot(oc, ray_direction)
        c = glm.dot(oc, oc) - sphere_radius * sphere_radius
        discriminant = b * b - 4 * a * c
        return discriminant > 0

    def check_intersections(self, camera, objects, screen_x, screen_y, window_width, window_height):
        ray_direction = self.cast_ray(camera, screen_x, screen_y, window_width, window_height)
        ray_origin = camera.position
        
        for obj in objects:
            if self.intersect_sphere(ray_origin, ray_direction, obj.position, obj.radius):
                obj.color = (1.0, 1.0, 0.0)
                return obj
        return None
