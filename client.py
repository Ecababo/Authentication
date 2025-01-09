from flask import Flask
import requests
import random
import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
import os
import threading

# Configuration
AUTH_URL = "http://radius-server-service:5001/authenticate"
FAILURE_RATE = 0.8
AUTHENTICATION_INTERVAL = 2  # Seconds
MAX_EXECUTIONS = 10  # Limit the number of executions

# Global state variables
execution_count = 0
authentication_successful = False

# Load user credentials
def load_user_credentials():
    with open('user_password_pairs.json') as f:
        data = json.load(f)
    return data["valid_users"]

# Perform authentication
def perform_authentication():
    global execution_count, authentication_successful
    if execution_count >= MAX_EXECUTIONS or authentication_successful:
        print("Stopping authentication attempts.")
        # Call shutdown asynchronously
        threading.Thread(target=scheduler.shutdown, args=(False,)).start()
        return

    username = random.choice(list(user_credentials.keys()))
    password = user_credentials[username]

    if random.random() < FAILURE_RATE:
        password = "invalid"

    try:
        response = requests.post(AUTH_URL, json={'username': username, 'password': password})
        if response.status_code == 200:
            status = "success"
            authentication_successful = True
            print(f"Authentication succeeded for {username}.")
        else:
            status = "failure"
    except requests.exceptions.RequestException as e:
        status = "error"

    # Log the result
    with open('auth_log.txt', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] Username: {username}, Password: {password}, Status: {status}\n")

    print(f"Authentication for {username}: {status}")

    # Increment the execution count
    execution_count += 1

    # Stop the scheduler if we've reached the max executions
    if execution_count >= MAX_EXECUTIONS:
        print("Max executions reached. Stopping the scheduler.")
        # Call shutdown asynchronously
        threading.Thread(target=scheduler.shutdown, args=(False,)).start()

# Start the authentication loop
def start_authentication_loop():
    global execution_count, authentication_successful
    execution_count = 0
    authentication_successful = False

    try:
        os.remove('auth_log.txt')  # Remove old logging file if it exists
    except FileNotFoundError:
        pass

    # Start the scheduler only if it is not already running
    if not scheduler.running:
        scheduler.start()
        return "Authentication loop started", 200
    else:
        return "Authentication loop already running", 409

# Stop the authentication loop
def stop_authentication_loop():
    if scheduler.running:
        # Shutdown asynchronously using threading to avoid blocking the main thread
        threading.Thread(target=scheduler.shutdown, args=(False,)).start()
        return "Authentication loop stopped", 200
    else:
        return "Authentication loop already stopped", 409

# Initialize user credentials
user_credentials = load_user_credentials()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(perform_authentication, 'interval', seconds=AUTHENTICATION_INTERVAL)

# Flask app setup
app = Flask(__name__)

@app.route('/start_authentication', methods=['POST'])
def start_loop():
    return start_authentication_loop()

@app.route('/stop_authentication', methods=['POST'])
def stop_loop():
    return stop_authentication_loop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
