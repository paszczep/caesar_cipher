from message import CaesarCipher,EncodingOption
from decypher import break_shift

def endcode_decode():
    content = CaesarCipher.read_message_file()

    for shift_value in range(1, 5):
        for encoding_option in EncodingOption.shift_options():
            encoded = CaesarCipher(content, shift_value).encode_message(encoding_option)
            decoded = CaesarCipher(encoded, shift_value).decode_message(encoding_option)


        print(encoding_option, encoded, decoded, sep='\n')

if __name__ == '__main__':
    # endcode_decode()
    break_shift()
