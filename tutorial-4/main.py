import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
)

get_model=kfp.components.load_component_from_file("get_model_component.yaml")

@component(
    packages_to_install=['torch','torchvision'],
    base_image='python:3.8',
)
def loads(source: Input[Artifact]):
    import tarfile
    tarfile.open(name=source.path, mode="r").extractall('.')
    from src_test.src.nn import my_nn
    mynn = my_nn()
    print(mynn)

@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline(datatype: str):
  src = get_model(githubpath='https://github.com/javierdarksoul/src_test.git')
  load_task= loads(src.outputs['output1path'])

compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

client = kfp.Client()
client.create_run_from_pipeline_func(
    nnpipeline,
    arguments={'datatype': "fmnist"},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)
