from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
app = Flask(__name__)

caesar_cipher = CaesarCipher()
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)