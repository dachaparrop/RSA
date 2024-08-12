# randomart.py

import hashlib
import os

def generate_empty_randomart():
    """
    Generate an empty randomart template using a loop.
    """
    
    randomart_template = [
        "+-----------------+",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "+-----------------+",
    ]

    empty_randomart = ""
    for line in randomart_template:
        empty_randomart += line + "\n"

    return empty_randomart.strip()

def generate_randomart(number):
    number_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')
    hash_bytes = hashlib.sha256(number_bytes).digest()

    randomart_template = [
        "+-----------------+",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "|                 |",
        "+-----------------+",
    ]

    x, y = 8, 4
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    for byte in hash_bytes:
        direction = byte % 8
        x += moves[direction][0]
        y += moves[direction][1]
        x = max(1, min(x, 17))
        y = max(1, min(y, 9))
        randomart_template[y] = randomart_template[y][:x] + '*' + randomart_template[y][x+1:]

    randomart_template[4] = randomart_template[4][:8] + 'S' + randomart_template[4][9:]
    randomart_template[4] = randomart_template[4][:8] + 'E' + randomart_template[4][9:]

    return "\n".join(randomart_template)

def read_number_from_file(file_path):
    with open(file_path, 'r') as file:
        hex_number = file.read().strip().replace('\n', '')
        return int(hex_number, 16)

def generate_randomart_from_public_key():
    file_path = os.path.join(os.getcwd(), "public_key.txt")
    large_number = read_number_from_file(file_path)
    return generate_randomart(large_number)