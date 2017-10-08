
FROM ubuntu:xenial


ENV DEBIAN_FRONTEND noninteractive

ENV uid 1000
ENV gid 1000

RUN useradd -m voc

RUN apt-get update \
	&& apt-get install -y gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps vim-tiny wget \
	&& apt-get install -y --no-install-recommends gstreamer1.0-tools libgstreamer1.0-0 python3 python3-gi gir1.2-gstreamer-1.0 gstreamer1.0-plugins-bad \
	&& apt-get install -y gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 gir1.2-gtk-3.0 gstreamer1.0-x ffmpeg python3-gi python3-gi-cairo python-gst-1.0 python-gst-1.0-dbg \
	&& apt-get install -y libdc1394-22-dev libdc1394-22 libdc1394-utils sudo python-gtk2-dev python-gtk2 libgtk-3-dev\
	&& apt-get install -y gir1.2-gst-rtsp-server-1.0 gstreamer1.0-libav \
	&& apt-get clean

RUN ln -s /dev/null /dev/raw1394
RUN wget -q https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64 -O /bin/gosu && chmod +x /bin/gosu

RUN mkdir -p /opt/stream-forward

EXPOSE 8554
VOLUME /video

# Set the application directory
WORKDIR /opt/faceblur



# Copy our code from the current folder to /opt/faceblur/ inside the container
COPY . /opt/faceblur/

# Install our requirements.txt
RUN python3 get-pip.py
RUN pip install -r requirements.txt
#RUN python3 app.py



# ENTRYPOINT ["/opt/stream-forward/docker-ep.sh"]
# Define our command to be run when launching the container
