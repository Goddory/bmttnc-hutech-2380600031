from cipher.caesar import ALPHABET
class CaesarCipher:
    def __init__(self):
        """Khởi tạo Caesar Cipher với bộ chữ cái từ alphabet module."""
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        """Mã hóa text bằng Caesar Cipher.
        Tác dụng: Chuyển đổi mỗi ký tự bằng cách dịch nó đi key vị trí trong bộ chữ cái.
        Ví dụ: Với key=3, A->D, B->E, Z->C (quay vòng)
        Tham số: text (văn bản cần mã hóa), key (số vị trí dịch)
        Trả về: Chuỗi ký tự đã mã hóa (chỉ chứa ký tự trong bộ chữ cái)
        """
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index + key) % alphabet_len
            encrypted_text.append(output_index)
            return ''.join(encrypted_text)
        
    def decrypt_text(self, text: str, key: int) -> str:
        """Giải mã text bằng Caesar Cipher.
        Tác dụng: Đảo ngược quá trình mã hóa bằng cách dịch mỗi ký tự ngược lại key vị trí.
        Tham số: text (văn bản đã mã hóa), key (số vị trí dịch ban đầu)
        Trả về: Chuỗi ký tự gốc đã được giải mã
        """
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index - key) % alphabet_len
            decrypted_text.append(output_index)
        return ''.join(decrypted_text)