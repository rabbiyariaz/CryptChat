# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import secrets
import base64

app = Flask(__name__)
CORS(app)

# WARNING: demo storage only. In production use a DB or secure KV store.
latest_key_bits = None

def simulate_bb84(key_length=16, eavesdrop=False):
    """
    Deterministic-ish BB84 simulation for demo purposes.
    Returns sifted bits, QBER (fraction), and final key (bit-string).
    """
    alice_bits = [secrets.randbelow(2) for _ in range(key_length)]
    alice_bases = [secrets.choice(['Z','X']) for _ in range(key_length)]
    bob_bases = [secrets.choice(['Z','X']) for _ in range(key_length)]

    # Eve guesses bases if eavesdrop=True
    eve_bases = [secrets.choice(['Z','X']) for _ in range(key_length)] if eavesdrop else [None]*key_length

    bob_results = []
    # Simulate transmission / measurement
    for i in range(key_length):
        a_bit = alice_bits[i]
        a_basis = alice_bases[i]
        b_basis = bob_bases[i]

        if not eavesdrop:
            # If bases match -> Bob sees same bit; else random
            if a_basis == b_basis:
                bob_results.append(a_bit)
            else:
                bob_results.append(secrets.randbelow(2))
        else:
            # Eve intercept-resend
            e_basis = eve_bases[i]
            # Eve measures: if she guessed correct basis she learns a_bit, else random
            if e_basis == a_basis:
                eve_meas = a_bit
            else:
                eve_meas = secrets.randbelow(2)
            # Eve re-encodes eve_meas and sends to Bob
            if e_basis == b_basis:
                # if Eve's basis equals Bob's basis, Bob measures eve_meas correctly
                bob_results.append(eve_meas)
            else:
                # otherwise Bob sees random result
                bob_results.append(secrets.randbelow(2))

    # Sifting: keep indices where alice_bases == bob_bases
    sifted_indices = [i for i in range(key_length) if alice_bases[i] == bob_bases[i]]
    alice_sifted = [alice_bits[i] for i in sifted_indices]
    bob_sifted = [bob_results[i] for i in sifted_indices]

    # Compute QBER: fraction of differing bits in sifted key
    if len(alice_sifted) == 0:
        qber = 0.0
    else:
        diff = sum(1 for a,b in zip(alice_sifted, bob_sifted) if a != b)
        qber = diff / len(alice_sifted)

    # For demo, use the first N bits of sifted as final key. N = min(32, len(sifted))
    final_key_len = min(32, len(alice_sifted))
    final_key_bits = alice_sifted[:final_key_len]
    final_key_str = ''.join(str(b) for b in final_key_bits)
    # integer and hex representation
    if final_key_str == "":
        key_int = 0
        key_hex = ""
    else:
        key_int = int(final_key_str, 2)
        key_hex = hex(key_int)[2:]

    return {
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "sifted_key_bits": alice_sifted,
        "sifted_length": len(alice_sifted),
        "qber": qber,  # fraction 0.0 - 1.0
        "eavesdrop_detected": eavesdrop and (qber > 0.1),  # demo threshold 10%
        "final_key_bits": final_key_str,
        "final_key_int": key_int,
        "final_key_hex": key_hex
    }

@app.route('/generate_key', methods=['POST'])
def generate_key():
    global latest_key_bits
    data = request.get_json() or {}
    eavesdrop = bool(data.get('eavesdrop', False))
    key_length = int(data.get('key_length', 16))
    # clamp key_length
    key_length = max(8, min(1024, key_length))

    res = simulate_bb84(key_length=key_length, eavesdrop=eavesdrop)
    latest_key_bits = res['final_key_bits']  # store bit-string (demo only)
    return jsonify(res)

@app.route('/get_key', methods=['GET'])
def get_key():
    global latest_key_bits
    if latest_key_bits:
        return jsonify({
            "final_key_bits": latest_key_bits,
            "final_key_hex": hex(int(latest_key_bits,2))[2:] if latest_key_bits!="" else "",
        })
    return jsonify({"error":"No key generated yet"}), 400

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """
    Expects JSON:
    { "message": "<utf8 string>", "key_bits": "101010..." }
    Returns base64 ciphertext.
    """
    payload = request.get_json() or {}
    message = payload.get("message", "")
    key_bits = payload.get("key_bits", "")
    if key_bits == "" or len(key_bits) == 0:
        return jsonify({"error":"Key not provided"}), 400

    # convert key_bits -> bytes
    nbytes = (len(key_bits) + 7) // 8
    key_int = int(key_bits, 2) if key_bits!="" else 0
    key_bytes = key_int.to_bytes(nbytes, 'big')

    msg_bytes = message.encode('utf-8')
    cipher = bytes([msg_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(msg_bytes))])
    return jsonify({"cipher_b64": base64.b64encode(cipher).decode()})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    payload = request.get_json() or {}
    cipher_b64 = payload.get("cipher_b64", "")
    key_bits = payload.get("key_bits", "")
    if key_bits == "" or len(key_bits) == 0:
        return jsonify({"error":"Key not provided"}), 400
    try:
        cipher = base64.b64decode(cipher_b64)
    except Exception as e:
        return jsonify({"error":"Invalid base64 cipher"}), 400

    nbytes = (len(key_bits) + 7) // 8
    key_int = int(key_bits, 2) if key_bits!="" else 0
    key_bytes = key_int.to_bytes(nbytes, 'big')

    plain = bytes([cipher[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(cipher))])
    try:
        text = plain.decode('utf-8')
    except:
        text = plain.decode('utf-8', errors='replace')
    return jsonify({"plaintext": text})

@app.route('/')
def home():
    return "QryptChat Quantum Backend Server is Running!"

if __name__ == '__main__':
    # Bind to 0.0.0.0 for external testing (ngrok/Railway). For local-only use 127.0.0.1
    app.run(host='0.0.0.0', port=8000, debug=True)
