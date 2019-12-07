# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /data_service

# Copy the current directory contents into the container at /app
COPY . /data_service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "data_service_app.py"]

