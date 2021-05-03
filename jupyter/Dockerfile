FROM jupyter/base-notebook:python-3.7.6

USER root
RUN apt-get update \
    && apt-get install -y \
                       gcc \
                       libmysqlclient-dev \
                       libpq-dev \
                       python3-dev
USER jovyan

COPY ./requirements.txt /opt/api/requirements.txt
RUN pip install --upgrade pip==21.0.1
RUN pip install -r /opt/api/requirements.txt

COPY ./nltk.txt /opt/api/nltk.txt
COPY ./utils/nltk.py /opt/api/utils/nltk.py
RUN PYTHONPATH=/opt/api python -c "from utils.nltk import import_nltk; import_nltk(download_dir='/home/jovyan/nltk_data');"

USER root
COPY ./tmp /opt/api/tmp
RUN chown jovyan:users /opt/api/tmp
USER jovyan

EXPOSE 8888
