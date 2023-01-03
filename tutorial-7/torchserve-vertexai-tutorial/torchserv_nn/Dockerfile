FROM pytorch/torchserve:latest-cpu

# install dependencies

# copy model artifacts, custom handler and other dependencies
COPY ./handler.py /home/model-server/
COPY ./weights /home/model-server/
COPY ./nn.py /home/model-server/
#COPY ./attentionLayer.py /home/model-server/

# create torchserve configuration file
USER root
RUN printf "\nservice_envelope=json" >> /home/model-server/config.properties
RUN printf "\ninference_address=http://0.0.0.0:7080" >> /home/model-server/config.properties
RUN printf "\nmanagement_address=http://0.0.0.0:7081" >> /home/model-server/config.properties
USER model-server

# expose health and prediction listener ports from the image
EXPOSE 7080
EXPOSE 7081

# create model archive file packaging model artifacts and dependencies
RUN torch-model-archiver -f \
  --model-name=example-model \
  --model-file=nn.py\
  --version=1.0 \
  --serialized-file=/home/model-server/weights \
  --handler=/home/model-server/handler.py \
  #--extra-files /home/model-server/attentionLayer.py \
  --export-path=/home/model-server/model-store/

# run Torchserve HTTP serve to respond to prediction requests
CMD ["torchserve", \
     "--start", \
     "--ts-config=/home/model-server/config.properties", \
     "--models", \
     "Attentionmodel=Attentionmodel.mar", \
     "--model-store", \
     "/home/model-server/model-store"]

