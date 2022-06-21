# !/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv


### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-b", "--background", help="Input background file.", required=False)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the workflow.

### Main workflow
def main():
    # Get options
    args = options()

    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    # Read image
    img, path, filename = pcv.readimage(filename=args.image)
    background_img, background_path, background_filename = pcv.readimage(filename=args.background)

#    cv2.imwrite(args.outdir/filename, img)
#    cv2.imwrite(args.outdir/background_filename, background_img)

#    outfile=False
#    if args.writeimg == True:
#    outfile = args.outdir + "/colorspaces-" + filename

    
    # Examine all colorspaces at one glance
    colorspace_img = pcv.visualize.colorspaces(rgb_img=img)
    outfile = args.outdir + "/colorspaces-" + filename
    cv2.imwrite(outfile, colorspace_img)

    l = pcv.rgb2gray_lab(rgb_img=img, channel='l')
    lback = pcv.rgb2gray_lab(rgb_img=background_img, channel='l')
    lsub = pcv.background_subtraction(l,lback)
    # Threshold the blue image
#    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
#    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

    # Fill small objects
    # b_fill = pcv.fill(b_thresh, 10)

    # Join the thresholded value and lightness images


    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img=img, mask=lsub, mask_color='white')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, 
                                      max_value=255, object_type='light')
    ab_fill = pcv.fill(bin_img=maskedb_thresh, size=150)
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=0, y=0, h=1200, w=1600)
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                                   roi_hierarchy=roi_hierarchy, 
                                                                   object_contour=id_objects, 
                                                                   obj_hierarchy=obj_hierarchy,
                                                                   roi_type='partial')
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
    output  = cv2.drawContours(img, obj, -1,(255,50,0),thickness=1 )
#    pcv.plot_image(output)
    #save img plus object contour?
#    pcv.print_image(output, "./output.jpg")

    outfile = args.outdir + "/filled-" + filename
    cv2.imwrite(outfile, output)


#    Background Subtract   
#    b_subtract = pcv.background_subtraction(img, img_b)
#    outfile = args.outdir + "/background-subract-" + filename
#    cv2.imwrite(outfile, b_subtract)

    # Convert RGB to HSV and extract the saturation channel

    # Threshold the saturation image
#    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

    # Median Blur
#    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
#    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel


    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
#    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
#    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    # Threshold the green-magenta and blue images
#    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
#    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
#    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images (OR)
#    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
#    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # Fill small objects
#    ab_fill = pcv.fill(bin_img=ab, size=200)

    # Apply mask (for VIS images, mask_color=white)
#    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')

    # Identify objects
#    id_objects, obj_hierarchy = pcv.find_objects(img=img, mask=fill)

    # Define ROI
#    roi1, roi_hierarchy= pcv.roi.rectangle(img=img, x=0, y=0, h=1200, w=1600)

    # Decide which objects to keep
#    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
#                                                               roi_hierarchy=roi_hierarchy, 
#                                                               object_contour=id_objects, 
#                                                               obj_hierarchy=obj_hierarchy,
#                                                               roi_type='partial')

    # Object combine kept objects
#    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)


#    masked2 = pcv.apply_mask(img=img, mask=obj, mask_color='white')
#    outfile = args.outdir + "/masked-" + filename
#    cv2.imwrite(outfile, output)

    ############### Analysis ################

#    outfile=False
#    if args.writeimg == True:
#        outfile = args.outdir + "/" + filename

    # Find shape properties, output shape image (optional)
#    shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask)

    # Shape properties relative to user boundary line (optional)
#    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680)

    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
#    color_histogram = pcv.analyze_color(rgb_img=img, mask=kept_mask, hist_plot_type='all')

    # Pseudocolor the grayscale image
#    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=kept_mask, cmap='jet')

    # Write shape and color data to results file
#    pcv.print_results(filename=args.result)

if __name__ == '__main__':
    main()
