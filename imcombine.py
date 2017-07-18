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
parser.add_option("-i", "--input", dest="input", help='Input pattern: e.g. b*.fits',type='string',default="")
parser.add_option("-o", "--output", dest="output", help='Output file',type='string',default="")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Error: check usage with imcombine.py -h ";sys.exit(1);

if options.verbose:
    print 'Input pattern: ', options.input
    print 'Output file: ', options.output

verbose = options.verbose
 
files = glob.glob(options.input)

header = getheader(files[0], 0)

x = []
for img in files :
    if options.verbose:
        print "Input image ->",img
    ccddata = fits.getdata(img, 0)
    x.append(CCDData(ccddata, unit = 'adu'))
            
combinedImage = Combiner(x)
combinedImageMedian = combinedImage.median_combine() #average/median
NPcombinedImage = np.asarray(combinedImageMedian)

if options.verbose:
    print "Writing output image:",options.output

if os.path.exists(options.output) :
    os.remove(options.output)

fits.writeto(options.output, NPcombinedImage, header)

