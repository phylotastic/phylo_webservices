# Use an official Python runtime as a parent image
FROM python:2.7.15-stretch

# Set the working directory to /app
WORKDIR /name_resolver

# Copy the current directory contents into the container at /app
COPY . /name_resolver

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5051 available to the world outside this container
EXPOSE 5051

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "resolve_names_app.py"]

