__author__ = 'Taavi'


__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging
from game.board import *
from PIL import Image, ImageTk

class Application(Tk.Frame):
    #
    # States
    #

    SETTING_UP = 2
    NOT_CONNECTED = 4
    CONNECTED = 5
    PLAYING = 6

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()

        self.master.title("Client App as Unknown")
        master.geometry('{}x{}'.format(1100, 600))

        #
        # Logic stuff
        #

        self.msg_queue = Queue.Queue()
        self.state = self.SETTING_UP

        self.ships_left = dict()
        self.ships_left["Carrier"] = 5
        self.ships_left["Battleship"] = 4
        self.ships_left["Cruiser"] = 3
        self.ships_left["Submarine"] = 3
        self.ships_left["Destroyer"] = 2

        #
        # Variables
        #

        self.name_var = Tk.StringVar()
        self.name_var.set('Unknown')

        self.selected_tool_var = Tk.StringVar()
        self.selected_tool_var.set("Set ships")

        self.selected_state_var = Tk.StringVar()
        self.selected_state_var.set("SETTING_UP")

        self.selected_direction_var = Tk.StringVar()
        self.selected_direction_var.set("N")

        self.selected_ship_var = Tk.StringVar()
        self.selected_ship_var.set("Carrier")

        self.selected_ship_size_var = Tk.StringVar()
        self.selected_ship_size_var.set("1")

        self.own_board = Board()
        self.other_board = Board()

        #
        #Widgets
        #

        self.ship_menu = None
        self.setup_ready_button = None
        self.setup_frame = None

        self.create_widgets()
        self.inner_loop()
        self.state_machine()

    # Handles all requests from another threads and runs them in its own
    def inner_loop(self):
        try:
            f = self.msg_queue.get(False)
            f()
        except Queue.Empty:
            pass

        self.master.after(10, self.inner_loop)

    def state_machine(self):
        if self.state == self.SETTING_UP:
            logging.info("State: SETTING UP")
        elif self.state == self.NOT_CONNECTED:
            for child in self.setup_frame.winfo_children():
                child.configure(state='disable')
            logging.info("State: NOT CONNECTED")
        elif self.state == self.CONNECTED:
            logging.info("State: CONNECTED")
        elif self.state == self.PLAYING:
            logging.info("State: PLAYING")

        self.master.after(500, self.state_machine)

    def create_widgets(self):
        master_frame = Tk.Frame(self)
        self.setup_frame = self.build_setup_frame(master_frame)
        self.setup_frame.grid(row=0, column=0, pady=10)

        own_board_frame = self.own_board.init_board(master_frame, True)
        self.own_board.on_click_delegate = self.on_own_board_click

        other_board_frame = self.other_board.init_board(master_frame, False)

        own_board_frame.grid(row=1, column=0, padx=10, columnspan=2)
        other_board_frame.grid(row=1, column=2, padx=10, columnspan=2)

        menu_frame = Tk.Frame(master_frame)
        state_menu = Tk.OptionMenu(menu_frame, self.selected_state_var, "SETTING_UP", "NOT CONNECTED", "CONNECTED", "PLAYING")
        state_menu.pack(side=Tk.RIGHT)

        tool_menu = Tk.OptionMenu(menu_frame, self.selected_tool_var, "Set ships", "Set hit")
        tool_menu.pack(side=Tk.RIGHT)

        ship_direction_menu = Tk.OptionMenu(menu_frame, self.selected_direction_var, "N", "W", "S", "E")
        ship_direction_menu.pack(side=Tk.RIGHT)

        ship_size_menu = Tk.OptionMenu(menu_frame, self.selected_ship_size_var, "1", "2", "3", "4")
        ship_size_menu.pack(side=Tk.RIGHT)

        menu_frame.grid(row=0, column=2, pady=10)
        master_frame.pack()

    def build_setup_frame(self, parent):
        setup_frame = Tk.Frame(parent)
        name_label = Tk.Label(setup_frame, text="Nickname:")
        name_box = Tk.Entry(setup_frame, textvariable=self.name_var)

        ship_label = Tk.Label(setup_frame, text="Set ships:")
        self.ship_menu = Tk.OptionMenu(setup_frame, self.selected_ship_var, *self.ships_left.keys())

        ship_direction_menu = Tk.OptionMenu(setup_frame, self.selected_direction_var, "N", "W", "S", "E")

        self.setup_ready_button = Tk.Button(setup_frame, text="Ready", command=self.setup_ready_button_pressed)

        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_box.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        ship_label.grid(row=1, column=0, padx=5, pady=5)
        self.ship_menu.grid(row=1, column=1, padx=5, pady=5)
        ship_direction_menu.grid(row=1, column=2, padx=5, pady=5)
        self.setup_ready_button.grid(row=2, column=0, padx=5, pady=5)

        return setup_frame

    def on_own_board_click(self, loc):
        logging.debug("client_main.on_board_click()")

        if self.state == self.SETTING_UP:
            if len(self.ships_left) != 0:
                ship = self.selected_ship_var.get()

                if self.own_board.place_ship(loc[0], loc[1], self.ships_left[ship], self.selected_direction_var.get()):
                    del self.ships_left[ship]
                    self.ship_menu["menu"].delete(0, "end")

                    for ship in self.ships_left.keys():
                        self.ship_menu["menu"].add_command(label=ship, command=lambda v=ship: self.selected_ship_var.set(v))
            else:
                self.selected_ship_var.set("No more ships to place")

            if len(self.ships_left) != 0:
                self.selected_ship_var.set(self.ships_left.keys()[0])

        # if self.selected_state_var.get() == "PLAYING":
        #     logging.info("State: PLAYING")
        #     self.own_board.set_state(Board.PLAYING)
        # elif self.selected_state_var.get() == "SETTING SHIPS":
        #     logging.info("State: SETTING SHIPS")
        #     self.own_board.set_state(Board.SETTING_SHIPS)
        #
        # if self.selected_tool_var.get() == "Set ships":
        #     logging.info("Setting ship")
        #     self.own_board.place_ship(loc[0], loc[1], int(self.selected_ship_size_var.get()), self.selected_direction_var.get())
        #     #self.own_board.set_ship(loc[0], loc[1])
        # elif self.selected_tool_var.get() == "Set hit":
        #     logging.info("Setting hit")
        #     self.own_board.set_hit(loc[0], loc[1])

    def setup_ready_button_pressed(self):
        logging.debug("Setup ready button pressed")
        if len(self.ships_left) == 0 and self.name_var.get() != "Unknown":
            logging.info("Confirmed ready")
            self.state = self.NOT_CONNECTED

    def get_test_state(self):
        str_state = self.selected_state_var.get()
        state = self.SETTING_UP

        if str_state == "SETTING UP":
            state = self.SETTING_UP
        elif str_state == "NOT_CONNECTED":
            state = self.NOT_CONNECTED
        elif str_state == "CONNECTED":
            state = self.CONNECTED
        elif str_state == "PLAYING":
            state = self.PLAYING

        return state
    #
    # PUBLIC
    #

logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()


