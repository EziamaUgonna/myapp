# myapp
Building of application 
1. Clone the code from the GitHub repository to your local machine:
git clone https://github.com/EziamaUgonna/myapp.git
2. Install the required dependencies listed in the requirements.txt file:

pip install -r requirements.txt

3. Build and run the Docker container using the Dockerfile:

docker build -t my-app.
docker run -p 8080:8080 my-app

4. Verify that the application is running by visiting http://localhost:8080 in a web browser or using the curl command:

curl http://localhost:8080
This file contains the definition for the Kubernetes deployment resource, including the container image, port configuration, and environment variable for the MongoDB URI.

To deploy the application using Helm, you would run the following commands:
# Add the Helm chart repository
$ helm repo add myapp-chart https://github.com/EziamaUgonna/myapp.git

# Update the local Helm chart repository cache
$ helm repo update

# Install the application using the Helm chart
$ helm install myapp myapp-chart
This will deploy the FastAPI application and create a Kubernetes deployment, service, and pod based on the configuration in the Helm chart's values.yaml and deployment.yaml files.

Note: The instructions provided assume that you have Docker and Helm installed on your local machine.
