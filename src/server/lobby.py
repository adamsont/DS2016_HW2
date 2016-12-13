__author__ = 'Taavi'
import logging
import pika
from server_connection import *
import common.protocol as P
from common.packets import *
from player import *
from game import *


class Lobby(SynchronizedRequestHandler):

    def __init__(self, channel, queue_name):
        SynchronizedRequestHandler.__init__(self, channel, queue_name)
        self.players = []
        self.games = []

    def handle_request(self, message):
        packet = try_parse_packet(message)

        response = P.RESPOND_NOT_OK

        if packet is not None:
            packet_type = packet.__class__.__name__

            logging.info("Received: " + packet_type)

            if packet_type == 'IntroductionPacket':
                response = self.handle_introduction_packet(packet)
            elif packet_type == "NewGamePacket":
                response = self.handle_new_game_packet(packet)
            elif packet_type == "RequestGameListPacket":
                response = self.handle_request_game_list_packet(packet)
            elif packet_type == "JoinGamePacket":
                response = self.handle_join_game_packet(packet)
            elif packet_type == "RequestPlayerListPacket":
                response = self.handle_request_player_list_packet(packet)
            elif packet_type == "StartGamePacket":
                response = self.handle_start_game_packet(packet)
            elif packet_type == "PollGameStartPacket":
                response = self.handle_poll_game_start_packet(packet)

        return response

    def handle_introduction_packet(self, packet):
        player = Player(packet.source, packet.serialized_board)

        if not self.exists(player):
            logging.info("New player in lobby: " + player.name)
            self.players.append(player)
            return P.RESPOND_OK
        else:
            return P.RESPOND_NOT_OK

    def handle_new_game_packet(self, packet):
        for game in self.games:
            if game.name == packet.game_name:
                return P.RESPOND_NOT_OK

        player = self.get_player_by_name(packet.source)

        if player is None:
            logging.info("No such player while trying to make new game")
            return P.RESPOND_NOT_OK

        logging.info("Starting new game: " + packet.game_name)
        game = Game(packet.game_name)
        game.players.append(player)
        self.games.append(game)

        return P.RESPOND_OK

    def handle_join_game_packet(self, packet):
        join_game = None

        for game in self.games:
            if game.name == packet.game_name:
                join_game = game

        if join_game is None:
            return P.RESPOND_NOT_OK

        logging.info("Adding player: " + packet.source + " to game: " + join_game.name)

        player = self.get_player_by_name(packet.source)

        if player is None:
            logging.info("Wtf where did he go?!")
            return P.RESPOND_NOT_OK

        join_game.players.append(player)
        logging.info("Game " + join_game.name + " currently has " + str(len(join_game.players)) + " players")

        return P.RESPOND_OK

    def handle_request_game_list_packet(self, packet):
        game_names = []
        for game in self.games:
            game_names.append(game.name)

        packet = RespondGameListPacket(game_names)

        return packet.serialize()

    def handle_request_player_list_packet(self, packet):
        source = packet.source
        game = self.get_game_by_player(source)

        if game is None:
            logging.info("Requested player list by player not in any games")
            return P.RESPOND_NOT_OK

        player_names = []

        for player in game.players:
            player_names.append(player.name)

        if source in player_names:
            player_names.remove(source)

        packet = RespondPlayerListPacket(player_names)

        return packet.serialize()

    def handle_start_game_packet(self, packet):
        source = packet.source
        game = self.get_game_by_player(source)
        player = self.get_player_by_name(source)

        if game is None:
            logging.info("Requested start game by player not in any games")
            return P.RESPOND_NOT_OK

        if len(game.players) < 2:
            logging.info("Not enough players to start a game")
            return P.RESPOND_NOT_OK

        if game.ongoing:
            logging.info("Game already ongoing")
            return P.RESPOND_NOT_OK

        if player == game.players[0]:
            game.ongoing = True
            return P.RESPOND_OK
        else:
            return P.RESPOND_NOT_OK


    def handle_poll_game_start_packet(self, packet):
        source = packet.source
        game = self.get_game_by_player(source)

        if game.ongoing:
            return P.RESPOND_OK
        else:
            return P.RESPOND_NOT_OK

    def exists(self, new_player):
        for player in self.players:
            if player.name == new_player.name:
                return True

        return False

    def get_game_by_player(self, player_name):
        for game in self.games:
            for player in game.players:
                if player.name == player_name:
                    return game

        return None

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

        return None