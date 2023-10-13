import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
plt.style.use(astropy_mpl_style)
quantity_support()
from astropy.coordinates import get_body

def path_tracking(latitude, longitude, date, planet_string):
    loc = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=0*u.m)
    utcoffset = 5.5*u.hour
    time_mid = Time(date, format='iso',scale='utc')+ utcoffset
    time_delta = np.linspace(-10,10, 10)*u.hour
    time_frame = time_mid + time_delta
    
    object = SkyCoord.from_name(planet_string)
    
    time_frame_alt_az = AltAz(obstime=time_frame, location=loc)
    object_alt_az = object.transform_to(time_frame_alt_az)
    mumbai_loc_obstime=object_alt_az.obstime + 8*u.hour
    obstime=[time.value for time in mumbai_loc_obstime]
    obstime_hrs=[hrs[11:16] for hrs in obstime]
    az=np.deg2rad(object_alt_az.az)
    alt=object_alt_az.alt

    return alt, az, obstime_hrs, obstime


    
def visualise(alt, az, obstime_hrs, obstime, planet_string):
    fig=plt.figure(figsize=(10,15))  
    
    ax=fig.add_subplot(2,1,1, projection='polar')
    #ax = plt.subplot(1, 1, 1, projection='polar')
    ax.set_rlim(90, 0, 1)
    ax.scatter(az,alt, marker='o', s=50)
    
    ax.set_theta_zero_location('N')  # North as 0 degrees
    ax.set_theta_direction(-1)  # Clockwise direction
    ax.set_xticklabels(['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'], fontsize=10)
    ax.set_rlabel_position(200)  # Position of radial labels
    plt.title('{0:s}\n Altitude vs Azimuth\n on {1:s}'.format(planet_string, date))
    for i, txt in enumerate(obstime):
        ax.annotate(txt[11:16],(az[i],alt[i]), fontsize=10)
    
    
    ax1=fig.add_subplot(2,1,2)
    ax1.scatter(obstime_hrs,alt )
    for i, txt in enumerate(obstime):
        ax1.annotate(txt[11:16],(obstime_hrs[i],alt[i]), fontsize=10)
    
        
    # Add a title and legend
    plt.title('{0:s}\n Altitude vs time\n on {1:s}'.format(planet_string, date))
    # Show the plot
    fig.savefig('moon_map_{0:s}.png'.format(date))


if __name__ == "__main__":
    latitude=19.3547
    longitude=72.8328 
    date='2023-10-14 12:00:00'
    planet_string='jupiter'

    alt, az, obstime_hrs, obstime= path_tracking(latitude, longitude, date, planet_string)
    'visualise(alt, az, obstime_hrs, obstime, planet_string)
