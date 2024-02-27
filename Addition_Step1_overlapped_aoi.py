# Import libraries
import numpy as np
import pandas as pd

def check_in_rect(fixation_data, rectangle_coordinates):
    """
    returns an array with the length of fixation_data, which is True, when the entry in fixation_data
    was inside rectangle_coordinates and False otherwise.
    """

    # unpack the rectangle coordinates
    rect_x, rect_y, rect_width, rect_height = rectangle_coordinates

    # check if the fixation was within the x- and y-borders
    x_hit = fixation_data["fixation x [px]"].between(rect_x, rect_x + rect_width)
    y_hit = fixation_data["fixation y [px]"].between(rect_y, rect_y + rect_height)

    in_rect_idx = x_hit & y_hit

    return in_rect_idx

def label_overlap_aoi(pic, version, overlap_aoi_number):

    path_to_fixation_data = "./Manuscript_2"
    fixations = pd.read_csv(f"{path_to_fixation_data}/labelled_fixations_diff_version.csv")
    #import the saved AOI information
    aoi_filepath = 'Manuscript_2_1_AOIs.csv'
    aois = pd.read_csv(aoi_filepath, sep=',')
    aois = aois.to_numpy()
    paintings = [idx for idx in range(len(aois))]
        
    # create a new column of 'None's in our data frame
    column_name = 'AOI_test'
    fixations[column_name] = None

    AOI_number = overlap_aoi_number
    index_list = fixations.index
    index_list_total = index_list[check_in_rect(fixations, aois[(AOI_number - 1)])].to_list()

    for i in range(0, (len(aois) -1)):
        list_overlap = index_list[check_in_rect(fixations, aois[i])].to_list()
        non_overlap = [x for x in index_list_total if x not in list_overlap]
        index_list_total[:]  = non_overlap
    
    # assign the AOI ID to those fixations that were inside the AOI
    for aoi_id, aoi in enumerate(aois):
        if aoi_id < (len(aois)-1):
            fixations.loc[check_in_rect(fixations, aoi), column_name] = paintings[aoi_id]
        else:
            fixations.loc[index_list_total, column_name] = (AOI_number - 1)
            
                
    save_file_name = 'final_labelled_fixations_diff_version.csv'
    fixations.to_csv(f"{path_to_fixation_data}/{save_file_name}", index=False)  