import torch
class attentionLayer(torch.nn.Module):
    def __init__(self,in_channels ,out_channels, kernel_size = 3, stride=1, padding=1):
        super(attentionLayer,self).__init__()
        self.padding=padding
        self.stride = stride
        self.in_channels= in_channels
        self.out_channels= out_channels
        self.kernel_size=kernel_size
        self.conv_query = torch.nn.Conv2d(in_channels,out_channels,1)
        self.conv_keys = torch.nn.Conv2d(in_channels,out_channels,1)
        self.conv_values= torch.nn.Conv2d(in_channels,out_channels,1)
        self.unfold=torch.nn.Unfold(kernel_size=(3,3),padding=padding,stride=stride)
        self.soft = torch.nn.Softmax(dim=-1)
        self.pad= torch.nn.ReflectionPad2d(padding)
    
    def forward(self,input_):
        batch,channels,h,w = input_.size()
        padded_input = self.pad(input_)
        query = self.conv_query(input_)
        keys = self.conv_keys(padded_input)
        values = self.conv_values(padded_input)
        keys=(  keys.unfold(2,self.kernel_size,self.stride).unfold(3,self.kernel_size,self.stride)).reshape(batch,self.out_channels*h*w,self.kernel_size*self.kernel_size)
        values=(  values.unfold(2,self.kernel_size,self.stride).unfold(3,self.kernel_size,self.stride)).reshape(batch,self.out_channels*h*w,self.kernel_size*self.kernel_size)
        query= query.reshape(batch,-1,1)
        qdotk = self.soft(query*keys)
        qdotk_dotv = qdotk * values 
        return qdotk_dotv.sum(-1).view(batch,self.out_channels,h,w)