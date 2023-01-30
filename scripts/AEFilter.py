from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.pipeline import Pipeline
import logging

logging.getLogger("tensorflow").setLevel(logging.ERROR)

import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from utils import confusionMatrixScikit

def prepareLayers(X,n_max=4):
    n_output = 2
    #print(X.shape[1])
    #n_max = 4
    nLayers = max(int(X.shape[1]/10),n_max)+1
    n = max(round(X.shape[1]),n_max+20)
    ns = np.linspace(n_output, n, nLayers,endpoint = False).astype(int)
    #layers = [round(X.shape[1])]
    ns = list(ns) + [X.shape[1]]
    ns = list(reversed(ns))
    layers = ns +list(reversed(ns))[1:]
    #print(layers)

    return layers

def mad_score(points):
    """https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm """
    m = np.median(points)
    ad = np.abs(points - m)
    mad = np.median(ad)
    
    return 0.6745 * ad / mad


def compute_cm(THRESHOLD,reconstructions, X, y_noisy, y_clean):
    #THRESHOLD = 3.5
    noiseInd = y_noisy[y_noisy!=y_clean].index
    #reconstructions = autoencoder.predict(X,verbose = 0)
    mse = np.mean(np.power(X - reconstructions, 2), axis=1)
    z_scores = mad_score(mse)

    noiseInd = y_clean[y_clean!=y_noisy].index
    foundNoiseInd = np.where(z_scores > THRESHOLD)[0]
    cm = confusionMatrixScikit(y_clean,noiseInd,foundNoiseInd)[1]
    cm['Retrieved'] = (len(foundNoiseInd)/reconstructions.shape[0])
    return foundNoiseInd, cm


def AEFilter(X,noisyLabels,y):
    ## https://www.kaggle.com/code/robinteuwens/anomaly-detection-with-auto-encoders/notebook

   


    pipeline = Pipeline(
        [
            #('normalizer', Normalizer()),
                         ('scaler', MinMaxScaler())])

    input_dim = X.shape[1]
    BATCH_SIZE = 256
    EPOCHS = 1000

    X_temp = X

    X_temp['Label'] = noisyLabels

    pipeline.fit(X_temp);
    #X_transformed = X_temp
    X_transformed = pipeline.transform(X_temp)

    #X_transformed = np.column_stack((X_transformed , noisyLabels.values))


    #X_transformed = X.values
    ff = []
    #n_max in [1,2,3,4,5,6,7,8,9,10]:
    n_max = 4
    layer_sizes = prepareLayers(X,n_max)
    #layer_sizes = ns + list(reversed(ns))[1:]
    print(n_max,layer_sizes)
    # train // validate - no labels since they're all clean anyway
    X_train_transformed,X_test_transformed, y_train_noisy, y_test_noisy  = train_test_split(X_transformed, noisyLabels,
                                           test_size=0.3, 
                                           random_state=1234)



    y_test_clean = y[y_test_noisy.index].reset_index(drop = True)
    y_train_clean = y[y_train_noisy.index].reset_index(drop = True)

    y_test_noisy = y_test_noisy.reset_index(drop = True)
    y_train_noisy = y_train_noisy.reset_index(drop = True)

   # noiseIndTest = y_test_noisy.tr
   # noiseIndTrain = y_train_noisy.index


    autoencoder = tf.keras.models.Sequential(

        [tf.keras.layers.Dense(layer_size, activation = 'elu') 
                                        for layer_size in layer_sizes]

    )

    # https://keras.io/api/models/model_training_apis/
    autoencoder.compile(optimizer="adam", 
                        loss="mse",
                        metrics=["acc"])

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='loss',
        min_delta=0.0001,
        patience=10,
        verbose=0, 
        mode='min',
        restore_best_weights=True
    )
    cb = [early_stop]
    history = autoencoder.fit(
        X_train_transformed, X_train_transformed,
        shuffle=True,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=cb,
      #  validation_data=(X_test_transformed, X_test_transformed),
        verbose = 0
    );


    # pass the transformed test set through the autoencoder to get the reconstructed result
    th = 1
    reconstructions = autoencoder.predict(X_transformed, verbose = 0)
    foundNoiseInd, cm = compute_cm(th,reconstructions = reconstructions, X = X_transformed, y_noisy = noisyLabels, y_clean = y)
    
    cms = pd.DataFrame()
    li = [0.2,0.5,1,2,3,4,5,6,7,8,9,10]
    li = list(np.linspace(0,15,30))
    #li = [6]
    
    reconstructions = autoencoder.predict(X_test_transformed, verbose = 0)

    for th in li:   
        
        cm = compute_cm(th,reconstructions = reconstructions, X = X_test_transformed, y_noisy = y_test_noisy, y_clean = y_test_clean)[1]
        cms = cms.append(cm)
    cms.index = li
    
    return pd.Series(foundNoiseInd), cms.to_dict()
    
    