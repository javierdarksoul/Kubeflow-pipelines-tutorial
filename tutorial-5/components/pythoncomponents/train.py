from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
)
@component(
    packages_to_install=['torch','torchvision'],
    output_component_file='component.yaml',
    base_image='python:3.8',
)
def train(source: Input[Artifact],dataset: Input[Artifact]):
    import pickle
    import torch
    import tarfile
    tarfile.open(name=source.path, mode="r").extractall('.')
    from src.nn import my_nn
    with open(dataset.path,'rb') as file:
        dataloaders = pickle.load(file)
    model= my_nn()
    train_loader=dataloaders["train_loader"]
    valid_loader=dataloaders["valid_loader"]
    criterion = torch.nn.CrossEntropyLoss()
    global_loss = 1e10
    optimizer = torch.optim.Adam(model.parameters(),1e-3)
    for epoch in range(10):
        print(epoch)
        train_loss=0.0
        for image,label in train_loader:
            optimizer.zero_grad()
            output=model(image.reshape(-1,28*28))
            loss = criterion(output,label)
            loss.backward()
            optimizer.step()
            train_loss+= loss.item()
            

