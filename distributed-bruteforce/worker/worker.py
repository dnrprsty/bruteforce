from flask import Flask, request
import requests
from utils.generator import generate_range
from utils.hash_utils import hash_password

app = Flask(__name__)

MASTER_URL = "http://127.0.0.1:5000"

@app.route('/task', methods=['POST'])
def receive_task():
    data = request.json
    
    start = data['start']
    end = data['end']
    target_hash = data['hash']
    charset = data['charset']
    length = data['length']

    print(f"[WORKER] Task received: {start} -> {end}")

    combinations = generate_range(charset, length, start, end)

    for password in combinations:
        hashed = hash_password(password)
        
        if hashed == target_hash:
            print(f"[FOUND] Password: {password}")
            
            requests.post(f"{MASTER_URL}/result", json={
                "password": password
            })
            return {"status": "found"}

    return {"status": "not found"}

if __name__ == '__main__':
    app.run(port=5001)