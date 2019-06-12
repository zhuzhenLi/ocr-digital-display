#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' generate train and val dataset script '

__author__ = 'Zhuzhen Li'

import os
import random

def _main():
    trainval_percent = 0.1
    train_percent = 0.9
    xmlfilepath = './VOC2007/Annotations'
    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open('./VOC2007/ImageSets/Main/trainval.txt', 'w')
    ftest = open('./VOC2007/ImageSets/Main/test.txt', 'w')
    ftrain = open('./VOC2007/ImageSets/Main/train.txt', 'w')
    fval = open('./VOC2007/ImageSets/Main/val.txt', 'w')

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


if __name__ == '__main__':
    _main()
