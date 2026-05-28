class RailFenceCipher:
    def __init__(self):
        """Khởi tạo Rail Fence Cipher."""
        pass

    def rail_fence_encrypt(self, plaintext, num_rails):
        """Mã hóa text bằng Rail Fence Cipher (Zigzag Cipher).
        Tác dụng: Sắp xếp ký tự theo hình zigzag với số dòng (rails) cho trước,
        sau đó đọc theo từng dòng để tạo ciphertext.
        Ví dụ: plaintext='HELLO', num_rails=2 sẽ tạo:
          H L O (dòng 1)
          E L   (dòng 2)
          Kết quả: 'HLOEL'
        Tham số: plaintext (văn bản gốc), num_rails (số dòng)
        Trả về: Chuỗi đã mã hóa
        """
        rails = ['' for _ in range(num_rails)]
        rail_index = 0
        direction = 1

        for char in plaintext:
            rails[rail_index] += char
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        cipher_text = ''.join(''.join(rails) for rails in rails)
        return cipher_text
    
    def rail_fence_decrypt(self, cipher_text, num_rails):
        """Giải mã text bằng Rail Fence Cipher.
        Tác dụng: Đảo ngược quá trình mã hóa bằng cách:
        1. Tính độ dài từng dòng dựa trên hình zigzag
        2. Chia ciphertext thành các phần tương ứng với mỗi dòng
        3. Đọc theo thứ tự zigzag để khôi phục plaintext gốc
        Tham số: cipher_text (văn bản đã mã hóa), num_rails (số dòng)
        Trả về: Chuỗi gốc đã được giải mã
        """
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start + length])
            start += length

        
        plaintext = ''
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            plaintext += rails[rail_index][0]
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plaintext