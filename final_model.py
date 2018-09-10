# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 02:57:22 2018

@author: Dillon
"""
import numpy as np
import pandas as pd
# Import function to create training and test set splits
from sklearn.cross_validation import train_test_split
# Import function to automatically create polynomial features! 
from sklearn.preprocessing import PolynomialFeatures
# Import Linear Regression and a regularized regression function
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.linear_model import LassoLarsIC
# Finally, import function to make a machine learning pipeline
from sklearn.pipeline import make_pipeline

# Alpha (regularization strength) of LASSO regression
lasso_eps = 0.0001
lasso_nalpha=20
lasso_iter=50000
# Min and max degree of polynomials features to consider
degree_min = 1
degree_max = 3
# Test/train split
#main = md.drop(['CF_ID','Committee_Name','Name','Office'],axis=1)
X = main.drop(['Percent'],axis=1)
Y = main.Percent
X_train, X_test, y_train, y_test = train_test_split(X, Y,test_size=.8)

# Make a pipeline model with polynomial transformation and LASSO regression with cross-validation, run it for increasing degree of polynomial (complexity of the model)
for degree in range(degree_min,degree_max+1):
    model = make_pipeline(
            PolynomialFeatures(degree, interaction_only=False), 
            LassoCV(eps=lasso_eps,
                    n_alphas=lasso_nalpha,
                    max_iter=lasso_iter,
                    normalize=True,
                    cv=20,n_jobs=-1,verbose=True,tol=0.001))
    
    
model.fit(X_train,y_train)
test_pred = np.array(model.predict(X_test))
RMSE=np.sqrt(np.sum(np.square(test_pred-y_test)))
test_score = model.score(X_test,y_test)
    
    