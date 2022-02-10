from sklearn.model_selection import train_test_split

from cleanlab.classification import LearningWithNoisyLabels
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def runPU(X,y, targetData, test_size =0.7):
  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size)

    pu_class = 0
    # Should be 0 or 1. Label of class with NO ERRORS. (e.g., P class in PU)
    lnl = LearningWithNoisyLabels(clf=LinearDiscriminantAnalysis(), pulearning=pu_class)
    lnl.fit(X=X_train, s=y_train)
    predicted_test_labels = lnl.predict(X_test)
    a = len(predicted_test_labels[predicted_test_labels!=y_test])/len(y_test)
    print('Fraction of identified mislabellings:', a)
    targetLabels = lnl.predict(targetData)

    return targetLabels

