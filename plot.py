# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
from optparse import OptionParser

from scipy.stats import binned_statistic

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help='Input light curve',type='string',default="")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Error: check usage with runPhotometry.py -h ";sys.exit(1);

if options.verbose:
    print 'Input light curve: ', options.input

depth = 0.0183

t,x,y,f,ef,x1,y1,f1,ef1,x2,y2,f2,ef2,x3,y3,f3,ef3,x4,y4,f4,ef4,x5,y5,f5,ef5,x6,y6,f6,ef6,x7,y7,f7,ef7 = np.loadtxt(options.input,delimiter=' ', usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32), unpack=True)

t = t - t[0]

#df =f/(f1+f2+f3+f4+f5+f6+f7)
df =f/(f1+f2+f4+f5)
#dfref = f
dfref = y

df1 = f/f1
df2 = f/f2
df3 = f/f3
df4 = f/f4
df5 = f/f5
df6 = f/f6
df7 = f/f7

s = np.std(df)

s1 = np.std(df1)
s2 = np.std(df2)
s3 = np.std(df3)
s4 = np.std(df4)
s5 = np.std(df5)
s6 = np.std(df6)
s7 = np.std(df7)

print "----------------------------"
print "All stars - Precision:", s*100
print "----------------------------"
print "Star 1 - Precision:", s1*100
print "Star 2 - Precision:", s2*100
print "Star 3 - Precision:", s3*100
print "Star 4 - Precision:", s4*100
print "Star 5 - Precision:", s5*100
print "Star 6 - Precision:", s6*100
print "Star 7 - Precision:", s7*100
print "----------------------------"

snr = depth/s

snr1 = depth/s1
snr2 = depth/s2
snr3 = depth/s3
snr4 = depth/s4
snr5 = depth/s5
snr6 = depth/s6
snr7 = depth/s7

print "------------------------"
print "All stars - SNR:", snr
print "------------------------"
print "Star 1 - SNR:", snr1
print "Star 2 - SNR:", snr2
print "Star 3 - SNR:", snr3
print "Star 4 - SNR:", snr4
print "Star 5 - SNR:", snr5
print "Star 6 - SNR:", snr6
print "Star 7 - SNR:", snr7
print "------------------------"

dfn = df / np.median(df)
plt.plot(t,dfn,'.')

nbins = 70
statistic='median'

binnedTime = binned_statistic(t, t, statistic=statistic, bins=nbins)[0]
binnedFlux = binned_statistic(t, dfn, statistic=statistic, bins=nbins)[0]

plt.plot(binnedTime,binnedFlux,'o-', lw=2)

plt.ylabel('flux')
plt.xlabel('time (d)')

#dfrefn = dfref / np.median(dfref)
#plt.plot(t,dfrefn,'-.')

plt.show()

