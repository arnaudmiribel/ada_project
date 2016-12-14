# -*- coding: utf-8 -*-

"""
Helpers function
"""

import numpy as np
import matplotlib.pyplot as plt

#########################################################################################
################       data-processing : building features          #####################
#########################################################################################


def dummy_encode(df):
    """ applies dummy encoding to a dataframe """
    
    from sklearn.preprocessing import LabelEncoder
    columnsToEncode = list(df.select_dtypes(include=['category','object']))
    le = LabelEncoder()
    for feature in columnsToEncode:
        try:
            df[feature] = le.fit_transform(df[feature])
        except:
            print('error encoding '+feature)
    return df


def build_poly(x, degree):
    """polynomial basis functions for input data x, for j=0 up to j=degree."""
    poly = np.ones((len(x), 1))
    for deg in range(1, degree+1):
        poly = np.c_[poly, np.power(x, deg)]
    return poly


#########################################################################################
################           data modelling - regressions             #####################
#########################################################################################


def calculate_mae(e):
    """Calculate the mae for vector e."""
    return np.mean(np.abs(e))


def compute_loss(y, tx, w):
    """Calculate the loss.

    Here we calculate the loss using mae
    """
    e = y - tx.dot(w)
    return calculate_mae(e)


def standardize(x, mean_x=None, std_x=None):
    """Standardize the original data set."""
    if mean_x is None:
        mean_x = np.mean(x, axis=0)
    x = x - mean_x
    if std_x is None:
        std_x = np.std(x, axis=0)
    x[:, std_x>0] = x[:, std_x>0] / std_x[std_x>0]
    
    tx = np.hstack((np.ones((x.shape[0],1)), x))
    print("standardized")
    return tx, mean_x, std_x


def compute_gradient(y, tx, w):
    """Compute the gradient."""
    err = y - tx.dot(w)
    grad = -tx.T.dot(err) / len(err)
    return grad, err


def gradient_descent(y, tx, initial_w, max_iters, gamma):
    """Gradient descent algorithm."""
    # Define parameters to store w and loss
    ws = [initial_w]
    losses = []
    w = initial_w
    for n_iter in range(max_iters):
        # compute loss, gradient
        grad, err = compute_gradient(y, tx, w)
        loss = calculate_mae(err)
        # gradient w by descent update
        w = w - gamma * grad
        # store w and loss
        ws.append(w)
        losses.append(loss)
        if n_iter%1000==0:
            print("Gradient Descent({bi}/{ti}): loss={l}".format(
                  bi=n_iter, ti=max_iters - 1, l=loss))
    return losses, ws


def split_data(x, y, ratio, seed=1):
    """split the dataset based on the split ratio."""
    # set seed
    np.random.seed(seed)
    # generate random indices
    num_row = len(y)
    indices = np.random.permutation(num_row)
    index_split = int(np.floor(ratio * num_row))
    index_tr = indices[: index_split]
    index_te = indices[index_split:]
    # create split
    x_tr = x[index_tr]
    x_te = x[index_te]
    y_tr = y[index_tr]
    y_te = y[index_te]
    return x_tr, x_te, y_tr, y_te


def ridge_regression(y, tx, lambda_):
    """implement ridge regression."""
    aI = 2 * tx.shape[0] * lambda_ * np.identity(tx.shape[1])
    a = tx.T.dot(tx) + aI
    b = tx.T.dot(y)
    return np.linalg.solve(a, b)

    
def build_k_indices(y, k_fold, seed):
    """build k indices for k-fold."""
    num_row = y.shape[0]
    interval = int(num_row / k_fold)
    np.random.seed(seed)
    indices = np.random.permutation(num_row)
    k_indices = [indices[k * interval: (k + 1) * interval] for k in range(k_fold)]
    return np.array(k_indices)

    
def cross_validation(y, x, k_indices, k, lambda_, degree):
    """return the loss of ridge regression."""
    # get k'th subgroup in test, others in train
    te_indice = k_indices[k]
    tr_indice = k_indices[~(np.arange(k_indices.shape[0]) == k)]
    tr_indice = tr_indice.reshape(-1)
    y_te = y[te_indice]
    y_tr = y[tr_indice]
    x_te = x[te_indice]
    x_tr = x[tr_indice]
    # form data with polynomial degree
    tx_tr = build_poly(x_tr, degree)
    tx_te = build_poly(x_te, degree)
    # ridge regression
    w = ridge_regression(y_tr, tx_tr, lambda_)
    # calculate the loss for train and test data
    loss_tr = compute_loss(y_tr, tx_tr, w)
    loss_te = compute_loss(y_te, tx_te, w)
    return loss_tr, loss_te


def cross_validation_visualization(param, lambdas, mse_tr, mse_te):
    """visualization the curves of mae_tr and mae_te."""
    plt.semilogx(lambdas, mse_tr, marker=".", color='b', label='train error')
    plt.semilogx(lambdas, mse_te, marker=".", color='r', label='test error')
    plt.xlabel(param)
    plt.ylabel("mae")
    plt.title("cross validation")
    plt.legend(loc=2)
    plt.grid(True)
    plt.savefig("cross_validation")
    
def cross_validation_demo_degrees(x_train, y, degrees, lambda_=0.1, k_fold=4):
    seed = 1
    # split data in k fold
    k_indices = build_k_indices(y, k_fold, seed)
    # define lists to store the loss of training data and test data
    mae_tr = []
    mae_te = []
    # cross validation
    for degree_ in degrees:
        mae_tr_tmp = []
        mae_te_tmp = []
        for k in range(k_fold):
            loss_tr, loss_te = cross_validation(y, x_train, k_indices, k, lambda_, degree_)
            mae_tr_tmp.append(loss_tr)
            mae_te_tmp.append(loss_te)
        mae_tr.append(np.mean(mae_tr_tmp))
        mae_te.append(np.mean(mae_te_tmp))
        
    cross_validation_visualization("degree", degrees, mae_tr, mae_te)

    
def cross_validation_demo_lambdas(x_train, y_train, lambdas, degree=1, k_fold=4):
    seed = 1
    k_fold = 4
    # split data in k fold
    k_indices = build_k_indices(y_train, k_fold, seed)
    # define lists to store the loss of training data and test data
    mae_tr = []
    mae_te = []
    # cross validation
    for lambda_ in lambdas:
        mae_tr_tmp = []
        mae_te_tmp = []
        for k in range(k_fold):
            loss_tr, loss_te = cross_validation(y_train, x_train, k_indices, k, lambda_, degree)
            mae_tr_tmp.append(loss_tr)
            mae_te_tmp.append(loss_te)
        mae_tr.append(np.mean(mae_tr_tmp))
        mae_te.append(np.mean(mae_te_tmp))

    cross_validation_visualization("lambda", lambdas, mae_tr, mae_te)
    
    
def dimension_reduction(X, dim):  
    """reduces dimension of X in dim dimensions using PCA"""
    from sklearn.decomposition import PCA
    model = model(n_components=dim)
    model.fit(X)
    print(model.explained_variance_ratio_)
    X_reducted = model.transform(X)
    return X_reducted