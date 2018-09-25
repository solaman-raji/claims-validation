FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /code/
