__author__ = 'Taavi'


__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging
from game.board import *
from PIL import Image, ImageTk

class Application(Tk.Frame):

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()

        self.master.title("Client App as Unknown")
        master.geometry('{}x{}'.format(1100, 600))

        #
        # Variables
        #

        self.msg_queue = Queue.Queue()
        self.last_text = list()
        self.name_var = Tk.StringVar()
        self.name_var.set('Unknown')
        self.initialized = False
        self.introduced = False

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

    def create_widgets(self):
        master_frame = Tk.Frame(self)
        board1 = Board()
        board_frame1 = board1.init_board(master_frame)

        board2 = Board()
        board_frame2 = board2.init_board(master_frame)

        board_frame1.pack(side=Tk.LEFT, padx=10)
        board_frame2.pack(side=Tk.RIGHT, padx=10)

        master_frame.pack()
    #
    # PUBLIC
    #

logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()


