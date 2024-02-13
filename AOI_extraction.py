# This script is used for 1) the extraction of nested area(s) of interests; 
#                         2) saving the defined AOIs of each reference picture in an independant .csv file.
# It is a modified version of some codes in Pupil Labs' gallery_demo_analysis:
#       https://github.com/pupil-labs/gallery_demo_analysis/blob/main/1_Defining%20Nested%20AOIs.ipynb
# Please note, all reference pictures are saved in the same folder, and this folder is in the same directory with this script.

# Import necessary libraries
import cv2
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Set the directory of the folder containing all reference pictures
path_to_reference_image = ("./Reference_pic")

# This function is for reading the reference picture name.
# It is n
extract_name = lambda name: name.split(".jpeg")[0]

def extract_ref_pics(path):
    all_ref_pic = os.listdir(path)
    ref_pic_dict = {}
    for pic in all_ref_pic:
        reference_image = cv2.imread(f"{path}/{pic}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        ref_pic_dict[extract_name(pic)] = reference_image
    return ref_pic_dict

reference_picture = extract_ref_pics(path_to_reference_image)     

# this function is for extracting the AOIs once for each picture
# for different versions of AOIs from the same picture, see the function below

def extract_aoi_info_diff_pic(ref_pic_list):
    for pic in ref_pic_list:
        scaling_factor = 0.5
        picture = reference_picture.get(pic)
        scaled_image = picture.copy()
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor)
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image)
        cv2.destroyAllWindows()
        aois = scaled_aois / scaling_factor
        aoi_df = pd.DataFrame(aois)
        filename = pic+"_AOIs.csv"
        aoi_df.to_csv(filename, index=False)

def extract_aoi_info_same_pic(ref_pic, aoi_versions):
    for version in range(aoi_versions):
        reference_image = cv2.imread(f"{path_to_reference_image}/{ref_pic}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        scaling_factor = 0.5
        scaled_image = reference_image.copy()
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor)
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image)
        cv2.destroyAllWindows()
        aois = scaled_aois / scaling_factor
        aoi_df = pd.DataFrame(aois)
        filename = ref_pic.split(".jpeg")[0]+'_'+str(version)+"_AOIs.csv"
        aoi_df.to_csv(filename, index=False)

