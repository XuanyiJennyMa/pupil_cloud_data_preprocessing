import cv2
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math 

# larger labels are nicer to read
plt.rcParams.update({"font.size": 18})

# ACTION NEEDED: define the path on your own PC

def plot_aoi_patches(aois, ax, aoi_colors, n_colorsteps):
    for idx, aoi in enumerate(aois):
        ax.add_patch(
            patches.Rectangle(
                aoi, *aoi[2:], alpha=0.2, color=aoi_colors(idx / n_colorsteps)
            )
        )
        ax.text(aoi[0] + 20, aoi[1] + 120, f"{idx}", color="black")

#extract the preprocessed AOI information and plot them on the right reference pictures

def paint_save_aoi_diff_picture(list_of_pics):
    for pic in list_of_pics:  
        aoi_filepath = pic+'_AOIs.csv'
        path_to_reference_image = ("./Reference_pic")
        reference_image_file = pic+'.png'
        reference_image = cv2.imread(f"{path_to_reference_image}/{reference_image_file}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        
        aois = pd.read_csv(aoi_filepath, sep=',')
        aois = aois.to_numpy()
        aoi_colors = matplotlib.cm.get_cmap("plasma")
        n_colorsteps = len(aois) - 1
        
        h_1, w_1, c_1 = reference_image.shape
        ratio = w_1/h_1
        if ratio <= 1:
            marked_ref_fig = plt.figure(figsize=(math.trunc(ratio*20), 20))
        else:
            marked_ref_fig = plt.figure(figsize=(20, math.trunc(20/ratio)))

        plt.imshow(np.asarray(reference_image))
        
        plot_aoi_patches(aois, plt.gca(),aoi_colors, n_colorsteps)
        plt.gca().set_axis_off()
        save_file_name = pic + '_aois.png'

        marked_ref_fig.savefig(save_file_name)

def paint_save_aoi_same_picture(pic, versions):
    for version in range(versions):  
        aoi_filepath = pic+'_'+str(version)+'_AOIs.csv'
        path_to_reference_image = ("./Reference_pic")
        reference_image_file = pic+'.jpeg'
        reference_image = cv2.imread(f"{path_to_reference_image}/{reference_image_file}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        
        aois = pd.read_csv(aoi_filepath, sep=',')
        aois = aois.to_numpy()
        aoi_colors = matplotlib.cm.get_cmap("plasma")
        n_colorsteps = len(aois) - 1
        
        h_1, w_1, c_1 = reference_image.shape
        ratio = w_1/h_1
        if ratio <= 1:
            marked_ref_fig = plt.figure(figsize=(math.trunc(ratio*20), 20))
        else:
            marked_ref_fig = plt.figure(figsize=(20, math.trunc(20/ratio)))

        plt.imshow(np.asarray(reference_image))
        
        plot_aoi_patches(aois, plt.gca(),aoi_colors, n_colorsteps)
        plt.gca().set_axis_off()
        save_file_name = pic + '_' + str(version) + '_aois.png'

        marked_ref_fig.savefig(save_file_name)