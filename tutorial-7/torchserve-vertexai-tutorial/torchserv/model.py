import torch
import attentionLayer as attentionLayer

class attentionModel(torch.nn.Module):
    def __init__(self):
        super(attentionModel,self).__init__()
        self.mpool= torch.nn.MaxPool2d(2)
        self.attention1 = attentionLayer.attentionLayer(1,16)
        self.attention2 = attentionLayer.attentionLayer(16,32)
        self.attention3 = attentionLayer.attentionLayer(32,8)
        self.linear1=torch.nn.Linear(24*3,128)
        self.linear2=torch.nn.Linear(128,64)
        self.linear3=torch.nn.Linear(64,10)
        self.relu= torch.nn.ReLU()
        self.soft= torch.nn.Softmax(dim=-1)

    def forward(self,x):
    
        x=self.mpool(self.relu(self.attention1(x)))
        x=self.mpool(self.relu(self.attention2(x)))
        x=self.mpool(self.relu(self.attention3(x)))
        x=x.view(x.size()[0],-1)
        x=self.relu(self.linear1(x))
        x=self.relu(self.linear2(x))
        x=self.soft(self.linear3(x))
        return x
