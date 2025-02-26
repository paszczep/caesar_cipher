from string import ascii_lowercase, ascii_uppercase, printable
from dataclasses import dataclass, fields
from typing import Literal


class CaesarCipher:
    EncodeOption = Literal["ascii", "printable", "order"]

    def __init__(self, message_content: str, shift: int):
        self.text = message_content
        self.shift = shift

    def map_chars(self, chars: str) -> dict:
        left, right = chars[:self.shift], chars[self.shift:]
        return dict(zip(chars, right + left))

    @property
    def char_map_ascii(self) -> dict:
        return self.map_chars(ascii_lowercase) | self.map_chars(ascii_uppercase)

    @property
    def char_map_printable(self) -> dict:
        return self.map_chars(printable)

    def encoder_ascii(self, char: str) -> str:
        return self.char_map_ascii.get(char, char)

    def encoder_printable(self, char: str) -> str:
        return self.char_map_printable.get(char, char)

    def encoder_ord(self, char: str) -> str:
        return char.replace(char, chr(ord(char) + self.shift))

    @property
    def encoder_map(self) -> callable:
        return {'ascii': self.encoder_ascii, 'printable': self.encoder_printable, 'order': self.encoder_ord}

    def encode_message(self, option: EncodeOption) -> str:
        return ''.join(self.encoder_map[option](char) for char in self.text)
    
    def decode_message(self, encoder: callable) -> str:
        self.shift *= -1
        return self.encode_message(encoder)


if __name__ == '__main__':

    with open('file.txt') as file:
        content = file.read()
        print(content, end='\n\n')
        for _s in range(1, 5):
            ascii_encoded = CaesarCipher(content, _s).encode_message('ascii')
            ascii_decoded = CaesarCipher(ascii_encoded, _s).decode_message('ascii')
            printable_encoded = CaesarCipher(content, _s).encode_message('printable')
            printable_decoded = CaesarCipher(printable_encoded, _s).decode_message('printable')
            order_encoded = CaesarCipher(content, _s).encode_message('order')
            order_decoded = CaesarCipher(order_encoded, _s).decode_message('order')

            print(_s,
            'ascii',
            ascii_encoded,
            ascii_decoded,
            'printable',
            printable_encoded,
            printable_decoded,
            'order',
            order_encoded,
            order_decoded, sep='\n')
