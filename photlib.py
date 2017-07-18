# -*- coding: iso-8859-1 -*-
"""
    Created on Wed Jul 12, 2017
    @author: Eder Martioli & Janderson Oliveira
    Laboratorio Nacional de Astrofisica, Brazil
"""

from numpy import *
 
class Target:
	'Common base class for a target'
	count = 0
	name = 'NONE'
 
	flux = 0.0
	fluxvar = 0.0
 
	skyflux = 0.0
	skyfluxvar = 0.0
 
	photradius = 0.0
	numberofpixels = 0
 
	def __init__(self, x=0, y=0):
		self.x=x
		self.y=y
		self.count += 1
 
	def getSNR(self) :
		if self.fluxvar :
			return self.flux/sqrt(self.fluxvar)
		else:
			return 0.0
 
	def setphotradius(self, Radius) :
		self.photradius = Radius
 
	def recenter(self, im, Radius, usemax=False, working_mask=None) :
 
		if working_mask==None:
			working_mask = ones(im.shape,bool)
 
		ym, xm = indices(im.shape, dtype=float32) # note order of x, y!
 
		r = sqrt((xm - self.x)**2 + (ym - self.y)**2)
 
		mask = (r < Radius) * working_mask
 
		pixels = im[where(mask)]

		if usemax :
			# Recenter using maximum value
			max_idx = argmax(pixels)
			self.x = xm[where(mask)][max_idx]
			self.y = ym[where(mask)][max_idx]
		else :
			# Recenter using centroid:
			self.x = (pixels * xm[where(mask)]).sum() / pixels.sum()
			self.y = (pixels * ym[where(mask)]).sum() / pixels.sum()
 
	def calculate_photradius(self, im, searchRadius, working_mask=None) :
		maxsnr = 0
		maxradius = 0
		for photRadius in range(0,searchRadius) :
			self.calculateSky(im, photRadius, searchRadius, working_mask)
			self.aperPhotometry(im, photRadius, working_mask)
			if self.getSNR() > maxsnr :
				maxsnr = self.getSNR()
				maxradius = photRadius
		self.photradius = maxradius
 
	def calculateSky(self, im, innerRadius, outerRadius, working_mask=None) :
 
		if working_mask==None:
			working_mask = ones(im.shape,bool)
 
		ym, xm = indices(im.shape, dtype=float32)
 
		r = sqrt((xm - self.x)**2 + (ym - self.y)**2)
 
		skymask = (r > innerRadius) * (r < outerRadius) * working_mask
 
		self.skyflux = median(im[where(skymask)])
		self.skyfluxvar = median(abs(im[where(skymask)] - self.skyflux)) / 0.674433
 
	def aperPhotometry(self, im, photRadius=None, working_mask=None) :
		if photRadius :
			self.photradius = photRadius
		
		if working_mask==None:
			working_mask = ones(im.shape,bool)
 
		ym, xm = indices(im.shape, dtype=float32)
 
		r = sqrt((xm - self.x)**2 + (ym - self.y)**2)
 
		photmask = (r < self.photradius) * working_mask
 
		self.flux = (im[where(photmask)] - self.skyflux).sum()
		self.fluxvar = (im[where(photmask)] + self.skyfluxvar).sum()
		self.numberofpixels = len(im[where(photmask)])
 
	def displayTarget(self) :
		print "Name: ",self.name, ", count: ", self.count, ", x: ", self.x, ", y: ", self.y
