import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import pickle

class MiniDraw:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Draw")

        # Create a canvas for drawing
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize drawing state variables
        self.current_color = 'black'  # Current drawing color
        self.current_points = []  # Points for the current drawing
        self.current_bezier_points = []  # Bezier control points for smooth curves
        self.polygons = []  # List of polygons drawn
        self.lines = []  # List of lines drawn
        self.show_points = True  # Toggle to show/hide control points
        self.dragging_point = None  # Index of the point being dragged
        self.dragging_control_point = None  # Index of the control point being dragged
        self.dragging_canvas = False  # Flag for dragging the canvas
        self.canvas_offset_x = 0  # Horizontal offset of the canvas
        self.canvas_offset_y = 0  # Vertical offset of the canvas
        self.control_point_size = 5  # Size of the control points

        # Bind mouse and keyboard events
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<Button-2>", self.on_middle_click)
        self.canvas.bind("<B2-Motion>", self.on_middle_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_right_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_release)

        self.root.bind("<KeyPress-x>", self.toggle_points)
        self.root.bind("<KeyPress-c>", self.clear_canvas)
        self.root.bind("<KeyPress-s>", self.save_canvas)
        self.root.bind("<KeyPress-l>", self.load_canvas)
        self.root.bind("<KeyPress-p>", self.pick_color)
        self.root.bind("<KeyPress-f>", self.fill_polygon)
        self.root.bind("<KeyPress-n>", self.new_line)

    # Event handlers for mouse clicks and drags
    def on_left_click(self, event):
        # Add a point where the left mouse button was clicked
        x = event.x - self.canvas_offset_x
        y = event.y - self.canvas_offset_y
        self.current_points.append((x, y))
        # Calculate mid-point for Bezier curves
        if len(self.current_points) > 1:
            mid_x = (self.current_points[-2][0] + x) / 2
            mid_y = (self.current_points[-2][1] + y) / 2
            self.current_bezier_points.append((mid_x, mid_y))
        self.draw()

    def on_left_drag(self, event):
        # Drag a point or control point
        if self.dragging_point is not None:
            self.current_points[self.dragging_point] = (event.x - self.canvas_offset_x, event.y - self.canvas_offset_y)
            self.update_bezier_points()
            self.draw()
        elif self.dragging_control_point is not None:
            self.current_bezier_points[self.dragging_control_point] = (event.x - self.canvas_offset_x, event.y - self.canvas_offset_y)
            self.draw()

    def on_left_release(self, event):
        # Reset dragging state
        self.dragging_point = None
        self.dragging_control_point = None

    def on_middle_click(self, event):
        # Start dragging the canvas
        self.dragging_canvas = True
        self.start_x = event.x
        self.start_y = event.y

    def on_middle_drag(self, event):
        # Drag the canvas
        if self.dragging_canvas:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move("all", dx, dy)
            self.canvas_offset_x += dx
            self.canvas_offset_y += dy
            self.start_x = event.x
            self.start_y = event.y

    def on_middle_release(self, event):
        # Stop dragging the canvas
        self.dragging_canvas = False

    def on_right_click(self, event):
        # Start dragging a point or control point
        for i, point in enumerate(self.current_points):
            if abs(point[0] - (event.x - self.canvas_offset_x)) < self.control_point_size and abs(point[1] - (event.y - self.canvas_offset_y)) < self.control_point_size:
                self.dragging_point = i
                return
        for i, ctrl in enumerate(self.current_bezier_points):
            if abs(ctrl[0] - (event.x - self.canvas_offset_x)) < self.control_point_size and abs(ctrl[1] - (event.y - self.canvas_offset_y)) < self.control_point_size:
                self.dragging_control_point = i
                return

    def on_right_drag(self, event):
        # Drag a point or control point
        if self.dragging_point is not None:
            self.current_points[self.dragging_point] = (event.x - self.canvas_offset_x, event.y - self.canvas_offset_y)
            self.update_bezier_points()
            self.draw()
        elif self.dragging_control_point is not None:
            self.current_bezier_points[self.dragging_control_point] = (event.x - self.canvas_offset_x, event.y - self.canvas_offset_y)
            self.draw()

    def on_right_release(self, event):
        # Reset dragging state
        self.dragging_point = None
        self.dragging_control_point = None

    # Keyboard event handlers
    def toggle_points(self, event):
        # Toggle visibility of control points
        self.show_points = not self.show_points
        self.draw()

    def clear_canvas(self, event):
        # Clear the canvas and reset state
        self.canvas.delete("all")
        self.current_points = []
        self.current_bezier_points = []
        self.polygons = []
        self.lines = []

    def save_canvas(self, event):
        # Save the current drawing state to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            with open(file_path, 'wb') as f:
                pickle.dump((self.current_points, self.current_bezier_points, self.polygons, self.lines, self.current_color, self.canvas_offset_x, self.canvas_offset_y), f)

    def load_canvas(self, event):
        # Load a drawing state from a file
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            with open(file_path, 'rb') as f:
                self.current_points, self.current_bezier_points, self.polygons, self.lines, self.current_color, self.canvas_offset_x, self.canvas_offset_y = pickle.load(f)
            self.draw()

    def pick_color(self, event):
        # Open a color picker and set the current color
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def fill_polygon(self, event):
        # Add the current points as a filled polygon
        if len(self.current_points) > 2:
            self.polygons.append((self.current_points[:], self.current_bezier_points[:], self.current_color))
            self.current_points = []
            self.current_bezier_points = []
            self.draw()

    def new_line(self, event):
        # Add the current points as a new line
        if self.current_points:
            self.lines.append((self.current_points[:], self.current_bezier_points[:], self.current_color))
        self.current_points = []
        self.current_bezier_points = []
        self.draw()

    # Drawing methods
    def draw(self):
        # Redraw the canvas
        self.canvas.delete("all")
        for polygon, bezier_points, color in self.polygons:
            self.draw_filled_polygon(polygon, bezier_points, color)
        for points, bezier_points, color in self.lines:
            self.draw_bezier_curve(points, bezier_points, color)
        if len(self.current_points) > 1:
            self.draw_bezier_curve(self.current_points, self.current_bezier_points, self.current_color)
        if self.show_points:
            for x, y in self.current_points:
                self.canvas.create_rectangle(x + self.canvas_offset_x - self.control_point_size, y + self.canvas_offset_y - self.control_point_size,
                                             x + self.canvas_offset_x + self.control_point_size, y + self.canvas_offset_y + self.control_point_size, fill='red')
            for x, y in self.current_bezier_points:
                self.canvas.create_rectangle(x + self.canvas_offset_x - self.control_point_size, y + self.canvas_offset_y - self.control_point_size,
                                             x + self.canvas_offset_x + self.control_point_size, y + self.canvas_offset_y + self.control_point_size, fill='blue')

    def draw_bezier_curve(self, points, bezier_points, color):
        # Draw a Bezier curve connecting points
        if len(points) < 2:
            return

        for i in range(1, len(points)):
            p0 = points[i-1]
            p1 = points[i]
            c = bezier_points[i-1]
            self.draw_bezier(p0, p1, c, color)

    def draw_bezier(self, p0, p1, c, color):
        # Helper function to draw a single Bezier curve
        def bezier(t):
            return (1-t)**2 * p0[0] + 2 * (1-t) * t * c[0] + t**2 * p1[0], \
                   (1-t)**2 * p0[1] + 2 * (1-t) * t * c[1] + t**2 * p1[1]
        points = [(x + self.canvas_offset_x, y + self.canvas_offset_y) for x, y in [bezier(t/100) for t in range(101)]]
        self.canvas.create_line(points, fill=color)

    def draw_filled_polygon(self, points, bezier_points, color):
        # Draw a filled polygon with Bezier curves
        if len(points) < 2:
            return

        filled_points = []
        for i in range(1, len(points)):
            p0 = points[i-1]
            p1 = points[i]
            c = bezier_points[i-1]
            filled_points += self.get_bezier_points(p0, p1, c)
        
        filled_points = [(x + self.canvas_offset_x, y + self.canvas_offset_y) for x, y in filled_points]
        self.canvas.create_polygon(filled_points, fill=color, outline=color)

    def get_bezier_points(self, p0, p1, c):
        def bezier(t):
            return (1-t)**2 * p0[0] + 2 * (1-t) * t * c[0] + t**2 * p1[0], \
                   (1-t)**2 * p0[1] + 2 * (1-t) * t * c[1] + t**2 * p1[1]
        return [bezier(t/100) for t in range(101)]

    def update_bezier_points(self):
        for i in range(1, len(self.current_points)):
            mid_x = (self.current_points[i-1][0] + self.current_points[i][0]) / 2
            mid_y = (self.current_points[i-1][1] + self.current_points[i][1]) / 2
            self.current_bezier_points[i-1] = (mid_x, mid_y)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniDraw(root)
    root.mainloop()
