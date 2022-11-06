from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
)

@component(
    packages_to_install=['torch'],
    base_image='python:3.8',
)
def loads(source: Input[Artifact]):
    import tarfile
    tarfile.open(name=source.path, mode="r").extractall('.')
    import nn