import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sigpyproc.readers import FilReader
from scipy.fft import fft
import argparse

def process_data(in_file, dm, subband):
    fil_file_path=Path(in_file)
    fil_file=FilReader(fil_file_path.as_posix())
    fil_file.header
    
    tdownsamp=1
    data = fil_file.read_block(0, fil_file.header.nsamples)
    data = data.dedisperse(dm)
    data = data.downsample(tdownsamp, subband)
    data = data.normalise()
    tseries = data.get_tim()
    return data, fil_file

def perform_fourier_transform(data):
    nchannels, nsamples = data.shape  #nchannels=N =is number of samples in data
    sampling =fil_file.header.tsamp #sampling rate=T
    x = np.linspace(0.0, nsamples*fil_file.header.tsamp , nsamples)
    y = data.mean(axis=0)  # Taking the mean along the first axis (channel-wise mean)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*fil_file.header.tsamp), nsamples//2)
    mag = 2.0/(nsamples * fil_file.header.tsamp) * np.abs(yf[:nsamples//2])
    return xf, mag


#Return the top strong candidates from fourier plot
def top_cand(arr,top):
    candidate = []
    # Delete the first and second element fourier transform
    arr[0]=0
    arr[1]=0
    for i in range(top):
        # We add 1 as the 0th index = period of 1 not 0
        index = np.argmax(arr)
        candidate.append(index+1)
        arr[index]=0
        
    print('The possible candidates are:', candidate)
    return candidate 

def plot_fourier(xf, mag, candidate):
    # Plotting the magnitude of the Fourier transform
    plt.figure(figsize=(10,3))
    plt.plot(mag)
    plt.grid()
    plt.title('Fourier Transform of Filterbank Data')
    plt.xlabel("Periods")
    plt.ylabel("Magnitude of Fourier Transform")
    plt.savefig('Fouriered_spectra.png')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('in_file', type=str,
        help='Path to the txt file containing injected file path')
    parser.add_argument('--dm', type=int, default=10)
    parser.add_argument('--subband', type=int, default=2)
    
    args = parser.parse_args()
    
    in_file=args.in_file
    dm=args.dm
    subband=args.subband
    print('A simple code to perform fourier transform on dedispersed filterbank data')
    #Process the filterbank with sigpyproc and obtain the data array and fil_file object
    data,fil_file =process_data(in_file,dm,subband)
    #Perform fourier and obtain mag of fourier transform and the frequencies
    xf,mag=perform_fourier_transform(data)
    #Find the top strongest candidates from the fourier 
    candidate=top_cand(mag,20)
    #PLot the fourier 
    plot_fourier(xf,mag,candidate)