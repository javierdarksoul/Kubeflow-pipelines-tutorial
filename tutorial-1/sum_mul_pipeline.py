import kfp
import kfp.dsl as dsl
from kfp.v2.dsl import component
from kfp import compiler
@component
def add(a: float, b: float) -> float:
  return a + b

@component
def mul(a: float, b: float) -> float:
  return a * b


@dsl.pipeline(
  name='add-mul-pipeline',
  description='An example pipeline that performs addition calculations.',
  # pipeline_root='gs://my-pipeline-root/example-pipeline'
)
def my_pipeline(a: float = 1, b: float = 7, c: float = 2.3):
  add_task = add(a, b)
  mul_task = mul(add_task.output, c)




compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(pipeline_func=my_pipeline, package_path='pipeline.yaml')

client = kfp.Client()
# run the pipeline in v2 compatibility mode
client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={'a': 7, 'b': 8, 'c': 3.2},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)