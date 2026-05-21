import math


class TranspositionCipher:
    def __init__(self):
        """Khoi tao Transposition Cipher."""
        pass

    def encrypt(self, plaintext, key):
        key = int(key)
        ciphertext = [""] * key

        for col in range(key):
            current_index = col
            while current_index < len(plaintext):
                ciphertext[col] += plaintext[current_index]
                current_index += key

        return ''.join(ciphertext)

    def decrypt(self, ciphertext, key):
        key = int(key)
        num_cols = math.ceil(len(ciphertext) / key)
        num_rows = key
        num_empty_boxes = (num_cols * num_rows) - len(ciphertext)
        plaintext = [""] * num_cols
        col = 0
        row = 0

        for char in ciphertext:
            plaintext[col] += char
            col += 1

            if col == num_cols or (col == num_cols - 1 and row >= num_rows - num_empty_boxes):
                col = 0
                row += 1

        return ''.join(plaintext)
