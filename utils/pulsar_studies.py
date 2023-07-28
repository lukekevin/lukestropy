#!/usr/bin/env python
# coding: utf-8
#A HARD CODED PRIMITIVE script TO SHOW HOW PULSAR DATA IS ANALYSED BY SIGPYPROC3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sigpyproc.readers import FilReader
from scipy.fft import fft

#Load the converted fil file
filfile_path=Path('/DATA/chime-slow/raw/filterbank/2022/06/18/0120/016ms/1655547755_1655551360_beam_0120_016ms.fil')
fil_file=FilReader(filfile_path.as_posix())
fil_file.header

#Perform dedispersion and downsampling
tdownsamp=1
subband=2
DM=140
data = fil_file.read_block(0, fil_file.header.nsamples)
data = data.dedisperse(DM)
data = data.downsample(tdownsamp, subband)
data = data.normalise()
tseries = data.get_tim()
data.shape    

#Fold timeseries to get the pulse
from sigpyproc.timeseries import TimeSeries
def folder(tseries, fil_file, period, nbin,nint):
    
    series=TimeSeries(tseries, fil_file.header)
    folded=series.fold(period, nbins=nbin, nints=nint)
    profile=folded.get_profile()
    waterfall=folded.get_time_phase()
    
    
    plt.figure(figsize=(7,5))
    
    plt.subplot(2,2,1)
    plt.title('Normal dedispersed timeseries')
    plt.xlabel('samples')
    plt.ylabel('Power, arbitrary units')
    plt.plot(tseries)
    
    plt.subplot(2,2,2)
    plt.title('Folded timeseries of a pulsar')
    plt.xlabel('Phase bins')
    plt.ylabel('Power, arbitrary units')
    plt.plot(profile)
    plt.axis('off')
    
    plt.subplot(2,2,4)
    plt.xlabel('Phase bin')
    plt.imshow(waterfall, aspect='auto', cmap='hot', vmax=10, vmin=-10)
    
    
folder(tseries, fil_file, 0.4, 25,100)    

