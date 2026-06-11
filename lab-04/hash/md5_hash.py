import math


SHIFT_AMOUNTS = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
]

TABLE_CONSTANTS = [
    int(abs(math.sin(index + 1)) * (2**32)) & 0xFFFFFFFF
    for index in range(64)
]


def left_rotate(value, shift):
    value &= 0xFFFFFFFF
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def md5(message: bytes):
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    original_bit_length = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    padded = bytearray(message)
    padded.append(0x80)

    while len(padded) % 64 != 56:
        padded.append(0)

    padded.extend(original_bit_length.to_bytes(8, "little"))

    for offset in range(0, len(padded), 64):
        chunk = padded[offset : offset + 64]
        words = [
            int.from_bytes(chunk[index : index + 4], "little")
            for index in range(0, 64, 4)
        ]

        a, b, c, d = a0, b0, c0, d0

        for index in range(64):
            if index < 16:
                f = (b & c) | (~b & d)
                g = index
            elif index < 32:
                f = (d & b) | (~d & c)
                g = (5 * index + 1) % 16
            elif index < 48:
                f = b ^ c ^ d
                g = (3 * index + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * index) % 16

            f &= 0xFFFFFFFF
            temp = d
            d = c
            c = b
            b = (b + left_rotate(a + f + TABLE_CONSTANTS[index] + words[g], SHIFT_AMOUNTS[index])) & 0xFFFFFFFF
            a = temp

        a0 = (a0 + a) & 0xFFFFFFFF
        b0 = (b0 + b) & 0xFFFFFFFF
        c0 = (c0 + c) & 0xFFFFFFFF
        d0 = (d0 + d) & 0xFFFFFFFF

    digest = (
        a0.to_bytes(4, "little")
        + b0.to_bytes(4, "little")
        + c0.to_bytes(4, "little")
        + d0.to_bytes(4, "little")
    )
    return digest.hex()


def main():
    input_string = input("Nhap chuoi can bam: ")
    digest = md5(input_string.encode("utf-8"))
    print("Ma bam MD5 cua chuoi '{}' la: {}".format(input_string, digest))


if __name__ == "__main__":
    main()
