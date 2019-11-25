# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /name_converter

# Copy the current directory contents into the container at /app
COPY . /name_converter


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5057 available to the world outside this container
EXPOSE 5057

# Run app.py when the container launches
CMD ["python3", "name_converter_app.py"]

