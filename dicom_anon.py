
ROBARTS_DCM_UID = '1.2.826.0.1.XXXXXXX.X.XXXX.'

#generate study_instance_UID 

def generate_study_instance_UID(access_num):
    host_id = socket.gethostbyname(socket.gethostname()) #local ip address
    tt = time.time() # time(). e.g. '1335218455.013'(14), '1335218447.9189999'(18)
    shorttime = '%10.5f' % (tt)
    study_instance_UID = ROBARTS_DCM_UID + shorttime + '.' + host_id + str(access_num).strip()

    return study_instance_UID

#generate seriesInstanceUID	
def generate_seriesInstanceUID(series_number ,index):
    host_id = socket.gethostbyname(socket.gethostname()) #local ip address
    tt= time.time() # time(). e.g. '1335218455.013'(14), '1335218447.9189999'(18)
    shorttime = '%10.5f' % (tt)
    host_id_width = len(host_id)
    shost_ID = host_id[host_id_width-6:host_id_width] # Take the last 6 digits
    series_instance_UID = ROBARTS_DCM_UID + '' + shorttime + '' + shost_ID + series_number + str(index).zfill(2)

    return series_instance_UID
	
def annonymize(series_dirs, access_num):

    '''
   annoymize


    Todo: follow the BASIC APPLICATION LEVEL CONFIDENTIALITY PROFILE:http://dicom.nema.org/Dicom/supps/sup55_03.pdf
        Patient's Name (0010,0010)
        Patient ID (0010,0020)
        Patient's Birth Date (0010,0030)
        Patient's Sex (0010,0040)
        Patient's Birth Time (0010,0032)
        Other Patient IDs (0010,1000)
        Other Patient Names (0010,1001)
        Ethnic Group (0010,2160)
        Patient Comments (0010,4000)
        Referring Physician's Name (0008,0090)
        Study ID (0020,0010)
        Accession Number (0008,0050)
        Study Description (0008,1030)
        Physician(s) of Record (0008,1048)
        Name of Physician(s) Reading Study (0008,1060)
        Admitting Diagnoses Description (0008,1080)
        Patient's Age (0010,1010)
        Patient's Size (0010,1020)
        Patient's Weight (0010,1030)
        Occupation (0010,2180)
        Additional Patient’s History (0010,21B0)
        Performing Physicians’ Name (0008,1050)
        Protocol Name (0018,1030)
        Series Description (0008,103E)
        Operators' Name (0008,1070)
        Institution Name (0008,0080)
        Institution Address (0008,0081)
        Station Name (0008,1010)
        Institutional Department Name (0008,1040)
        Device Serial Number (0018,1000)
        Derivation Description (0008,2111)
        Image Comments (0020,4000)
    '''

    patient_id_anon = cad_patient_num + 'Pat'
    patinet_name_anon = 'Patient ' + cad_patient_num + 'Anon'
    ClinicTrialNo_anon = cad_patient_num
    study_instance_uid_anon = generate_study_instance_UID(access_num)

    index =0
    for series_dir in series_dirs:
        index = index+1
        series_number = os.path.split(series_dir)[-1]
        series_instance_uid_anon = generate_seriesInstanceUID(series_number,index)

        cmd = 'find {} -type f -name "*.IMA" -print0 '.format(series_dir)+\
             '| xargs --null dcmodify -ie -gin -nb -imt '+\
              ' -m "(0020,000D)={}"'.format(study_instance_uid_anon)+\
              ' -m "(0020,000e)={}"'.format(series_instance_uid_anon)+\
              ' -m "(0010,0010)={}"'.format(patinet_name_anon)+\
              ' -ma "(0010,0020)={}"'.format(patient_id_anon)+\
              ' -i "(0012,0010)={}"'.format(CLINICAL_TRIAL_SPONSOR)+\
              ' -i "(0012,0020)={}"'.format(CLINICAL_TRIAL_PROTOCOL_ID)+\
              ' -ea "(0008,0090)"'+\
              ' -ea "(0008,1050)"'+\
              ' -ea "(0008,1060)"'+\
              ' -ea "(0008,1070)"'+\
              ' -ea "(0010,0030)"'\
              ' -ea "(0010,1000)"'+\
              ' -ea "(0010,1001)"'+\
              ' -i  "(0012,0040)={}"'.format(ClinicTrialNo_anon)+\
              ' -ea "(0032,1032)"'+\
              ' -ea "(0033,1002)"'+\
              ' -ea "(0033,1013)"'+\
              ' -ea "(0033,1016)"'+\
              ' -ea "(0033,1019)"'+\
              ' -ea "(0033,1006)"'+\
              ' -ea "(0033,1008)"'

        
        logger.debug(cmd)
        output = subprocess.check_output(cmd, shell = True)