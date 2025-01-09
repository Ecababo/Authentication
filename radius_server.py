from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open('user_password_pairs.json') as f:
    data = json.load(f)
valid_users = data["valid_users"]

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in valid_users and valid_users[username] == password:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
