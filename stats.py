#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 23:57:22 2016

@author: dan
"""
#a = np.where(a<13000, a, 0)
#more efficient:
np.clip(a, 0, 13000)
avg = np.average(a, axis=2)

plt.hist(a[445,550,...])