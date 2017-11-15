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

	##########################
	########## ANAT ##########
	##########################

	#Sequence 10 - 14 (mp2rage)
	inv1_mp2rage = create_key('sub-{subject}/anat/sub-{subject}_inv-1_MP2RAGE')
	t1map = create_key('sub-{subject}/anat/sub-{subject}_T1map')
	t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
	uni_mp2rage = create_key('sub-{subject}/anat/sub-{subject}_acq-UNI_MP2RAGE')
	inv2_mp2rage = create_key('sub-{subject}/anat/sub-{subject}_inv-2_MP2RAGE')
	
	#Sequence #23 - 26 (mp2rage derivatives)
	dis2d_T1w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_rec-DIS2D_T1w')
	dis3d_T1w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_rec-DIS3D_T1w')
	uni_dis2d_T1w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-UNI_rec-DIS2D_T1w')
	uni_dis3d_T1w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-UNI_rec-DIS3D_T1w')

	#Sequence #29 - 30 (spc T2w)
	spc_T2w = create_key('sub-{subject}/anat/sub-{subject}_acq-spc_T2w')

	#Sequence #31 - 32 (spc T2w derivatives)
	DIS2D_spc_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-spc_rec-DIS2D_T2w')
	DIS3D_spc_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-spc_rec-DIS3D_T2w')

	#Sequence #33 (tse tra T2w)
	tse_tra_T2w = create_key('sub-{subject}/anat/sub-{subject}_acq-tsetra_T2w')
	
	#Sequence #34 - 35 (tse tra T2w derivatives)
	tse_tra_DIS2D_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-tsetra_rec-DIS2D_T2w')
	tse_tra_DIS3D_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-tsetra_rec-DIS3D_T2w')

	#Sequence #36 - 42 (TOF angio)
	TOF_ND_angio = create_key('sub-{subject}/anat/sub-{subject}_acq-TOF_rec-ND_angio')
	TOF_angio = create_key('sub-{subject}/anat/sub-{subject}_acq-TOF_angio')
	TOF_MIP_SAG = create_key('sub-{subject}/anat/sub-{subject}_acq-TOFSAG_mip')
	TOF_MIP_COR = create_key('sub-{subject}/anat/sub-{subject}_acq-TOFCOR_mip')
	TOF_MIP_TRA = create_key('sub-{subject}/anat/sub-{subject}_acq-TOFTRA_mip')

	#Sequence #41 - 42 (TOF angio derivatives)
	TOF_DIS2D_angio = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-TOF_rec-DIS2D_angio')
	TOF_DIS3D_angio = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-TOF_rec-DIS3D_angio')

	#Sequence #43 (susceptibility ND magnitude)
	mag_ND_echo_GRE = create_key('sub-{subject}/anat/sub-{subject}_part-mag_rec-ND_echo_GRE')

	#Sequence #44 (susceptibility magnitude)
	mag_echo_GRE = create_key('sub-{subject}/anat/sub-{subject}_part-mag_echo_GRE')

	#Sequence #45 (susceptibility ND phase)
	phase_ND_echo_GRE = create_key('sub-{subject}/anat/sub-{subject}_part-phase_rec_ND_echo_GRE')

	#Sequence #46 (susceptibility phase)
	phase_echo_GRE = create_key('sub-{subject}/anat/sub-{subject}_part-phase_echo_GRE')

	#Sequence #47 (T2star)
	T2_star = create_key('sub-{subject}/anat/sub-{subject}_T2star')

	#Sequence #54 (susceptibility S43 derivatives)
	S43_DIS2D_echo_GRE = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_part-mag_acq-S43_rec-DIS2D_echo_GRE')

	#Sequence #55 (susceptibility S45 derivatives)
	S45_DIS2D_echo_GRE = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_part-mag_acq-S43_rec-DIS2D_echo_GRE')

	#Sequence #58 (tse cor T2w)
	tse_cor_T2w = create_key('sub-{subject}/anat/sub-{subject}_acq-tsecor_T2w')

	#Sequence #59 - 60 (tse cor T2w derivatives)
	tse_cor_DIS2D_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-tsecor_rec-DIS2D_T2w')
	tse_cor_DIS3D_T2w = create_key('derivatives/distortion_corrected/sub-{subject}/anat/sub-{subject}_acq-tsecor_rec-DIS3D_T2w')

	#########################
	########## DWI ##########
	#########################

	#Sequence #48 - 53 (mbep2d dwi)
	AP_dwi = create_key('sub-{subject}/dwi/sub-{subject}_acq-AP_dwi')
	AP_TRACEW_dwi = create_key('sub-{subject}/dwi/sub-{subject}_acq-APTRACEW_dwi')
	PA_b0_dwi = create_key('sub-{subject}/dwi/sub-{subject}_acq-PAb0_dwi')

	##########################
	########## FMAP ##########
	##########################

	##Sequence #3 - 6 (rel B1)
	#mag_rel_B1 = create_key('sub-{subject}/fmap/sub-{subject}_part-mag_acq-rel_B1')
	#phase_rel_B1 = create_key('sub-{subject}/fmap/sub-{subject}_part-phase_acq-rel_B1')
	#mag_rel_B1_rel_B1 = create_key('sub-{subject}/fmap/sub-{subject}_part-mag_acq-rel_B1_rel_B1')
	#phase_rel_B1_rel_B1 = create_key('sub-{subject}/fmap/sub-{subject}_part-phase_acq-rel_B1_rel_B1')

	##Sequence #7 - 9 (abs B1)
	#mag_absB1 = create_key('sub-{subject}/fmap/sub-{subject}_acq-absB1_B1')
	#phase_absB1 = create_key('sub-{subject}/fmap/sub-{subject}_acq-absB1_B1')
	#absB1_AFI = create_key('sub-{subject}/fmap/sub-{subject}_acq-absB1_AFI')

	#Sequence #15 - 16 (sa2rage inversion 1)
	ND_inv_1_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_rec-ND_inv-1_SA2RAGE')
	inv_1_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_inv-1_SA2RAGE')

	#Sequence #17 - 18 (sa2rage inversion 2)
	ND_inv_2_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_rec-ND_inv-2_SA2RAGE')
	inv_2_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_rec-ND_inv-2_SA2RAGE')

	#Sequence #19 - 20 (sa2rage b1map)
	b1map_ND_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_acq-b1map_rec-ND_SA2RAGE')
	b1map_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_acq-b1map_SA2RAGE')

	#Sequence #21 - 22 (sa2rage b1Div)
	b1Div_ND_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_acq-b1Div_rec-ND_SA2RAGE')
	b1Div_sa2rage = create_key('sub-{subject}/fmap/sub-{subject}_acq-b1Div_SA2RAGE')

	#Sequence #27 - 28 (sa2rage b1map derivatives)
	b1map_DIS2D_sa2rage = create_key('derivatives/distortion_corrected/sub-{subject}/fmap/sub-{subject}_acq-b1map_rec-DIS2D_SA2RAGE')
	b1map_DIS3D_sa2rage = create_key('derivatives/distortion_corrected/sub-{subject}/fmap/sub-{subject}_acq-b1map_rec-DIS3D_SA2RAGE')

	#Sequence #56 - 57 (GRE field map)
	mag_GRE = create_key('sub-{subject}/fmap/sub-{subject}_part-mag_GRE')
	phase_GRE = create_key('sub-{subject}/fmap/sub-{subject}_part-phase_GRE')


	info = {inv1_mp2rage:[],t1map:[],t1w:[],uni_mp2rage:[],inv2_mp2rage:[],

			dis2d_T1w:[], dis3d_T1w:[], uni_dis2d_T1w:[], uni_dis3d_T1w:[],

			spc_T2w:[], DIS2D_spc_T2w:[], DIS3D_spc_T2w:[],

			tse_tra_T2w:[], tse_tra_DIS2D_T2w:[], tse_tra_DIS3D_T2w:[],

			TOF_ND_angio:[], TOF_angio:[], TOF_MIP_SAG:[], TOF_MIP_COR:[], TOF_MIP_TRA:[], TOF_DIS2D_angio:[], TOF_DIS3D_angio:[],

			mag_ND_echo_GRE:[],

			mag_echo_GRE:[],

			phase_ND_echo_GRE:[],

			phase_echo_GRE:[],

			T2_star:[],

			S43_DIS2D_echo_GRE:[],

			S45_DIS2D_echo_GRE:[],

			tse_cor_T2w:[], tse_cor_DIS2D_T2w:[], tse_cor_DIS3D_T2w:[],

			AP_dwi:[], AP_TRACEW_dwi:[], PA_b0_dwi:[],

			ND_inv_1_sa2rage:[], inv_1_sa2rage:[],

			ND_inv_2_sa2rage:[], inv_2_sa2rage:[],

			b1map_ND_sa2rage:[], b1map_sa2rage:[],

			b1Div_ND_sa2rage:[], b1Div_sa2rage:[],

			b1map_DIS2D_sa2rage:[], b1map_DIS3D_sa2rage:[],

			mag_GRE:[], phase_GRE:[]
			}


	for idx, s in enumerate(seqinfo):

		##########################
		########## ANAT ##########
		##########################

		#mp2rage
		if ('mp2rage' in s.series_description) and ('DIS' not in s.series_description):
			if ('_INV1' in (s.series_description).strip()):
				info[inv1_mp2rage].append({'item': s.series_id})
			if ('_T1_Images' in (s.series_description).strip()):
				info[t1map].append({'item': s.series_id})
			if ('_UNI-DEN' in (s.series_description).strip()):
				info[t1w].append({'item': s.series_id})
			if ('_UNI_Images' in (s.series_description).strip()):
				info[uni_mp2rage].append({'item': s.series_id})
			if ('_INV2' in (s.series_description).strip()):
				info[inv2_mp2rage].append({'item': s.series_id})

		#mp2rage derivatives
		if ('mp2rage' in s.series_description) and ('DIS' in s.series_description):
			if ('_UNI-DEN_S12_DIS2D' in (s.series_description).strip()):
				info[dis2d_T1w].append({'item': s.series_id})
			if ('_UNI-DEN_S12_DIS3D' in (s.series_description).strip()):
				info[dis3d_T1w].append({'item': s.series_id})
			if ('_UNI_Images_S13_DIS2D' in (s.series_description).strip()):
				info[uni_dis2d_T1w].append({'item': s.series_id})
			if ('_UNI_Images_S13_DIS3D' in (s.series_description).strip()):
				info[uni_dis3d_T1w].append({'item': s.series_id})

		#spc T2w
		if ('spc' in s.series_description) and ('DIS' not in s.series_description):
			if ('ND' in (s.series_description).strip()):
				info[spc_T2w].append({'item': s.series_id})

		#spc T2w derivatives
		if ('spc' in s.series_description) and ('DIS' in s.series_description):
			if ('DIS2D' in (s.series_description).strip()):
				info[DIS2D_spc_T2w].append({'item': s.series_id})
			if ('DIS3D' in (s.series_description).strip()):
				info[DIS3D_spc_T2w].append({'item': s.series_id})

		#tse tra T2w
		if ('tse_tra' in s.series_description) and ('DIS' not in s.series_description):
			info[tse_tra_T2w].append({'item': s.series_id})

		#tse tra T2w derivatives
		if ('tse_tra' in s.series_description) and ('DIS' in s.series_description):
			if ('DIS2D' in (s.series_description).strip()):
				info[tse_tra_DIS2D_T2w].append({'item': s.series_id})
			if ('DIS3D' in (s.series_description).strip()):
				info[tse_tra_DIS3D_T2w].append({'item': s.series_id})

		#TOF angio
		if ('3D_TOF' in s.series_description) and ('DIS' not in s.series_description):
			if ('ND' in (s.series_description).strip()):
				info[TOF_ND_angio].append({'item': s.series_id})
			if ('ND' and 'MIP' not in (s.series_description).strip()):
				info[TOF_angio].append({'item': s.series_id})
			if ('MIP_SAG' in (s.series_description).strip()):
				info[TOF_MIP_SAG].append({'item': s.series_id})
			if ('MIP_COR' in (s.series_description).strip()):
				info[TOF_MIP_COR].append({'item': s.series_id})
			if ('MIP_TRA' in (s.series_description).strip()):
				info[TOF_MIP_TRA].append({'item': s.series_id})

		#TOF angio derivatives
		if ('3D_TOF' in s.series_description) and ('DIS' in s.series_description):
			if ('DIS2D' in (s.series_description).strip()):
				info[TOF_DIS2D_angio].append({'item': s.series_id})
			if ('DIS3D' in (s.series_description).strip()):
				info[TOF_DIS3D_angio].append({'item': s.series_id})

		#susceptibility ND multiecho
		if ('susc3d' in s.series_description) and ('ND' in s.series_description) and ('DIS' not in s.series_description):
			if ('M' in (s.image_type[2].strip())):
				info[mag_ND_echo_GRE].append({'item': s.series_id})
			if ('P' in (s.image_type[2].strip())):
				info[phase_ND_echo_GRE].append({'item': s.series_id})

		#susceptibility multiecho
		if ('susc3d' in s.series_description) and ('ND' not in s.series_description):
			if ('M' in (s.image_type[2].strip())):
				info[mag_echo_GRE].append({'item': s.series_id})
			if ('P' in (s.image_type[2].strip())):
				info[phase_echo_GRE].append({'item': s.series_id})

		#T2star
		if ('T2Star' in s.series_description):
			info[T2_star].append({'item': s.series_id})

		#susceptibility S43 derivatives
		if ('susc3d' in s.series_description) and ('S43' in s.series_description):
			info[S43_DIS2D_echo_GRE].append({'item': s.series_id})

		#susceptibility S45 derivatives
		if ('susc3d' in s.series_description) and ('S45' in s.series_description):
			info[S45_DIS2D_echo_GRE].append({'item': s.series_id})

		#tse cor T2w
		if ('tse_cor' in s.series_description) and ('DIS' not in s.series_description):
			info[tse_cor_T2w].append({'item': s.series_id})

		#tse cor T2w derivatives
		if ('tse_cor' in s.series_description) and ('DIS' in s.series_description):
			if ('DIS2D' in (s.series_description).strip()):
				info[tse_cor_DIS2D_T2w].append({'item': s.series_id})
			if ('DIS3D' in (s.series_description).strip()):
				info[tse_cor_DIS3D_T2w].append({'item': s.series_id})

		#########################
		########## DWI ##########
		#########################

		#mbep2d dwi
		if ('mbep2d' in s.series_description):
			if ('ADC' and 'TRACEW' and 'FA' and 'colFA' and 'B0_PA' not in s.series_description):
				info[AP_dwi].append({'item': s.series_id})
			if ('TRACEW' in (s.series_description).strip()):
				info[AP_TRACEW_dwi].append({'item': s.series_id})
			if ('B0_PA' in (s.series_description).strip()):
				info[PA_b0_dwi].append({'item': s.series_id})

		##########################
		########## FMAP ##########
		##########################

		#rel B1 sourcedata

		#abs B1 sourcedata

		#sa2rage
		if ('sa2rage' in s.series_description) and ('ND' in s.series_description) and ('DIS' not in s.series_description):
			if ('invContrast1' in s.series_description):
				info[ND_inv_1_sa2rage].append({'item': s.series_id})
			if ('invContrast2' in s.series_description):
				info[ND_inv_2_sa2rage].append({'item': s.series_id})
			if ('Contrast' and 'DivImg' not in s.series_description):
				info[b1map_ND_sa2rage].append({'item': s.series_id})
			if ('b1DivImg' in s.series_description):
				info[b1Div_ND_sa2rage].append({'item': s.series_id})

		if ('sa2rage' in s.series_description) and ('ND' not in s.series_description):
			if ('invContrast1' in s.series_description):
				info[inv_1_sa2rage].append({'item': s.series_id})
			if ('invContrast2' in s.series_description):
				info[inv_2_sa2rage].append({'item': s.series_id})
			if ('Contrast' and 'DivImg' not in s.series_description):
				info[b1map_sa2rage].append({'item': s.series_id})
			if ('b1DivImg' in s.series_description):
				info[b1Div_sa2rage].append({'item': s.series_id})

		if ('sa2rage' in s.series_description):
			if ('DIS2D' in s.series_description):
				info[b1map_DIS2D_sa2rage].append({'item': s.series_id})
			if ('DIS3D' in s.series_description):
				info[b1map_DIS3D_sa2rage].append({'item': s.series_id})

		#GRE field map
		if ('GRE' in s.series_description) and ('susc' not in s.series_description):
			if ('mag' in s.series_description):
				info[mag_GRE].append({'item': s.series_id})
			if ('phase' in s.series_description):
				info[phase_GRE].append({'item': s.series_id})

		



	return info


		