import astropy.units as u
import astropy.cosmology.units as cu
from astropy.cosmology import Planck18
from astropy import uncertainty as uc

z = 0.14 * cu.redshift
d = z.to(u.Mpc, cu.redshift_distance(Planck18, kind="comoving"))
print(d)
