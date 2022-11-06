from components.dataset import load_dataset
from components.build_src import build_src
from components.loads import loads
import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline(datatype: str):
  dataset= load_dataset(datatype)
  src = build_src()
  load_task= loads(src.outputs["source"],dataset.outputs["dataset"])
 
  



compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

client = kfp.Client()
client.create_run_from_pipeline_func(
    nnpipeline,
    arguments={'datatype': "fmnist"},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)