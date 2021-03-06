import numpy as np
import skcuda.linalg as linalg
import skcuda.misc
import pycuda.cumath

from crow.transfer.gputransfer import *
### Selective functions ###

def dot(A, B, C, transa='N', transb='N'):
    linalg.dot(A, B, out=C, transa=transa, transb=transb)
    return C

def bigsparse(X, B, C, transa='N', transb='N'):
    # TODO: transpose B
    #if transb == 'T':
    #    B = linalg.transpose(B)
    if transa == 'T':
        raise Exception("Transposing sparse matrix not supported")
    C = X.mm(B)
    return C

def load_kernel():
    X = gpuzeros(10,10)
    Y = gpuones(10,10)
    Z = gpuzeros(10,10)
    kernel(X, Y, Z)

### Dynamic functions ###

def multiply(A, B, C):
    return skcuda.misc.multiply(A, B)

def divide_safe(A, B, C):
    if B.shape[0] == 1:
        D = np.divide(A.get(), B.get() + EPSILON)
        C = togpu(D)
    else:
        #C = skcuda.misc.divide(A, B)
        kern_div(A, B, C)
    
    return C

def axis_sum(X, C, transa='N'):
    if transa == 'T':
        return skcuda.misc.sum(X, axis=1, out=C)
    else:
        return skcuda.misc.sum(X, axis=0, out=C)

def kernel(A, B, C, transa='N'):
    if transa == 'T':
        kern(linalg.transpose(A), B, C)
    else:
        kern(A, B, C)

def transpose(A):
    return linalg.transpose(A)

def sub(A, B, C):
    return skcuda.misc.subtract(A, B)

def add(A, B, C):
    return skcuda.misc.add(A, B)

def sum_all(A, C):
    e = A.get().sum()
    C = C.get()
    C[0,0] = e
    C = togpu(C)
    return C

def sqrt(A, C):
    pycuda.cumath.sqrt(A, out=C)
    return C

FUNCTIONS = {
    '_multiply': multiply,
    '_divide': divide_safe,
    '_axis_sum': axis_sum,
    '_tr': transpose,
    '_add': add,
    '_sub': sub,
    '_sum': sum_all,
    'kernel': kernel,
    '_sqrt': sqrt,
}