import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
import google.cloud.aiplatform as aip
import os
from components.pythoncomponents.train import train
from components.pythoncomponents.test import test
get_model=kfp.components.load_component_from_file("components/yaml-components/get_model_component.yaml")
get_data=kfp.components.load_component_from_file("components/yaml-components/get_data_component.yaml")


@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline():
  src = get_model(githubpath='https://github.com/javierdarksoul/src_test.git')
  data = get_data(githubpath=' https://github.com/javierdarksoul/data_test.git',folder ="FashionMNIST")
  train_task= train(src.outputs["output1path"], data.outputs["trainloader"])#.add_node_selector_constraint('cloud.google.com/gke-accelerator','NVIDIA_TESLA_P100').set_gpu_limit(1))
  test(src.outputs["output1path"],train_task.outputs["weights"], data.outputs["testloader"])
 

compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

import google.auth
cred = google.auth.default() #google.auth.load_credentials_from_file("../../../credentials/credentials.json")
job = aip.PipelineJob(
    display_name="train_nn_pipeline",
    template_path="pipeline.json",
    pipeline_root="gs://example-vertex-ai",
    credentials=cred[0],
    project	= "zippedi-project-01",
    location = "us-central1",
    parameter_values={
    }
)
#print(job)
job.submit()
os.system("rm pipeline.json")
