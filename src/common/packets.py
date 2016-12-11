__author__ = 'Taavi'

import common.protocol as P


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