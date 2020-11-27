FROM python:3.9.0

LABEL maintainer="infomuscle10@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir /stock-crawler
WORKDIR /stock-crawler

ADD requirements.txt /stock-crawler

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /stock-crawler

CMD ["python3", "manage.py", "runserver", "0:8001"]

EXPOSE 8001