# Use an official Python runtime as a parent image
FROM python:2.7.15-stretch

# Set the working directory to /app
WORKDIR /image_info_retrieval

# Copy the current directory contents into the container at /app
COPY . /image_info_retrieval

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5054 available to the world outside this container
EXPOSE 5054

# Run app.py when the container launches
CMD ["python", "get_image_info_app.py"]
