import base64


def main():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            encoded_string = file.read().strip()

        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")

        print("Chuoi sau khi giai ma:", decoded_string)
    except Exception as exc:
        print("Loi:", exc)


if __name__ == "__main__":
    main()
