import pandas as pd 
from sklearn.datasets import load_iris
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('model/iris.csv')

X=np.array(data.iloc[:, 0:4])
y=np.array(data.iloc[:, 4:])

# print(data.head())

le=LabelEncoder()
y=le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

def training_model():
    sv=SVC(kernel='linear').fit(X_train, y_train.ravel())
    print(sv)
    return sv

print(training_model())



# def training_model():

#     svm = SVC(kernel='rbf', random_state=0, gamma=.10, C=1.0)
#     trained_model = svm.fit(X_train, y_train.ravel())
#     # print('The accuracy of the SVM classifier on training data is {:.2f}'.format(svm.score(X_train, y_train)))
#     # print('The accuracy of the SVM classifier on test data is {:.2f}'.format(svm.score(X_test, y_test)))
#     return trained_model
#     # model = DecisionTreeClassifier()
#     # trained_model = model.fit(X_train, y_train)
#     # return trained_model
# training_model()
# # print(training_model())