# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""
 
import os
from astropy.io.fits import getheader
import astropy.io.fits as fits
 
import photlib
from numpy import *
 
######################
def get_fitsfilepaths(directory):

	"""
	This function generates a list of file names in a directory
	tree by walking the tree either top-down or bottom-up. For each
	directory in the tree rooted at directory top (including top itself),
	it yields a 3-tuple (dirpath, dirnames, filenames).
	"""
	file_paths = []  # List which will store all of the full filepaths.
 
	# Walk the tree.
	for root, directories, files in os.walk(directory):
		for filename in files:
			# Merge strings to form full filepaths
			filepath = os.path.join(root, filename)
#			if filename.endswith(".fits") or filename.endswith(".fits.gz") or filename.endswith(".fits.fz") :
			if filename.endswith(".fits") or filename.endswith(".fits.gz"):
				file_paths.append(filepath)
	file_paths.sort()
	return file_paths  # Self-explanatory.
######################
 
######################
def bzunpack(directory, verbose):
	"""
	This function run bzip to unzip files in case they haven't been unzipped yet
	"""
	file_paths = []  # List which will store all of the full filepaths.
 
	# Walk the tree.
	for root, directories, files in os.walk(directory):
		for filename in files:
			# Merge strings to form full filepaths
			filepath = os.path.join(root, filename)
			if filename.endswith(".fits.bz2") :
				bzipcommand = 'bzip2 -d '+ filepath
				if(verbose) :
					print bzipcommand
					os.system(bzipcommand)
	return
######################

###############################################
def createObjectList(datadir, night, objectname, filter, objectlistfilename, savetofile):
	"""
	This function generates a list of object file names.
	If option savetofile is true, then it will create an file with a list of object file paths
	and it will return the list file name. If option savetofile is false then it returns a
	array of object file paths.
	"""
	obstypekeyvalue = 'Object'
 
	objectlist = []
 
	filelist = get_fitsfilepaths(datadir)
 
	for image in filelist:
		#print "Processing image: " + image.rstrip('\n')
		header = getheader(image.rstrip('\n'), 0)
 
		#if(header['OBSTYPE'] == obstypekeyvalue and header['OBJECT'] == objectname) :
		
		objectlist.append(image.rstrip('\n'))
 
	listfile = open(objectlistfilename, 'w')
	for objects in objectlist:
		listfile.write(objects+'\n')
	listfile.close()
	return objectlist
 
###############################################
 
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
 
			outfilecontents +=  " " + str(sqrt(target.x**2+target.y**2)) +  \
			               " " + str(target.skyflux) + \
			               " " + str(target.flux) +  \
			               " " + str(sqrt(target.fluxvar))
                       
		outfilecontents += '\n'

	if outputfile :
		outfile = open(outputfile, 'w')
		outfile.write(outfilecontents)
		outfile.close()
	else :
		print outfilecontents

	return
###########################################


