from __future__ import print_function  # Only needed for Python 2
from qtim_tools.qtim_utilities.nifti_util import nifti_2_numpy, save_numpy_2_nifti
import numpy as np
import os
import glob
from random import shuffle
from subprocess import call



BRATS_PATH = '/eminas/Ken/BRATS2015/BRATS2015_Training'
OUTPUT_PATH = '/eminas/DeepMedic_Data'
GRADES = ['HGG','LGG']

def Convert_BRATS_Data():

	subdirs = []

	for grade in GRADES:
		subdirs += glob.glob(os.path.join(BRATS_PATH, grade, '*') + '/')

	for subdir in subdirs:

		print(subdir)

		#Flair
		Flair_dir = glob.glob(subdir + '*Flair*/')
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
		if len(ROI_dir) == 0:
			ROI_dir = glob.glob(subdir + '/*OT*/')
			ROI_file = glob.glob(ROI_dir[0] + '/*OT*.mha')[0]			
		else:
			ROI_file = glob.glob(ROI_dir[0] + '/*more*.mha')[0]


		output_directory = os.path.join(OUTPUT_PATH, os.path.basename(os.path.dirname(subdir)))

		if not os.path.exists(output_directory):
			os.mkdir(output_directory)

		images_mha = [Flair_file, T1_file, T1c_file, T2_file, ROI_file]
		images_output = ['FLAIR','T1', 'T1c', 'T2', 'ROI']
		images_output_filenames = [label + '.nii.gz' for label in images_output]
		images_output_filenames_preprocessed = [label + '_pp.nii.gz' for label in images_output]

		for img_idx, image_mha in enumerate(images_mha):


			output_filename = os.path.join(output_directory, images_output_filenames[img_idx])
			output_filename_preprocessed = os.path.join(output_directory, images_output_filenames_preprocessed[img_idx])

			print(output_filename)
			if not os.path.exists(output_filename):
				Slicer_Command = ['Slicer','--launch','ResampleScalarVectorDWIVolume',image_mha, output_filename]
				call(' '.join(Slicer_Command), shell=True)

			if not os.path.exists(output_filename_preprocessed):
				img = nifti_2_numpy(output_filename)

				if images_output[img_idx] == 'FLAIR':
					mask = np.copy(img)
					mask[mask > 0] = 1
					save_numpy_2_nifti(mask, output_filename, os.path.join(output_directory, 'MASK.nii.gz'))

				if images_output[img_idx] == 'ROI':
					img[img > 0] = 1
				else:
					masked_img = np.ma.masked_where(img == 0, img)
					normed_img = (img - np.ma.mean(masked_img))/np.ma.std(masked_img)
					normed_img[img == 0] = 0
					img = normed_img

				print(images_output_filenames[img_idx])
				save_numpy_2_nifti(img, output_filename, output_filename_preprocessed)

	return

def splitPerc(L, perc):
    
    start_index = 0
    perc = np.cumsum(perc) / 100.

    print(perc)
    indexes = [int(x) for x in perc * len(L)]
    print(indexes)

    split_list = []
    for chunk_idx, chunk in enumerate(indexes):
    	split_list += [L[start_index:int(chunk)]]
    	start_index = int(chunk)

    print(split_list)
    return split_list

def Sort_BRATS():

	config_path = '/home/abeers/Github/deepmedic/qtim_tests/Full_Brats_Dataset/configFiles/deepMedic_Full_Brats/'

	subdirs = []

	subdirs = glob.glob(OUTPUT_PATH + '/*/')
	print(OUTPUT_PATH + '/*/')

	# Comment out if training/validation should be deterministic
	shuffle(subdirs)

	validation_training_test_ratio = [20, 60, 20]

	validation_training_test_subdirs = splitPerc(subdirs, validation_training_test_ratio)

	type_labels = ['train/validation', 'train', 'test']
	prefix_labels = ['validation', 'train', 'test']

	for class_idx, class_type in enumerate(validation_training_test_subdirs):
		
		output_textfile_dir = os.path.join(config_path, type_labels[class_idx])

		if not os.path.exists(output_textfile_dir):
			os.mkdir(output_textfile_dir)

		all_files_present = True

		output_configs = ['Channels_flair.cfg', 'Channels_t1.cfg', 'Channels_t1c.cfg', 'Channels_t2.cfg', 'Channels_GroundTruth.cfg', 'Channels_Masks.cfg']
		
		for config in output_configs:
			if os.path.exists(os.path.join(output_textfile_dir, prefix_labels[class_idx] + config)):
				os.remove(os.path.join(output_textfile_dir, prefix_labels[class_idx] + config))

		for subdir in class_type:

			required_files = [os.path.join(subdir, label + '_pp.nii.gz') for label in ['FLAIR','T1', 'T1c', 'T2', 'ROI']] + [os.path.join(subdir, 'MASK.nii.gz')]

			for required_file in required_files:
				if not os.path.exists(required_file):
					print(required_file)
					all_files_present = False

			if all_files_present:

				#FLAIR

				for config_idx, config in enumerate(output_configs):
					with open(os.path.join(output_textfile_dir, prefix_labels[class_idx] + config), 'a') as the_file:
						the_file.write(required_files[config_idx] + '\n')

				if prefix_labels[class_idx] == 'validation':
					with open(os.path.join(output_textfile_dir, prefix_labels[class_idx] + 'Predictions.cfg'), 'a') as the_file:
						the_file.write(os.path.basename(os.path.normpath(subdir)) + '_PREDICTION.nii.gz' + '\n')

	return

if __name__ == '__main__':
	# Convert_BRATS_Data()
	Sort_BRATS()
