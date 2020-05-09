FROM docker_python_base

WORKDIR /app

COPY api/web/app.py /app
COPY Pipfile Pipfile.lock /app/

RUN apt-get update && apt-get install -y git

RUN pip install pipenv
RUN pipenv sync --dev --python 3.7
