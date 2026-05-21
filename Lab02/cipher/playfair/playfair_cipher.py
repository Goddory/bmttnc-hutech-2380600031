class PlayfairCipher:
    def __init__(self):
        """Khoi tao Playfair Cipher."""
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    def create_matrix(self, key):
        key = key.upper().replace("J", "I")
        matrix_text = ""

        for char in key + self.alphabet:
            if char.isalpha() and char not in matrix_text:
                matrix_text += char

        return [list(matrix_text[i:i + 5]) for i in range(0, 25, 5)]

    def find_position(self, matrix, char):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col
        return None

    def prepare_plaintext(self, plaintext):
        plaintext = ''.join(char for char in plaintext.upper().replace("J", "I") if char.isalpha())
        prepared_text = ""
        index = 0

        while index < len(plaintext):
            first_char = plaintext[index]
            second_char = plaintext[index + 1] if index + 1 < len(plaintext) else "X"

            if first_char == second_char:
                prepared_text += first_char + "X"
                index += 1
            else:
                prepared_text += first_char + second_char
                index += 2

        if len(prepared_text) % 2 != 0:
            prepared_text += "X"

        return prepared_text

    def prepare_ciphertext(self, ciphertext):
        ciphertext = ''.join(char for char in ciphertext.upper().replace("J", "I") if char.isalpha())
        if len(ciphertext) % 2 != 0:
            ciphertext += "X"
        return ciphertext

    def encrypt(self, plaintext, key):
        matrix = self.create_matrix(key)
        plaintext = self.prepare_plaintext(plaintext)
        encrypted_text = ""

        for index in range(0, len(plaintext), 2):
            first_char = plaintext[index]
            second_char = plaintext[index + 1]
            first_row, first_col = self.find_position(matrix, first_char)
            second_row, second_col = self.find_position(matrix, second_char)

            if first_row == second_row:
                encrypted_text += matrix[first_row][(first_col + 1) % 5]
                encrypted_text += matrix[second_row][(second_col + 1) % 5]
            elif first_col == second_col:
                encrypted_text += matrix[(first_row + 1) % 5][first_col]
                encrypted_text += matrix[(second_row + 1) % 5][second_col]
            else:
                encrypted_text += matrix[first_row][second_col]
                encrypted_text += matrix[second_row][first_col]

        return encrypted_text

    def decrypt(self, ciphertext, key):
        matrix = self.create_matrix(key)
        ciphertext = self.prepare_ciphertext(ciphertext)
        decrypted_text = ""

        for index in range(0, len(ciphertext), 2):
            first_char = ciphertext[index]
            second_char = ciphertext[index + 1]
            first_row, first_col = self.find_position(matrix, first_char)
            second_row, second_col = self.find_position(matrix, second_char)

            if first_row == second_row:
                decrypted_text += matrix[first_row][(first_col - 1) % 5]
                decrypted_text += matrix[second_row][(second_col - 1) % 5]
            elif first_col == second_col:
                decrypted_text += matrix[(first_row - 1) % 5][first_col]
                decrypted_text += matrix[(second_row - 1) % 5][second_col]
            else:
                decrypted_text += matrix[first_row][second_col]
                decrypted_text += matrix[second_row][first_col]

        return decrypted_text
