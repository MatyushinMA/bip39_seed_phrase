import sys
from time import time
from hashlib import sha256

import numpy.random as npr

SIZE = 256
PRINT_SIZE = 32
WORDS_PRINT_SIZE = 6

def load_word_list(lang='en'):
    if lang == 'en':
        filename = "english.txt"
    elif lang == 'cn':
        filename = "chinese_simplified.txt"
    else:
        raise NotImplementedError(f"{lang} language is not supported")

    words = []
    with open(filename, 'r') as fr:
        for ln in fr:
            words.append(ln.strip())

    return words

def set_seed():
    seed = int(time())
    npr.seed(seed)
    return seed

def print_bits(bits, wording="Generated entropy"):
    pretty_bits = '\n'.join([''.join(list(map(str, bits))[x:x + PRINT_SIZE]) for x in range(0, len(bits), PRINT_SIZE)])
    print(f"""
{wording}:
{pretty_bits}
    """)

def print_words(words):
    pretty_words = '\n'.join([' '.join(words[x:x + WORDS_PRINT_SIZE]) for x in range(0, len(words), WORDS_PRINT_SIZE)])
    print(f"""
Generated seed phrase:
{pretty_words}
    """)

def bits_sha(bits):
    str_list = [''.join(map(str, bits[x:x+8])) for x in range(0, SIZE, 8)]
    for s in str_list:
        assert len(s) == 8
    int_list = map(lambda x : int(x, 2), str_list)
    data = b''.join(map(lambda x : x.to_bytes(1, sys.byteorder), int_list))
    sha_val = sha256(data).hexdigest()
    return sha_val

def add_additional_bits(bits, sha_val):
    additional_bytes = sha_val[:2] if SIZE == 256 else sha_val[:1]
    for b in additional_bytes:
        bits.extend(map(int, f"{int(b, 16):04b}"))
    return bits

def gen_words(bits, words):
    for word_ind in [int(''.join(map(str, bits[x:x+11])), 2) for x in range(0, len(bits), 11)]:
        assert 0 < word_ind < len(words)
        yield words[word_ind]

if __name__ == "__main__":
    num_words = int(sys.argv[1])
    assert num_words in [12, 24]
    SIZE = 256 if num_words == 24 else 128

    lang = sys.argv[2]
    words = load_word_list(lang)

    seed = set_seed()
    print(f"Seed set to {seed}")

    bits = npr.choice([0, 1], size=SIZE).tolist()

    sha_value = bits_sha(bits)
    bits = add_additional_bits(bits, sha_value)

    words = [w for w in gen_words(bits, words)]
    assert len(words) == num_words
    print_words(words)
