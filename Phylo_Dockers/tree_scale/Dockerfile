FROM r-base:latest

RUN apt-get -y update -qq && apt-get install -y --no-install-recommends \
    libgsl0-dev libssl-dev libffi-dev zlib1g-dev libxml2-dev libcurl4-openssl-dev libmagick++-dev libxslt1-dev libreadline-dev wget zip unzip python3-pip python3-dev

RUN \
  python3 -m pip install --no-cache-dir --upgrade pip && \
  python3 -m pip install --no-cache-dir --upgrade setuptools && \
  python3 -m pip install --no-cache-dir --upgrade wheel && \
  rm -rf /root/.cache

RUN \
  python3 -m pip install --no-cache-dir \
       https://bitbucket.org/rpy2/rpy2/get/version_2.9.x.tar.gz && \
  rm -rf /root/.cache

RUN wget https://mafft.cbrc.jp/alignment/software/mafft-7.453-with-extensions-src.tgz && gunzip -cd mafft-7.453-with-extensions-src.tgz | tar xfv - && cd mafft-7.453-with-extensions/core/ && \
    make clean && make && make install

# Set the working directory to /tree_scale
WORKDIR /tree_scale

# Copy the current directory contents into the container at /tree_scale
COPY . /tree_scale

RUN chmod +x /tree_scale/install_pathd8.sh

RUN /tree_scale/install_pathd8.sh

RUN Rscript install_packages.R

RUN R -e "devtools::install_github('phylotastic/datelife')" 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5056 available to the world outside this container
EXPOSE 5056

# Run app.py when the container launches
CMD ["python3", "tree_scaling_app.py"]
