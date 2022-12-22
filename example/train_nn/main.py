import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp
import google.cloud.aiplatform as aip
import os
import google.auth
from google_cloud_pipeline_components import aiplatform as gcc_aip
from components.pythoncomponents.train import train
from components.pythoncomponents.test import test
get_model=kfp.components.load_component_from_file("components/yaml-components/get_model_component.yaml")
get_data=kfp.components.load_component_from_file("components/yaml-components/get_data_component.yaml")
mar_comp=kfp.components.load_component_from_file("components/yaml-components/component_mar.yaml")
build_torchserve=kfp.components.load_component_from_file("components/yaml-components/build_torchserve_component.yaml")

@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline():
  project_id = "zippedi-project-01"
  region= "us-central1"
  src_repo = 'https://github.com/javierdarksoul/src_test.git'
  data_repo = 'https://github.com/javierdarksoul/data_test.git'
  dataset = "FashionMNIST"
  model_name= "example-model"
  artifact_folder = "us-docker.pkg.dev/zippedi-project-01/kubeflow-components/"
  tensorboard_route = "gs://example-vertex-ai/tensorboard_runs/example001/"
  src = get_model(githubpath=src_repo)
  data = get_data(githubpath=data_repo,folder =dataset)
  train_task= train(src.outputs["output1path"], data.outputs["trainloader"],tensorboard_route,True).add_node_selector_constraint('cloud.google.com/gke-accelerator','nvidia-tesla-t4').set_gpu_limit(1)
  test_task=test(src.outputs["output1path"],train_task.outputs["weights"], data.outputs["testloader"])
  test_task.set_caching_options(False)

  with dsl.Condition(test_task.outputs['output']>0.8):

    mar_comp_task=mar_comp(src.outputs["output1path"],model_name,train_task.outputs["weights"] )
    task=build_torchserve(model_name,mar_comp_task.outputs["output_1"],artifact_folder,project_id)
    task.set_caching_options(False)
    model_upload_op = gcc_aip.ModelUploadOp(
        project=project_id,
        display_name=model_name,
        serving_container_image_uri=task.outputs['output_1'],
        serving_container_predict_route="/predictions/{}".format(model_name),
        serving_container_health_route="/ping",
        location=region,
        serving_container_ports=[{"containerPort": 7080}]      
    )
    model_upload_op.set_caching_options(False)
    
  # gcc_aip.EndpointCreateOp.component_spec.implementation.container.image = "gcr.io/ml-pipeline/google-cloud-pipeline-components:0.1.7"
    endpoint_create_op = gcc_aip.EndpointCreateOp(
          project=project_id,
          display_name=model_name+"-endpoint",
          location=region
      ).set_caching_options(False)
    
    #gcc_aip.ModelDeployOp.component_spec.implementation.container.image = "gcr.io/ml-pipeline/google-cloud-pipeline-components:0.1.7"
    model_deploy_op = gcc_aip.ModelDeployOp(
          #project=project_id,
          endpoint=endpoint_create_op.outputs["endpoint"],
          model=model_upload_op.outputs["model"],
          deployed_model_display_name=model_name,
          dedicated_resources_machine_type="n1-standard-4",
          dedicated_resources_min_replica_count=1,
          #accelerator_type='NVIDIA_TESLA_P100',  # CHANGE THIS as necessary
          #accelerator_count=1        
      )
    
    
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
