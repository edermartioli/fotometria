# FOTOMETRIA

FOTOMETRIA is a Python package with libraries and tools to perform aperture photometry time series. 

To start using the FOTOMETRIA tools, download the following libraries:

* `photlib.py`
* `photUtils.py`

Make sure you have the following depencies installed:

`numpy`, `scipy`, `astropy`

Usage example:
```python
  from photlib import Target
  import astropy.io.fits as fits
  
  im = fits.getdata("image.fits")
  
  xcoord,ycoord = (503,235)  # in pixel units
  star = Target(xcoord,ycoord)
  
  searchRadius = 50  # in pixels units
  star.recenter(im, searchRadius, None)
  
  star.calculateSky(im, innerRadius=25, outerRadius=50)
  print star.skyflux, star.skyfluxvar
  
  star.aperPhotometry(im, photRadius=15, working_mask=None)
  print star.flux, star.fluxvar
```
One can find more examples on how to use the FOTOMETRIA libraries in the tools available. For instance, there is a tool called `photometry.py`, which is a command line application to perform photometry time series of several images. Along with this we also include the tools `imcombine.py` and `flatcombine.py` for stacking images, which are useful to create a master bias and a master flat. There is also a plot tool `plot.py` to visualize the differential photometry time series. Finally we include a pipeline tool called `pipeline.py`, which calls all the above tools in sequence to perform the full reduction. One can use the pipeline tool as usage examples of all other tools.
