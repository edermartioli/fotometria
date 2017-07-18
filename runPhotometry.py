# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""

import numpy
import photUtils

import sys
from optparse import OptionParser

import glob

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help='Input pattern: e.g. f*.fits',type='string',default="")
parser.add_option("-o", "--output", dest="output", help='Output photometry file',type='string',default="")
parser.add_option("-X", "--xycoords", dest="xycoords", help='File containing list of xy coordinates',type='string',default="")
parser.add_option("-P", "--photRadius", dest="photradius", help='Phot Radius',type='string',default="1")
parser.add_option("-S", "--skyRadius", dest="skyradius", help='Sky Radius',type='string',default="")
parser.add_option("-b", "--bias", dest="bias", help='Bias image',type='string',default="")
parser.add_option("-f", "--flat", dest="flat", help='Flat image',type='string',default="")
parser.add_option("-C", "--calibrations", dest="calibration", help='Calibration',type='string',default="")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Error: check usage with runPhotometry.py -h ";sys.exit(1);

if options.verbose:
    print 'Input pattern: ', options.input
    print 'Output photometry file: ', options.output
    print 'xycoords: ', options.xycoords
    print 'photRadius: ', options.photradius
    print 'skyRadius: ', options.skyradius
    print 'bias: ', options.bias
    print 'flat: ', options.flat
    print 'calibration: ', options.calibration

verbose = options.verbose

 
########### FILE LIST ##################
#### Generate list of files
objectlist = glob.glob(options.input)
###########################################

########### LIST OF TARGET COORDINATES ##################
#### Generate list of targets
targets = photUtils.tableofcoordinates(options.xycoords, verbose)
###########################################

########### SPARTAN PHOTOMETRY ###########
# Recenter and perform photometry on each target of the list
# Output:
#	mjd npixels photraius flux_target1 fluxvar_target1 ...
photUtils.Photometry(objectlist, targets, float(options.photradius), float(options.skyradius), options.output, verbose, biasfile=options.bias, flatfile=options.flat)
###########################################
