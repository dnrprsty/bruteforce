from flask import Flask, request
import requests
from utils.generator import generate_range
from utils.hash_utils import hash_password

app = Flask(__name__)

WORKER_URL = "http://127.0.0.1:5001"

found = False

@app.route('/start', methods=['POST'])
def start_task():
    global found
    
    data = request.json
    password = data['password']
    charset = data['charset']
    length = data['length']

    target_hash = hash_password(password)

    print(f"[MASTER] Target hash: {target_hash}")

    combinations = generate_range(charset, length)

    # ambil sebagian kecil dulu (demo)
    start = combinations[0]
    end = combinations[len(combinations)//2]

    print(f"[MASTER] Sending task: {start} -> {end}")

    requests.post(f"{WORKER_URL}/task", json={
        "start": start,
        "end": end,
        "hash": target_hash,
        "charset": charset,
        "length": length
    })

    return {"status": "task sent"}

@app.route('/result', methods=['POST'])
def receive_result():
    global found
    
    if not found:
        data = request.json
        print(f"[MASTER] PASSWORD FOUND: {data['password']}")
        found = True

    return {"status": "received"}

if __name__ == '__main__':
    app.run(port=5000)