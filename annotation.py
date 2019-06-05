# imports
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

sample = 128


def _main():
    
    for i in range (10):
    
        src = '00'+ str(i) +'000.xml'
    
        for j in range (sample):
            index = j+1
            if j < 10:
                j = '00'+ str(index)
            elif j < 100:
                j = '0'+ str(index)
            else:
                j = str(index)
            
            des = '00'+ str(i) + index +'.xml'
            copyfile(src, des)
        
            # edit file
            tree = ET.parse(des)
            root = tree.getroot()
        
            file_name = root.find("filename")
            file_name.text =  '00'+ str(i) + index +'.jpg'
        
        
            file_path = root.find("path")
            file_path.text='/Users/missbamboo/Desktop/intel/ocr/ocr-digital-display/VOC2007/JPEGImages/00'+ str(i) + j +'.jpg'
            tree.write(des)

def clear(dir):
    filesToRemove = [os.path.join(dir, file) for file in os.listdir(dir)]
    for file in filesToRemove :
        os.remove(file)
    


if __name__ == '__main__':
    xml_dir = '/Users/missbamboo/Desktop/intel/ocr/ocr-digital-display/VOC2007/Annotations'
    clear(xml_dir)
    os.chdir(xml_dir)
    _main()


