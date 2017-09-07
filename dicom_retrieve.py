#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
author: YingLi Lu
date: 2017-08-10
version:1.0
'''

import os
import subprocess
import sys
import socket
import time
from shutil import move,rmtree
from collections import defaultdict

from imp import reload
import logging
reload(logging)


CONNECT = 'CFMM-Public@dicom.cfmm.robarts.ca:11112'

#patient ID(0010,0020)

def retrieve(connect,subj_dir,matching_key,username,password):
    '''
    retrieve by mathing key
    '''

    if not os.path.exists(subj_dir):
        os.makedirs(subj_dir)
    
    #getscu --bind DEFAULT --connect CFMM-Public@dicom.cfmm.robarts.ca:11112 --tls-aes --user YOUR_UWO_USERNAME --user-pass YOUR_PASSWORD -m StudyInstanceUID=1.3.12.2.1107.5.2.34.18932.30000017052914152689000000013
    cmd = 'getscu' +\
          ' -L PATIENT -M PatientRoot '+\
          ' --bind  DEFAULT ' +\
          ' --connect {} '.format(connect) +\
          '--tls-aes --user {} --user-pass {} '.format(username,password) +\
          ' -m {}'.format(matching_key) +\
          ' --directory {}'.format(subj_dir)

    logger.debug(cmd)
    output = subprocess.check_output(cmd, shell=True)
	
if __name__ == '__main__':

    if len(sys.argv) < 5:
        print ("usage: python dicom_retrieve.py list.txt output_directory username password")
        print ("example: python dicom_retrieve.py 7T_BIDS_project_cases.txt ~/test UWO_username UWO_password")
        sys.exit()

    output_dir = sys.argv[2]    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    username = sys.argv[3]
    password = sys.argv[4]

    #log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)#DEBUG

    #log to console
    console_formatter = logging.Formatter('%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)#INFO
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)
    #log to file:output_dirctory/list_log.txt
    log_file_fullname = os.path.join(sys.argv[2],sys.argv[1][:-4]+'_log.txt')
    
    file_formatter = logging.Formatter('%(filename)s:%(lineno)s:%(funcName)s:%(message)s')
    fh = logging.FileHandler(log_file_fullname,'w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    processed_patientID=[] #avoid re-retrieve if there are duplicates in the list
    failed_cases=[]
    with open(sys.argv[1],"r") as f:
        lines = f.readlines()
        for line in lines:

            line_s = line.strip()
            if (line_s == ''): #ignore blank line
                continue

            line_s = line_s.split()
            patientID = line_s[0].strip()

            if patientID[0]=='#': #ignore comment line
                continue

            if patientID in processed_patientID: #avoid re-retrieve
                continue
           
            logger.debug('----------------------------------------------------') #To log file
            logger.info('Processing: {}'.format(patientID))

            #1. retrieve
            try:
                
                subj_dir=os.path.join(output_dir,patientID)
                matching_key='PatientID={}'.format(patientID)
                
                retrieve(CONNECT,subj_dir,matching_key,username,password)
                
            except subprocess.CalledProcessError as e:
                logger.info('   FAILED: retrive!')
                logger.debug(e)
                logger.debug(e.output) #tell why the subprocess call FAILED
                failed_cases.append(patientID)
                continue

            except Exception as e:
                logger.info('   FAILED: retrive!')
                logger.debug(e)
                failed_cases.append(patientID)
                continue

            else:
                if os.listdir(subj_dir) == []:
                    logger.info('   FAILED: retrive: no data retrived!')
                    continue
                else:
                    logger.info('   succeed: retrive!')

            ##2. anonnmize
            # try:
                # annonymize(series_dirs, access_num)

            # except subprocess.CalledProcessError as e:
                #ignore dcmmodify 'Tag not found' error: even with '-imt  --ignore-missing-tags', dcmodify return non-zero code
                # if 'Tag not found' in e.output:
                   # logger.info('   succeed: annonymize!')
                   # continue
                # else:
                    # logger.info('   FAILED: annonymize!!!!')
                    # logger.debug(e)
                    # logger.debug(e.output) #tell why the subprocess call FAILED
                    # failed_cases.append((cad_patient_num,access_num))
                    # continue

            # except Exception as e:
                # logger.info('   FAILED: annonymize!')
                # logger.debug(e)
                # failed_cases.append((cad_patient_num,access_num))
                # continue

            # else:
               # logger.info('   succeed: annonymize!')

            processed_patientID.append(patientID)

    logger.info('\n---------Summary---------')
    if failed_cases:
        logger.info('FAILED cases:')
        for e in failed_cases:
            logger.info('   {} {}'.format(e[0],e[1]))

        logger.info('Log file: ' + log_file_fullname)
    else:
        logger.info('All cases successed!')
        logger.info('Log file: ' + log_file_fullname)

	