from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
)

@component(
    packages_to_install=['torch','torchvision'],
    base_image='python:3.8',
)
def loads(source: Input[Artifact],dataset: Input[Artifact]):
    import tarfile
    import torchvision
    tarfile.open(name=dataset.path, mode="r").extractall('.')
    tarfile.open(name=source.path, mode="r").extractall('.')
    from nn import my_nn
    data = torchvision.datasets.FashionMNIST( ".", train=True, download = False, transform=torchvision.transforms.ToTensor())
    mynn = my_nn()

    print(data)
    print(mynn)
