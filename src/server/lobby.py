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

        logging.info("Starting new game: " + packet.game_name)
        game = Game(packet.game_name)
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

        player = self.get_player(packet.source)

        if player is None:
            logging.info("Wtf where did he go?!")
            return P.RESPOND_NOT_OK

        join_game.players.append(player)

        return P.RESPOND_OK

    def handle_request_game_list_packet(self, packet):
        game_names = []
        for game in self.games:
            game_names.append(game.name)

        packet = RespondGameListPacket(game_names)

        return packet.serialize()

    def exists(self, new_player):
        for player in self.players:
            if player.name == new_player.name:
                return True

        return False

    def get_game_index(self, player):
        return False

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player

        return None