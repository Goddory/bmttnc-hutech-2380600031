from flask import Flask, request, jsonify, render_template
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayfairCipher
from cipher.transposition import TranspositionCipher
app = Flask(__name__)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayfairCipher()
transposition_cipher = TranspositionCipher()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/caesar', methods=['GET', 'POST'])
def caesar():
    result = ''
    text = ''
    key = ''
    action = 'encrypt'

    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        action = request.form.get('action', 'encrypt')

        if text and key:
            if action == 'decrypt':
                result = caesar_cipher.decrypt_text(text, key)
            else:
                result = caesar_cipher.encrypt_text(text, key)

    return render_template('index.html', result=result, text=text, key=key, action=action)

@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    """Mã hóa text bằng Caesar Cipher - nhận text và key từ JSON POST request,
    trả về encrypted_text. Yêu cầu cả text và key, nếu thiếu trả về lỗi 400."""
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    """Giải mã text bằng Caesar Cipher - nhận encrypted text và key từ JSON POST request,
    trả về decrypted_text bằng cách dịch ngược key lần."""
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    """Mã hóa text bằng Vigenere Cipher - nhận text và key từ JSON POST request,
    sử dụng key lặp lại để mã hóa từng ký tự chữ cái."""
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = vigenere_cipher.vigenere_encrypt(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    """Giải mã text bằng Vigenere Cipher - nhận encrypted text và key từ JSON POST request,
    dịch ngược quá trình mã hóa bằng cách trừ key shift."""
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = vigenere_cipher.vigenere_decrypt(text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = railfence_cipher.encrypt(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = railfence_cipher.decrypt(text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = playfair_cipher.encrypt(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = playfair_cipher.decrypt(text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/playfair/create-matrix', methods=['POST'])
def playfair_create_matrix():
    data = request.get_json()
    key = data.get('key')
    if key is None:
        return jsonify({'error': 'Missing key'}), 400
    matrix = playfair_cipher.create_matrix(key)
    return jsonify({'matrix': matrix})

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    encrypted_text = transposition_cipher.encrypt(text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    if text is None or key is None:
        return jsonify({'error': 'Missing text or key'}), 400
    decrypted_text = transposition_cipher.decrypt(text, key)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
