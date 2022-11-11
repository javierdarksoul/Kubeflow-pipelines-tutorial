import argparse
import os
import tarfile
import pickle
import sys
from torch.utils.data import DataLoader, SubsetRandomSampler
import torchvision
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--githubpath', type=str,
  help='Path al repositorio git, si es privado, proporcionarlo con el token')
parser.add_argument('--folder', type=str,
  help='Nombre de la carpeta a ser pulleada')
parser.add_argument('--output1path', type=str,
  help='Path a los archivos comprimidos.')
args = parser.parse_args()

print("begin")
project_name=args.githubpath[args.githubpath.rfind("/") +1 : -4]
os.system("git clone " + args.githubpath)
os.chdir(project_name)
os.system("dvc remote modify --local myremote credentialpath /pipelines/credentials/credentials.json")
os.system("dvc pull "+args.folder)
#with tarfile.open(args.output1path, "w") as tar:
#  tar.add(args.folder)

train_data= torchvision.datasets.FashionMNIST( ".", train=True, transform=torchvision.transforms.ToTensor())
idx = list(range(len(train_data)))
split = int(0.7*len(idx))
train_loader= DataLoader(train_data,batch_size=128,sampler=SubsetRandomSampler(idx[:split])) 
valid_loader= DataLoader(train_data,batch_size=128, sampler=SubsetRandomSampler(idx[split:])) 
# open a file, where you ant to store the data
dataload = {"train_loader": train_loader, "valid_loader": valid_loader}
with open(args.output1path,'wb') as file:
  pickle.dump(dataload, file)
print("Done!!")