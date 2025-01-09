# Define the service URL (change it to your actual service name)
SERVICE_URL="http://client-container-service:8080/start_authentication"

# Number of requests to send
NUM_REQUESTS=5

# Loop to send multiple POST requests to the service
for i in $(seq 1 $NUM_REQUESTS); do
    echo "Sending POST request #$i to $SERVICE_URL"
    curl -X POST $SERVICE_URL
    echo "Request #$i sent"
done
