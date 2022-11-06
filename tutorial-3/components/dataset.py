from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Artifact,
)

@component(
    packages_to_install=['torchvision'],
    output_component_file='component.yaml',
    base_image='python:3.8',
)
def load_dataset(type : str, dataset: Output[Artifact]):
    import torchvision
    import tarfile

    if type=="fmnist":
        torchvision.datasets.FashionMNIST( ".", train=True, download = True, transform=torchvision.transforms.ToTensor())
        with tarfile.open(dataset.path, "w") as tar:
            tar.add("FashionMNIST")
    elif type=="mnist":
        torchvision.datasets.MNIST( ".", train=True, download = True, transform=torchvision.transforms.ToTensor())
        with tarfile.open(dataset.path, "w") as tar:
            tar.add("MNIST")

