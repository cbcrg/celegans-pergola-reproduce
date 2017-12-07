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
import h5py
from sys import stderr
import numpy as np
from csv import writer
from os.path import basename

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

f = h5py.File(input_file, 'r')
time_series = f['features_timeseries']

## speed stuff
velocity_keys = ['headTip', 'head', 'midbody', 'tail', 'tailTip']
## velocity_keys = ['head_tip', 'head', 'midbody', 'tail', 'tail_tip']

fs = open(file_name + ".csv",'wb')

writer_out = writer(fs, dialect = 'excel-tab')

writer_out.writerow(['frame_start', 'frame_end']  + sorted(velocity_keys) + ['foraging_speed', 'tail_motion', 'crawling'])


for frame in range(0, len(time_series)):
    list_v = list()
    list_v.extend([frame, frame + 1])

    velocity_keys = range(43, 47 + 1)

    # foraging angle speed index=54
    # tail motion (in the new files tail_orientation index 20)
    # Crawling in the new file midbody_crawling_amplitude index 39
    velocity_keys.extend([54, 20, 39])
    # velocity_keys = [45]
    for velocity_k in sorted(velocity_keys):

        try:
            v = time_series[frame][velocity_k]
        except KeyError:
            raise KeyError("Velocity field %s is corrupted and can not be retrieved from hdf5 file"
                           % (velocity_k, frame))

        if np.isnan(v): v = -10000

        list_v.append(v)

    writer_out.writerows([list_v])

fs.close()
f.close()