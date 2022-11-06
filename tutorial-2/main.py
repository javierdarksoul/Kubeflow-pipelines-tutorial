from components.dataset import load_dataset
import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline(datatype: str):
  dataset= load_dataset(datatype)



compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

client = kfp.Client()
client.create_run_from_pipeline_func(
    nnpipeline,
    arguments={'datatype': "mnist"},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)