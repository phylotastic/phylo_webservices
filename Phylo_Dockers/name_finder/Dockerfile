# Use an official Python runtime as a parent image
FROM python:2.7.15-stretch

# Set the working directory to /app
WORKDIR /name_finder

# Copy the current directory contents into the container at /app
COPY . /name_finder

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Run app.py when the container launches
CMD ["python", "find_names_app.py"]

