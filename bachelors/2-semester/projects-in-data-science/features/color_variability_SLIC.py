import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.segmentation import slic, mark_boundaries
from skimage.color import label2rgb
from skimage.measure import regionprops
import cv2
import math

def convert_to_rgb(image):
    '''
    Function to convert RGBA to RGB (4channels to 3 channels).
    '''
    return image[:, :, :3]

def preprocess_mask(mask):
    """
    Function to convert mask from RGB to Binary
    """
    #Convert the mask to grayscale
    grayscale_mask = np.mean(mask, axis=2) 
    # Threshold the grayscale mask to obtain a binary mask
    binary_mask = (grayscale_mask > 0).astype(np.uint8)
    return binary_mask

def manhatten(true_color, pixel_color):
        '''
        Function to calculate distance between color in color_dict and average color from current segment.
        Example: 'black':[(48, 51, 49),0]  vs [50,55,50], the distance is = 2+4+1= 7
        '''
        return np.sum(np.abs(true_color - pixel_color))

def proportion_cancel(marked_count, all_segments):
    '''
    Function to calculate probability of cancer in the image
    '''
    return round((marked_count/all_segments), 2)

def get_slic_visual(image, mask):
    '''
    This function will use slic alg. to segment the image where is masked. Then It will calculate
    average color in each segment - superpixel. 
    It will compare it to the colors in dictionary, that are pre-defined from all images and add count if match.

    Input: Image and mask
    Output: Group with the most color matches
    '''
    not_match = 0
    # Set threshold for manhatten function. Default 100
    threshold_for_manhatten = 100

    # Check if image is in RGBA. If true, convert it to RGB
    if image.shape[-1] == 4:
        image = convert_to_rgb(image)

    # Check if mask in binary
    mask = preprocess_mask(mask)

    # Apply SLIC algorithm
    segments_slic = slic(image, n_segments=100, compactness=10, sigma=1, mask=mask)
    # Dictionary with pre-defined colors (top1 from each group or top2)
    color_dict = {
            'CANCER1':[(46, 50, 49),0],
            'CANCER2':[(116, 96, 80),0],
            'CANCER3':[(42, 44, 43),0],
            'CANCER4':[(157, 137, 112),0],
            'CANCER5':[(112, 93, 82),0],
            'CANCER6':[(136, 117, 105),0],
            'CANCER7':[(116, 93, 79),0],
            'CANCER8':[(93, 71, 61),0],
            'CANCER9':[(90, 76, 71),0],
            'CANCER10':[(97, 80, 75),0],
            'NONCANCER1':[(198, 138, 109),0],
            'NONCANCER2':[(124, 76, 56),0],
            'NONCANCER3':[(108, 66, 48),0],
            'NONCANCER4':[(124, 78, 60),0],
            'NONCANCER5':[(151, 105, 91),0],
            'NONCANCER6':[(120, 73, 53),0],
            'NONCANCER7':[(97, 70, 58),0],
            'NONCANCER8':[(135, 82, 58),0],
            'NONCANCER9':[(92, 65, 51),0],
            'NONCANCER10':[(136, 82, 60),0]
    }

    for segment in np.unique(segments_slic):
        segment_mask = segments_slic == segment
        if np.any(mask[segment_mask]):
            segment_pixels = image[segment_mask]
            mean_color = np.mean(segment_pixels, axis=0)

            # Find the closest color match
            closest_match = None
            min_distance = float('inf')
            for color_name, (color_value, count) in color_dict.items():
                distance = manhatten(color_value, mean_color)
                if distance < min_distance:
                    min_distance = distance
                    closest_match = color_name

            # Check if the closest color is within the acceptable threshold
            if min_distance < threshold_for_manhatten:
                color_dict[closest_match][1] += 1
            else:
                not_match += 1 
    # Print results
    for color_name, (color_value, count) in color_dict.items():
        print(f"Segments close to {color_name}: {count}")


    
    # Visualizing the segments - OPTIONAL
    '''
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax[0].set_title('Original Image')
    ax[0].axis('off')

    ax[1].imshow(mask, cmap='gray')
    ax[1].set_title('Mask')
    ax[1].axis('off')

    marked_image = mark_boundaries(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), segments_slic)
    ax[2].imshow(marked_image)
    ax[2].set_title('Segmented Image')
    ax[2].axis('off')

    plt.show()
    '''

    # Get the key with the most color matches
    max_key = max(color_dict, key=lambda k: color_dict[k][1])

    cancer_segments_count = 0
    non_cancer_segments_count = 0
    for key, value in color_dict.items():
        key_group = key[:-1]
        if key_group == "CANCER":
            cancer_segments_count += value[1]
        else:
            not_match += 1

    return proportion_cancel(cancer_segments_count, cancer_segments_count+not_match)
    




    
