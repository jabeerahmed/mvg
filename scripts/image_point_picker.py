from __future__ import print_function
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
import numpy as np
from numpy.random import rand
from matplotlib.backend_bases import MouseEvent, KeyEvent

import argparse

if __name__ == '__main__':
    plt.switch_backend('Qt4Agg')

    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=argparse.FileType())
    args = parser.parse_args()

    class LineBuilder:
        def __init__(self, line):
            self.line = line
            self.xs = list(line.get_xdata())
            self.ys = list(line.get_ydata())
            self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

        def __call__(self, event):
            print('click', event)
            if event.inaxes!=self.line.axes: return
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click to build line segments')
    plt.imshow(plt.imread(args.image_path))
    xs, ys = [], []
    undo_stack = []

    def plot():
        ax.plot(xs, ys, 'rx-')

    def add_point(x, y):
        xs.append(x)
        ys.append(y)
        plot()

    def handle_key(event):
        key = event.key.lower()
        print("Key " + key + " isZ: {}".format(key == 'z'))
        if key == "z" and len(xs) > 0:
            undo_stack.append((xs.pop(-1), ys.pop(-1)))
            print("Undo.\nStack:{}\n".format(undo_stack))
            plot()
        elif key == 'x' and len(undo_stack) > 0:
            add_point(*undo_stack.pop(-1))
        elif key == 'l' and len(xs) > 0:
            add_point(xs[0], ys[0])
            print(xs, ys)

    def handle_mouse(event):
        if event.inaxes != ax:
            print("Exit event inaxes.\n{}".format(event.inaxes))
            return
        add_point(event.xdata, event.ydata)

    def handle(event):
        if isinstance(event, KeyEvent):
            handle_key(event)
        elif isinstance(event, MouseEvent):
            handle_mouse(event)
        fig.canvas.draw()
        print("----------------------------------------")
        print("\n".join("{}, {}".format(*v) for v in zip(xs, ys)))
        print("----------------------------------------")
    fig.canvas.mpl_connect('button_press_event', handle)
    fig.canvas.mpl_connect('key_press_event', handle)

    plt.show()
    print("image: '{}'".format(args.image_path.name))
    print("points:")
    print("\n".join("    [{}, {}],".format(*v) for v in zip(xs, ys)))
