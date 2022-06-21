#!/bin/bash

# Here we are running a VIS top-view workflow over a flat directory of images

# Image names for this example look like this: cam1_16-08-06-16:45_el1100s1_p19.jpg

/home/a/Desktop/plantcv/plantcv-workflow.py \
-d ./data \
-a filename \
-s %H-%M-%S \
-l _ \
-j ./pipeline.json \
-p ./pipeline.py \
-i ./output-images \
-f timestamp \
-t jpg \
-T 1 \
-w  \
--other_args="--background ./background/11-42-40.jpg" \
#--other_args="--debug print" 
