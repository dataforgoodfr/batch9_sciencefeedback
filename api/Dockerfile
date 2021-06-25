FROM python:3.7

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/api

COPY ./requirements.txt /opt/api/requirements.txt
COPY ./requirements-dev.txt /opt/api/requirements-dev.txt
RUN pip install --upgrade pip==21.1.2
RUN pip install -r /opt/api/requirements.txt -r /opt/api/requirements-dev.txt

COPY ./nltk.txt /opt/api/nltk.txt
COPY ./utils/nltk.py /opt/api/utils/nltk.py
RUN PYTHONPATH=/opt/api python -c "from utils.nltk import import_nltk; import_nltk();"

RUN mkdir -p /tmp/.newspaper_scraper/article_resources
COPY ./tmp /opt/api/tmp
RUN chown -R nobody:nogroup /opt/api/tmp

EXPOSE 5000
