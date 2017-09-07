import os

def create_key(template, outtype=('nii.gz'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1 = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    #t2 = create_key('anat/sub-{subject}_T2w')
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_acq-{acq}_run-{item:02d}_bold')
    dwi_PA = create_key('sub-{subject}/dwi/sub-{subject}_acq-PA_run-{item:02d}_dwi')
    dwi_AP = create_key('sub-{subject}/dwi/sub-{subject}_acq-AP_run-{item:02d}_dwi')
    fmap_diff = create_key('sub-{subject}/fmap/sub-{subject}_run-{item:02d}_phasediff')
    fmap_magnitude = create_key('sub-{subject}/fmap/sub-{subject}_run-{item:02d}_magnitude')

    #info = {t1:[], t2:[], rest:[], face:[], gamble:[], conflict:[], dwi:[], fmap_rest:[], fmap_dwi:[]}
    info = {t1:[],rest:[],dwi_PA:[],dwi_AP:[],fmap_diff:[],fmap_magnitude:[]}
    for idx, s in enumerate(seqinfo):
        #anat
        if  ('mp2rage' in s.protocol_name):
            if (s.dim4 == 1) and ('UNI-DEN' in (s.series_description).strip()):
                info[t1] = [s.series_id]

        #func    
        if ('bold' in s.protocol_name):
            if (s.dim4 == 360) and ('mbep2d_bold_mb3_p3_AP_rs' in (s.series_description).strip()):
                info[rest].append({'item': s.series_id, 'acq': 'AP'})
            #if (s.dim4 == 1) and ('mbep2d_bold_mb3_p3_PA' == s.series_description):
            #    info[rest].append({'item': s.series_id, 'dir': 'PA'})

        #dwi
        if ('diff' in s.protocol_name):
            #if (s.dim4 == 66) and ('mbep2d_diff_b1000_AP' == s.series_description):
            if ( s.dim4 > 1 and ('mbep2d_diff_b1000_AP' == (s.series_description).strip()) ) :
                info[dwi_AP].append({'item': s.series_id})
            #if (s.dim4 == 66) and ('mbep2d_diff_b1000_PA' == s.series_description):
            if ( s.dim4 > 1 and ('mbep2d_diff_b1000_PA' == (s.series_description).strip()) ):
                info[dwi_PA].append({'item': s.series_id})

        #field map   
        if ('field_mapping' in s.protocol_name):   
            if (s.dim4 == 1) and ('gre_field_mapping' == (s.series_description).strip()):
                if(s.dim3 == 64):
                    info[fmap_diff].append({'item': s.series_id})
                if(s.dim3 == 128):
                    info[fmap_magnitude].append({'item': s.series_id})
        
    return info
