
# QryptChat: Quantum Key Distribution Simulator

QryptChat is an educational application that demonstrates the principles of Quantum Key Distribution (QKD), specifically the BB84 protocol. It simulates how two parties can generate a shared secret key using quantum mechanics, with security that guarantees detection of any eavesdropping attempt.


## ✨ Features

-   **BB84 Protocol Simulation:** Visually demonstrates the entire quantum key exchange process.
-   **Eavesdropper Detection:** Toggle an "Eavesdropper" to see how the Quantum Bit Error Rate (QBER) reveals their presence.
-   **Interactive Encryption:** Use the generated quantum key to encrypt and decrypt messages in a simulated chat interface.
-   **Educational Focus:** Designed to make complex quantum cryptography concepts accessible and understandable.

## 🛠️ Installation & How to Run

### Prerequisites

-   **Python 3.8+**
-   **pip** (Python package manager)
-   A free account on [Railway](https://railway.app/) (for deployment) or ngrok (for tunneling).

### 1. Running the Backend Locally

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd qryptchat-backend

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the Flask server
python app.py
```

The backend API will be running at `http://127.0.0.1:8000`.

**To deploy the backend online (recommended):**
1.  Push your code to GitHub.
2.  Connect your repository to [Railway](https://railway.app/).
3.  Railway will automatically deploy it and provide you with a public URL (e.g., `https://your-app-name.railway.app`).

### 2. Running the Frontend (FlutterFlow)

The frontend is built using FlutterFlow.
1.  The live web version is automatically hosted by FlutterFlow.
2.  To view the project structure, you can [request access via FlutterFlow](https://flutterflow.io/).

## 📦 Dependencies

### Backend (Python - `requirements.txt`)
```
Flask==2.3.3
flask-cors==4.0.0
qiskit==0.44.0
```
*   **Flask:** The web framework used to create the REST API.
*   **Flask-CORS:** Essential for allowing the FlutterFlow web app to communicate with the backend.
*   **Qiskit:** The open-source quantum computing framework from IBM, used to simulate the quantum aspects of the BB84 protocol.

### Frontend (FlutterFlow)
*   **HTTP Client:** For making API calls to the backend.
*   **Custom Dart Functions:** For local XOR encryption/decryption logic.

## ⚛️ Clear Explanation of the Quantum Aspect

### The Core Principle: BB84 Protocol

QryptChat simulates the **BB84 protocol**, the first and most famous Quantum Key Distribution (QKD) scheme. Its security is based on the fundamental principles of quantum mechanics:

1.  **Superposition:** Alice (the sender) encodes each bit of her key into a quantum bit (qubit). She randomly chooses one of two bases (e.g., Rectilinear '+' or Diagonal '×') to prepare each qubit in a superposition state.
2.  **Measurement:** Bob (the receiver) independently and randomly chooses a basis to measure each qubit he receives. **Only if Bob's measurement basis matches Alice's preparation basis will he measure the correct bit value.**
3.  **Sifting:** Alice and Bob publicly compare their choice of bases (but not their bit values). They discard all bits where their bases did not match. The remaining bits form their "sifted key."
4.  **Eavesdropping Detection (The Quantum Advantage):** This is the most important part. Any attempt by an eavesdropper (Eve) to intercept and measure the qubits **disturbs their quantum state** due to the **No-Cloning Theorem**. This disturbance introduces errors into the key.
5.  **Quantum Bit Error Rate (QBER):** Alice and Bob calculate the error rate in their sifted key by comparing a subset of bits. A **high QBER indicates with certainty that Eve was listening**, and the key is discarded. A low QBER confirms the channel was secure.

### What QryptChat Simulates

This app provides a classical simulation of this quantum process. It demonstrates:
-   The random generation of bits and bases for Alice and Bob.
-   The sifting process to create a shared key.
-   The calculation of the QBER and the clear detection of an eavesdropper.
-   The use of the resulting key for encryption, which fails if the key was compromised.

This simulation makes the abstract concept of "unhackable" quantum communication tangible.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
