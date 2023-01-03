import torch 
class my_nn(torch.nn.Module):
    def __init__(self):
        super(my_nn,self).__init__()
        self.linear1= torch.nn.Linear(28*28,256)
        self.linear2= torch.nn.Linear(256,64)
        self.linear3= torch.nn.Linear(64,32)
        self.linear4= torch.nn.Linear(32,10)
        self.soft = torch.nn.Softmax()
        self.relu= torch.nn.ReLU()
    
    def forward(self,x):
        
        x=x.reshape(-1,28*28)
        x=self.relu(self.linear1(x))
        x=self.relu(self.linear2(x))
        x=self.relu(self.linear3(x))
        return self.soft(self.linear4(x))

