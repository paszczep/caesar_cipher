from string import ascii_lowercase, ascii_uppercase, printable
from typing import Literal
from pathlib import Path
from functools import cached_property


class _CaesarShift:

    def map_chars(self, chars: str) -> dict:
        left, right = chars[:self.shift], chars[self.shift:]
        return dict(zip(chars, right + left))

    @cached_property
    def char_map_ascii(self) -> dict:
        self.shift = self.shift % len(ascii_lowercase)
        return self.map_chars(ascii_lowercase) | self.map_chars(ascii_uppercase)

    @cached_property
    def char_map_printable(self) -> dict:
        self.shift = self.shift % len(printable)
        return self.map_chars(printable)

    def encoder_ascii(self, char: str) -> str:
        """Caesar shift occurs in the scope of ASCII characters"""
        return self.char_map_ascii.get(char, char)

    def encoder_printable(self, char: str) -> str:
        """Caesar shift occurs in the scope of all printable characters"""
        return self.char_map_printable.get(char, char)

    def encoder_ord(self, char: str) -> str:
        """Caesar shift occurs in unicode character number"""
        return char.replace(char, chr(ord(char) + self.shift))

    @property
    def encoder_map(self) -> dict[str, callable]:
        return {
            'ascii': self.encoder_ascii, 
            'printable': self.encoder_printable, 
            'order': self.encoder_ord}

    
class CaesarCipher(_CaesarShift):

    def __init__(self, message_content: str, shift: int):
        self.text = message_content
        self.shift = shift

    @staticmethod
    def read_message_file(file: str ="text.txt") -> str:
        return Path(file).read_text()
    
    EncodeOption = Literal["ascii", "printable", "order"]

    def decode_message(self, encoder: EncodeOption) -> str:
        self.shift *= -1
        return self.encode_message(encoder)

    def encode_message(self, option: EncodeOption) -> str:
        return ''.join(self.encoder_map[option](char) for char in self.text)


if __name__ == '__main__':

    content = CaesarCipher.read_message_file()

    for shift_value in range(1, 5):
        for encoding_option in ["ascii", "printable", "order"]:
            _encoded = CaesarCipher(content, shift_value).encode_message(encoding_option)
            _decoded = CaesarCipher(_encoded, shift_value).decode_message(encoding_option)


        print(encoding_option, _encoded, _decoded, sep='\n')
