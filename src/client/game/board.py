__author__ = 'Taavi'

import Tkinter as Tk
from PIL import Image, ImageTk
from slot import *


class Board:
    # States

    SETTING_SHIPS = 0
    PLAYING = 1
    INACTIVE = 2

    def __init__(self):
        self.label_LUT = {}
        self.empty_img = ImageTk.PhotoImage(Image.open("../../resources/empty.jpg"))
        self.hit_img = ImageTk.PhotoImage(Image.open("../../resources/hit.jpg"))
        self.miss_img = ImageTk.PhotoImage(Image.open("../../resources/miss.jpg"))
        self.ship_img = ImageTk.PhotoImage(Image.open("../../resources/ship.jpg"))

        self.slots = []
        self.state = self.SETTING_SHIPS

    def init_board(self, master_frame):
        frame = Tk.Frame(master_frame)

        for i in range(11):
            for j in range(11):
                l = Tk.Label(frame, image=self.empty_img)
                l.bind("<Button-1>", self.on_click)
                l.grid(row=i, column=j)
                l.image = self.empty_img
                self.label_LUT[l] = (i,j)

                slot = Slot(i, j)
                self.slots.append(slot)

        return frame

    #
    # PUBLIC
    #

    def set_hit(self, x, y):
        if self.state == self.SETTING_SHIPS:
            return False

        for slot in self.slots:
            if slot.x == x and slot.y == y:
                if slot.state == Slot.SHIP:
                    self.set_picture(x, y, Slot.HIT)
                    return True
                elif slot.state == Slot.EMPTY:
                    self.set_picture(x, y, Slot.MISS)
                    return True
                else:
                    return False

        return False

    def set_ship(self, x, y):
        if self.state == self.PLAYING:
            return False

        for slot in self.slots:
            if slot.x == x and slot.y == y:
                if slot.state == Slot.EMPTY:
                    self.set_picture(x, y, Slot.SHIP)
                    return True
                elif slot.state == Slot.SHIP or \
                     slot.state == Slot.HIT or \
                     slot.state == Slot.MISS:
                    return False

            return False

    def clear(self):
        for label in self.label_LUT.keys():
            label.config(image=self.empty_img)

        for slot in self.slots:
            slot.state = Slot.EMPTY

    #
    # PRIVATE
    #

    def on_click(self, event):
        loc = self.label_LUT[event.widget]
        print loc
        self.set_hit(loc[0], loc[1])

    def set_picture(self, x, y, condition):
        for label in self.label_LUT.keys():
            if self.label_LUT[label][0] == x and self.label_LUT[label][1] == y:
                if condition == Slot.HIT:
                    label.config(image=self.hit_img)
                elif condition == Slot.MISS:
                    label.config(image=self.miss_img)
                elif condition == Slot.SHIP:
                    label.config(image=self.ship_img)


