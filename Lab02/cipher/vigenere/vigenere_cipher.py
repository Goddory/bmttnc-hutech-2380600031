class VigenereCipher:
    def __init__(self):
        """Khởi tạo Vigenere Cipher."""
        pass

    def vigenere_encrypt(self, plaintext, key):
        """Mã hóa text bằng Vigenere Cipher.
        Tác dụng: Sử dụng key (khóa) lặp lại để mã hóa từng ký tự chữ cái.
        Mỗi ký tự bị dịch bởi một giá trị tương ứng với ký tự trong key.
        Ví dụ: plaintext='HELLO', key='KEY' sẽ dịch:
          H (+K=10) -> R, E (+E=4) -> I, L (+Y=24) -> J, L (+K=10) -> V, O (+E=4) -> S
        Các ký tự không phải chữ cái giữ nguyên.
        Tham số: plaintext (văn bản gốc), key (khóa mã hóa)
        Trả về: Chuỗi đã mã hóa
        """
        encrypted_text = ""
        key_index = 0
        for char in plaintext:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, ciphertext, key):
        """Giải mã text bằng Vigenere Cipher.
        Tác dụng: Đảo ngược quá trình mã hóa bằng cách trừ (thay vì cộng) key shift.
        Mỗi ký tự bị dịch ngược lại bởi một giá trị tương ứng với ký tự trong key.
        Các ký tự không phải chữ cái giữ nguyên.
        Tham số: ciphertext (văn bản đã mã hóa), key (khóa mã hóa - phải giống khi mã hóa)
        Trả về: Chuỗi gốc đã được giải mã
        """
        decrypted_text = ""
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text
