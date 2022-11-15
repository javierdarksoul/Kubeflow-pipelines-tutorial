import kfp
import kfp.dsl as dsl
from kfp.v2.dsl import component
from kfp.v2 import compiler
import google.cloud.aiplatform as aip
import os
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
  mul_task_1 = mul(add_task_1.output, c)
  add_task_2 = add(add_task_1.output, mul_task_1.output)
  mul_task_2 = mul(add_task_2.output, mul_task_1.output)




compiler.Compiler().compile(pipeline_func=my_pipeline, package_path='sum_mul_paralell.json')

import google.auth
cred = google.auth.load_credentials_from_file("../../../credentials/credentials.json")
print(cred)

job = aip.PipelineJob(
    display_name="sum_mul_paralell",
    template_path="sum_mul_paralell.json",
    pipeline_root= "gs://test-bucket-dvc",
    credentials=cred[0],
    project	= "nerf-360414",
    parameter_values={
        'a': 1,
        'b': 2,
        'c': 3
    }
)
#print(job)
job.submit()
os.system("rm sum_mul_paralell.json")
""" 
client = kfp.Client()
# run the pipeline in v2 compatibility mode
client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={'a': 7, 'b': 8, 'c': 3.2},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)
"""