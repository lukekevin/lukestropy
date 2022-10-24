"""
Author: Kevin Luke
Date created: 23 OKT 2022
Date edited: 24 OKT 2022
"""

from astroquery.ipac.ned import Ned
import astropy.units as u
import os
from astropy.wcs import WCS
from astropy.io import ascii
import argparse
import astropy.coordinates as coord
import matplotlib.pyplot as plt


def ned_query(zoom_deg,loc, region_name=None ):
    """
    For the region entered do a ned query to list all objects and then plot the objects
    """
    #Conver the string of RA AND DEC into suitable floats
    name_loc.split(',')
    RA=float(name_loc[0])
    DEC=float(name_loc[1])
    #Feed them into the location variable for the coordinates generation
    location=coord.SkyCoord(ra=RA, dec=DEC,unit=(u.deg, u.deg), frame='icrs')
    #NED QUERY
    result_table = Ned.query_region(location, radius=zoom_deg * u.deg)
    print(result_table)
    #Save the table
    ascii.write(result_table, 
                'nedtable_ra_{0:f}_dec_{1:f}.dat'.format(RA,DEC), 
                overwrite=True)

    #Take out the list of the object names from the result_table
    object_list=result_table['Object Name']
    
    #Plotting part for all the objects
    for objects in object_list:
        print(objects)
        images = Ned.get_images(objects)
        hdu=images[0][0]
        # Tell matplotlib how to plot WCS axes
        wcs = WCS(hdu.header)
        fig = plt.figure(figsize=(20, 10))
        ax = fig.gca(projection=wcs)
        # Plot the image
        ax.imshow(hdu.data)
        ax.set(xlabel="RA", ylabel="Dec")
        fig.savefig('nedquery_{}.jpeg'.format(objects))
        
    for obj in object_list:
        spectra = Ned.get_spectra(obj)
        print(len(spectra))
        if len(spectra)==0:
            print('Spectra Not Found for the region')
        for spectras,i in zip(spectra,range(len(spectra))):
            d=str(i)
            print(spectras[0].shape)
            fig = plt.figure(figsize=(20, 10))
            ax=fig.add_subplot(111)
            ax.set(xlabel='wavelenght',ylabel='flux')
            ax.plot(spectras[0].data)
            fig.savefig(d+'spec.jpg')
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('name_loc', type=str,
                       help='Input the RA, DEC or name of the region. eg: 34.45,56,78')
    
    args = parser.parse_args()
    name_loc=args.name_loc
    
    #Specify the foa of the area
    print('Enter the radius to be zoomed in degree')
    zoom_deg=float(input())
    
    #Do the search and plot the images
    ned_query(zoom_deg,name_loc)
