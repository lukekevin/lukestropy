import matplotlib 
import numpy as np
import matplotlib.pyplot as plt
from urllib.parse import urlencode
from urllib.request import urlretrieve
from astropy import units as u
from astropy import coordinates as coords
from astropy.coordinates import SkyCoord
import argparse
from PIL import Image

def skyservice_extract(RA,DEC,zoom):
    """
    SImple function to retrieve images from sky service of SDSS DR 12
    """
    #Image radius and pixels
    im_size = zoom*u.deg 
    im_pixels = 1024
    
    #Conver the RA DEC to astropy positions 
    pos = coords.SkyCoord(RA*u.deg, DEC*u.deg, frame='icrs')
    print('Position entered in degrees:')
    print(pos)
    #This is the url where the search is to be made
    cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx'
    #This is the field on the GUI that is field from here
    query_string = urlencode(dict(ra=RA,
                                  dec=DEC,
                                  width=im_pixels, height=im_pixels,
                                  scale=im_size.to(u.arcsec).value/im_pixels))
    #The url of the image finally
    url = cutoutbaseurl + '?' + query_string

    # this downloads the image
    image_name = '{0:f}ra_{1:f}dec_{2:f}radius_SDSS_skyservice.jpg'.format(RA,DEC,im_size)
    #Retrieve the url 
    urlretrieve(url, image_name)
    
    print('COnverting the downloaded image to a numpy array and then saving the numpy array and the cmap image')
    #Load the saved image for numpy conversion
    image = Image.open(image_name)
    np_img = np.array(image)
    print(np_img.shape)
    fig=plt.figure(figsize=(10,10))
    ax=fig.subplots()
    ax.imshow(np_img[:,:,1])
    fig.savefig('{0:f}ra_{1:f}dec_{2:f}radius_numpy_imshow.jpg'.format(RA,DEC,im_size))
    #Save the numpy array
    np.save('{0:f}ra_{1:f}dec_{2:f}radius_numpy.npy'.format(RA,DEC,im_size), np_img)

    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('RA', type=float,
                       help='Input the RA')
    parser.add_argument('DEC', type=float,
                       help='Input the DEC')
    parser.add_argument('--zoom', default=0.03, type=float,
                       help='radius around the loc in degrees')
    args = parser.parse_args()
    zoom=args.zoom
    RA=args.RA
    DEC=args.DEC
    
    #Launch the image retrieval
    skyservice_extract(RA,DEC,zoom)
