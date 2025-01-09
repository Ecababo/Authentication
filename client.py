from flask import Flask
import requests
import random
import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
import os
# Configuration (move these to a separate config file for better maintainability)
AUTH_URL = "http://radius-server:5001/authenticate"
FAILURE_RATE = 0.2
AUTHENTICATION_INTERVAL = 2  # Seconds
MAX_EXECUTIONS = 100  # Limit the number of executions

# Global state variable (using a file-based flag)
START_FLAG_PATH = "./client.py"

# Global counter for executions
execution_count = 0

def load_user_credentials():
    with open('user_password_pairs.json') as f:
        data = json.load(f)
    return data["valid_users"]

def perform_authentication():
    global execution_count
    username = random.choice(list(user_credentials.keys()))
    password = user_credentials[username]

    if random.random() < FAILURE_RATE:
        password = "invalid"

    try:
        response = requests.post(AUTH_URL, json={'username': username, 'password': password})
        status = "success" if response.status_code == 200 else "failure"
    except requests.exceptions.RequestException as e:
        status = "error"

    with open('auth_log.txt', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] Username: {username}, Password: {password}, Status: {status}\n") 

    print(f"Authentication for {username}: {status}")
    
    # Increment the execution count
    execution_count += 1

    # Stop the scheduler if we've reached the max executions
    if execution_count >= MAX_EXECUTIONS:
        print("Max executions reached. Stopping the scheduler.")
        scheduler.shutdown()

def should_start_authentication():
    return os.path.exists(START_FLAG_PATH)

def start_authentication_loop():
    if not should_start_authentication():
        return "Authentication loop already stopped", 409
    try:
        os.remove('auth_log.txt')  # Remove old logging file if it exists
    except FileNotFoundError:
        pass
    try:
        if scheduler.running:
            scheduler.shutdown()  # stop the scheduler if already running
    except Exception as e:
        print(f"Error shutting down scheduler: {e}") 

    scheduler.start()
    return "Authentication loop started", 200

def stop_authentication_loop():
    if not scheduler.running:
        return "Authentication loop already stopped", 409

    scheduler.shutdown()
    os.remove(START_FLAG_PATH)  # Remove the flag file
    return "Authentication loop stopped", 200

# Initialize user credentials
user_credentials = load_user_credentials()

# Initialize scheduler
scheduler = BackgroundScheduler()

# Schedule the authentication task
scheduler.add_job(perform_authentication, 'interval', seconds=AUTHENTICATION_INTERVAL)

# Flask app setup
app = Flask(__name__)

@app.route('/authenticate', methods=['GET'])
def authenticate():
    perform_authentication()
    return "OK"

@app.route('/start_authentication', methods=['POST'])
def start_loop():
    return start_authentication_loop()

@app.route('/stop_authentication', methods=['POST'])
def stop_loop():
    return stop_authentication_loop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
