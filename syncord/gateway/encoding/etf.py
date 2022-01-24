from earl import pack, unpack
from websocket import ABNF

from syncord.gateway.encoding.base import BaseEncoder


class ETFEncoder(BaseEncoder):
    TYPE = "etf"
    OPCODE = ABNF.OPCODE_BINARY

    @staticmethod
    def encode(obj):
        return pack(obj)

    @staticmethod
    def decode(obj):
        return unpack(obj, encoding="utf-8", encode_binary_ext=True)
