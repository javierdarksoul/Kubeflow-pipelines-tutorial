FROM python:3.8
RUN pip install dvc
RUN pip install "dvc[gs]"
RUN pip install torch
RUN pip install torchvision
COPY ./src /pipelines/component/src
#COPY ./credentials/ /pipelines/credentials

