"""
Author: Kevin Luke
Date: Created 28 OKT 2022
"""

import matplotlib 
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import coordinates as coords
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astroquery.sdss import SDSS
import argparse


def image_sdss(galaxy_name,band_name):
    """
    Get the image of any object or galaxy from SDSS
    """
    #galaxy name to be resolved into coordinates
    galaxy = SkyCoord.from_name(galaxy_name)
    pos = coords.SkyCoord(galaxy.ra, galaxy.dec, frame='icrs')
    
    #query the sdss database for the given pos coordinates
    xid = SDSS.query_region(pos, spectro=True)
    print('Data found in the search:' )
    print(xid)
    
    #Get the image of that galaxy from SDSS database
    images = SDSS.get_images(matches=xid, band=band_name)
    image_data=images[0][0].data
    
    #special filter to be done on the ismage so that the galaxy is visible
    clipped_image = image_data.copy()
    clipped_image[clipped_image>1.0]=1.0
    
    #plot the image
    fig= plt.figure(figsize=(10,10))
    ax=fig.subplots()
    ax.imshow(clipped_image)
    fig.savefig('galaxy_image_galname_{0:s}.jpg'.format(galaxy_name))
    
    return xid

def spectra_sdss(xid,galaxy_name):
    """
    get the spectra of the hits I:e xid found in the sdss for the given object or the galaxy
    """
    spectra = SDSS.get_spectra(matches=xid)
    #from IPython import embed; embed()
    
    for spec,i in zip(spectra,range(len(spectra))):
        #spectra[x] where x is the number of hits
        #spectra[x][1].data is the data
        spectra_data=spec[1].data  #The np rec array
        
        #Write the fits for each match
       #spec.writeto('spectable_{0:d}_galname_{1:s}.fits'.format(i,galaxy_name))
        
        #write the table to a .dat format
        np.save('spectable_{0:d}_galname_{1:s}.npy'.format(i,galaxy_name),spectra_data)
        
        #plot the spectras from the hits obtained from the database
        fig = plt.figure(figsize=(5, 5))
        ax = fig.subplots()
        ax.plot(10**spectra_data['loglam'], spectra_data['flux'])
        ax.set_xlabel('wavelenght (Angstrom)')
        ax.set_ylabel('flux (nanomaggies)')
        fig.savefig('galaxy_spectra_{0:d}_galname_{1:s}.jpg'.format(i,galaxy_name))
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('galaxy_name', type=str, 
                       help='Type the name of the galaxy like NGC5406')
    parser.add_argument('--band_name', type=str, default='g',
                       help='Specify the band name to be used from u, g, i, r of SDSS CCD')
    parser.add_argument('--make_spectra',dest='make_spectra',
                        default=None, action='store_true',
                       help='Do you want a spectra?')

    args = parser.parse_args()
    galaxy_name=args.galaxy_name
    band_name=args.band_name
    make_spectra=args.make_spectra
    
    #do the image search 
    xid= image_sdss(galaxy_name, band_name)
    
    if make_spectra is not None:
        #do the spectra search
        spectra_sdss(xid, galaxy_name)
