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
  add_task_1 = add(a, b)
  add_task_4 = add(10, 10)
  mul_task_1 = mul(add_task_1.output, c)
  add_task_2 = add(add_task_1.output, mul_task_1.output)
  mul_task_2 = mul(add_task_2.output, mul_task_1.output)




compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(pipeline_func=my_pipeline, package_path='pipeline.yaml')

client = kfp.Client()
# run the pipeline in v2 compatibility mode
client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={'a': 7, 'b': 8, 'c': 3.2},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)