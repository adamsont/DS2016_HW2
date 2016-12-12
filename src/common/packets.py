__author__ = 'Taavi'

import common.protocol as P


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
                break
            count += 1

        return packet


class IntroductionPacket:
    def __init__(self, source, serialized_board):
        self.source = source
        self.serialized_board = serialized_board

    def serialize(self):
        message = "INTRO" + P.HEADER_FIELD_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.serialized_board

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_FIELD_SEPARATOR)

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
        message = "NEW GAME" + P.HEADER_FIELD_SEPARATOR
        message += self.source + P.FIELD_SEPARATOR
        message += self.game_name

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_FIELD_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "NEW GAME":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = NewGamePacket(fields[0], fields[1])
        return packet


class RequestGameListPacket:
    def __init__(self, source):
        self.source = source

    def serialize(self):
        message = "REQ GAME LIST" + P.HEADER_FIELD_SEPARATOR
        message += self.source

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_FIELD_SEPARATOR)

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
        message = "RESP GAME LIST" + P.HEADER_FIELD_SEPARATOR

        for game_name in self.games:
            message += game_name + P.FIELD_SEPARATOR

        message = message[:-1]

        return message

    @staticmethod
    def try_parse(message):
        parts = message.split(P.HEADER_FIELD_SEPARATOR)

        if len(parts) != 2:
            return None

        if parts[0] != "RESP GAME LIST":
            return None

        fields = parts[1].split(P.FIELD_SEPARATOR)

        packet = RespondGameListPacket(fields)
        return packet