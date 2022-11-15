from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Input,
    Artifact,
    ClassificationMetrics,

)
@component(
    packages_to_install=['numpy','torch','torchvision',"scikit-learn"],
    output_component_file='',
    base_image='python:3.8',
)
def test(source: Input[Artifact],  weights: Input[Artifact], dataset: Input[Artifact], metrics: Output[ClassificationMetrics]):
    import pickle
    import torch
    import tarfile
    from sklearn.metrics import confusion_matrix
    tarfile.open(name=source.path, mode="r").extractall('.')
    from src.nn import my_nn
    with open(dataset.path,'rb') as file:
        dataloaders = pickle.load(file)
    model= my_nn()
    test_loader=dataloaders["test_loader"]
    model.load_state_dict(torch.load(weights.path))
    y_preds_list=[]
    y_real_list=[]
    for image,label in test_loader:
        output = model(image.reshape(-1,28*28)).argmax(dim=1)
        y_preds= output.detach().numpy()
        y_real= label.detach().numpy()
        for k in range(len(y_preds)):
            y_preds_list.append(y_preds.item(k))
            y_real_list.append(y_real.item(k))
    
    metrics.log_confusion_matrix(
        ['T-shirt', 'Trouser', 'Pullover','Dress','Coat', 'Sandal' , 'Shirt','Sneaker','Bag','Ankle Boot'],
        confusion_matrix(y_real_list, y_preds_list).tolist() # .tolist() to convert np array to list.
    )