# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code into the container
COPY main.py .
COPY config.py .
COPY instance ./instance
COPY static ./static
COPY templates ./templates

# Expose the port your Flask app is running on (default is 5000)
EXPOSE 5000

# Set environment variables, if required
ENV FLASK_APP=main.py

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
