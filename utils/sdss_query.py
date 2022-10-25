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


def spectra_sdss(galaxy_name):
    """
    Get the spectra of any object or galaxy from SDSS
    """
    
    #galaxy name to be resolved into coordinates
    galaxy = SkyCoord.from_name(galaxy_name)
    pos = coords.SkyCoord(galaxy.ra, galaxy.dec, frame='icrs')
    
    #query the sdss database for the given pos coordinates
    xid = SDSS.query_region(pos, spectro=True)
    print('Data found in the search:' )
    print(xid)
    
    #get the spectra of the hits I:e xid found in the sdss for the given object or the galaxy
    spectra = SDSS.get_spectra(matches=xid)
    for spec,i in zip(spectra,range(len(spectra))):
        #spectra[x] where x is the number of hits
        #spectra[x][1].data is the data
        spectra_data=spec[1].data
        #write the table to a .dat format
        ascii.write(spectra_data ,
                    'spectable_{0:d}_galname_{1:s}.dat'.format(i,galaxy_name), 
                    overwrite=True)
        
        #plot the spectras from the hits obtained from the database
        fig = plt.figure(figsize=(5, 5))
        ax = fig.subplots()
        ax.plot(10**spectra_data['loglam'], spectra_data['flux'])
        ax.set_xlabel('wavelenght (Angstrom)')
        ax.set_ylabel('flux (nanomaggies)')
        fig.savefig('galaxy_spectra_{0:d}_galname_{1:s}.jpg'.format(i,galaxy_name))
        
     #return the number of hits obtained for further query   
    return xid

def image_sdss(xid, galaxy_name):
    
    """
    Get the image of that galaxy from SDSS database
    """
    images = SDSS.get_images(matches=xid, band='g')
    image_data=images[0][0].data
    
    #special filter to be done on the image so that the galaxy is visible
    clipped_image = image_data.copy()
    clipped_image[clipped_image>1.0]=1.0
    
    #plot the image
    fig= plt.figure(figsize=(10,10))
    ax=fig.subplots()
    ax.imshow(clipped_image)
    fig.savefig('galaxy_image_galname_{0:s}.jpg'.format(galaxy_name))
    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('galaxy_name', type=str)
    args = parser.parse_args()
    galaxy_name=args.galaxy_name
    
    #do the spectra search 
    xid= spectra_sdss(galaxy_name)
    
    #do the image search
    image_sdss(xid, galaxy_name)
