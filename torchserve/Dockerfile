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
RUN pip install --upgrade pip==21.1.2
RUN pip install -r /home/model-server/requirements.txt


COPY ./download_model.py /home/model-server/download_model.py
RUN python /home/model-server/download_model.py

COPY ./transformers_handler.py /home/model-server/transformers_handler.py
COPY ./init_model.sh /home/model-server/init_model.sh

USER root
RUN ls
RUN ls sentence_model
RUN ls model-store
RUN chmod +x /home/model-server/init_model.sh
USER model-server
RUN /home/model-server/init_model.sh

EXPOSE 8080 8081
