#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 23:57:22 2016

@author: dan
"""
from scipy import ndimage
from astropy import stats

def rebin(a, *args):
    '''rebin ndarray data into a smaller ndarray of the same rank whose dimensions
    are factors of the original dimensions. eg. An array with 6 columns and 4 rows
    can be reduced to have 6,3,2 or 1 columns and 4,2 or 1 rows.
    example usages:
    >>> a=rand(6,4); b=rebin(a,3,2)
    >>> a=rand(6); b=rebin(a,2)
    '''
    shape = a.shape
    lenShape = len(shape)
    factor = np.asarray(shape)/np.asarray(args)
    evList = ['a.reshape('] + \
             ['args[%d],factor[%d],'%(i,i) for i in range(lenShape)] + \
             [')'] + ['.sum(%d)'%(i+1) for i in range(lenShape)] + \
             ['/factor[%d]'%i for i in range(lenShape)]
    print(''.join(evList))
    return eval(''.join(evList))
    
def lingray(x, a=None, b=None):
    """
    Auxiliary function that specifies the linear gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)
    return (x.clip(a,b)-float(a))/(b-a)
#    return 255.0 * (x-float(a))/(b-a)

def std_chunk(image,x,y):
    return np.std(image[x*100:x*100+100,y*100:y*100+100])

sub_list = list(filter(lambda x: x.ISO == 1600 and int(x.exptime) == 30 and \
	x.temp < 11, sub_EOSM))
#max is ~15300; need int16, not uint16, so don't have problems later w/ negative values
#a = np.concatenate([np.array(misc.imread(aux.filename), dtype='int16')[..., np.newaxis] \
#                       for    aux in sub_list], axis=2)
#avg = np.average(a, axis=2)
#dev = a.std(axis=2)

#bias = np.concatenate([np.array(misc.imread(aux.filename), dtype='int16')[..., np.newaxis] \
 #                      for    aux in bias_list], axis=2)
#bias_avg = np.average(bias, axis=2)

#plt.hist(a[445,550,...])