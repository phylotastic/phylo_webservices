FROM rocker/verse:3.5.0

RUN apt-get -y update -qq && apt-get install -y python-pip python-dev build-essential

RUN apt-get install -y --no-install-recommends \
    libgsl0-dev libssl-dev libffi-dev zlib1g-dev libxml2-dev libxslt1-dev libreadline-dev

# Set the working directory to /app
WORKDIR /tree_retrieval

# Copy the current directory contents into the container at /app
COPY . /tree_retrieval

RUN Rscript install_packages.R

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5052 available to the world outside this container
EXPOSE 5052

# Run app.py when the container launches
CMD ["python", "get_tree_app.py"]
