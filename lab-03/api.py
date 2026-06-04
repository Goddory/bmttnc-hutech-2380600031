from flask import Flask, jsonify, request

from cipher.ecc import ECCCipher
from cipher.rsa import RSACipher


app = Flask(__name__)
rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()


@app.route("/api/rsa/generate_keys", methods=["GET"])
def generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({"message": "Keys generated successfully"})


@app.route("/api/rsa/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    key_type = data.get("key_type", "public")

    if not message:
        return jsonify({"error": "Missing message"}), 400

    private_key, public_key = rsa_cipher.load_keys()
    key = public_key if key_type == "public" else private_key
    encrypted_bytes = rsa_cipher.encrypt(message, key)
    return jsonify({"encrypted_message": encrypted_bytes.hex()})


@app.route("/api/rsa/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json(silent=True) or {}
    ciphertext_hex = data.get("ciphertext", "")
    key_type = data.get("key_type", "private")

    if not ciphertext_hex:
        return jsonify({"error": "Missing ciphertext"}), 400

    if key_type != "private":
        return jsonify({"error": "Decrypt requires a private key"}), 400

    try:
        private_key, _ = rsa_cipher.load_keys()
        plaintext = rsa_cipher.decrypt(bytes.fromhex(ciphertext_hex), private_key)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"decrypted_message": plaintext})


@app.route("/api/rsa/sign", methods=["POST"])
def sign_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Missing message"}), 400

    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({"signature": signature.hex()})


@app.route("/api/rsa/verify", methods=["POST"])
def verify_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    signature_hex = data.get("signature", "")

    if not message or not signature_hex:
        return jsonify({"error": "Missing message or signature"}), 400

    try:
        _, public_key = rsa_cipher.load_keys()
        is_verified = rsa_cipher.verify(message, bytes.fromhex(signature_hex), public_key)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"is_verified": is_verified})


@app.route("/api/ecc/generate_keys", methods=["GET"])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({"message": "Keys generated successfully"})


@app.route("/api/ecc/sign", methods=["POST"])
def ecc_sign_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Missing message"}), 400

    signing_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, signing_key)
    return jsonify({"signature": signature.hex()})


@app.route("/api/ecc/verify", methods=["POST"])
def ecc_verify_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    signature_hex = data.get("signature", "")

    if not message or not signature_hex:
        return jsonify({"error": "Missing message or signature"}), 400

    try:
        _, verifying_key = ecc_cipher.load_keys()
        is_verified = ecc_cipher.verify(message, bytes.fromhex(signature_hex), verifying_key)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"is_verified": is_verified})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
