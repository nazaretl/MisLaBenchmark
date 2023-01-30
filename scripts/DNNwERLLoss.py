import torch
import numpy as np
from torch import nn, optim
import sys, importlib
import pandas as pd
#import NN
#importlib.reload(sys.modules['NN'])
from NN import Net, elr_loss, prepare_layers



def DNNwERLLoss(X,y,noisyLabels,beta,plusLayers,learningRate, loss):

    net = Net(X,y,noisyLabels, plusLayers)
    optimizer = optim.Adam(net.parameters(), lr=learningRate)

    if loss=="CrossEntropy":
        criterion = nn.CrossEntropyLoss()
    else:
        criterion = elr_loss(num_examp = net.X_train.shape[0],num_classes=net.num_classes,beta = beta)
    
    for epoch in range(2000):
        #print(epoch)
        y_pred = torch.squeeze(net(net.X_train))
        y_test_pred = torch.squeeze(net(net.X_test))

        if loss=="CrossEntropy":

            train_loss = criterion(y_pred,net.y_train)
            test_loss = criterion(y_test_pred, net.y_test)
        else:

            train_loss = criterion(net.indexTrain,y_pred,net.y_train)
            test_loss = criterion(net.indexTest,y_test_pred, net.y_test)

        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
        net.metrics(y_pred, y_test_pred,train_loss,test_loss)


    #pd.DataFrame(net.Metrics1,columns = ['train_loss', 'test_loss', 'train_acc', 'test_acc']).plot()
    #pd.DataFrame(net.Metrics2,columns = ['p_train', 'r_train', 'p_test', 'r_test']).plot()



    BestModelE = Net(X,y,noisyLabels,plusLayers )
    BestModelE.load_state_dict(net.state_dict())
    BestModelE.eval()
   # BestModelE(net.X_test)
    y_final_pred = BestModelE(net.X)#.argmax(axis = 1)
    filteredNoiseInd = np.where(net.y!=y_final_pred.argmax(axis = 1))[0]
    
    return pd.Series(filteredNoiseInd), net.Metrics1

