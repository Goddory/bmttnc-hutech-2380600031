import sys

from PIL import Image


END_MARKER = "1111111111111110"


def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path).convert("RGB")
    width, height = img.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], "08b")[-1]
                if binary_message.endswith(END_MARKER):
                    useful_bits = binary_message[: -len(END_MARKER)]
                    return bits_to_text(useful_bits)

    return bits_to_text(binary_message)


def bits_to_text(binary_message):
    message = ""
    for index in range(0, len(binary_message), 8):
        byte = binary_message[index : index + 8]
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))
    return message


def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)


if __name__ == "__main__":
    main()
