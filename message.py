from string import ascii_lowercase, ascii_uppercase, printable
from typing import Literal
from pathlib import Path
from functools import cached_property
from random import shuffle
from enum import Enum, auto


class Message:
    @staticmethod
    def read_message_file(file: str ="text.txt") -> str:
        return Path(file).read_text()


class CaesarShift:

    @staticmethod
    def _random_char_map(chars: str = (ascii_lowercase + ascii_uppercase)) -> dict:
        return dict(zip(chars, shuffle(chars)))

    def _shift_char_map(self, chars: str) -> dict:
        left, right = chars[:self.shift], chars[self.shift:]
        return dict(zip(chars, right + left))

    @cached_property
    def _char_map_ascii(self) -> dict:
        self.shift = self.shift % len(ascii_lowercase)
        return self._shift_char_map(ascii_lowercase) | self._shift_char_map(ascii_uppercase)

    @cached_property
    def _char_map_printable(self) -> dict:
        self.shift = self.shift % len(printable)
        return self._shift_char_map(printable)

    def _encoder_ascii(self, char: str) -> str:
        """shift occurs in the scope of ASCII characters"""
        return self._char_map_ascii.get(char, char)

    def _encoder_printable(self, char: str) -> str:
        """shift occurs in the scope of all printable characters"""
        return self._char_map_printable.get(char, char)

    def _encoder_unicode_nr(self, char: str) -> str:
        """shift occurs in unicode character number"""
        return char.replace(char, chr(ord(char) + self.shift))

    def _encoder_random(self, char: str) -> str:
        """characters randomly replaced in the scope of ASCII characters"""
        return self._random_char_map.get(char, char)


class EncodingOption(Enum):
    SHIFT_ASCII = auto()
    SHIFT_PRINTABLE = auto()
    SHIFT_UNICODE = auto()
    RANDOM_ASCII = auto()

    @classmethod
    def shift_options(cls) -> list['EncodingOption']:
        return [option for option in cls if option.name.startswith("SHIFT")]

    
class CaesarCipher(Message, CaesarShift):

    def __init__(self, message: str, shift: int, encoding: EncodingOption):
        self.text = message
        self.shift = shift
        self.encoding = encoding

    @property
    def encoder(self) -> callable:
        return {
            EncodingOption.SHIFT_ASCII: self._encoder_ascii,
            EncodingOption.SHIFT_PRINTABLE: self._encoder_printable, 
            EncodingOption.SHIFT_UNICODE: self._encoder_unicode_nr,
            EncodingOption.RANDOM_ASCII: self._encoder_random
            }.get(self.encoding)

    def encode_message(self) -> str:
        return ''.join(self.encoder(char) for char in self.text)

    def decode_message(self) -> str:
        self.shift *= -1
        return self.encode_message()



