import hashlib


def calculate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode("utf-8"))
    return md5_hash.hexdigest()


def main():
    input_string = input("Nhap chuoi can bam: ")
    digest = calculate_md5(input_string)
    print("Ma bam MD5 cua chuoi '{}' la: {}".format(input_string, digest))


if __name__ == "__main__":
    main()
