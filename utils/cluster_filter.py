#!/usr/bin/env python
# coding: utf-8

"""
HARDCODED VERSION OF LEGACY CODE DEVELOPED BY ME IN PRIMITIVE FORM UPON WHICH THE 
SOPHISTICATED FILTERING ALGORITHM OF THE CHIME/SLOW CLUSTERING IS BASED ON.

This code works on clustered singlepulse search data and finds only peaky signals by
analysing the DM vs SNR space and DM vs TIME space.

THIS CODE IS NOT USABLE HERE BUT CAN SERVE AS TEMPLATE UPON WHICH FURTHER WORK CAN BE BUILT.
"""
import ast
import argparse
from tkinter import W
import hdbscan
import h5py
import numpy as np
from numpy.lib.recfunctions import unstructured_to_structured
import matplotlib.pyplot as plt
import seaborn as sns



hf = h5py.File('1648579542_1648584342_beam_2123_016_ms.h5', 'r')
cluster_info = np.array(hf.get('cluster_info'))
det_info_unclean = np.array(hf.get('det_events'))
n_clusters = len(np.unique(det_info_unclean['Labels'])[1:])

DM_norm= 1
TIME_norm= 1
dmspace=50
maxminsnr=3
dmmaxsnr=15
minclussize=5
minsamsize=5
beam=2123
date='2022/03/29'

#WORKING ON UNCLEAN DATA
color_palette = sns.color_palette('CMRmap', n_clusters)
cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in det_info_unclean['Labels']]
cluster_member_colors = [sns.desaturate(x, p) for x, p in zip(cluster_colors,
                                                              det_info_unclean['Prob'])]

plt.figure(figsize=(20, 15))
#PLOT UNCLEAN DATA 
plt.subplot(2,1,1)
plt.title('Without filter \nminclussize:{0:d},minsamsize:{1:d},beam:{2:d},date:{3:s}'.format(minclussize,
                                                                                             minsamsize,
                                                                                            beam,
                                                                                            date))
   
plt.xlabel('TIME (s)', fontsize=15)
plt.ylabel('DM (pc $cm^{-3}$)', fontsize=15)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim([TIME_norm*det_info_unclean['TIME'].min()-1000,
          TIME_norm*det_info_unclean['TIME'].max()+1000])

plt.scatter(det_info_unclean['TIME']*TIME_norm, det_info_unclean['DM']*DM_norm, marker='.',
            s=10*det_info_unclean['SNR'], alpha=1, c=cluster_colors)


#Filter to retain clusters away from zero dm with short streaks,peak structure in snr vs dm
retaining=np.where((cluster_info['DiffDM']<=50) & 
                   (cluster_info['Max-MinSNR']>=3) &  
                   (cluster_info['DMMaxSNR']>=15))

#Discard clusters which dont fullfill the filter condition
cluster_info_discard= np.delete(cluster_info, retaining)

#Retain clusters that fullfill the filter condition
cluster_info=cluster_info[retaining]
print('No of clusters after filteration',len(cluster_info['Labels']))

#REPLACING THE LABELS for the discarded cluster labels with -1 (noise)
det_info_unclean['Labels'][np.isin(det_info_unclean['Labels'],
                                            cluster_info_discard['Labels'])] = -1

det_info= det_info_unclean


#WORKING ON CLEAN DATA
good_labels_clean = det_info['Labels'] > -1
det_info = det_info[good_labels_clean]

color_palette_clean = sns.color_palette('CMRmap', n_clusters)
cluster_colors_clean = [color_palette_clean[x] if x >= 0 else (0.5, 0.5, 0.5) for x in det_info['Labels']]
cluster_member_colors_clean = [sns.desaturate(x, p) for x, p in zip(cluster_colors_clean,
                                                              det_info['Prob'])]

#PLOT CLEAN DATA
plt.subplot(2,1,2)
plt.title('With filter \ndmspace:{0:d},max-minsnr:{1:d},dmmaxsnr:{2:d},minclussize:{3:d},minsamsize:{4:d}'.format(dmspace,
                                                                                                    maxminsnr,
                                                                                                    dmmaxsnr,
                                                                                                    minclussize,
                                                                                                    minsamsize))
plt.xlabel('TIME (s)', fontsize=15)
plt.ylabel('DM (pc $cm^{-3}$)', fontsize=15)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim([TIME_norm*det_info_unclean['TIME'].min()-1000,
          TIME_norm*det_info_unclean['TIME'].max()+1000])
plt.ylim([DM_norm*det_info_unclean['DM'].min(),
        DM_norm*det_info_unclean['DM'].max()])

plt.scatter(det_info['TIME']*TIME_norm, det_info['DM']*DM_norm, marker='.',
            s=10*det_info['SNR'], alpha=1, c=cluster_colors_clean)
                                                                                                
plt.savefig('filter_nofilter_plot.jpg')


