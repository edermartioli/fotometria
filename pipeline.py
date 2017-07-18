#!/opt/anaconda/bin/python
# Description: Script to perform time series photometry
# Author: Eder Martioli
# Laboratorio Nacional de Astrofisica, Brazil
# Jul 2017
#

import os, sys
import time

start_time = time.time()

#--- SET UP PIPELINE PARAMETERS ---
PHOTROOTDIR="/Users/edermartioli/Desktop/fotometria/"
NIGHT="17jul13"
OBJECT="hats-24"

PIPELINEDIR = PHOTROOTDIR + "/pipeline/"
SCIDATADIR = PHOTROOTDIR + "/data/" + NIGHT + "/" + OBJECT + "/"
CALIBDATADIR = PHOTROOTDIR + "/data/" + NIGHT + "/calibrations/"
PRODUCTDIR = PHOTROOTDIR + "/reduced/" + NIGHT + "/" + OBJECT + "/"

biaspattern = 'bias_final_0*.fits'
flatpattern = 'flat_I_final*.fits'

photRadius = '15'
skyRadius = '50'
append = False

outputbias = PHOTROOTDIR + NIGHT + ".mbias_final.fits"
outputflat = PHOTROOTDIR + NIGHT + ".mflat_I_final.fits"
outputphot = PHOTROOTDIR + OBJECT + ".I.phot"
#---------------------------

print "Running pipeline..."

currdir = os.getcwd()
os.chdir(PIPELINEDIR)

#--- CREATE MASTER BIAS ---
biascommand = 'python imcombine.py --input=' + CALIBDATADIR + biaspattern + \
' --output=' + outputbias + ' -v'
if os.path.exists(outputbias) : os.remove(outputbias)
print biascommand; os.system(biascommand)
#---------------------------

#--- CREATE MASTER FLAT ---
flatcommand = 'python flatcombine.py --input=' + CALIBDATADIR + flatpattern + \
' --bias=' + outputbias + ' --output=' + outputflat + ' -vn'
if os.path.exists(outputflat) : os.remove(outputflat)
print flatcommand; os.system(flatcommand)
#---------------------------

#--- PERFORM APERTURE PHOTOMETRY ---
photcommand = ''
if append :
	photcommand = 'python photometry.py --input=' + SCIDATADIR + OBJECT + "*.fits" + \
	' --xycoords=' + PRODUCTDIR + "xycoords.txt" + ' --photRadius=' + photRadius + \
	' --skyRadius=' + skyRadius + ' --bias=' + outputbias + ' --flat=' + outputflat + \
	' -v >> ' + outputphot
else :
	photcommand = 'python photometry.py --input=' + SCIDATADIR + OBJECT + "*.fits" + \
	' --xycoords=' + PRODUCTDIR + "xycoords.txt" + ' --photRadius=' + photRadius + \
	' --skyRadius='+ skyRadius + ' --bias=' + outputbias + ' --flat=' + outputflat + \
	' --output=' + outputphot + ' -v'

if os.path.exists(outputphot) : os.remove(outputphot)
print photcommand; os.system(photcommand)
#---------------------------

#--- PLOT LIGHT CURVE ---
plotcommand = 'python plot.py --input=' + outputphot
print plotcommand; os.system(plotcommand)
#---------------------------

os.chdir(currdir)

print("--- Total time: %s seconds ---" % (time.time() - start_time))
