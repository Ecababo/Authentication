# Kubernetes Authentication

This repository is part of a personal project to learn the basics of Kubernetes and Docker in a CI/CD environment. It simulates a RADIUS-like service that validates usernames and passwords, returning appropriate HTTP responses. The project provides a hands-on exploration of container orchestration and service interaction within a Kubernetes cluster.

## Overview
### Key Components
#### Python Scripts:
- RADIUS Service Simulation: A Python script that acts as a RADIUS-like service. It validates username and password payloads, returning appropriate HTTP status codes based on the authentication result.
- Client Simulation: A Python script that simulates a client attempting to connect to the RADIUS service using random username-password combinations.
#### Docker
- Docker Integration: Each Python script is containerized using Docker, forming the basis for two separate Docker images.
#### Kubernetes
- Kubernetes Deployment: A Kubernetes pod hosts the RADIUS service. Multiple client pods are created to simulate concurrent user authentication attempts.
#### CI/CD
- Skaffold is used to dynamically build and deploy the project if changes occur in the sourcefile

## How it works
- The Client Pod interacts with the RADIUS Service Pod by sending POST requests containing username-password pairs.
Authentication attempts are triggered via a curl command:
```
curl -X POST http://$pod_ip:8080/start_authentication
```
Upon receiving the request, the client begins a loop, attempting to authenticate every 2 seconds using random credentials from a predefined source file. 

## Next steps
### Planned Enhancements
- **Error Handling**:
Improve logging and exception management for edge cases, such as service unavailability or malformed requests.

- **Metrics and Monitoring**:
Integrate tools like Prometheus and Grafana to monitor authentication success rates and system performance.

- **Database Integration**:
Replace the static credential source file with a database-backed solution for dynamic user management.

- **Scalability**:
Implement a dynamic scaling for the Kubernetes deployment. Users should pop in and try to authenticate, be shutdown when the connection succeeds or a maximum amount of failed attempts is reached.
