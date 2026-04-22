import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request
import requests
from utils.hash_utils import hash_password

app = Flask(__name__)

MASTER_URL = "http://100.83.227.108:5000"
STOP = False

@app.route('/task', methods=['POST'])
def receive_task():
    global STOP
    STOP = False

    data = request.json
    passwords = data['passwords']
    target_hash = data['hash']

    print(f"[WORKER] Received {len(passwords)} tasks")

    for pwd in passwords:
        if STOP:
            print("[WORKER] Stopped")
            break

        if hash_password(pwd) == target_hash:
            print(f"[FOUND] {pwd}")
            requests.post(f"{MASTER_URL}/result", json={"password": pwd})
            break

    return {"status": "done"}

@app.route('/stop', methods=['POST'])
def stop():
    global STOP
    STOP = True
    return {"status": "stopping"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)