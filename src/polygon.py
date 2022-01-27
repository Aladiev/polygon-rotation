from config import *
import math

class MyPolygon(object):
    def __init__(self, points, canvas):
        self.canvas = canvas

        self.points, self.initial_points = [], []

        for point in points:
            self.initial_points.append(point.copy())
            self.points.append(point.copy())

        self.lines_ids = []

        self.draw_lines()
        self.draw_points()

        self.angle = 0

        self.center = 0

        self.child_offset = [0, 0]

        self.perimeter = 0

        self.calculate_center()
        self.calculate_offset()
        self.calculate_perimeter()

    def rotation(self, angle):
        self.angle = angle
        for i in range(len(self.points)):
            self.points[i][0] = self.center[0] + (self.initial_points[i][0] - self.center[0]) * math.cos(angle) - (
                    self.initial_points[i][1] - self.center[1]) * math.sin(angle)
            self.points[i][1] = self.center[1] + (self.initial_points[i][0] - self.center[0]) * math.sin(
                angle) + (self.initial_points[i][1] - self.center[1]) * math.cos(angle)

        self.draw_lines()
        self.draw_points()
        self.move_child()

    def set_center(self, center):
        self.center = center.copy()

        for i in range(len(self.initial_points)):
            self.initial_points[i][0] = self.center[0] + self.offset[i][0]
            self.initial_points[i][1] = self.center[1] + self.offset[i][1]

    def calculate_center(self):
        summa_x = 0
        summa_y = 0

        for i in range(len(self.points)):
            summa_x += self.points[i][0]
            summa_y += self.points[i][1]

        self.center = [summa_x // len(self.points), summa_y // len(self.points)]

    def calculate_offset(self):
        self.offset = []

        for point in self.initial_points:
            self.offset.append([point[0] - self.center[0], point[1] - self.center[1]])

    def calculate_perimeter(self):
        self.perimeter = 0

        for i in range(len(self.points)):
            right_index = (i + 1) % len(self.points)

            dx = self.points[i][0] - self.points[right_index][0]
            dy = self.points[i][1] - self.points[right_index][1]

            self.perimeter += math.sqrt(dx ** 2 + dy ** 2)

    def draw_lines(self):
        for line in self.lines_ids:
            self.canvas.delete(line)

        self.lines_ids = []

        for point_id in range(len(self.points)):
            self.lines_ids.append(self.canvas.create_line(self.points[point_id][0],
                                                          self.points[point_id][1],
                                                          self.points[(point_id + 1) % len(self.points)][0],
                                                          self.points[(point_id + 1) % len(self.points)][1]))

    def draw_points(self):
        for point in self.points:
            self.canvas.delete(point[3])

            point[3] = self.canvas.create_oval(
                point[0] - radius,
                point[1] - radius,
                point[0] + radius,
                point[1] + radius,
                outline=point[2], fill=point[2], tags="point"
            )

    def get_child_position(self):
        if self.child_offset != -1:
            right_index = (self.child_offset[0] + 1) % len(self.points)
            left_index = self.child_offset[0]

            dx = self.points[right_index][0] - self.points[left_index][0]
            dy = self.points[right_index][1] - self.points[left_index][1]

            x = self.points[left_index][0] + dx * self.child_offset[1] / math.sqrt(dx ** 2 + dy ** 2)
            y = self.points[left_index][1] + dy * self.child_offset[1] / math.sqrt(dx ** 2 + dy ** 2)

            return [x, y]

        self.child_offset = [0, 0]
        return self.points[0].copy()

    def move_child(self):
        if self.child_offset != -1:
            right_index = (self.child_offset[0] + 1) % len(self.points)

            dx = self.points[self.child_offset[0]][0] - self.points[right_index][0]
            dy = self.points[self.child_offset[0]][1] - self.points[right_index][1]

            if math.sqrt(dx ** 2 + dy ** 2) < (self.child_offset[1] + 0.001 * self.perimeter):
                movement = 0.001 * self.perimeter + self.child_offset[1] - math.sqrt(dx ** 2 + dy ** 2)
                self.child_offset = [right_index, movement]
                self.calculate_child_offset()
            else:
                self.child_offset[1] += 0.001 * self.perimeter

    def calculate_child_offset(self):
        right_index = (self.child_offset[0] + 1) % len(self.points)

        dx = self.points[self.child_offset[0]][0] - self.points[right_index][0]
        dy = self.points[self.child_offset[0]][1] - self.points[right_index][1]

        if self.child_offset[1] > math.sqrt(dx ** 2 + dy ** 2):
            movement = self.child_offset[1] - math.sqrt(dx ** 2 + dy ** 2)
            self.child_offset = [right_index, movement]
            self.calculate_child_offset()

    def calculate_perimeter(self):
        self.perimeter = 0

        for i in range(len(self.initial_points)):
            right_index = (i + 1) % len(self.initial_points)

            dx = self.initial_points[i][0] - self.initial_points[right_index][0]
            dy = self.initial_points[i][1] - self.initial_points[right_index][1]

            self.perimeter += math.sqrt(dx ** 2 + dy ** 2)
