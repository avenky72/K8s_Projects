# docker build . --no-cache -t  atulv1/webapp

FROM ubuntu:22.04
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker
RUN DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
USER root
RUN  apt update -y && apt upgrade -y \
  && apt install -y openssh-server python3-pip python3.10-venv \
  && apt install -y sudo lsof curl iputils-ping net-tools vim mysql-client \
  && rm -rf /var/lib/apt/lists/*
RUN mkdir /app
WORKDIR /app
ENV PATH=".:/app:${PATH}"
COPY requirements.txt /app
COPY webapp.py /app
COPY startapp /app
EXPOSE 5000
ENV FLASK_APP=webapp.py
ENV FLASK_RUN_HOST=127.0.0.1
RUN python3 -m venv venv && . ./venv/bin/activate &&  pip3 install -r ./requirements.txt
ENTRYPOINT ["./startapp"] ## GOOD but need to figure this work after port map
