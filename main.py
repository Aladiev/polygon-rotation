from tkinter import *
import math

width = 1280
height = 720
[c_x, c_y] = [width / 2, height / 2]

radius = 300
square_size = 50

root = Tk()

run  = False

# Init, FIRST POINT ADDED, SOME POINT ADDED, LAST POINT ADDED
INIT = 'INIT'
FIRST = 'FIRST POINT ADDED'
SOME = 'SOME POINT ADDED'
LAST = 'LAST POINT ADDED'

state = init

polygons = []

def draw_first_polygon(point):

def get_figure(point):
    for polygon in polygons:
        flag = polygon.is_intersection(point)
        if flag > -1:
            return flag

    return -1

def key(event):
    print("pressed", repr(event.char))

def callback(event):
    print("clicked at", event.x, event.y)
    print(get_figure([event.x, event.y]))

def on_start():
    global run
    run = True
    print('START')

def on_stop():
    global run
    run = False
    print('STOP')

def rotate(x, y, cx, cy, phi):
    x -= cx
    y -= cy

    return [x * math.cos(phi) + y * math.sin(phi) + cx, -x * math.sin(phi) + y * math.cos(phi) + cy]

class MyPolygon(object):
    def __init__(self, points):
        self.points = points.copy()
        self.current_points = self.points.copy()
        self.count = len(self.current_points) // 2

        self.calculate_center()
        self.calculate_offset()
    
    def add_vertex(self, point):
        self.points.insert(self.count, point[0])
        self.points.append(point[1])

        canvas.delete('first_center')

        canvas.create_line(point[0],
                           point[1],
                           self.points[self.count - 1],
                           self.points[self.count * 2])

        canvas.create_oval(point[0] - 5, point[1] - 5,
                           point[0] + 5, point[1] + 5, fill="#476042")

        self.count += 1

        self.current_points = self.points.copy()

        self.calculate_center()
        self.calculate_offset()

        self.center_figure = create_oval(self.current_points[i] - 3, self.current_points[i + self.count] - 3,
                           self.current_points[i] + 3, self.current_points[i + self.count] + 3, fill="#FF0000")

    def rotation(self, angle):
        for i in range(self.count):
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

        for i in range(self.count):
            summa_x += self.current_points[i]
            summa_y += self.current_points[i + self.count]

        self.center = [summa_x // self.count, summa_y // self.count]

    def calculate_offset(self):
        self.offset = dict()

        for i in range(self.count):
            self.offset[i] = self.points[i] - self.center[0]
            self.offset[i + self.count] = self.points[i + self.count] - self.center[1]

    def draw(self):
        canvas.create_oval(self.current_points[i] - 3, self.current_points[i + self.count] - 3,
                           self.current_points[i] + 3, self.current_points[i + self.count] + 3, fill="#FF0000")

        for i in range(0, self.count):
            canvas.create_line(self.current_points[i],
                               self.current_points[i + self.count],
                               self.current_points[(i + 1) % self.count],
                               self.current_points[(i + 1) % self.count + self.count])

            canvas.create_oval(self.current_points[i] - 5, self.current_points[i + self.count] - 5,
                               self.current_points[i] + 5, self.current_points[i + self.count] + 5, fill="#476042")

    def is_intersection(self, point):
        for i in range(self.count):
            x_condition = self.current_points[i] - 5 <= point[0] and self.current_points[i] + 5 >= point[0]
            y_condition = self.current_points[i + self.count] - 5 <= point[1] and self.current_points[i + self.count] + 5 >= point[1]

            if x_condition and y_condition:
                return i

        return -1

canvas = Canvas(root, width=width, height=height, bg='white')
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.pack()

startButton = Button(root, text ="START", command = on_start)
stopButton = Button(root, text ="STOP", command = on_stop)
startButton.pack()
stopButton.pack()

time = 0

# for i in range(0, 12):
#     phi = i * math.pi / 6
#
#     x = c_x + radius * math.cos(phi + time)
#     y = c_y + radius * math.sin(phi + time)
#
#     points = [x - square_size / 2,
#                    x,
#                    x + square_size / 2,
#                    x + square_size * 2,
#                    x - square_size / 4,
#                    y - square_size / 2,
#                    y - square_size,
#                    y - square_size / 2,
#                    y + square_size / 2,
#                    y + square_size / 2]
#
#     polygons.append(MyPolygon(points))
#
#     polygons[i].draw()

def draw():
    global time
    if run:
        canvas.delete('all')

        # canvas.create_oval(c_x - radius,
        #                    c_y - radius,
        #                    c_x + radius,
        #                    c_y + radius)

        # for i in range(0, 12):
            # phi = i * math.pi / 6
            #
            # x = c_x + radius * math.cos(phi + time)
            # y = c_y + radius * math.sin(phi + time)
            #
            # cx = x
            # cy = y
            #
            # [new_x, new_y] = rotate(x, y, cx, cy, time)
            #
            # polygons[i].set_center([new_x, new_y])
            # polygons[i].rotation(-1 * time)
            # polygons[i].draw()


        time += math.pi / 180
    root.after(10, draw)


draw()


root.mainloop()



