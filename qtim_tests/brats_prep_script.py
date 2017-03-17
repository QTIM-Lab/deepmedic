import qtim_tools
import numpy as np
import os
import glob
import skimage.io as io

BRATS_PATH = '/mnt/eminas01/Ken/BRATS2015/BRATS2015_Training'
OUTPUT_PATH = '/mnt/eminas01/DeepMedic_Data'
GRADES = ['HGG','LGG']

def Convert_BRATS_Data():

	subdirs = []

	for grade in GRADES:
		subdirs += glob.glob(os.path.join(BRATS_PATH, grade, '*') + '/')

	for subdir in subdirs:

		print subdir

		#Flair
		Flair_dir = glob.glob(subdir + '*Flair*/')
		print Flair_dir
		Flair_file = glob.glob(Flair_dir[0] + '/*Flair*.mha')[0]

		#T1
		T1_dir = glob.glob(subdir + '/*T1*/')
		T1_file = glob.glob(T1_dir[0] + '/*T1*.mha')[0]

		#T1c
		T1c_dir = glob.glob(subdir + '/*T1c*/')
		T1c_file = glob.glob(T1c_dir[0] + '/*T1c*.mha')[0]

		#T2
		T2_dir = glob.glob(subdir + '/*T2*/')
		T2_file = glob.glob(T2_dir[0] + '/*T2*.mha')[0]

		#ROI
		ROI_dir = glob.glob(subdir + '/*more*/')
		ROI_file = glob.glob(ROI_dir[0] + '/*more*.mha')[0]

		output_directory = os.path.join(OUTPUT_PATH, os.path.basename(os.path.dirname(ROI_dir[0])))

		if not os.path.exists(output_directory):
			os.mkdir(output_directory)

		for image_mha in [Flair_file, T1_file, T1c_file, T2_file, ROI_file]:

			img = io.imread(image_mha,plugin='simpleitk')

			print img

			# io.imsave(os.path.join(output_directory, image_mha[0:-3] + '.nii.gz'),img,plugin='simpleitk')

	return

def Sort_BRATS():

	return

if __name__ == '__main__':
	Convert_BRATS_Data()
