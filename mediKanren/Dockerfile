# Pull from base image
from ubuntu:18.04

RUN \
  export DISPLAY=127.0.0.1:10.0

# Install git/python and download kgx
RUN \
  apt-get update && \
  apt-get install -y x11-apps && \
  apt-get install -y git && \
  apt-get install -y racket && \
  apt-get install -y python3-pip && \
  apt-get install -y python3-venv && \
  apt-get install -y software-properties-common

RUN \
  add-apt-repository -y ppa:deadsnakes/ppa && \
  apt-get update && \
  apt-get install -y python3.7

RUN \
  git clone https://github.com/webyrd/mediKanren.git && \
  git clone https://github.com/NCATS-Tangerine/kgx.git && \
  cd kgx && \
  git checkout source-sink && \
  python3.7 -m pip install -r requirements.txt && \
  rm config.yml

COPY config.yml kgx/config.yml

Run \
  cd kgx && \
  python3.7 neo4j_download.py

Run \
  mkdir /mediKanren/biolink/data/rtx_kg2 && \
  mv /kgx/rtx_kg2.edge.csv ../mediKanren/biolink/data/rtx_kg2/rtx_kg2.edge.csv && \
  mv /kgx/rtx_kg2.edgeprop.csv ../mediKanren/biolink/data/rtx_kg2/rtx_kg2.edgeprop.csv && \
  mv /kgx/rtx_kg2.node.csv ../mediKanren/biolink/data/rtx_kg2/rtx_kg2.node.csv && \
  mv /kgx/rtx_kg2.nodeprop.csv ../mediKanren/biolink/data/rtx_kg2/rtx_kg2.nodeprop.csv

#RUN \
#  cd /mediKanren/biolink && \
#  racket csv-graph-to-db.rkt data rtx_kg2 && \
#  racket build-string-index.rkt data rtx_kg2

