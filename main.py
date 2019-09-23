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
INIT = 0 # 'INIT'
FIRST = 1# 'FIRST POINT ADDED'
SOME = 2 # 'SOME POINT ADDED'
LAST = 3 # 'LAST POINT ADDED'
SECOND = 4 # 'SECOND POINT ADDED'
SOME_SECOND = 5 # 'SOME POINT IN SECOND POLYGON ADDED'
END = 6 # 'END'

moving_point = -1

last_state = INIT
state = INIT

polygons = []

def set_state(new_state):
    global state, last_state

    last_state = state
    state = new_state

def get_figure(point):
    for polygon_id in range(len(polygons)):
        flag = polygons[polygon_id].is_intersection(point)
        if flag > -1:
            return polygon_id, flag

    return -1, -1

def key(event):
    print("pressed", repr(event.char))

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
    def __init__(self, point):
        self.points = point.copy()
        self.current_points = self.points.copy()
        self.count = len(self.current_points) // 2
        self.center_figure = -1
        self.calculate_center()
        self.calculate_offset()

        self.lines_ids = {}
        self.points_ids = {}

        self.points_ids[0] = canvas.create_oval(point[0] - 5, point[1] - 5,
                           point[0] + 5, point[1] + 5, fill="#476042")
    
    def add_vertex(self, point):
        self.points.insert(self.count, point[0])
        self.points.append(point[1])

        if self.center_figure != -1:
          canvas.delete(self.center_figure)

        self.lines_ids[str(self.count - 1) + ' ' + str(self.count)] = canvas.create_line(point[0],
                           point[1],
                           self.points[self.count - 1],
                           self.points[self.count * 2])

        self.points_ids[self.count] = canvas.create_oval(point[0] - 5, point[1] - 5,
                           point[0] + 5, point[1] + 5, fill="#476042")

        self.count += 1

        self.current_points = self.points.copy()

        self.calculate_center()
        self.calculate_offset()

        self.center_figure = canvas.create_oval(self.center[0] - 3, self.center[1] - 3,
                           self.center[0] + 3, self.center[1] + 3, fill="#FF0000")

    def set_vertex(self, id, point):
        print('DELETING ' + str(id))
        print(self.points_ids)
        print(self.lines_ids)
        self.points[id] = point[0]
        self.points[id + self.count] = point[1]

        if self.center_figure != -1:
            canvas.delete(self.center_figure)

        right_index = (id + 1) % self.count

        if right_index > id:
            left, right = id, right_index
        else:
            left, right = right_index, id

        if str(left) + ' ' + str(right) in self.lines_ids: # Delete line to right point
            print('DELETE FROM ' + str(left) + ' TO ' + str(right))
            canvas.delete(self.lines_ids[str(left) + ' ' + str(right)])

            print('DRAW FROM ' + str(left) + ' TO ' + str(right))
            self.lines_ids[str(left) + ' ' + str(right)] = canvas.create_line(self.points[left],
                           self.points[left + self.count],
                           self.points[right],
                           self.points[right + self.count])
        # Delete line to left point
        left_index = id - 1 if id > 0 else id - 1 + self.count

        if left_index < id:
            left2, right2 = left_index, id
        else:
            left2, right2 = id, left_index

        print('LOOK LEFT LINE FROM ' + str(left2) + ' TO ' + str(right2))
        if str(left2) + ' ' + str(right2) in self.lines_ids:
            print('DELETE FROM ' + str(left2) + ' TO ' + str(right2))
            canvas.delete(self.lines_ids[str(left2) + ' ' + str(right2)])

            print('DRAW FROM ' + str(left2) + ' TO ' + str(right2))
            self.lines_ids[str(left2) + ' ' + str(right2)] = canvas.create_line(self.points[right2],
                                                                                            self.points[right2 + self.count],
                                                                                            self.points[left2],
                                                                                            self.points[
                                                                                                left2 + self.count])

        canvas.delete(self.points_ids[id])
        self.points_ids[id] = canvas.create_oval(point[0] - 5, point[1] - 5,
                           point[0] + 5, point[1] + 5, fill="#476042")

        self.current_points = self.points.copy()

        self.calculate_center()
        self.calculate_offset()

        self.center_figure = canvas.create_oval(self.center[0] - 3, self.center[1] - 3,
                                                self.center[0] + 3, self.center[1] + 3, fill="#FF0000")

    def last_vertex(self):
        self.lines_ids[str(0) + ' ' + str(self.count - 1)] = canvas.create_line(self.points[0],
                           self.points[self.count],
                           self.points[self.count - 1],
                           self.points[self.count * 2 - 1])

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
        canvas.create_oval(self.center[0] - 3, self.center[1] - 3,
                           self.center[0] + 3, self.center[1] + 3, fill="#FF0000")

        for i in range(0, self.count):
            right_index = (i + 1) % self.count

            if right_index > i:
                left, right =  i, right_index
            else:
                left, right =  right_index, i
            self.lines_ids[str(left) + ' ' + str(right)] = canvas.create_line(self.current_points[i],
                               self.current_points[i + self.count],
                               self.current_points[right_index],
                               self.current_points[right_index + self.count])

            self.points_ids[i] = canvas.create_oval(self.current_points[i] - 5, self.current_points[i + self.count] - 5,
                               self.current_points[i] + 5, self.current_points[i + self.count] + 5, fill="#476042")

    def is_intersection(self, point):
        for i in range(self.count):
            x_condition = self.current_points[i] - 5 <= point[0] and self.current_points[i] + 5 >= point[0]
            y_condition = self.current_points[i + self.count] - 5 <= point[1] and self.current_points[i + self.count] + 5 >= point[1]

            if x_condition and y_condition:
                return i

        return -1

def on_click_canvas(point):
    global state, polygons, run, moving_point
    print(state)
    if state == INIT:
        polygons.append(MyPolygon(point))
        set_state(FIRST)
    else:
        polygon_id, point_id = get_figure(point)
        if polygon_id > -1:
            if polygon_id == 0 and point_id == 0 and state == SOME:
                polygons[0].last_vertex()
                set_state(LAST)
                return
            else:
                moving_point = [polygon_id, point_id]
                run = False
                return

        if moving_point != -1:
            polygons[moving_point[0]].set_vertex(moving_point[1], point)

            set_state(last_state)

            moving_point = -1
            return

        if state == FIRST:
            polygons[0].add_vertex(point)
            set_state(SOME)
        else:
            if state == SOME:
                if polygon_id > -1:
                    if get_figure(point) == 0:
                        polygons[0].last_vertex()
                        set_state(LAST)
                        run = True    
                else:
                    polygons[0].add_vertex(point)
            else:
                if state == LAST:
                    pass

def callback(event):
    print("clicked at", event.x, event.y)
    print(get_figure([event.x, event.y]))
    on_click_canvas([event.x, event.y])

canvas = Canvas(root, width=width, height=height, bg='white')
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.pack()

start_button = Button(root, text ="START", command = on_start)
stop_button = Button(root, text ="STOP", command = on_stop)
start_button.pack()
stop_button.pack()

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
        polygons[0].rotation(-1 * time)
        polygons[0].draw()

        time += math.pi / 180
    root.after(10, draw)


draw()


root.mainloop()
