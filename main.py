from tkinter import *
import math

width = 1280
height = 720
[c_x, c_y] = [width / 2, height / 2]

radius = 300
square_size = 50

root = Tk()
canvas = Canvas(root, width=width, height=height, bg='white')
canvas.pack()

time = 0


class MyPolygon(object):
    def __init__(self, points):
        self.points = points.copy()
        self.current_points = self.points.copy()
        self.count = len(self.current_points) // 2

        self.calculate_center()
        self.calculate_offset()



    def rotation(self, angle):
        for i in range(0, self.count):
            self.current_points[i] = self.center[0] + (self.points[i] - self.center[0]) * math.cos(angle) - (
                        self.points[i + self.count] - self.center[1]) * math.sin(angle)
            self.current_points[i + self.count] = self.center[1] + (self.points[i] - self.center[0]) * math.sin(angle) + (
                        self.points[i + self.count] - self.center[1]) * math.cos(angle)

    def set_center(self, center):
        self.center = center.copy()

        self.points = [0, 0] * self.count

        for i in range(self.count):
            self.points[i] = self.center[0] + self.offset[i]
            self.points[i + self.count] = self.center[1] + self.offset[i + self.count]

    def calculate_center(self):
        summa_x = 0
        summa_y = 0

        for i in range(0, self.count):
            summa_x += self.current_points[i]
            summa_y += self.current_points[i + self.count]

        self.center = [summa_x // self.count, summa_y // self.count]

    def calculate_offset(self):
        self.offset = dict()

        for i in range(self.count):
            self.offset[i] = self.points[i] - self.center[0]
            self.offset[i + self.count] = self.points[i + self.count] - self.center[1]

    def draw(self):
        for i in range(0, self.count):
            canvas.create_line(self.current_points[i],
                               self.current_points[i + self.count],
                               self.current_points[(i + 1) % self.count],
                               self.current_points[(i + 1) % self.count + self.count])



def rotate(x, y, cx, cy, phi):
    x -= cx
    y -= cy

    return [x * math.cos(phi) + y * math.sin(phi) + cx, -x * math.sin(phi) + y * math.cos(phi) + cy]

rectangles = []

for i in range(0, 12):
    phi = i * math.pi / 6

    x = c_x + radius * math.cos(phi + time)
    y = c_y + radius * math.sin(phi + time)

    points = [x - square_size / 2,
                   x,
                   x + square_size / 2,
                   x + square_size * 2,
                   x - square_size / 4,
                   y - square_size / 2,
                   y - square_size,
                   y - square_size / 2,
                   y + square_size / 2,
                   y + square_size / 2]

    rectangles.append(MyPolygon(points))

    rectangles[i].draw()

def draw():
    global time

    canvas.delete('all')

    canvas.create_oval(c_x - radius,
                       c_y - radius,
                       c_x + radius,
                       c_y + radius)

    for i in range(0, 12):
        phi = i * math.pi / 6

        x = c_x + radius * math.cos(phi + time)
        y = c_y + radius * math.sin(phi + time)

        cx = x
        cy = y

        [new_x, new_y] = rotate(x, y, cx, cy, time)

        rectangles[i].set_center([new_x, new_y])
        rectangles[i].rotation(-1 * time)
        rectangles[i].draw()


    time += math.pi / 180
    root.after(10, draw)


draw()


root.mainloop()



