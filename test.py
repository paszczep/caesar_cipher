from message import CaesarCipher
import unittest
import base64


class TestEncoding(unittest.TestCase):
    def test_encode_decode(self):

        
        message_text = CaesarCipher.read_message_file()
        available_encoding_options = [
            "ascii",
            "printable", 
            "order"
            ]
        for shift_value in range(1, 200):
            for encoding_option in available_encoding_options:
                with self.subTest(shift=shift_value, option=encoding_option):
                    encoded = CaesarCipher(message_text, shift_value).encode_message(encoding_option)
                    decoded = CaesarCipher(encoded, shift_value).decode_message(encoding_option)

                    self.assertNotEqual(encoded, message_text, "Should actually encode the message")
                    self.assertEqual(decoded, message_text, "Should decode back to original")


if __name__ == "__main__":
    unittest.main()
