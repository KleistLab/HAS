from scipy import optimize
import numpy as np

def f_old(x, mu):
    N = len(x)
    A = np.ones((N,N)) - np.identity(N)
    B = np.diag(x)
    return(np.matmul(B, np.matmul(A,x)) - mu)

def get_rates_old(mu):
    N = len(mu)
    sol = optimize.root(f, mu, args = mu, method='hybr')
    r = sol.x
    return(r)


def f(x, unique, counts):
    #unique, counts = np.unique(mu, return_counts=True)
    N = len(unique)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,:] = counts
        A[i,i] -= 1
    B = np.diag(x)
    return(np.matmul(B, np.matmul(A,x)) - unique)

def get_rates(mu):
    unique, counts = np.unique(mu, return_counts=True)
    guess = np.ones(len(unique))
    sol = optimize.root(f, guess, args = (unique, counts), method='hybr')
    r = sol.x
    
    res_dict = {}
    
    for i in range(len(unique)):
        res_dict[unique[i]] = r[i]
    
    lambda_vec = np.zeros(len(mu))
    for i in range(len(mu)):
        lambda_vec[i] = res_dict[mu[i]]
    
    
    return(lambda_vec)
