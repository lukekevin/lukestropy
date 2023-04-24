import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py
from matplotlib import gridspec
import argparse
from pathlib import Path

def hdf_process(hdf_file):
    inj_events=np.array(hdf_file.get('inj_events'))
    clust_info=np.array(hdf_file.get('cluster_info'))
    
    #make the cluster info to pd dataframe
    clust_info=pd.DataFrame(clust_info)
    #sort inj events by time
    inj_events=inj_events[inj_events['TIME'].argsort()]    #
    #Sort the cluster info by time
    clust_info=clust_info.sort_values(by='TimeMaxSNR',ascending=True)    #  


    #filtering part of cluster info  based on labels for inj events
    good_labels=inj_events['Label']>0
    inj_events=inj_events[good_labels]
    good_prob=inj_events['Prob']>0.1  
    inj_events=inj_events[good_prob]
    filtered_presto = clust_info[(clust_info['Label'].isin(inj_events['Label'].astype(int)))]
    
    return inj_events, filtered_presto,clust_info

def make_plots(inj_events, filtered_presto, plot_name,clust_info):
    # Initiate a figure and make 6 grids in it for various subplots
    fig = plt.figure(figsize=(40, 30), dpi=100)
    grid = gridspec.GridSpec(ncols=3, nrows=2, height_ratios=[2, 2], width_ratios=[2,2,2])

    #Presto SNR vs Inj fluence/sqrt Width plot
    #fit a line to the scatter plot
    a,b=np.polyfit(filtered_presto['MaxSNR'], 
                   (inj_events['FLUENCE']/np.sqrt(inj_events['WIDTH'])), 
                   1)
    Y=10*a+b
    
    ax0 = fig.add_subplot(grid[1])
    ax0.scatter(filtered_presto['MaxSNR'], 
                inj_events['FLUENCE']/np.sqrt(inj_events['WIDTH']))
    ax0.plot(filtered_presto['MaxSNR'], a*filtered_presto['MaxSNR']+b)
    ax0.set_xlabel("Presto SNR")
    ax0.set_ylabel("Fluence/ sqrt width")
    ax0.set_title( "Fluence/Sqrt Width at SNR 10 is {0}, Slope is {1} ".format(Y,a))


    #Width vs Inj Fluence/sqrt width
    #fit a line to the scatter plot
    a1,b1=np.polyfit(inj_events['WIDTH'], 
                   (inj_events['FLUENCE']/np.sqrt(inj_events['WIDTH'])), 
                   1)

    ax1=fig.add_subplot(grid[0])
    ax1.scatter(inj_events['WIDTH'], 
                inj_events['FLUENCE']/np.sqrt(inj_events['WIDTH']))
    ax1.plot(inj_events['WIDTH'], a1*inj_events['WIDTH']+b1)
    ax1.set_xlabel("Width")
    ax1.set_ylabel("Fluence/ sqrt Width")
    ax1.set_title( "slope a is {0} , intercept b is {1} ".format(a1,b1))

    #Presto SNR vs Inj SNR
    #fit a line to the scatter plot
    a2,b2=np.polyfit(filtered_presto['MaxSNR'], 
                   inj_events['SNR'], 
                   1)

    ax2=fig.add_subplot(grid[2])
    ax2.scatter(filtered_presto['MaxSNR'], 
               inj_events['SNR'])
    ax2.plot(filtered_presto['MaxSNR'], a2*filtered_presto['MaxSNR']+b2)
    ax2.set_xlabel("Presto SNR")
    ax2.set_ylabel("Inj SNR")
    ax2.set_title( "slope a is {0} , intercept b is {1} ".format(a2,b2))

    #Histogram of Inj SNR
    ax3 = fig.add_subplot(grid[3])
    ax3.hist(inj_events['SNR'], bins= 20)
    ax3.set_xlabel("Inj SNR")
    ax3.set_ylabel("Counts")

    #Histogram of Presto SNR
    ax4 = fig.add_subplot(grid[4])
    ax4.hist(clust_info['MaxSNR'], bins= 20)
    ax4.set_xlabel("Presto SNR")
    
    fig.savefig(plot_name, dpi=100)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("h5", type=str, help='path to h5 candidate file')
    args = parser.parse_args()
    h5 = args.h5
    
    #Use path lib to workout with paths
    h5_path = Path(args.h5)
    #extract the parent dir from h5_path
    parent_dir = h5_path.parent
    #make the plotname with path to be passed to make_plots func
    plot_name= parent_dir.joinpath(parent_dir,"stats.png")
    
    #read the h5 file with h5py
    hdf_file=h5py.File(h5_path,'r')
    #process the hdf data
    inj_events, filtered_presto,clust_info= hdf_process(hdf_file)
    
    #make the plots for various statistical estimates
    make_plots(inj_events, filtered_presto, plot_name,clust_info)
