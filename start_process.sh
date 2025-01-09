#!/bin/bash

pod_ips=$(kubectl get pods -l app=client-container -o jsonpath={.items[*].status.podIP} | tr ' ' '\n')

# Loop through each IP and send a POST request to it
for pod_ips in $pod_ips; do
    echo "Sending POST request to $pod_ips:8080/start_authentication"
    curl -X POST "http://$pod_ips:8080/start_authentication"
    echo "Request sent to $pod_ips"
done
