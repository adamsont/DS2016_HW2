__author__ = 'Taavi'


__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging

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

        self.name_entry = Tk.Entry(master_frame, textvariable=self.name_var)
        self.name_entry.config(state=Tk.DISABLED)
        self.name_entry.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.set_name_button = Tk.Button(master_frame, text="Set name", command=self.set_name)
        self.set_name_button.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.text_box = Tk.Text(master_frame, width=100, height=1000)
        self.text_box.bind("<KeyRelease>", self.on_text_changed_handler)
        self.text_box.pack(side=Tk.TOP)
        self.text_box.config(state=Tk.DISABLED)

        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()
        master_frame.pack()
    #
    # PUBLIC
    #

logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()


