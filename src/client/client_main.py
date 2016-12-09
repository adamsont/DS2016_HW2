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

    PLAYING = 1
    SETTING_UP = 2
    NOT_CONNECTED = 3

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

        #
        # Variables
        #

        self.name_var = Tk.StringVar()
        self.name_var.set('Unknown')

        self.selected_tool_var = Tk.StringVar()
        self.selected_tool_var.set("Set ships")

        self.selected_state_var = Tk.StringVar()
        self.selected_state_var.set("SETTING SHIPS")

        self.selected_direction_var = Tk.StringVar()
        self.selected_direction_var.set("N")

        self.selected_ship_size_var = Tk.StringVar()
        self.selected_ship_size_var.set("1")

        self.own_board = Board()
        self.other_board = Board()

        #
        #Widgets
        #
        
        self.create_widgets()
        self.inner_loop()

    # Handles all requests from another threads and runs them in its own
    def inner_loop(self):
        try:
            f = self.msg_queue.get(False)
            f()
        except Queue.Empty:
            pass

        self.master.after(10, self.inner_loop)

    def state_machine(self):
        self.master.after(2, self.state_machine)

        if

    def create_widgets(self):
        master_frame = Tk.Frame(self)
        self.own_board = Board()
        own_board_frame = self.own_board.init_board(master_frame, True)
        self.own_board.on_click_delegate = self.on_board_click

        self.other_board = Board()
        other_board_frame = self.other_board.init_board(master_frame, False)

        own_board_frame.grid(row=1, column=0, padx=10)
        other_board_frame.grid(row=1, column=1, padx=10)

        menu_frame = Tk.Frame(master_frame)
        state_menu = Tk.OptionMenu(menu_frame, self.selected_state_var, "PLAYING", "SETTING SHIPS")
        state_menu.pack(side=Tk.RIGHT)

        tool_menu = Tk.OptionMenu(menu_frame, self.selected_tool_var, "Set ships", "Set hit")
        tool_menu.pack(side=Tk.RIGHT)

        ship_direction_menu = Tk.OptionMenu(menu_frame, self.selected_direction_var, "N", "W", "S", "E")
        ship_direction_menu.pack(side=Tk.RIGHT)

        ship_size_menu = Tk.OptionMenu(menu_frame, self.selected_ship_size_var, "1", "2", "3", "4")
        ship_size_menu.pack(side=Tk.RIGHT)

        menu_frame.grid(row=0, column=0, pady=10)

        master_frame.pack()

    def on_board_click(self, loc):
        logging.debug("client_main.on_board_click()")

        if self.selected_state_var.get() == "PLAYING":
            logging.info("State: PLAYING")
            self.own_board.set_state(Board.PLAYING)
        elif self.selected_state_var.get() == "SETTING SHIPS":
            logging.info("State: SETTING SHIPS")
            self.own_board.set_state(Board.SETTING_SHIPS)

        if self.selected_tool_var.get() == "Set ships":
            logging.info("Setting ship")
            self.own_board.place_ship(loc[0], loc[1], int(self.selected_ship_size_var.get()), self.selected_direction_var.get())
            #self.own_board.set_ship(loc[0], loc[1])
        elif self.selected_tool_var.get() == "Set hit":
            logging.info("Setting hit")
            self.own_board.set_hit(loc[0], loc[1])
    #
    # PUBLIC
    #

logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()


