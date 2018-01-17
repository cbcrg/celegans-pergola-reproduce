#!/usr/bin/env python

#  Copyright (c) 2014-2017, Centre for Genomic Regulation (CRG).
#  Copyright (c) 2014-2017, Jose Espinosa-Carrasco and the respective authors.
#
#  This file is part of Pergola.
#
#  Pergola is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pergola is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Pergola.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################
### Jose Espinosa-Carrasco NPMMD/CB-CRG Group. May 2016                   ###
#############################################################################
### Reads mat lab files downloaded from the Wormbehavior DB               ###
### (http://wormbehavior.mrc-lmb.cam.ac.uk/). Each file contains several  ###
### features extracted from C.elegans video trackings.                    ###
### Read features are foraging_speed, crawling, tail_motion and speeds    ###
### measured on different body parts                                      ###
#############################################################################

# Loading libraries
from argparse import ArgumentParser
from sys import stderr
import numpy as np
from csv import writer
from os.path import basename
from os import rename
import pandas as pd

parser = ArgumentParser(description='File input arguments')
parser.add_argument('-i', '--input', help='Worms data hdf5 format matlab file', required=True)

args = parser.parse_args()

print >> stderr, "Input file: %s" % args.input

# Input files
input_file = args.input

file_name = basename(input_file).split('.')[0]
file_name = file_name.replace(" ", "_")
file_name = file_name.replace('(', '')
file_name = file_name.replace(')', '')

with pd.HDFStore(input_file, 'r') as fid:
    time_series = fid['/features_timeseries']

## motion stuff
f_b = open(file_name + "." + "backward" + ".csv",'wb')
f_p = open(file_name + "." + "paused" + ".csv",'wb')
f_f = open(file_name + "." + "forward" + ".csv",'wb')

writer_out_b = writer(f_b, dialect='excel-tab')
writer_out_p = writer(f_p, dialect='excel-tab')
writer_out_f = writer(f_f, dialect='excel-tab')

writer_out_b.writerow(['frame_start', 'frame_end', 'value', 'direction'])
writer_out_p.writerow(['frame_start', 'frame_end', 'value', 'direction'])
writer_out_f.writerow(['frame_start', 'frame_end', 'value', 'direction'])

def motion_state_f(x):
    return {
        -1:'backward',
        1: 'forward',
        0: 'paused',
        'nan': 'nan'
    }[x]

motion_index = 3
p_motion_state = "first"

# for frame in range(0, len(time_series)):
for frame in range(0, time_series['motion_modes'].size - 1):
    try:
        motion_integer = time_series['motion_modes'][frame]
    except KeyError:
        raise KeyError("Motion field %s is corrupted and can not be retrieved from hdf5 file"
                       % (frame))

    if not np.isnan(motion_integer):
        motion_state = motion_state_f(motion_integer)
    else:
        motion_state = 'nan'

    if motion_state == "first":
        start_frame = frame

    elif motion_state != p_motion_state:
        if p_motion_state == "forward":
            writer_out_f.writerows([[start_frame, frame-1, 1000, p_motion_state]])

        elif p_motion_state == "backward":
            writer_out_b.writerows([[start_frame, frame-1, 1000, p_motion_state]])

        elif p_motion_state == "paused":
            writer_out_p.writerows([[start_frame, frame-1, 1000, p_motion_state]])

        start_frame = frame

    p_motion_state = motion_state

f_b.close()
f_p.close()
f_f.close()
