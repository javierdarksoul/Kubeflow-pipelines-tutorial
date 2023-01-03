FROM python:3.8.8-slim
WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt && pip cache purge
RUN pip install mlem==0.4.1 && pip cache purge

COPY . ./
ENV MLEM_DEBUG=true
ENV MLEM_EXTENSIONS=mlem.contrib.callable,mlem.contrib.github,mlem.contrib.gitlabfs,mlem.contrib.bitbucketfs,mlem.contrib.pip,mlem.contrib.requirements,mlem.contrib.venv


CMD sh run.sh