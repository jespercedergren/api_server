FROM python_base

WORKDIR /app

RUN apt-get update && apt-get install -y git

ADD ./requirements_git.txt /srv/requirements_git.txt
RUN pip install -r /srv/requirements_git.txt

ADD ./requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

COPY ./app.py /app
