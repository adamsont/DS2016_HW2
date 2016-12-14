__author__ = 'Taavi'

import common.protocol as P
import logging


def try_parse_packet(message):
        packet = None
        count = 0

        while True:
            if packet is not None:
                break
            elif count == 0:
                packet = IntroductionPacket.try_parse(message)
            elif count == 1:
                packet = NewGamePacket.try_parse(message)
            elif count == 2:
                packet = RequestGameListPacket.try_parse(message)
            elif count == 3:
                packet = RespondGameListPacket.try_parse(message)
            elif count == 4:
                packet = JoinGamePacket.try_parse(message)
            elif count == 5:
                packet = RequestPlayerListPacket.try_parse(message)
            elif count == 6:
                packet = RespondPlayerListPacket.try_parse(message)
            elif count == 7:
                packet = StartGamePacket.try_parse(message)
            elif count == 8:
                packet = PollGameStartPacket.try_parse(message)
            elif count == 9:
                packet = RespondRefreshPacket.try_parse(message)
            elif count == 10:
                packet = PollRefreshPacket.try_parse(message)
            elif count == 11:
                packet = RequestPlayerBoardPacket.try_parse(message)
            elif count == 12:
                packet == RespondPlayerBoardPacket.try_parse(message)
            elif count == 13:
                packet = ShootPacket.try_parse(message)
            elif count == 14:
                logging.info("Try parse failed to recognize any packet")
                break
            count += 1

        return packet


class IntroductionPacket:
    def __init__(self, source, serialized_board):
        self.source = source
        self.serialized_board = serialized_board

    def serialize(self):
        message = "INTRO" + P.HEADER_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.serialized_board

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "INTRO":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = IntroductionPacket(fields[0], fields[1])
        return packet


class NewGamePacket:
    def __init__(self, source, game_name):
        self.source = source
        self.game_name = game_name

    def serialize(self):
        message = "NEW GAME" + P.HEADER_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.game_name

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "NEW GAME":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = NewGamePacket(fields[0], fields[1])
        return packet


class JoinGamePacket:
    def __init__(self, source, game_name):
        self.source = source
        self.game_name = game_name

    def serialize(self):
        message = "JOIN GAME" + P.HEADER_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.game_name

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "JOIN GAME":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = JoinGamePacket(fields[0], fields[1])
        return packet


class RequestGameListPacket:
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "REQ GAME LIST" + P.HEADER_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "REQ GAME LIST":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RequestGameListPacket(fields[0])
        return packet


class RespondGameListPacket:
    def __init__(self, games):
        self.games = games

    def serialize(self):
        message = "RESP GAME LIST" + P.HEADER_SEPARATOR

        for game_name in self.games:
            message += game_name + P.FIELD_SEPARATOR

        if len(self.games) != 0:
            message = message[:-1]

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "RESP GAME LIST":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RespondGameListPacket(fields)
        return packet


class RequestPlayerListPacket():
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "REQ PLAYER LIST" + P.HEADER_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "REQ PLAYER LIST":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RequestPlayerListPacket(fields[0])
        return packet


class RespondPlayerListPacket:
    def __init__(self, players):
        self.players = players

    def serialize(self):
        message = "RESP PLAYER LIST" + P.HEADER_SEPARATOR

        for player_name in self.players:
            message += player_name + P.FIELD_SEPARATOR

        if len(self.players) != 0:
            message = message[:-1]

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "RESP PLAYER LIST":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RespondPlayerListPacket(fields)
        return packet


class StartGamePacket():
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "START GAME" + P.HEADER_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "START GAME":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = StartGamePacket(fields[0])
        return packet


class PollGameStartPacket():
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "POLL START" + P.HEADER_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "POLL START":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = PollGameStartPacket(fields[0])
        return packet


class PollRefreshPacket():
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "POLL REFRESH" + P.HEADER_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "POLL REFRESH":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = PollRefreshPacket(fields[0])
        return packet


class RespondRefreshPacket():
    def __init__(self, is_turn, current_board):
        self.is_turn = is_turn
        self.current_serialized_board = current_board

    def serialize(self):
        message = "RESP REFRESH" + P.HEADER_SEPARATOR
        message += str(self.is_turn) + P.FIELD_SEPARATOR
        message += self.current_serialized_board

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "RESP REFRESH":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        bool_value = False

        if fields[0] == "True":
            bool_value = True

        packet = RespondRefreshPacket(bool_value, fields[1])
        return packet


class ShootPacket():
    def __init__(self, source, target, result_board):
        self.source = source
        self.target = target
        self.result_board = result_board

    def serialize(self):
        message = "SHOOT" + P.HEADER_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.target + P.FIELD_SEPARATOR
        message += self.result_board

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "SHOOT":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = ShootPacket(fields[0], fields[1], fields[2])
        return packet


class RequestPlayerBoardPacket():
    def __init__(self, player):
        self.player = player

    def serialize(self):
        message = "REQ PLAYER BOARD" + P.HEADER_SEPARATOR
        message += self.player

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "REQ PLAYER BOARD":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RequestPlayerBoardPacket(fields[0])
        return packet


class RespondPlayerBoardPacket():
    def __init__(self, board):
        self.board = board

    def serialize(self):
        message = "RESP PLAYER BOARD" + P.HEADER_SEPARATOR
        message += self.board

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "RESP PLAYER BOARD":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RespondPlayerBoardPacket(fields[0])
        return packet