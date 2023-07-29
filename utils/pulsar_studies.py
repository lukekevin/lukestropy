#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sigpyproc.readers import FilReader
from scipy.fft import fft
get_ipython().run_line_magic('matplotlib', 'inline')


#Load the converted fil file
filfile_path=Path('filterbanks/1655547760_1655551362_beam_1134_016ms.fil')
fil_file=FilReader(filfile_path.as_posix())
fil_file.header


data=fil_file
freq=1.89 #Hz FROM ATNF
DM=22.54 #FROM ATNF
bins=100 
ints=20
bands=128

#Fold the data
folded=data.fold(period=1/freq,dm=DM,accel=0 , 
                 nbins=bins, nints=ints,
                 nbands=bands)

print('Shape of folded data',folded.shape)
#Get the waterfall
waterfall=folded.get_freq_phase()
#Get the profile 
profile=folded.get_profile()
print('Shape of watefall',waterfall.shape)

plt.figure(figsize=(4,6))

plt.subplot(2,1,1)
plt.title('Folded Plot of PSR B2021+51')
plt.xlabel('Phase bins')
plt.ylabel('Power arbitrary units')
plt.plot(profile[:])

plt.subplot(2,1,2)
plt.xlabel('Phase bins')
plt.ylabel('Frequency bands')
plt.imshow(waterfall[:,:], aspect='auto', cmap='hot', 
           vmax=max(np.nanmedian(waterfall, axis=0)), 
           vmin=min(np.nanmedian(waterfall, axis=0)))

plt.tight_layout()
