"""
Randomly encode message, randomly decode message, classify result.
"""
from message import CaesarCipher, EncodingOption
from gibberishclassifier import classify
from random import randint, choice


def break_shift():
    content = CaesarCipher.read_message_file()
    N = (1, 100)
    shift_value = randint(*N)
    encoding_option = EncodingOption.SHIFT_ASCII
    encoded = CaesarCipher(content, shift_value, encoding_option).encode_message()
    
    guesses = []
    for _s in range(*N):
        decoded = CaesarCipher(encoded, _s, encoding_option).decode_message()
        guesses.append((classify(decoded), decoded))
    
    best_guess = min(score for score, _ in guesses)
    best_indexes = [i for i, guess in enumerate(guesses) if guess[0] == best_guess]

    for _index in best_indexes:
        print(_index, guesses[_index])
    