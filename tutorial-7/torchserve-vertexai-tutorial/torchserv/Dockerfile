FROM pytorch/torchserve:latest-cpu

# install dependencies

# copy model artifacts, custom handler and other dependencies
COPY ./handler.py /home/model-server/
COPY ./model.pth /home/model-server/
COPY ./model.py /home/model-server/
COPY ./attentionLayer.py /home/model-server/

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
  --model-name=Attentionmodel \
  --model-file=model.py\
  --version=1.0 \
  --serialized-file=/home/model-server/model.pth \
  --handler=/home/model-server/handler.py \
  --extra-files /home/model-server/attentionLayer.py \
  --export-path=/home/model-server/model-store/

# run Torchserve HTTP serve to respond to prediction requests
CMD ["torchserve", \
     "--start", \
     "--ts-config=/home/model-server/config.properties", \
     "--models", \
     "Attentionmodel=Attentionmodel.mar", \
     "--model-store", \
     "/home/model-server/model-store"]


#torch-model-archiver -f --model-name=Attentionmodel --model-file=model.py --version=1.0 --serialized-file=model.pth --handler=handler.py --extra-files attentionLayer.py --export-path=model-store
#torchserve --start --ts-config=config.properties --models Attentionmodel=Attentionmodel.mar --model-store model-store/
