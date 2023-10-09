import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
plt.style.use(astropy_mpl_style)
quantity_support()
from astropy.coordinates import get_body

loc = EarthLocation(lat=19*u.deg, lon=72.8*u.deg, height=0*u.m)
utcoffset = 5.5*u.hour
time_mid = Time('2023-10-9 16:00:00', scale='utc')+ utcoffset



time_delta = np.linspace(-6,12, 20)*u.hour
time_frame = time_mid + time_delta
time_frame_alt_az = AltAz(obstime=time_frame, location=loc)

from astropy.coordinates import get_body

moon_path = get_body("moon", time_frame)
moon_path_alt_az = moon_path.transform_to(time_frame_alt_az)

az_moon=np.deg2rad(moon_path_alt_az.az)
alt_moon=moon_path_alt_az.alt


ax = plt.subplot(1, 1, 1, projection='polar')

ax.set_rlim(90, 0, 1)
ax.scatter(az_moon,alt_moon, marker='*')

ax.set_theta_zero_location('N')  # North as 0 degrees
ax.set_theta_direction(-1)  # Clockwise direction

#ax.set_rlabel_position(90)  # Position of radial labels
#Time string
obstime=[time.value for time in moon_path_alt_az.obstime[moon_path_alt_az.alt>0]]
#Print the rise time and transit times with their altitudes
for alt, time in zip(moon_path_alt_az.alt[moon_path_alt_az.alt>0], 
                     moon_path_alt_az.obstime[moon_path_alt_az.alt>0]):

    print(alt, time)

# Add a title and legend
plt.title('Moon Altitude vs Azimuth')


# Show the plot
plt.show()

