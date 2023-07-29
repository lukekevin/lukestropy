import argparse
from pathlib import Path
import numpy as np

def converter(ignorechan,nchans, flip_list=None):
    #Open the comma separated ranges
    with open(ignorechan) as ig:
        data=ig.read()
    #A sample file will look like this #data='0:9,24,33:59,77,83,85:86'
    unflipped_chan = []
    #Check for the comma and split it throughout file
    for part in data.split(','):
        #if the double colon  that means it is range of number 
        if ':' in part:
            #split the higher number in the range and the lower number in the range
            a, b = part.split(':')
            #Convert them to int
            a, b = int(a), int(b)
            #Fill the ranges with integers using extend func
            unflipped_chan.extend(range(a, b + 1))
        else:
            #If double colon not present then it is just a comma seperated collection of numbers/channels
            a = int(part)
            unflipped_chan.append(a)
    #Flip the channels order if specified
    if flip_list is not None:
        flipped_chan=[]
        for channel in unflipped_chan:
            flipped=(nchans-1)-channel
            flipped_chan.append(flipped)
        ignore_channel=np.array(flipped_chan,dtype='int32')
        fname='ignore_channel_filled_range.txt'
        np.savetxt(fname,ignore_channel)
        print('\n')
        print('The shape of the filled list is:\n')
        print(ignore_channel.shape)
   #If flipping not specified then forget about flipping
    else:
        ignore_channel=np.array(unflipped_chan,dtype='int32')
        fname='ignore_channel_filled_range.txt'
        np.savetxt(fname,ignore_channel)
        print('\n')
        print('The shape of the filled list is:\n')
        print(ignore_channel.shape)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('ignorechan', type=str,
        help='Path to the txt file containing injected file path')
    parser.add_argument('--nchans', type=float,
        help='number of channels in the file', default=1024)
    parser.add_argument("--flip_list", default=False, dest='flip_list', 
                        action='store_true')
    args = parser.parse_args()
    
    ignorechan=Path(args.ignorechan)
    nchans=args.nchans
    flip_list=args.flip_list
    
    print('Simple code to convert PRESTO ignore channels comma sepearated ranges to txt file list of all the number in the range which could be used in RFI mitigation work.\n')
    #Start the conversion
    if flip_list:
        print('\nFlipping the order of the list')
        converter(ignorechan.as_posix(), nchans, flip_list)
    else:
        print('\nNot flipping the order of the list')
        converter(ignorechan.as_posix(), nchans)