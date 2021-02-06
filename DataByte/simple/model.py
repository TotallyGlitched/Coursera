import pandas as pd
import numpy as np

df = pd.read_csv('Iris.csv')

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

df['species'] = le.fit_transform(df['species'])

from sklearn.model_selection import train_test_split
X = df.drop(columns=['species'])
Y = df['species']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

def training_model():
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=4)

    model.fit(x_train, y_train)














# import pandas as pd 
# import numpy as np 
# import pickle 
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC 
# from sklearn.neighbors import KNeighborsClassifier


# data = pd.read_csv('iris.csv')

# # x = np.array(data.iloc[:, 0:4])
# # y = np.array(data.iloc[:, 4:])

# le = LabelEncoder()
# data['species'] = le.fit_transform(data['species'])

# x = data.drop(columns=['species'])
# y = data['species']

# y = le.fit_transform(y)


# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

# model = KNeighborsClassifier()
# iris_model = model.fit(x_train, y_train)

# print(iris_model)
# # sv=SVC(kernel='linear').fit(x_train, y_train.ravel())

# # pickle.dump(sv, open('iriss.pkl', 'wb'))
