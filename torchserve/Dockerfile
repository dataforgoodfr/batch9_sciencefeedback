FROM pytorch/torchserve:0.3.0-cpu

WORKDIR /home/model-server

USER root
RUN apt-get update && apt-get install -y \
                      gcc \
                      libpq-dev \
                      python3-dev \
                      python3-pip \
                      python3-venv \
                      python3-wheel \
                      unzip \
                      zip
USER model-server

COPY ./requirements.txt /home/model-server/requirements.txt
RUN pip install --upgrade pip==21.0.1
RUN pip install -r /home/model-server/requirements.txt


COPY ./download_model.py /home/model-server/download_model.py
RUN python /home/model-server/download_model.py

COPY ./sentence_transformers_handler.py /home/model-server/sentence_transformers_handler.py
COPY ./init_model.sh /home/model-server/init_model.sh

RUN cd sentence_model && zip -r ./model.pt 0_Transformer
RUN cd sentence_model && zip -r ./pool.zip 1_Pooling

USER root
RUN chmod +x /home/model-server/init_model.sh
USER model-server
RUN /home/model-server/init_model.sh

EXPOSE 8080 8081
