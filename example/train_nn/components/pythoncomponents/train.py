from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
    Metrics
)
@component(
    packages_to_install=['torchvision','tensorflow'],
    output_component_file='component.yaml',
    base_image='pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime',
)
def train(source: Input[Artifact],dataset: Input[Artifact], weights: Output[Artifact] ,metrics: Output[Metrics], tensorboard: str, usegpu: bool):
    import pickle
    import torch
    import tarfile
    from torch.utils.tensorboard import SummaryWriter
    tarfile.open(name=source.path, mode="r").extractall('.')
    from src.nn import my_nn
    with open(dataset.path,'rb') as file:
        dataloaders = pickle.load(file)
    model= my_nn()
    if usegpu: model=model.cuda()
    train_loader=dataloaders["train_loader"]
    valid_loader=dataloaders["valid_loader"]
    den_valid = valid_loader.__len__()*valid_loader.batch_size
    criterion = torch.nn.CrossEntropyLoss()
    writer = SummaryWriter(tensorboard,flush_secs=10)

    global_loss = 1e10
    optimizer = torch.optim.Adam(model.parameters(),1e-3)
    for epoch in range(30):
        print(epoch)
        train_loss=0.0
        for image,label in train_loader:
            if usegpu:
                image=image.cuda()
                label=label.cuda()
            optimizer.zero_grad()
            output=model(image)
            loss = criterion(output,label)
            loss.backward()
            optimizer.step()
            train_loss+= loss.item()
        writer.add_scalar('Loss/train', train_loss, epoch)
        valid_loss=0.0
        for image,label in valid_loader:
            if usegpu:
                image=image.cuda()
                label=label.cuda()
            y_pred=model(image)
            loss = criterion(y_pred,label)
            valid_loss+= loss.item()
            if valid_loss<global_loss:
                print("Se encontró un mejor modelo en la epoca: %i\nLoss Actual: =%f" % (epoch, valid_loss/den_valid))
                metrics.log_metric('Loss', valid_loss/den_valid)
                global_loss = valid_loss
                torch.save(model.state_dict(), weights.path)
            


#tb-gcp-uploader --tensorboard_resource_name projects/zippedi-project-01/locations/us-east1/tensorboards/5759540973453443072 --logdir=tensorboard_runs  --experiment_name=Exp-1 --one_shot=True