# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""
 
from astropy.io.fits import getheader
import astropy.io.fits as fits
 
import photlib
import numpy as np

########### READ TABLE OF COORDINATES ###########
# Get target x,y coordinates
def tableofcoordinates(tableofcoords, verbose) :

	if tableofcoords != '':
		try:
			file = open(tableofcoords,'r')
		except:
			print 'Error: missing file :'+tableofcoords
			exit
 
	targets = []
 	
	for line in file.readlines() :
		targets.append(photlib.Target(float(line.split()[0]),float(line.split()[1])))
		if(verbose) :
			print "Target coordinates: ", float(line.split()[0]), " , ", float(line.split()[1]) 
 
	return targets
###########################################
 
########### PHOTOMETRY ###########
# Recenter and perform photometry on each target of the list
# Output:
#	mjd flux_target1 flux_target2 ...
 
def Photometry(imlist, targets, photradius, searchRadius, outputfile=None, verbose=False, biasfile=None, flatfile=None) :
 
	# First calculate aperture for phototmetry from base image
	im = fits.getdata(imlist[0])

	if biasfile :
		bias = fits.getdata(biasfile)
		im = im - bias

	if flatfile :
		flat = fits.getdata(flatfile)
		im = im / flat

	maxphotradius = 0
	for target in targets :
		target.recenter(im, searchRadius, None)
		if photradius == 0 :
			target.calculate_photradius(im, searchRadius, None)
			if(target.photradius > maxphotradius) :
				maxphotradius = target.photradius 
	if photradius == 0 :	
		photradius = maxphotradius
	#---------------------------------------------------------

	outfilecontents = ''

	# Then perform photometry
	nimg = 0

	for img in imlist :
		if verbose :
			print "Performing photometry of image ",nimg,"/",len(imlist)," -> ",img
		nimg += 1
		
		header = getheader(img,0)
		im = fits.getdata(img)
 
		#mjd =header['MJD-OBS']
		jd=header['JD']
		outfilecontents += str(jd)

		for target in targets :
			target.recenter(im, 1.5*photradius, None)
			target.setphotradius(photradius)
			target.calculateSky(im, 1.5*photradius, searchRadius, None)
			target.aperPhotometry(im, photradius, None)
 
			outfilecontents +=  " " + str(np.sqrt(target.x**2+target.y**2)) +  \
			               " " + str(target.skyflux) + \
			               " " + str(target.flux) +  \
			               " " + str(np.sqrt(target.fluxvar))
                       
		outfilecontents += '\n'

	if outputfile :
		outfile = open(outputfile, 'w')
		outfile.write(outfilecontents)
		outfile.close()
	else :
		print outfilecontents

	return
###########################################


