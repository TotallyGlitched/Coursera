import pandas as pd 
from sklearn.datasets import load_iris
import numpy as np

import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


data = pd.read_csv('model/iris.csv')
# print(data.DESCR)

x=np.array(data.iloc[:, 0:4])
y=np.array(data.iloc[:, 4:])

# X = pd.DataFrame(data.data, columns=(sepal_length, sepal_width, petal_length, petal_width))
# y = pd.DataFrame(data.target, columns=['Species'])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

from sklearn.tree import DecisionTreeClassifier

def training_model():
    model = DecisionTreeClassifier()
    trained_model = model.fit(X_train, y_train)
    return trained_model
