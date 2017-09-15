# files:
dcm2BIDS_batch.py  
  * batch converts dicom to BIDS	

7T_TOPSY_BIDS_heuristic.py  
  * heuristic file

dicom_retrive.py:  
  * retrieve dicom files from CFMM-Public@dicom.cfmm.robarts.ca:11112 (use dcm4che getscu) by patientID
    example: python dicom_retrieve.py 7T_BIDS_patientID_list.txt ~/test username password
		
7T_BIDS_patientID_list.txt:  
  * patientID list to retrieve
		
dicom_anon.py:  
  * dicom anonymization(not finished yet!)
	
check_and_add_ImageType.py  
  * If dicom tag is missing, insert with specified value.
  some 7T topsy missing the ImageType tag, heudiconv reports and error! use this script to fix it.

# How to build your own heuristic.py file and run it? 
1. install bids-validator  
  *  Install Node.js (at least version 4.4.4)  
	`sudo apt-get update`  
	`sudo apt-get install nodejs`  
	`sudo apt-get install npm`  
	*  install bids-validator  
	`npm install -g bids-validator`  
	`npm install -g bids-validator`  
	`sudo ln -s /usr/bin/nodejs /usr/bin/node`  

2.  pull docker image:  
    `docker pull nipy/heudiconv`

3. test heudiconv:  
   `docker run --rm -it nipy/heudiconv -h`   
   you should get the following:

		usage: heudiconv [-h] [--version] [-d DICOM_DIR_TEMPLATE]
		...

4. prepare your dicom folders:  
  project1  
  |-test001  
	|-test002  
	...
	
	note 1: Use letters and numbers only for folder name.  
	note 2: test### can have sub-folders, which hold dicom files.
	
5. generate dicominfo.tsv file:  
	`docker run --rm -it -v /mnt/hgfs/data/project1:/data nipy/heudiconv --overwrite -b -d /data/{subject}/*IMA -s test001 -f /data/7T_TOPSY_BIDS_heuristic.py -c none -o /data/BIDS_output`
   
		-v, create a bind mount: mount local's '/mnt/hgfs/data/test' to container's '/data'
		-b, --bids            flag for output into BIDS structure
		--overwrite           flag to allow overwrite existing files
		-d DICOM_DIR_TEMPLATE, --dicom_dir_template DICOM_DIR_TEMPLATE
			  location of dicomdir that can be indexed with subject
				id {subject} and session {session}. Tarballs (can be
	
	This command create a hidden folder:
	`project1\BIDS_output\.heudiconv`
		
	The "project1\BIDS_output\\.heudiconv\004\info\dicominfo.tsv" file has the dicom parsing information for writing your project-specific heuristic.py file.
						
6. write your own heuristic.py based on the dicominfo.tsv, there are many examples:  
   https://github.com/nipy/heudiconv/tree/master/heuristics

7. test your heuristic.py file
	`docker run --rm -it -v /mnt/hgfs/data/project1:/data nipy/heudiconv --overwrite -b -d /data/{subject}/*IMA -s test001 -f /data/7T_TOPSY_BIDS_heuristic.py -c dcm2niix -b -o /data/BIDS_output`  

8. validator BIDS output
	`bids-validator BIDS_output`

9. batch converting(reference dcm2BIDS_batch.py)


# How to configure/run dicom_retrieve.py? 
1. install Java  
  `sudo apt-get install -y default-jre`

2. run '20.install_dcm4che_ubuntu.sh'  

3. test dcm4che's getscu  
`getscu --bind DEFAULT --connect CFMM-Public@dicom.cfmm.robarts.ca:11112 --tls-aes --user YOUR_UWO_USERNAME --user-pass YOUR_PASSWORD, -m StudyInstanceUID=1.3.12.2.1107.5.2.34.18932.30000017052914152689000000013`  
	note: use correct username and password(if give wrong credentials,there is an Error: java.lang.Thread.run(Thread.java.748)).

4. run dicom_retrive.py  
`python dicom_retrieve.py list.txt output_directory username password`  
note: put patientID in list.txt(refer example:7T_BIDS_patientID_list.txt)
  
