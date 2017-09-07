#!/bin/env python

"""
If dicom tag is missing, insert with specified value.
"""

import os
import subprocess


def find_dicoms(dicom_dir,dicom_ext="IMA"):
    """
    find dicom files
    """
    #note: for windows, copy git bash's find.exe in this source directory(otherwise, it will use windows' find)
    find_cmd = 'find {} -type f -name "*{}"'.format(dicom_dir,dicom_ext)
    find_output = subprocess.check_output(find_cmd, shell=True)
    full_filename_list = find_output.splitlines()
    return full_filename_list

def remove_non_dicom_file(full_filename_list):
    for filename in full_filename_list:
        try:
            dcmftest_cmd = 'dcmftest {}'.format(filename)
            dcmftest_output = subprocess.check_output(dcmftest_cmd, shell=True)
        except subprocess.CalledProcessError as e: #no in dcmftest_output
            os.remove(filename)
            print 'removed non-dicom file: ',filename

def check_and_insert_dicom_tag(full_filename_list,modify_tag_dict):
    """
    check dicom tag, if not present, insert

    for each file:
        1. if does not has dicom_tag
        2. insert dicom tag
    """
    
    for filename in full_filename_list:

        try:
            for k,v in modify_tag_dict.items():
                dcmdump_cmd = 'dcmdump --quiet +Ep +P {} {} '.format(k,filename)
                #print dcmdump_cmd

                dcmdump_output = subprocess.check_output(dcmdump_cmd, shell=True)
                #print dcmdump_output
                if k not in dcmdump_output:
                    dcmodify_cmd = 'dcmodify -i "({})={}" {}'.format(k,v,filename)
                    dcmodify_output = subprocess.check_output(dcmodify_cmd, shell=True)
                    print 'tag inserted: ',filename

        except subprocess.CalledProcessError as e:
            print "returncode ", e.returncode
            print "cmd ", e.cmd
            print "message", e.message
            print "output ", e.output
                
ROOT_DIR="D:\\shared_folder\\dicoms\\"
subj_dirs=['2017.03.01.TOPSY.002',
'2017.03.01.TOPSY.003', \
'2017.03.10.TOPSY.004', \
'2017.03.15.TOPSY.005', \
'2017.03.24.TOPSY.006', \
'2017.03.27.TOPSY.007', \
'2017.03.28.TOPSY.008', \
'2017.03.31.TOPSY.009', \
'2017.04.05.TOPSY.010', \
'2017.04.07.TOPSY.011', \
'2017.04.13.TOPSY.012', \
'2017.04.20.TOPSY.013', \
'2017.04.21.TOPSY.014', \
'2017.04.21.TOPSY.015', \
'2017.04.25.TOPSY.016', \
'2017.05.09.TOPSY.017', \
'2017.05.12.TOPSY.018', \
'2017.05.15.TOPSY.019', \
'2017.05.17.TOPSY.020', \
'2017.05.29.TOPSY.021', \
'2017.05.30.TOPSY.022']

#Can add more tag:value.
#0008,0008:imageType
modify_tag_dict={'0008,0008':'empty'} 
dicom_ext="IMA"

for subj_dir in subj_dirs:
    dicom_dir = os.path.join(ROOT_DIR,subj_dir)
    
    #remove non-dicom files
    full_filename_list = find_dicoms(dicom_dir,dicom_ext)
    remove_non_dicom_file(full_filename_list)

    #check and instert tag
    full_filename_list = find_dicoms(dicom_dir,dicom_ext)
    check_and_insert_dicom_tag(full_filename_list,modify_tag_dict)
