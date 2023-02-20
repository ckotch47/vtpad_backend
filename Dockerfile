
# pull the official docker image
FROM python:3.9

# set work directory
#WORKDIR /app
COPY ./.env /.env


# install dependencies
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

