import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
from secret import access_secret_version
from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
)
import json

#secret = projects/209915815446/secrets/vertex-ai-secret/versions/1

credentials=access_secret_version("209915815446","vertex-ai-secret", "1")
get_model=kfp.components.load_component_from_file("components/get_model_component.yaml")
get_data=kfp.components.load_component_from_file("components/get_data_component.yaml")

@component(
    packages_to_install=['torch','torchvision'],
    base_image='python:3.8',
)
def loads(dataset: Input[Artifact],source: Input[Artifact]):
    import pickle
    import torch
    import tarfile
    tarfile.open(name=source.path, mode="r").extractall('.')
    from src.nn import my_nn
    with open(dataset.path,'rb') as file:
        dataloaders = pickle.load(file)
    train_loader=dataloaders["train_loader"]
    valid_loader=dataloaders["valid_loader"]
    print(train_loader)
    for image,label in train_loader:
        print(image.shape)
        break

@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline():
  src = get_model(githubpath='https://github.com/javierdarksoul/src_test.git')
  data = get_data(githubpath=' https://github.com/javierdarksoul/data_test.git',folder ="FashionMNIST",credentials=credentials)
  load_task= loads(data.outputs['trainloader'],src.outputs['output1path'])

compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

client = kfp.Client()
client.create_run_from_pipeline_func(
    nnpipeline,
    arguments={},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)
