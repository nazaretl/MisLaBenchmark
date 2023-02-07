  

from torch.nn import Softmax
import torch.nn.functional as F
from torch import nn, optim
import numpy as np
import torch

from sklearn.model_selection import train_test_split


def prepare_layers(X, n_output,plusLayers):
    nLayers = max(int(X.shape[1]/10),3)+plusLayers
    n = X.shape[1]

    ns = np.linspace(n_output, n, nLayers,endpoint = True).astype(int)
    for i,j in enumerate(ns):
        exec(f'n{len(ns)-i} = j')

    ns = list(reversed(ns))
    layer_list = []
    for i in range(len(ns)-1):
        n1 = ns[i]
        n2 = ns[i+1]
        layer_list.append(nn.Linear(n1, n2))
    return layer_list

def calculate_accuracy(y_true, y_pred):
    predicted = y_pred.ge(.5).view(-1)
    return (y_true == predicted).sum().float() / len(y_true)

def round_tensor(t, decimal_places=3):
    return round(t.item(), decimal_places)


def precisionAndRecall(noisyLabels, predictions, cleanLabels):
    foundEr = (np.where(noisyLabels != predictions))[0]
    trueEr = np.where(noisyLabels!=cleanLabels)[0]
    if ((len(foundEr)==0) | (len(trueEr)==0)):
        recall, precision = 0, 0
    else:     
        recall = len((np.intersect1d(foundEr, trueEr)))/len(trueEr)
        precision = len((np.intersect1d(foundEr, trueEr)))/len(foundEr)
    return precision, recall



# https://github.com/shengliu66/ELR
# ISSUE criterion.target are predictions? not normalized criterion.target.argmax()!=y_pred.argmax()

class elr_loss(nn.Module):
    def __init__(self, num_examp,num_classes=2,lam=3,beta=0.6):

        super(elr_loss, self).__init__()
        self.num_classes = num_classes
       # self.USE_CUDA = torch.cuda.is_available()
        self.target = torch.zeros(num_examp,num_classes)
        self.beta = beta
        self.lam = lam
        

    def forward(self, index, output, label):
            r"""Early Learning Regularization.
             Args
             * `index` Training sample index, due to training set shuffling, index is used to track training examples in different iterations.
             * `output` Model's logits, same as PyTorch provided loss functions.
             * `label` Labels, same as PyTorch provided loss functions.
             """
            y_pred = F.softmax(output,dim=1)
            y_pred = output
            y_pred = torch.clamp(y_pred, 1e-4, 1.0-1e-4)
            y_pred_ = y_pred.data.detach()
            self.target[index] = self.beta * self.target[index] + (1-self.beta) * ((y_pred_)/(y_pred_).sum(dim=0,keepdim=True))
            ce_loss = F.cross_entropy(output, label)
            elr_reg = ((1-(self.target[index] * y_pred).sum(dim=1)).log()).mean()
            final_loss = ce_loss +  self.lam *elr_reg
            return  final_loss
    

    
# https://curiousily.com/posts/build-your-first-neural-network-with-pytorch/
# https://blog.paperspace.com/pytorch-101-advanced/ 

class Net(nn.Module):
    def __init__(self,X,y,noisyLabels, plusLayers):
        super(Net, self).__init__()    
        
        
        X_train, X_test, y_train, y_test = train_test_split(X, noisyLabels, test_size=0.2)
        self.indexTrain = list(range(X_train.shape[0]))
        self.indexTest = list(range(X_test.shape[0]))

        self.num_classes = len(y.unique())
        layer_list = prepare_layers(X, self.num_classes,plusLayers)
        self.trainInd = y_train.index.to_list()
        self.testInd = y_test.index.to_list()
        cleanLabels_train = y[self.trainInd].reset_index(drop = True)
        cleanLabels_test = y[self.testInd].reset_index(drop = True)


        self.X_train = torch.from_numpy(X_train.to_numpy()).float()
        self.y_train = torch.squeeze(torch.from_numpy(y_train.to_numpy()).long())
        self.X_test = torch.from_numpy(X_test.to_numpy()).float()
        self.y_test = torch.squeeze(torch.from_numpy(y_test.to_numpy()).long())
        self.cleanLabels_train = torch.squeeze(torch.from_numpy(cleanLabels_train.to_numpy()).long())
        self.cleanLabels_test = torch.squeeze(torch.from_numpy(cleanLabels_test.to_numpy()).long())
        
        self.X = torch.from_numpy(X.to_numpy()).float()
        self.y = torch.squeeze(torch.from_numpy(y.to_numpy()).long())
  
        
        self.layers = nn.ModuleList(layer_list)
        
        self.Metrics1 = []
        self.Metrics2 = []

        
    def forward(self, x):
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
          
        return F.softmax(self.layers[-1](x),dim=1)

    ## obsolete 
    def backward(self,):
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
        
    def metrics(self,y_pred, y_test_pred,train_loss,test_loss, index = True ):


            
        train_acc = calculate_accuracy(self.y_train, y_pred.argmax(axis = 1))
        # test everything on the noisy data 
      #  test_acc = calculate_accuracy(self.cleanLabels_test, y_test_pred.argmax(axis = 1))
        test_acc = calculate_accuracy(self. y_test, y_test_pred.argmax(axis = 1))
        self.Metrics1.append([round_tensor(train_loss), round_tensor(test_loss),
                            round_tensor(train_acc),round_tensor(test_acc)])
        
        p_train, r_train = precisionAndRecall(self.y_train,y_pred.argmax(axis = 1),self.cleanLabels_train)
        p_test, r_test = precisionAndRecall(self.y_test,y_test_pred.argmax(axis = 1),self.cleanLabels_test)
    
        self.Metrics2.append([round(num, 4) for num in [p_train, r_train, p_test, r_test]])
    


