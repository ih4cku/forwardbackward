#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

T = 3 # time num
S = 2 # state num
N = 2 # observation num

# init value
I = [0.1, 0.2] 

# pair-wise value
A = np.array([ 
    [1.2, 3.4], 
    [5.6, 7.8] ])

# position value
B = np.array([ 
    [1.1, 2.2],
    [4.4, 5.5] ])

# position value index
O = [1, 0, 1]

def pairwise(i, j):
    """
    pairwise potential function
    """
    if i==-1:
        return I[j]
    return A[i, j]

def position(s, t):
    """
    positional potential function
    """
    return B[s, O[t]]
    
def potential(s1, s2, t):
    """
    local potential function
    """
    print 'Phi(%d, %d, %d)' % (s1, s2, t)
    return pairwise(s1, s2)*position(s2, t)

def alpha(s, t):
    if t==0:
        return potential(-1, s, t)

    acc = 0.0
    for ss in range(S):
        acc += alpha(ss, t-1)*potential(ss, s, t)
    return acc

def beta(s, t):
    if t==T-1:
        return 1.0

    if t==-1:
        return potential(-1, s, t+1)*beta(s, t+1)

    acc = 0.0
    for ss in range(S):
        acc += beta(ss, t+1)*potential(s, ss, t+1)
    return acc

# exhaustive 
def seqPotential(seq):
    """
    state begin at 1
    """
    acc = 1.0
    for t in range(len(seq)):
        if t==0:
            s1 = -1
        else:
            s1 = seq[t-1]
        s2 = seq[t]
        acc *= potential(s1, s2, t)
    return acc


def Exhaustive():
    Z = 0.0
    i = 1
    for s1 in range(S):
        for s2 in range(S):
            for s3 in range(S):
                Z += seqPotential([s1, s2, s3])
                i += 1
    return Z

def Forward():
    Z = 0.0
    for s in range(S):
        Z += alpha(s, T-1)
    return Z


def Backward():
    Z = 0.0
    for s in range(S):
        Z += beta(s, -1)
    return Z

print '----------'
v1 = Exhaustive()
print '----------'
v2 = Forward()
print '----------'
v3 = Backward()
print '----------'
print v1
print v2
print v3
print '----------'
