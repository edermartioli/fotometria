# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""

import numpy as np
import sys, os
from optparse import OptionParser

from astropy.io.fits import getheader
import astropy.io.fits as fits
from ccdproc import Combiner, CCDData

import glob

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help='Input pattern: e.g. f*.fits',type='string',default="")
parser.add_option("-b", "--bias", dest="bias", help='Input bias',type='string',default="")
parser.add_option("-o", "--output", dest="output", help='Output file',type='string',default="")
parser.add_option("-n", action="store_true", dest="normalize", help="normalize",default=0)
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Error: check usage with flatcombine.py -h ";sys.exit(1);

if options.verbose:
    print 'Input pattern: ', options.input
    print 'Input bias: ', options.bias
    print 'Output file: ', options.output
    print 'Normalize: ', options.normalize

verbose = options.verbose
 
files = glob.glob(options.input)

header = getheader(files[0], 0)

biasdata = fits.getdata(options.bias, 0)

arr = []
for img in files :
    if options.verbose:
        print "Input image ->",img
    ccddata = fits.getdata(img, 0)

    ccddata = ccddata - biasdata

    arr.append(CCDData(ccddata, unit = 'adu'))
            
combiner = Combiner(arr)

scaling_func = lambda arr: 1/np.ma.median(arr)

combiner.scaling = scaling_func

combinedImageMedian = combiner.median_combine() #average/median
NPcombinedImage = np.asarray(combinedImageMedian)

if options.normalize :
    print "Applying normalization ..."
    NPcombinedImage = NPcombinedImage / np.median(NPcombinedImage)

if options.verbose:
    print "Writing output image:",options.output

if os.path.exists(options.output) :
    os.remove(options.output)

fits.writeto(options.output, NPcombinedImage, header)

