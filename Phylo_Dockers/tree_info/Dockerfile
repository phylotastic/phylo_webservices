# Use an official R runtime as a parent image
FROM r-base:latest

RUN apt-get -y update -qq && apt-get install -y --no-install-recommends \
    libgsl0-dev libssl-dev libffi-dev zlib1g-dev libxml2-dev libcurl4-openssl-dev libxslt1-dev libreadline-dev python3-pip python3-dev

RUN \
  python3 -m pip install --no-cache-dir --upgrade pip && \
  python3 -m pip install --no-cache-dir --upgrade setuptools && \
  python3 -m pip install --no-cache-dir --upgrade wheel && \
  rm -rf /root/.cache

# Set the working directory to /app
WORKDIR /tree_info

# Copy the current directory contents into the container at /app
COPY . /tree_info

RUN Rscript install_packages.R

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5058 available to the world outside this container
EXPOSE 5058

# Run app.py when the container launches
CMD ["python3", "tree_info_app.py"]

