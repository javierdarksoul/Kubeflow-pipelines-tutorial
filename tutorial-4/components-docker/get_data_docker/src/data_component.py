import argparse
import os
import tarfile
import pickle
import sys
from torch.utils.data import DataLoader, SubsetRandomSampler
import torchvision
import json
from pathlib import Path
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--githubpath', type=str,
  help='Path al repositorio git, si es privado, proporcionarlo con el token')

parser.add_argument('--folder', type=str,
  help='Nombre de la carpeta a ser pulleada')
parser.add_argument('--credentials', type=str,
  help='credenciales')
parser.add_argument('--trainloader', type=str,
  help='Path a los archivos comprimidos.')
parser.add_argument('--testloader', type=str,
  help='Path a los archivos comprimidos.')
args = parser.parse_args()

print("begin")
with open('credentials.json', 'w') as outfile:
    outfile.write(args.credentials)
os.system("ls")
project_name=args.githubpath[args.githubpath.rfind("/") +1 : -4]
os.system("git clone " + args.githubpath)
os.chdir(project_name)
os.system("dvc remote modify --local myremote credentialpath ../credentials.json")
os.system("dvc pull "+args.folder)
#with tarfile.open(args.output1path, "w") as tar:
#  tar.add(args.folder)

train_data= torchvision.datasets.FashionMNIST( ".", train=True, transform=torchvision.transforms.ToTensor())
test_data= torchvision.datasets.FashionMNIST( ".", train=False, transform=torchvision.transforms.ToTensor())
idx = list(range(len(train_data)))
split = int(0.7*len(idx))
train_loader= DataLoader(train_data,batch_size=128,sampler=SubsetRandomSampler(idx[:split])) 
valid_loader= DataLoader(train_data,batch_size=128, sampler=SubsetRandomSampler(idx[split:])) 
test_loader= DataLoader(test_data,batch_size=128)
# open a file, where you ant to store the data
Path(args.trainloader).parent.mkdir(parents=True, exist_ok=True)
Path(args.testloader).parent.mkdir(parents=True, exist_ok=True)

trainload = {"train_loader": train_loader, "valid_loader": valid_loader}
with open(args.trainloader,'wb') as file:
  pickle.dump(trainload, file)
testload = {"test_loader": test_loader}
with open(args.testloader,'wb') as file:
  pickle.dump(testload, file)
print("Done!!")