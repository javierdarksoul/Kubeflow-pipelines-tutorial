import argparse
import os
import tarfile
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--githubpath', type=str,
  help='Path al repositorio git, si es privado, proporcionarlo con el token')
parser.add_argument('--output1path', type=str,
  help='Path a los archivos comprimidos.')
args = parser.parse_args()
print("begin")
project_name=args.githubpath[args.githubpath.rfind("/") +1 : -4]
os.system("git clone " + args.githubpath)

with tarfile.open(args.output1path, "w") as tar:
  tar.add( project_name+"/src/nn.py")
print("Done!!")