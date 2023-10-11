import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
plt.style.use(astropy_mpl_style)
quantity_support()
from astropy.coordinates import get_body
from matplotlib import gridspec


def path_tracking(latitude, longitude, date):
    
    loc = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=0*u.m)
    utcoffset = 5.5*u.hour
    time_mid = Time(date, scale='utc')+ utcoffset
    time_delta = np.linspace(-12,12, 20)*u.hour
    time_frame = time_mid + time_delta
    time_frame_alt_az = AltAz(obstime=time_frame, location=loc)
    
    moon_path = get_body("moon", time_frame)
    moon_path_alt_az = moon_path.transform_to(time_frame_alt_az)
    
    az_moon=np.deg2rad(moon_path_alt_az.az[moon_path_alt_az.alt>0])
    alt_moon=(moon_path_alt_az.alt[moon_path_alt_az.alt>0])

    return az_moon, alt_moon, moon_path_alt_az
    

def visualise(az_moon, alt_moon, moon_path_alt_az, date):
    
    fig=plt.figure(figsize=(20,20), dpi=100)  

    ax=fig.add_subplot(1,1,1, projection='polar')
    #ax = plt.subplot(1, 1, 1, projection='polar')
    ax.set_rlim(90, 0, 1)
    ax.scatter(az_moon,alt_moon, marker='o', s=500)
    
    ax.set_theta_zero_location('N')  # North as 0 degrees
    ax.set_theta_direction(-1)  # Clockwise direction
    ax.set_xticklabels(['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'], fontsize=20)
    ax.set_rlabel_position(200)  # Position of radial labels
    
    #Time string
    obstime=[time.value for time in moon_path_alt_az.obstime[moon_path_alt_az.alt>0]]
    
    print("\n The obs time and corresponding altitudes are\n")

  
    for i, txt in enumerate(obstime):
        ax.annotate(txt[11:16],(az_moon[i],alt_moon[i]), fontsize=20)
        print(txt,alt_moon[i])
    
    # Add a title and legend
    plt.title('Moon Altitude vs Azimuth on {0:s}'.format(date))
    # Show the plot
    fig.savefig('moon_map_{0:s}.png'.format(date))
    
    fig.show()

if __name__ == "__main__":
    latitude=19
    longitude=72.8
    date='2023-10-11 16:00:00'
    
    az_moon, alt_moon, moon_path_alt_az= path_tracking(latitude, longitude, date)
    
    visualise(az_moon, alt_moon, moon_path_alt_az, date)
