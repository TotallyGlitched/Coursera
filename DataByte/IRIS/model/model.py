# import numpy as np
# import pandas as pd
# import pickle
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC

# df=pd.read_csv("iris.csv")

# X=np.array(df.iloc[:, 0:4])
# y=np.array(df.iloc[:, 4:])

# le=LabelEncoder()
# y=le.fit_transform(y)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# sv=SVC(kernel='linear').fit(X_train,y_train)
# LR_reg=LogisticRegression() 
# svc_model=SVC()
# LR_reg=lin_reg.fit(X_train,y_train)
# SVC_model=svc_model.fit(X_train,y_train)
# print(SVC_model)
