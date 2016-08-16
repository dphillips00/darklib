#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 23:57:22 2016

@author: dan
"""
a_clean = np.where(a<13000, 1, 0)*a
avg = np.average(a, axis=2)

plt.hist(a[445,550,...],bins=100)