# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire application's code
COPY . .

# Install dependencies
RUN pip install .

# Set the entrypoint
ENTRYPOINT ["adk", "web", "--host=0.0.0.0", "--port=10000", "--session_service_uri=sqlite:///session.db"]
