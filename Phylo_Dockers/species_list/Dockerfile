# Use an official Python runtime as a parent image
FROM python:2.7.15-stretch

# Set the working directory to /species_list
WORKDIR /species_list

# Copy the current directory contents into the container at /species_list
COPY . /species_list

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5055 available to the world outside this container
EXPOSE 5055

# Run app.py when the container launches
CMD ["python", "list_species_app.py"]

