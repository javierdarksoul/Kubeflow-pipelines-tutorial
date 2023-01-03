from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Output,
    Artifact,
)
@component(
)
def build_src(source: Output[Artifact]):
    import tarfile
    code = '''import torch \n\
class my_nn(torch.nn.Module):\n\
    def __init__(self):\n\
        super(my_nn,self).__init__()\n\
        self.linear1= torch.nn.Linear(28*28,256)\n\
        self.linear2= torch.nn.Linear(256,64)\n\
        self.linear3= torch.nn.Linear(64,32)\n\
        self.linear4= torch.nn.Linear(32,10)\n\
        self.soft = torch.nn.Softmax()\n\
        self.relu= torch.nn.ReLU()\n\
    def forward(self,x):\n\
        x=self.relu(self.linear1(x))\n\
        x=self.relu(self.linear2(x))\n\
        x=self.relu(self.linear3(x))\n\
        return self.soft(self.linear4(x))\n\
'''
    text_file = open("nn.py", "w")
    text_file.write(code)
    text_file.close()
    
    with tarfile.open(source.path, "w") as tar:
            tar.add("nn.py")