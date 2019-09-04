#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' make annotation files '

__author__ = 'Zhuzhen Li'

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
            if index < 10:
                index = '00'+ str(index)
            elif index < 100:
                index = '0'+ str(index)
            else:
                index = str(index)
        
            des = '00'+ str(i) + index +'.xml'
            copyfile(src, des)
            
            # edit file
            tree = ET.parse(des)
            root = tree.getroot()
            
            file_name = root.find("filename")
            file_name.text =  '00'+ str(i) + index +'.jpg'
            
            
            file_path = root.find("path")
            file_path.text='./VOC2007/JPEGImages/00'+ str(i) + index +'.jpg'
            
            for width in root.iter('width'):
                width.text = str(300)
            
            for height in root.iter("height"):
                height.text = str(400)
        tree.write(des)


def create_dir():
    os.chdir('./VOC2007')
    os.getcwd()
    # Create directory
    dirName = 'Annotations'
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory" , dirName ,  " Successfully Created ")
    
    except FileExistsError:
        filesToRemove = [os.path.join(dirName, f) for f in os.listdir(dirName)]
        for f in filesToRemove :
            os.remove(f)
        print("Directory" , dirName ,  "already exists, empty the existing directory.")



if __name__ == '__main__':
    create_dir()
    os.chdir("./../")
    
    digit_dir = './origin_xml'
    des_dir = './VOC2007/Annotations'
    copy_tree(digit_dir, des_dir)
    print(" Successully copy the original xmls to", des_dir)
    
    xml_dir = './VOC2007/Annotations'
    os.chdir(xml_dir)
    _main()

