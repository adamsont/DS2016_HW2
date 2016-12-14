__author__ = 'Taavi'


__author__ = 'Taavi'

from PIL import Image, ImageTk

from common.game.board import *
from client_connection import *


class Application(Tk.Frame):
    #
    # States
    #

    SETTING_UP = 2
    NOT_CONNECTED = 4
    CONNECTED = 5
    IN_GAME = 6
    PLAYING = 7

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()

        self.master.title("BattleShips 2000")
        master.geometry('{}x{}'.format(1100, 600))
        #
        # Connection stuff
        #

        self.connection = ConnectionActor()

        #
        # Logic stuff
        #

        self.msg_queue = Queue.Queue()
        self.state = self.SETTING_UP
        self.is_my_turn = False
        self.selected_opponent = None

        self.ships_left = dict()
        self.ships_left["Carrier"] = 5
        self.ships_left["Battleship"] = 4
        self.ships_left["Cruiser"] = 3
        self.ships_left["Submarine"] = 3
        self.ships_left["Destroyer"] = 2

        self.set_name = None

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

        self.new_game_name_var = Tk.StringVar()
        self.new_game_name_var.set("My game name")

        self.join_game_name_var = Tk.StringVar()
        self.join_game_name_var.set("")

        self.current_opponent_name_var = Tk.StringVar()
        self.current_opponent_name_var.set("")

        self.own_board = Board()
        self.other_board = Board()

        #
        #Widgets
        #

        self.setup_frame = None
        self.ship_menu = None

        self.connection_frame = None
        self.join_game_name_menu = None

        self.game_frame = None
        self.turn_indicator = None
        self.start_game_button = None
        self.no_turn_img = ImageTk.PhotoImage(Image.open("../../resources/no_turn.jpg"))
        self.turn_img = ImageTk.PhotoImage(Image.open("../../resources/turn.jpg"))
        self.inactive_img = ImageTk.PhotoImage(Image.open("../../resources/inactive.jpg"))

        self.current_opponent_name_menu = None

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
            self.enable_frame(self.setup_frame)
            self.disable_frame(self.connection_frame)
            self.disable_frame(self.game_frame)
            logging.info("State: SETTING UP")

        elif self.state == self.NOT_CONNECTED:
            self.enable_frame(self.setup_frame)
            self.disable_frame(self.connection_frame)
            self.disable_frame(self.game_frame)
            logging.info("State: NOT CONNECTED")

        elif self.state == self.CONNECTED:
            self.disable_frame(self.setup_frame)
            self.disable_frame(self.game_frame)
            self.enable_frame(self.connection_frame)
            logging.info("State: CONNECTED")

        elif self.state == self.IN_GAME:
            self.disable_frame(self.setup_frame)
            self.enable_frame(self.game_frame)
            self.disable_frame(self.connection_frame)

            packet = PollGameStartPacket(self.set_name)
            self.connection.send(packet, self.on_respond_game_start)
            logging.info("State: IN GAME")

        elif self.state == self.PLAYING:
            self.disable_frame(self.setup_frame)
            self.enable_frame(self.game_frame)
            self.disable_frame(self.connection_frame)

            self.own_board.set_state(Board.PLAYING)
            self.other_board.set_state(Board.PLAYING)
            self.start_game_button.config(state="disable")

            packet = PollRefreshPacket(self.set_name)
            self.connection.send(packet, self.on_respond_refresh)
            logging.info("State: PLAYING")

        self.master.after(100, self.state_machine)

    def create_widgets(self):
        master_frame = Tk.Frame(self)
        self.setup_frame = self.build_setup_frame(master_frame)
        self.setup_frame.grid(row=0, column=0, pady=10)

        self.connection_frame = self.build_connection_frame(master_frame)
        self.connection_frame.grid(row=0, column=1, pady=10)

        self.game_frame = self.build_game_frame(master_frame)
        self.game_frame.grid(row=0, column=2, pady=10)

        own_board_frame = self.own_board.init_board(master_frame, True)
        self.own_board.on_click_delegate = self.on_own_board_click

        other_board_frame = self.other_board.init_board(master_frame, True)
        self.other_board.on_click_delegate = self.on_other_board_click

        own_board_frame.grid(row=1, column=0, padx=10, columnspan=2)
        other_board_frame.grid(row=1, column=2, padx=10, columnspan=2)

        master_frame.pack()

    def build_setup_frame(self, parent):
        setup_frame = Tk.Frame(parent)

        name_label = Tk.Label(setup_frame, text="Nickname:")
        name_box = Tk.Entry(setup_frame, textvariable=self.name_var)

        ship_label = Tk.Label(setup_frame, text="Set ships:")
        self.ship_menu = Tk.OptionMenu(setup_frame, self.selected_ship_var, *self.ships_left.keys())

        ship_direction_menu = Tk.OptionMenu(setup_frame, self.selected_direction_var, "N", "W", "S", "E")
        setup_ready_button = Tk.Button(setup_frame, text="Ready", command=self.setup_ready_button_pressed)

        name_label.grid(row=0, column=0, padx=5, pady=0)
        name_box.grid(row=0, column=1, padx=5, pady=0, columnspan=2)
        ship_label.grid(row=1, column=0, padx=5, pady=0)
        self.ship_menu.grid(row=1, column=1, padx=5, pady=0)
        ship_direction_menu.grid(row=1, column=2, padx=5, pady=0)
        setup_ready_button.grid(row=2, column=0, padx=5, pady=0)

        return setup_frame

    def build_game_frame(self, parent):
        game_frame = Tk.Frame(parent)

        turn_indicator_label = Tk.Label(game_frame, text="Turn?")
        self.turn_indicator = Tk.Label(game_frame, image=self.inactive_img)
        self.turn_indicator.image = self.inactive_img
        self.start_game_button = Tk.Button(game_frame, text="Start game", command=self.start_game_button_pressed)

        opponent_label = Tk.Label(game_frame, text="Opponent: ")
        self.current_opponent_name_menu = Tk.OptionMenu(game_frame, variable=self.current_opponent_name_var, value="")
        select_opponent_button = Tk.Button(game_frame, text="Select", command=self.select_opponent_button_pressed)

        refresh_opponent_button = Tk.Button(game_frame, text="Refresh", command=self.refresh_opponent_button_pressed)
        leave_game_button = Tk.Button(game_frame, text="Leave game", command=self.leave_game_button_pressed)

        turn_indicator_label.grid(row=0, column=0, padx=5, pady=0)
        self.turn_indicator.grid(row=0, column=1, padx=5, pady=0)
        self.start_game_button.grid(row=0, column=2, padx=5, pady=0)
        opponent_label.grid(row=1, column=0, padx=5, pady=0)
        self.current_opponent_name_menu.grid(row=1, column=1, padx=5, pady=0)
        select_opponent_button.grid(row=1, column=2, padx=5, pady=0)
        refresh_opponent_button.grid(row=2, column=0, padx=5, pady=0)
        leave_game_button.grid(row=2, column=1, padx=5, pady=0)

        return game_frame

    def build_connection_frame(self, parent):
        connection_frame = Tk.Frame(parent)

        new_game_button = Tk.Button(connection_frame, text="New game", command=self.new_game_button_pressed)
        new_game_name_box = Tk.Entry(connection_frame, textvariable=self.new_game_name_var)

        join_game_button = Tk.Button(connection_frame, text="Join game", command=self.join_game_button_pressed)
        self.join_game_name_menu = Tk.OptionMenu(connection_frame, variable=self.join_game_name_var, value="")

        refresh_button = Tk.Button(connection_frame, text="Refresh", command=self.refresh_game_list_button_pressed)

        new_game_button.grid(row=0, column=0, padx=5, pady=0)
        new_game_name_box.grid(row=0, column=1, padx=5, pady=0)
        join_game_button.grid(row=1, column=0, padx=5, pady=0)
        self.join_game_name_menu.grid(row=1, column=1, padx=5, pady=0)
        refresh_button.grid(row=2, column=0, padx=5, pady=0)

        return connection_frame

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

                    if len(self.ships_left) != 0:
                        self.selected_ship_var.set(self.ships_left.keys()[0])
                    else:
                        self.selected_ship_var.set("No more ships to place")

            else:
                self.selected_ship_var.set("No more ships to place")


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

    def on_other_board_click(self, loc):
        if self.state != self.PLAYING or not self.is_my_turn:
            return

        if self.selected_opponent is None:
            return

        self.other_board.set_hit(loc[0], loc[1])
        packet = ShootPacket(self.set_name, self.selected_opponent, self.other_board.get_serialized_board())
        self.connection.send(packet, self.on_shoot_packet_response)

        self.selected_opponent = None

    def reset(self):
        self.ships_left = dict()
        self.ships_left["Carrier"] = 5
        self.ships_left["Battleship"] = 4
        self.ships_left["Cruiser"] = 3
        self.ships_left["Submarine"] = 3
        self.ships_left["Destroyer"] = 2


    # Button press handlers
    #------------------------

    def setup_ready_button_pressed(self):
        logging.debug("Setup ready button pressed")
        self.set_name = self.name_var.get()

        if len(self.ships_left) == 0 and self.set_name != "Unknown" \
                and P.FIELD_SEPARATOR not in self.set_name \
                and P.HEADER_SEPARATOR not in self.set_name \
                and self.set_name != "":
            self.state = self.NOT_CONNECTED
            packet = IntroductionPacket(self.set_name, self.own_board.get_serialized_board())
            self.connection.send(packet, self.on_introduction_response)

    def new_game_button_pressed(self):
        game_name = self.new_game_name_var.get()

        if P.FIELD_SEPARATOR in game_name or P.HEADER_SEPARATOR in game_name:
            return

        logging.info("Starting new game: " + game_name)

        if self.state == self.CONNECTED:
            packet = NewGamePacket(self.set_name, game_name)
            self.connection.send(packet, self.on_new_game_response)

    def join_game_button_pressed(self):
        game_name = self.join_game_name_var.get()

        logging.info("Joining game: " + game_name)

        if self.state == self.CONNECTED:
            packet = JoinGamePacket(self.set_name, game_name)
            self.connection.send(packet, self.on_join_game_response)

    def refresh_game_list_button_pressed(self):
        if self.state == self.CONNECTED:
            packet = RequestGameListPacket(self.set_name)
            self.connection.send(packet, self.on_respond_game_list)

    def select_opponent_button_pressed(self):
        if self.state == self.PLAYING:
            self.selected_opponent = self.current_opponent_name_var.get()

            if self.selected_opponent == "":
                return

            packet = RequestPlayerBoardPacket(self.selected_opponent)
            self.connection.send(packet, self.on_player_board_response)

    def refresh_opponent_button_pressed(self):
        if self.state == self.IN_GAME or self.state == self.PLAYING:
            packet = RequestPlayerListPacket(self.set_name)
            self.connection.send(packet, self.on_respond_player_list)

    def leave_game_button_pressed(self):
        pass

    def start_game_button_pressed(self):
        if self.state == self.IN_GAME:
            packet = StartGamePacket(self.set_name)
            self.connection.send(packet, self.on_respond_game_start)

    def disable_frame(self, frame):
        for child in frame.winfo_children():
            child.configure(state='disable')

    def enable_frame(self, frame):
        for child in frame.winfo_children():
            child.configure(state='normal')

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

    def on_introduction_result_handler(self, response):
        if self.state == self.NOT_CONNECTED:
            if response == P.RESPOND_OK:
                self.state = self.CONNECTED
            else:
                self.state = self.SETTING_UP

    def on_new_game_response_handler(self, response):
        if self.state == self.CONNECTED:
            if response == P.RESPOND_OK:
                self.state = self.IN_GAME

    def on_join_game_response_handler(self, response):
        if self.state == self.CONNECTED:
            if response == P.RESPOND_OK:
                self.state = self.IN_GAME

    def on_respond_game_list_handler(self, response):
        packet = RespondGameListPacket.try_parse(response)

        if packet is None:
            logging.info("Bad game list response packet received")
            return

        game_list = packet.games

        self.join_game_name_menu["menu"].delete(0, "end")

        for game_name in game_list:
            self.join_game_name_menu["menu"].add_command(label=game_name, command=lambda v=game_name: self.join_game_name_var.set(v))

    def on_respond_player_list_handler(self, response):
        packet = RespondPlayerListPacket.try_parse(response)

        if packet is None:
            logging.info("Bad player list response packet received")
            return

        player_list = packet.players

        self.current_opponent_name_menu["menu"].delete(0, "end")

        for player_name in player_list:
            self.current_opponent_name_menu["menu"].add_command(label=player_name, command=lambda v=player_name: self.current_opponent_name_var.set(v))

    def on_respond_game_start_handler(self, response):
        if self.state == self.IN_GAME and response == P.RESPOND_OK:
            self.state = self.PLAYING

    def on_respond_refresh_handler(self, response):
        packet = RespondRefreshPacket.try_parse(response)

        if packet is None:
            logging.info("Bad refresh response packet received")
            return

        self.own_board.parse_set_serialized_board(packet.current_serialized_board, False)

        if packet.is_turn:
            self.is_my_turn = True
            self.turn_indicator.config(image=self.turn_img)
        elif not packet.is_turn:
            self.is_my_turn = False
            self.turn_indicator.config(image=self.no_turn_img)
        else:
            self.is_my_turn = False
            self.turn_indicator.config(image=self.inactive_img)

    def on_player_board_response_handler(self, response):
        packet = RespondPlayerBoardPacket.try_parse(response)

        if packet is None:
            logging.info("Bad player board response packet received")
            return

        self.other_board.parse_set_serialized_board(packet.board, True)

    def on_shoot_packet_response_handler(self, response):
        pass

    #
    # PUBLIC
    #

    def on_introduction_response(self, response):
        self.msg_queue.put(lambda: self.on_introduction_result_handler(response))

    def on_new_game_response(self, response):
        self.msg_queue.put(lambda: self.on_new_game_response_handler(response))

    def on_join_game_response(self, response):
        self.msg_queue.put(lambda: self.on_join_game_response_handler(response))

    def on_respond_game_list(self, response):
        self.msg_queue.put(lambda: self.on_respond_game_list_handler(response))

    def on_respond_player_list(self, response):
        self.msg_queue.put(lambda: self.on_respond_player_list_handler(response))

    def on_respond_game_start(self, response):
        self.msg_queue.put(lambda: self.on_respond_game_start_handler(response))

    def on_respond_refresh(self, response):
        self.msg_queue.put(lambda: self.on_respond_refresh_handler(response))

    def on_player_board_response(self, response):
        self.msg_queue.put(lambda: self.on_player_board_response_handler(response))

    def on_shoot_packet_response(self, response):
        self.msg_queue.put(lambda: self.on_shoot_packet_response_handler(response))

logging.basicConfig(level=logging.INFO)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()


