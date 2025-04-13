from message import CaesarCipher, EncodingOption
import unittest
from logging import info

class TestEncoding(unittest.TestCase):
    def test_shifts(self):
        message_text = CaesarCipher.read_message_file()
        info(f'test text: {message_text[:40]}...')
        shift_encoding_options = EncodingOption.shift_options()
        info(f'test encodings: {str(shift_encoding_options)[1:-1]}')
        for shift_value in range(1, 200):
            for encoding_option in shift_encoding_options:
                with self.subTest(shift=shift_value, option=encoding_option):
                    encoded = CaesarCipher(message_text, shift_value, encoding_option).encode_message()
                    decoded = CaesarCipher(encoded, shift_value, encoding_option).decode_message()

                    self.assertNotEqual(encoded, message_text, "Should actually encode the message")
                    self.assertEqual(decoded, message_text, "Should decode back to original")


if __name__ == "__main__":
    unittest.main()
