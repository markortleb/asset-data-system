FROM ubuntu:xenial
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip
WORKDIR /usr/local/asset-data-system
COPY . .

CMD bash -c "/bin/bash"
#VOLUME ["/data"]

