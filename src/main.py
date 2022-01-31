from tkinter import *
from polygon import *
import random


class App(Frame):
    def __init__(self, root):
        self.run = False

        Frame.__init__(self, root)

        self.color = 'blue'

        self.points = []
        self.polygons = []

        self.canvas = Canvas(root, width=width, height=height, bg='white')
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-2>", self.finish_poly)
        self.canvas.bind("<Button-1>", self.create_point)
        start_button = Button(root, text="Play", command=self.play_simulation)
        stop_button = Button(root, text="Stop", command=self.stop_simulation)
        start_button.pack()
        stop_button.pack()

        self.time = 0
        self.draw()

    def draw(self):
        if self.run and len(self.polygons):
            self.canvas.delete('all')
            self.polygons[0].rotation(self.time)

            for i in range(1, len(self.polygons)):
                self.polygons[i].set_center(self.polygons[i - 1].get_child_position())
                self.polygons[i].rotation((-1 ** i) * self.time)

            self.time += math.pi / 180

        root.after(10, self.draw)

    def play_simulation(self):
        self.run = True

    def stop_simulation(self):
        self.run = False

    def finish_poly(self, _):
        if len(self.points) > 2:
            self.polygons.append(Polygon(self.points, self.canvas))

            self.generate_color()
            self.points = []

    def create_point(self, event):
        point_id = self.canvas.create_oval(
            event.x - radius,
            event.y - radius,
            event.x + radius,
            event.y + radius,
            outline=self.color, fill=self.color, tags="point"
        )

        self.points.append([event.x, event.y, self.color, point_id])

    def generate_color(self):
        self.color = random.choice(['magenta', 'red', 'green', 'cyan', 'yellow'])


if __name__ == "__main__":
    root = Tk()
    r = App(root)
    root.mainloop()