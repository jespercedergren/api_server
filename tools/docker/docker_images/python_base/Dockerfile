FROM debian:stretch AS python_base
MAINTAINER Getty Images "https://github.com/gettyimages"

RUN apt-get update \
 && apt-get install -y locales \
 && dpkg-reconfigure -f noninteractive locales \
 && locale-gen C.UTF-8 \
 && /usr/sbin/update-locale LANG=C.UTF-8 \
 && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Users with other locales should set this in their derivative image
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN apt-get update \
 && apt-get install -y curl unzip \
    python3 python3-setuptools \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && easy_install3 pip py4j \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# http://blog.stuart.axelbrooke.com/python-3-on-spark-return-of-the-pythonhashseed
ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# PYTHON
RUN apt-get update
RUN apt-get --yes install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev
RUN apt-get --yes install libsnappy-dev
RUN apt-get --yes install python3-dev

WORKDIR /usr/src
RUN curl -O https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
RUN tar xzf Python-3.7.4.tgz
WORKDIR Python-3.7.4
RUN ./configure --enable-optimizations
RUN make altinstall
WORKDIR /

ENV PYSPARK_PYTHON=python3.7
ENV PYSPARK_DRIVER_PYTHON=python3.7
RUN echo '\nalias python=python3.7' >> ~/.bashrc

RUN python3.7 -m pip install --upgrade --force pip

RUN apt-get --yes install python-distutils-extra
RUN pip install pypandoc
RUN pip install setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt