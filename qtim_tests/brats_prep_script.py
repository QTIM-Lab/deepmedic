import qtim_tools
import numpy as np
import os
import glob
from medpy.io import load, save

BRATS_PATH = '/mnt/eminas01/Ken/BRATS2015/BRATS2015_Training'
OUTPUT_PATH = '/mnt/eminas01/DeepMedic_Data'
GRADES = ['HGG','LGG']

def Convert_BRATS_Data():

	subdirs = []

	for grade in GRADES:
		subdirs += glob.glob(os.path.join(BRATS_PATH, grade, '*') + '/')

	for subdir in dirs:

		#FLAIR
		FLAIR_dir = glob.glob(subdir + '/*FLAIR*/')
		FLAIR_file = glob.glob(FLAIR_dir + '/*FLAIR*.mha')

		#T1
		T1_dir = glob.glob(subdir + '/*T1*/')
		T1_file = glob.glob(T1_dir + '/*T1*.mha')

		#T1c
		T1c_dir = glob.glob(subdir + '/*T1c*/')
		T1c_file = glob.glob(T1c_dir + '/*T1c*.mha')

		#T2
		T2_dir = glob.glob(subdir + '/*T2*/')
		T2_file = glob.glob(T2_dir + '/*T2*.mha')

		#ROI
		ROI_dir = glob.glob(subdir + '/*more*/')
		ROI_file = glob.glob(ROI_dir + '/*more*.mha')

		output_directory = os.join(OUTPUT_PATH, os.path.basename(os.path.dirname(ROI_dir)))

		if not os.path.exists():
			os.mkdir(output_directory)

		for image_mha in [FLAIR_file, T1_file, T1c_file, T2_file, ROI_file]:

			image_data, image_header = load(image_mha)
			save(image_data, os.path.join(output_directory, image_mha[0:-3] + '.nii.gz', image_header))


	return

def Sort_BRATS():

	return

if __name__ == '__main__':
	Convert_BRATS_Data()
