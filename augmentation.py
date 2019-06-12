#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' augmentation script '

__author__ = 'Zhuzhen Li'

import cv2 as cv
import numpy as np
import imageio
import imgaug as ia
from imgaug import augmenters as iaa
from imgaug import parameters as iap
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import os, shutil
from shutil import copyfile
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET
import pdb
import shutil

# global variables setting
input_height=128
input_width=96
list_size = 32
batch_size = 8
# red_range = (1, random.randint(1,200))
# blue_range = (1, random.randint(1,200))
# green_range = (1, random.randint(1,200))
red_range = (1, 200)
blue_range = (1, 200)
green_range = (1, 200)
resize_height= (0.3,0.5)
resize_width= (0.3,0.5)
superpixel_p = (0.1, 0.25)
superpixel_n = (32, 128)
gau_blur_size = (0.0, 3.0)
avg_blur_size = (2, 3)
med_blur_size = (3, 5)
sharpen_alpha=(0.0, 0.2)
sharpen_lightness=(0.0, 2.0)
emboss_alpha= (0.0, 0.2)
emboss_strength=(0.2, 0.4)
add_size = (-20, 20)
add_per_channel_size = 0.2
gaussian_noise=(0, 0.02*255)
multiply_scale= (0.9, 1.1)
dropout_p=(0, 0.2)
coarse_dropout = 0.02
contrast_normal_scale = (0, 1)
spnoise= (0.3, 300)
affine_translate_x=(-0.05, 0.05)
affine_translate_y=(-0.05, 0.05)
affine_rotate=(-30, 30)
affine_shear = (-2, 2)
piecewise_affine_scale= (0.01, 0.02)
elastic_alpha = (0,0.5)
elastic_sigma = 0.01
sample = 128

def coloring (digit):
    image_name = '00'+ str(digit)+ '000'+".jpg"
    # Load and display
    image = imageio.imread(image_name)
    # image = cv.resize(image, (input_width,input_height), interpolation=cv.INTER_CUBIC)
#    print("Original:", image.shape)
#    ia.imshow(image)

    images = np.array([image for _ in range(sample)], dtype=np.uint8)
    seq_color= iaa.Sequential([iaa.WithChannels(0, iaa.Add(red_range)),
                               iaa.WithChannels(1, iaa.Add(green_range)),
                               iaa.WithChannels(2, iaa.Add(blue_range))
                               ], random_order=True)
        
    images_color_aug = seq_color(images=images)
#    ia.imshow(ia.draw_grid(images_color_aug, cols=sample/8, rows=8))
    return images_color_aug

def trans (images_color_aug):
    #ia.seed(1)
    seq = iaa.Sequential([iaa.Resize({"height": resize_height , "width": resize_width }),
                          iaa.Affine(translate_percent={"x": affine_translate_x, "y": affine_translate_y}),
                          iaa.Affine(rotate=affine_rotate),
                          iaa.Affine(shear=affine_shear),
                          iaa.PiecewiseAffine(scale=piecewise_affine_scale),
                          iaa.ElasticTransformation(alpha=elastic_alpha, sigma=elastic_sigma)
                          ], random_order=True)
        
    images_trans_aug = seq(images=images_color_aug)
#    ia.imshow(ia.draw_grid(images_trans_aug, cols=sample/8, rows=8))
    return images_trans_aug


def distortion (images_trans_aug):
    #ia.seed(1)
    seq = iaa.Sequential([#   iaa.Superpixels(p_replace=superpixel_p, n_segments=superpixel_n),
                          iaa.GaussianBlur(sigma=gau_blur_size),
                          iaa.AverageBlur(k=avg_blur_size),
                          iaa.MedianBlur(k=med_blur_size),
                          iaa.Sharpen(alpha=sharpen_alpha, lightness=sharpen_lightness),
                          iaa.Emboss(alpha=emboss_alpha, strength=emboss_strength),
                          #   iaa.Add(add_size, per_channel= add_per_channel_size),
                          iaa.AdditiveGaussianNoise(scale=gaussian_noise, per_channel=0.2),
                          #   iaa.Multiply(multiply_scale, per_channel=0.2),
                          #   iaa.Dropout(p=dropout_p, per_channel=0.2),
                          #   iaa.CoarseDropout(0.1, size_percent=coarse_dropout, per_channel=0.2)
                          ], random_order=True)
    images_aug = seq(images=images_trans_aug)
#    ia.imshow(ia.draw_grid(images_aug, cols=sample/8, rows=8))
    return images_aug



def create_dir():
    os.chdir('./VOC2007')
    os.getcwd()
    
    # Create directory
    dirName = 'JPEGImages'
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory" , dirName ,  " Successfully Created ")
    
    except FileExistsError:
        filesToRemove = [os.path.join(dirName, f) for f in os.listdir(dirName)]
        for f in filesToRemove :
            os.remove(f)
        print("Directory" , dirName ,  "already exists, empty the existing directory.")



def save (images_aug, digit):
    path = './'
    # load images to directory
    for i in range (sample):
        index = i + 1
        if index < 10:
            index = '00' + str(index)
        elif index < 100:
            index = '0' + str(index)
        else:
            index = str(index)
        filename =  '00' + str(digit) + index +".jpg"
        # resize before save
        images_aug[i] = cv.resize(images_aug[i], (300,400), interpolation=cv.INTER_CUBIC)
        cv.imwrite(os.path.join(path, filename), images_aug[i])



if __name__=='__main__':
    create_dir()
    os.chdir("./../")
    
    digit_dir = './digit'
    des_dir = './VOC2007/JPEGImages'
    copy_tree(digit_dir, des_dir)
    print(" Successully copy the original images to", des_dir)

    os.chdir(des_dir)
    for i in range (10):
        augmentation = distortion(trans(coloring(i)))
        save(augmentation, i)

    # check if successful generate:
    number_of_files = len([item for item in os.listdir("./") if os.path.isfile(os.path.join("./",item))])
    if number_of_files != (sample * 10 + 10 + 1) :
        print ("Error occurs in image augmentation, please double check!")
    print (number_of_files-1, "files in", des_dir)
