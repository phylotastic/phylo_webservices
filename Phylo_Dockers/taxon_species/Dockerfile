# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /species_list
WORKDIR /taxon_species

# Copy the current directory contents into the container at /taxon_species
COPY . /taxon_species

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5053 available to the world outside this container
EXPOSE 5053

# Run app.py when the container launches
CMD ["python3", "taxon_species_app.py"]

