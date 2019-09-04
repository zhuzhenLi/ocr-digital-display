#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' generate voc2019 dataset '

__author__ = 'Zhuzhen Li'

import os
import random
import glob
import shutil
from distutils.dir_util import copy_tree

def _main():
    directory = "VOC2019"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory, "does not exist, created one!")
        annotation = "Annotations"
        set = "ImageSets"
        images = "JPEGImages"
        os.makedirs(directory+"/"+annotation)
        os.makedirs(directory+"/"+set)
        os.makedirs(directory+"/"+images)
        os.makedirs(directory+"/"+set+"/Main")  
    else:
        print(directory, "already exists, please double check!")

    copy_tree("./text_gen/TextRecognitionDataGenerator/out", "./VOC2019/JPEGImages")
    copy_tree("./text_gen/TextRecognitionDataGenerator/voc_ann", "./VOC2019/Annotations")



if __name__ == '__main__':
    _main()
