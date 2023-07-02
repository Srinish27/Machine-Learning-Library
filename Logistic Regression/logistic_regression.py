# -*- coding: utf-8 -*-
"""logistic_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kbdIBJ6ppGfiE0No19ZFga1iCHrN7Se3
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LogisticRegression:
  def __init__(self, alpha=0.5, lam=0.01, num_iters=150):
    ''' '__init__' method takes arguments as Learning Rate(alpha), Regularization Constant(lam), Number of iterations(num_iters).
        All of these values have been initialized by default values, but can be changed when required'''
    self.alpha = alpha
    self.lam = lam
    self.num_iters = num_iters
  
  def sigmoid(self, z):
    ''' 'sigmoid' method takes z as argument and returns sigmoid value of z.'''
    return 1/(1 + np.exp(-1*z))

  def scale(self,X):
    ''' 'scale' method takes X as argument
    Applies feature scaling by standardizing the data and returns the modified data.'''
    m, n = X.shape
    for i in range(n):
      X[:,i] = (X[:,i] - np.mean(X[:,i]))/(np.std(X[:,i]) + 0.00001)
    return X

  def hypothesis(self, X, theta):
    ''' 'hypothesis' method takes X, theta as arguments.
    Calculates and returns hypothesis values'''
    h = (self.sigmoid(X@theta.T))
    return h

  def cost(self, X, y, theta):
    ''' 'cost' method takes X, y, theta as arguments and returns cost value.'''
    m, n = X.shape
    h = self.hypothesis(X,theta)
    cost = (-1/m)*np.sum(y*np.log(h + 0.00001) + (1-y)*np.log(1-h + 0.00001)) + (self.lam/(2*m))*(np.sum(theta[:,1:]**2))
    return cost

  def fit(self, X, y, n_cls):
    ''' 'fit' method takes X, y, n_cls(Number of classes) as arguments.
    Applies Gradient Descent algorithm and updates parameters theta '''
    
    # Feature Scaling
    X = self.scale(X)
    X = np.hstack((np.ones((len(X),1)),X))    # Adds bias column.

    m, n = X.shape
    self.n_cls = n_cls

    # Convert y values to y_cls(One vs All matrix) 
    y_cls = np.zeros((m,self.n_cls))
    for i in range(m):
      y_cls[i,y[i]] = 1
    
    # Initializing some useful variables
    # 'J.hist' and 'iters' keeps track of cost with each iteration.
    self.J_hist = []
    self.iters = []

    # Intializing parameter vector theta    
    self.theta = np.zeros((self.n_cls,n))

    # Applying Gradient Descent algorithm.
    for i in range(self.num_iters):
      # Parameter update
      theta_temp = self.theta
      theta_temp[:,0:1] = 0
      h = self.hypothesis(X,self.theta)
      self.theta = self.theta - (self.alpha/m)*((h-y_cls).T@X + (self.lam*theta_temp))
      # Saving cost value with every iteration.
      self.J_hist.append(self.cost(X,y_cls,self.theta))
      self.iters.append(i)

  def plot(self):
    ''' 'plot' method takes no arguments.
    Plots the learning curve (Cost vs Number of Iterations)'''
    plt.plot(self.iters,self.J_hist)
    plt.xlabel("Number Of Iterations")
    plt.ylabel("Cost Function")
    plt.title("Cost Function vs Iteration")

  def predict(self,X):
    ''' 'predict' method takes X as arguments.
    Calculates and returns the predicted values given by the trained model.'''
    X = self.scale(X)
    X = np.hstack((np.ones((len(X),1)),X))
    y_pred = self.hypothesis(X,self.theta)
    y_pred = np.argmax(y_pred, axis=1).reshape(len(y_pred),1)
    return y_pred

  def predict_prob(self,X):
    ''' 'predict' method takes X as arguments.
    Calculates and returns the probability of the sample for each class in the model.'''
    X = self.scale(X)
    X = np.hstack((np.ones((m,1)),X))
    y_pred_prob = self.hypothesis(X,self.theta)
    return y_pred_prob

  def accuracy(self,y,y_pred):
    '''  'accuracy' method takes y(True values), y_pred(Predicted values) and returns the accuracy of the trained model'''
    return (np.mean(y==y_pred))*100

  def score(self, y, y_pred):
    ''' 'score' method takes y, y_pred as arguments.
    Calculates the y_mean and R2 score(Coefficient of determination), and returns R2 score'''
    score = 1 - ((y - y_pred)**2).sum()/((y - y.mean())**2).sum()
    return score