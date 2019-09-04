#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' generate train and val dataset script '

__author__ = 'Zhuzhen Li'

import os
import random
import shutil

def _main():
    trainval_percent = 0.1
    train_percent = 0.8
    xmlfilepath = './VOC2019/Annotations'
    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open('./VOC2019/ImageSets/Main/trainval.txt', 'w')
    ftest = open('./VOC2019/ImageSets/Main/test.txt', 'w')
    ftrain = open('./VOC2019/ImageSets/Main/train.txt', 'w')
    fval = open('./VOC2019/ImageSets/Main/val.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftest.write(name)
            else:
                fval.write(name)
        else:
            ftrain.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()


def create_dir(directory, folder_name):
    current_path = os.getcwd()
    os.chdir(current_path+directory)
    os.getcwd()
    
    # Create directory
    dirName = folder_name
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory" , dirName ,  " Successfully Created ")
    
    except FileExistsError:
        #filesToRemove = [os.path.join(dirName, f) for f in os.listdir(dirName)]
        #for f in filesToRemove :
        #    os.remove(f)
        shutil.rmtree(dirName)
        print("Directory" , dirName ,  "already exists, empty the existing directory.")


if __name__ == '__main__':
    _main()
    
    
