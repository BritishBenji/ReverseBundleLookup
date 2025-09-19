# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# This layer will be cached, speeding up rebuilds if requirements.txt doesn't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
# This will copy your app.py, fileManager.py, templates/, etc.
COPY . .

# Expose the port the app will run on
EXPOSE 5003

# Command to run the application using Waitress
# This is the correct way to run a production server.
CMD ["waitress-serve", "--listen=0.0.0.0:5003", "app:app"]