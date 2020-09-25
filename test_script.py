# -*- coding: utf-8 -*-

import math 
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np

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

# Determine if oscilation pattern 1
# If 0: pattern exists
# Else, no Oscillation 1 pattern
temp['osc1'] = \
    np.concatenate(temp.groupby('id')
                   .apply(lambda x: haversine(x['lat'], x['lon'], x['lat'].shift(2), x['lon'].shift(2))).values)

# Osciallation pattern 2 is if one_four = 0 AND two_three = 0
temp['one_four'] = \
    np.concatenate(temp.groupby('id')
                   .apply(lambda x: haversine(x['lat'], x['lon'], x['lat'].shift(3), x['lon'].shift(3))).values)

temp['two_three'] = \
    np.concatenate(temp.groupby('id')
                   .apply(lambda x: haversine(x['lat'].shift(), x['lon'].shift(), x['lat'].shift(2), x['lon'].shift(2))).values)

            


# Creating segments based on displacement of consecutive records
temp['segments_lprime'] = \
    np.concatenate(temp.groupby('id')
                   .apply(lambda x: segment_creation(x['displacement'], 3))

# Timestamp of first record in a segment (cluster)
temp['start_time_tprime'] = \
    np.concatenate(temp.groupby('segments').first())
                   #.apply(lambda x: x['timestamp'].first()))

# Timestamp of last record in a segment (cluster)
temp['end_time_dur'] = \
    np.concatenate(temp.groupby('segments').last())
                   #.apply(lambda x: x['timestamp'].last()))



# Determine statistics based on segments
# Calculate the midpoint of each segment (cluster)
temp['lat_sum'] = temp['lat'].groupby(temp['segments']).transform('sum')
temp['lon_sum'] = temp['lon'].groupby(temp['segments']).transform('sum')
temp['lat_len'] = temp['lat'].groupby(temp['segments']).transform('count')
temp['lon_len'] = temp['lon'].groupby(temp['segments']).transform('count')

temp['midpoint_lat_segment'] = temp['lat_sum']/temp['lat_len']
temp['midpoint_lon_segment'] = temp['lon_sum']/temp['lon_len']

# Second stage of clustering is segments that are within a predetermined distance but not consecutive (repeat visit to location)
gb_segs = pd.DataFrame(temp.groupby(['segments', 'segments_lprime', 'start_time_tprime', \
                        'end_time_dur', 'midpoint_lat_segment', 'midpoint_lon_segment'])
                       .count()).reset_index()

gb_segs['midpoint_displacement'] = \
    np.concatenate(gb_segs.groupby('segments')
                     .apply(lambda x: haversine(x['midpoint_lat_segment'], x['midpoint_lon_segment'], x['midpoint_lat_segment'].shift(), x['midpoint_lon_segment'].shift())).values)

gb_segs['new_segments'] = \
    np.concatenate(gb_segs.groupby('segments')
                   .apply(lambda x: segment_creation(x['midpoint_displacement'], 3))













