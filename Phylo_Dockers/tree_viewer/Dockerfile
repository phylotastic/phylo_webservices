# Use an official Python runtime as a parent image
FROM python:3

RUN apt-get -y update -qq && apt-get install -y --no-install-recommends libqt4-dev libxml2-dev libxslt1-dev 
    
RUN apt-get install -y libqt5dbus5 libqt5widgets5 libqt5network5 libqt5gui5 libqt5core5a libdouble-conversion1 \
    libxcb-xinerama0 libqt5x11extras5 libxcb-xkb1 libxcb-icccm4 libxcb-image0 libxcb-render-util0 
    
RUN apt-get install -y --no-install-recommends python3-numpy python3-pyqt5 python3-lxml python3-six xvfb

# Set the working directory to /
WORKDIR /

# Copy the current directory contents into the container at /viewer-service
COPY . /

RUN mkdir -p /trees

RUN useradd ete

RUN chown ete:ete /trees

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install --upgrade ete3

# Make port 8989 available to the world outside this container
EXPOSE 8989

USER ete

# Run app.py when the container launches
CMD ["uwsgi", "ete_pro.ini"]

