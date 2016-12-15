__author__ = 'Taavi'

import Tkinter as Tk
import logging
import copy

from PIL import Image, ImageTk

from common.game.slot import *


class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size


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

        self.on_click_delegate = None
        self.slots = []
        self.state = self.SETTING_SHIPS

    def init_board(self, master_frame, is_interactive, size):
        frame = Tk.Frame(master_frame)
        self.slots = []
        self.label_LUT = {}

        for i in range(size):
            for j in range(size):
                l = Tk.Label(frame, image=self.empty_img)

                if is_interactive:
                    l.bind("<Button-1>", self.on_click)

                l.grid(row=i, column=j)
                l.image = self.empty_img
                self.label_LUT[l] = (j,i)

                slot = Slot(j, i)
                self.slots.append(slot)

        return frame

    #
    # PUBLIC
    #

    def clear(self):
        for slot in self.slots:
            self.set_slot_state(slot, Slot.EMPTY)

    def reset(self):
        self.clear()
        self.state = self.SETTING_SHIPS

    def set_hit(self, x, y):
        if self.state == self.SETTING_SHIPS:
            return False

        for slot in self.slots:
            if slot.x == x and slot.y == y:
                if slot.state == Slot.SHIP:
                    self.set_slot_state(slot, Slot.HIT)
                    return True
                elif slot.state == Slot.EMPTY:
                    self.set_slot_state(slot, Slot.MISS)
                    return True
                else:
                    return False

        return False

    def set_ship(self, x, y):
        if self.state == self.PLAYING:
            logging.info("Returning")
            return False

        for slot in self.slots:
            if slot.x == x and slot.y == y:
                if slot.state == Slot.EMPTY:
                    self.set_slot_state(slot, Slot.SHIP)
                    return True
                elif slot.state == Slot.SHIP or \
                     slot.state == Slot.HIT or \
                     slot.state == Slot.MISS:
                    return False

        return False

    def set_state(self, state):
        self.state = state

    def parse_set_serialized_board(self, serialized_board, secret_ships):
        serialized_slots = serialized_board.split(Slot.OBJ_SEPARATOR)
        logging.info("Ships before clear: " + str(self.count_ships()))
        self.clear()
        logging.info("Ships after clear: " + str(self.count_ships()))

        for serialized_slot in serialized_slots:
            parts = serialized_slot.split(Slot.FIELD_SEPARATOR)
            slot = self.find_slot(int(parts[0]), int(parts[1]))

            if secret_ships:
                if int(parts[2]) != Slot.SHIP:
                    self.set_slot_state(slot, int(parts[2]))
                else:
                    slot.state = int(parts[2])
            else:
                self.set_slot_state(slot, int(parts[2]))

        logging.info("Ships after parse: " + str(self.count_ships()))

    def get_serialized_board(self):
        serialized_board = ""

        for slot in self.slots:
            serialized_board += slot.serialize()

        serialized_board = serialized_board[:-1]
        return serialized_board

    def is_over(self):
        for slot in self.slots:
            if slot.state == Slot.SHIP:
                return False
        return True
    #
    # PRIVATE
    #

    def on_click(self, event):
        loc = self.label_LUT[event.widget]

        if self.on_click_delegate is not None:
            self.on_click_delegate(loc)

    def find_slot(self, x, y):
        for slot in self.slots:
            if slot.x == x and slot.y == y:
                return slot

        return None

    def set_slot_state(self, slot, state):
        slot.state = state
        self.set_picture(slot.x, slot.y, state)

    def try_set_ship(self, x, y, direction, is_first):
        c_slot = self.find_slot(x, y)
        ex_slot = None


        if c_slot is None:
            return False
        else:
            if is_first:
                ex_slot = None
            elif direction == 'N':
                ex_slot = self.find_slot(c_slot.x, c_slot.y + 1)
            elif direction == 'S':
                ex_slot = self.find_slot(c_slot.x, c_slot.y - 1)
            elif direction == 'W':
                ex_slot = self.find_slot(c_slot.x + 1, c_slot.y)
            elif direction == 'E':
                ex_slot = self.find_slot(c_slot.x - 1, c_slot.y)

        surrounding_slots = self.get_surrounding_slots(c_slot)

        for slot in surrounding_slots:
            # if slot is not None:
            #     logging.debug("Testing: " + slot.to_string())
            #     if slot.state == 3:
            #         logging.debug("it is ship")
            #     if ex_slot is None:
            #         logging.debug("Nothing to exclude")
            #     elif slot.x == ex_slot.x and slot.y == ex_slot.y:
            #         logging.debug("Slot is ex_slot")
            #     else:
            #         logging.debug("Slot is not ex_slot")

            if slot is None:
                continue
            elif slot.state == Slot.SHIP:
                if ex_slot is None:
                    logging.debug("Returning false")
                    return False
                elif slot.x == ex_slot.x and slot.y == ex_slot.y:
                    continue
                else:
                    logging.debug("Returning false")
                    return False

        #self.set_slot_state(c_slot, Slot.SHIP)
        return True

    def set_picture(self, x, y, state):
        for label in self.label_LUT.keys():
            if self.label_LUT[label][0] == x and self.label_LUT[label][1] == y:
                if state == Slot.HIT:
                    label.config(image=self.hit_img)
                elif state == Slot.MISS:
                    label.config(image=self.miss_img)
                elif state == Slot.SHIP:
                    label.config(image=self.ship_img)
                elif state == Slot.EMPTY:
                    label.config(image=self.empty_img)

    def get_surrounding_slots(self, slot):
        surround_slots = []

        surround_slots.append(self.find_slot(slot.x - 1, slot.y - 1))
        surround_slots.append(self.find_slot(slot.x - 1, slot.y))
        surround_slots.append(self.find_slot(slot.x - 1, slot.y + 1))
        surround_slots.append(self.find_slot(slot.x, slot.y - 1))
        surround_slots.append(self.find_slot(slot.x, slot.y + 1))
        surround_slots.append(self.find_slot(slot.x + 1, slot.y - 1))
        surround_slots.append(self.find_slot(slot.x + 1, slot.y))
        surround_slots.append(self.find_slot(slot.x + 1, slot.y + 1))

        #logging.debug("Surrounding slot:" + slot.to_string())
        #for s_slot in surround_slots:
            #if s_slot is not None:
                #logging.debug(s_slot.to_string())
        return surround_slots

    #Direction N, E, S, W
    def place_ship(self, x, y, size, direction):
        start_slot = self.find_slot(x, y)
        ship_slots = []
        ship_slots.append(start_slot)
        l_slot = start_slot

        if start_slot is None:
            return

        for i in range(size-1):
            if direction == 'N':
                slot = self.find_slot(l_slot.x, l_slot.y - 1)
            elif direction == 'S':
                slot = self.find_slot(l_slot.x, l_slot.y + 1)
            elif direction == 'W':
                slot = self.find_slot(l_slot.x - 1, l_slot.y)
            elif direction == 'E':
                slot = self.find_slot(l_slot.x + 1, l_slot.y)

            if slot is None:
                return False
            else:
                ship_slots.append(slot)
                l_slot = copy.copy(slot)

        success = True
        for s_slot in ship_slots:
            if s_slot == start_slot:
                if not self.try_set_ship(s_slot.x, s_slot.y, direction, True):
                    success = False
            else:
                if not self.try_set_ship(s_slot.x, s_slot.y, direction, False):
                    success = False

        if success:
            for ss_slot in ship_slots:
                #logging.debug("Setting to ship: " + ss_slot.to_string())
                self.set_slot_state(ss_slot, Slot.SHIP)

        return success

    def count_ships(self):
        count = 0
        for slot in self.slots:
            if slot.state == Slot.SHIP:
                count += 1

        return count

    def remove_hits(self):
        for slot in self.slots:
            if slot.state == Slot.HIT:
                self.set_slot_state(slot, Slot.SHIP)
            elif slot.state == Slot.MISS:
                self.set_slot_state(slot, Slot.EMPTY)

    def refresh(self):
        for slot in self.slots:
            self.set_picture(slot.x, slot.y, slot.state)

    @staticmethod
    def board_size_from_serialized(serialized_board):
        serialized_slots = serialized_board.split(Slot.OBJ_SEPARATOR)
        return len(serialized_slots)
