# Simple routines

### 1) dat_to_filterbank.py
Dat file convertor to filterbank from the CHIME/SPS cluster. 
<br />
##### Usage
 `python dat_to_filterbank.py --args`
 
### 2) gaussian_filterbank.py 
Create a simple filterbank file of nchannels and nsamples using gaussian noise.
<br />
##### Usage
`python gaussian_filterbank.py --args`

### 3) msgpack_to_filterbank.py
MSGPACK to filterbank file converter for the CHIME/FRB intensity data.
<br />
##### Usage
`python msgpack_to_filterbank.py --args` 


### 4) msgpack_to_nparray.py
MSGPACK to nparray file converter for the CHIME/FRB intensity data.
<br />
##### Usage
`python msgpack_to_nparray.py --args` 

### 5) dynamicspectra.py
Plotting dynamic spectra i:e waterfall plots from the filterbank files
<br />
##### Usage
`python dynamicspectra.py --args` 

### 6) filpulse.py
Creating a fake frb with Kendrick Smith's simpulse and putting it in filterbank format.
<br />
##### Usage
`python filpulse.py --args` 

### 7) skyview_image.py
Query any of the popular survey and plot the image for a given coordinate.
<br />
##### Usage
`python skyview_image.py --args` 

### 8) simbad_query.py
Query any of the simbad data base survey and print the table with all the objects.
<br />
##### Usage
`python simbad_query.py --args` 

### 9) ned_query.py
Query any of the ned data base survey for a ra dec  and print the table with all the objects and save the table and plot the images along with saving them.
<br />
##### Usage
`python ned_query.py --args` 

### 10) sdss_query.py
Query any of the sdss data base survey for a given object name   and get the spectra and the image 
<br />
##### Usage
`python sdss_query.py --args` 

### 11) sdss_skyservice.py
Query any of the sdss skyservice client for a given ra and dec  and get the image 
<br />
##### Usage
`python sdss_skyservice.py --args` 

### 12) fourier_candidates.py
Perform fourier transform on pulsar timeseries data and check for frequencies of highest magnitude.
<br />
##### Usage
`python fourier_candidates.py --args` 

### 13) ignorechan_range_filler.py
Convert the PRESTO comma seperated range txt file containing ignorechannels to txt file of list of filled channels between the ranges
<br />
##### Usage
`python ignorechan_range_filler.py --args` 

### 14) msgpack_directconverter.py
Convert the CHIME/FRB L1 intensity msgpack data to numpy arrays.
<br />
##### Usage
`python msgpack_directconverter.py --args` 


`pulsar_studies.py and cluster_filter.py dont run. They are skeleton codes whose parts can be used somehwere useful ;)`






