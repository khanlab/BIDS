#!/usr/bin/env python

import os
import subprocess

# ROOT_DIR
	# -DICOM_DIR
		# -sub1
		# -sub2
		# ...
	# OUTPUT_SUBDIR
		# -sub1
		# -sub2
		# ...
	# HEURISTIC_FILE
	
ROOT_DIR='/mnt/hgfs/data/7T_BIDS/'
DICOM_SUBDIR='dicoms'
DICOM_EXT="IMA"
HEURISTIC_FILE = '7T_TOPSY_BIDS_heuristic.py'
OUTPUT_SUBDIR='BIDS_output2'


subjs = ['001', \
'002', \
'003', \
'004', \
'005', \
'006', \
'008', \
'010' \
'011', \
'012', \
'013', \
'014', \
'015', \
'016', \
'017', \
'018', \
'019', \
'020', \
'022'
]

subjs_str = ' '.join(subjs)

cmd = 'docker run --rm -it -v {}:/data nipy/heudiconv -b -d /data/{}/{{subject}}/*{} -s {}  -f /data/{} -c dcm2niix -b -o /data/{}'.format(ROOT_DIR,DICOM_SUBDIR,DICOM_EXT,subjs_str,HEURISTIC_FILE,OUTPUT_SUBDIR)
print cmd

try:
	output = subprocess.check_output(cmd, shell=True)
	print output
	
except subprocess.CalledProcessError as e:
	print "returncode ", e.returncode
	print "cmd ", e.cmd
	print "message", e.message
	print "output ", e.output			
