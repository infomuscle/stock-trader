FROM python:3.9.0

LABEL maintainer="infomuscle10@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir /stock-front
WORKDIR /stock-front

ADD requirements.txt /stock-front

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /stock-front

CMD ["python3", "manage.py", "runserver", "0:8000", "--settings=config.settings.settings_dev"]

EXPOSE 8000