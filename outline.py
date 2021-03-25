# Trying a skeleton outline of page 7 algorithm

# Step 1: Remove abnormal speed (> 120km/hr)



# Step 2: Clustering (Part A)

for id in data

for i in index():

d = diff_lat_lon(id[i], id[i+1])

if d > delta_d:
new_segment




import math 
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from sklearn_extra.cluster import KMedoids

def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return round(earth_radius * 2 * np.arcsin(np.sqrt(a)), 5)

def segment_creation(displacement, deltad):
    '''
    Labels consecutive records into clusters if within a certain distance

    Parameters
    ----------
    displacement (float): the distance between consecutive records
    deltad (float): max difference between consecutive records to be labeld "same location"

    Returns
    -------
    New column with cluster label

    '''
    i = 0
    if displacement < deltad:
        return 'Segment-' + i
    else:
        i+=1
        return 'Segment-' + i


temp = pd.read_csv(r'.csv')
temp = temp.sort_values(by=['id', 'date'])

# Displacement between consecutive records based on haversine distance
temp['displacement'] = \
    np.concatenate(temp.groupby('id')
                     .apply(lambda x: haversine(x['lat'], x['lon'], x['lat'].shift(), x['lon'].shift())).values)

    # Creating segments based on displacement of consecutive records
temp['segments_lprime'] = \
    np.concatenate(temp.groupby('id')
                   .apply(lambda x: segment_creation(x['displacement'], 3))

# Timestamp of first record in a segment (cluster)
temp['start_time_tprime'] = \
    np.concatenate(temp.groupby('segments').first())

# Timestamp of last record in a segment (cluster)
temp['end_time_tprime'] = \
    np.concatenate(temp.groupby('segments').last())

# Time duration of the segment
temp['segment_duration'] = \
	np.concatenate(temp.groupby('segments')
		.apply(lambda x: x['end_time_tprime'] - x['start_time_tprime']))

# Create a combined lat/lon in order to determine the mediod of the cluster
temp['combined_lat_lon'] = list(zip(temp['lat'], temp['lon']))

# Create a new DF with just the segment information
segments_df = pd.DataFrame(temp.groupby(['segments_lprime', 'start_time_tprime', 'segment_duration'])['combined_lat_lon'].apply(list)).reset_index()

# Calculate the mediod of each segment
segments_df['mediod'] = KMedoids(n_clusters=2, random_state=0).fit(segments_df['combined_lat_lon']).cluster_centers_

# At this point, We should have a data frame with the following columns:
# Segment number, the starting time, the duration of the segment, and the mediod of the segment

## Last paragraph, page 7, left column:
# Clustering Stage 2

# split the mediod into lat lon columns

segments_df[['mediod_lat','mediod_lon']] = segments_df.mediod.str.split(',', expand=True)


for mediod in segments_df:

	diff = comparing_mediods(mediod['lat'], mediod['lon'], delta)

def comparing_mediods(lat, lon, delta_d2):

	for mediod2 in segments_df:

		diff = haversine(lat, lon, mediod2['lat'], mediod2['lon'])

		if diff > 0 and diff < delta_d2:


