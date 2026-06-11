import sys

from PIL import Image


END_MARKER = "1111111111111110"


def encode_image(image_path, message):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    binary_message = "".join(format(ord(char), "08b") for char in message) + END_MARKER
    capacity = width * height * 3
    if len(binary_message) > capacity:
        raise ValueError("Thong diep qua dai, anh khong du suc chua.")

    data_index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3):
                if data_index >= len(binary_message):
                    break

                pixel[color_channel] = (pixel[color_channel] & 0xFE) | int(binary_message[data_index])
                data_index += 1

            img.putpixel((col, row), tuple(pixel))

            if data_index >= len(binary_message):
                encoded_image_path = "encoded_image.png"
                img.save(encoded_image_path)
                print("Steganography complete. Encoded image saved as", encoded_image_path)
                return


def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)


if __name__ == "__main__":
    main()
