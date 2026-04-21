import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request
import requests
from utils.generator import generate_all, split_list
from utils.hash_utils import hash_password

app = Flask(__name__)

# GANTI DENGAN IP TAILSCALE NANTI
WORKERS = [
    "http://127.0.0.1:5001",
    # tambah worker di sini
    # "http://127.0.0.1:5002",
    # "http://127.0.0.1:5003"
]

found = False

@app.route('/start', methods=['POST'])
def start():
    global found
    found = False

    data = request.json
    password = data['password']
    charset = data['charset']
    length = data['length']

    target_hash = hash_password(password)

    print(f"[MASTER] Target hash: {target_hash}")

    all_passwords = generate_all(charset, length)
    chunks = split_list(all_passwords, len(WORKERS))

    for i, worker in enumerate(WORKERS):
        print(f"[MASTER] Sending {len(chunks[i])} tasks to {worker}")

        try:
            requests.post(f"{worker}/task", json={
                "passwords": chunks[i],
                "hash": target_hash
            })
        except:
            print(f"[ERROR] Worker {worker} not reachable")

    return {"status": "distributed"}

@app.route('/result', methods=['POST'])
def result():
    global found

    if not found:
        data = request.json
        found = True

        print(f"[MASTER] PASSWORD FOUND: {data['password']}")

        for worker in WORKERS:
            try:
                requests.post(f"{worker}/stop")
            except:
                pass

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)