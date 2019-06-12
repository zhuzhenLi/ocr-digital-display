import os
from python_utils import *
import mxnet as mx
import numpy as np
import matplotlib.pyplot as plt
import xml.dom.minidom

def xmlDecode(path):
    annotation = xml.dom.minidom.parse(path)

    size = annotation.getElementsByTagName('size')[0]
    width = size.getElementsByTagName('width')[0].firstChild.data
    height = size.getElementsByTagName('height')[0].firstChild.data

    obj = annotation.getElementsByTagName('object')[0]
    cla = obj.getElementsByTagName('name')[0].firstChild.data  
    bndbox = obj.getElementsByTagName('bndbox')[0]              
    x1 = bndbox.getElementsByTagName('xmin')[0].firstChild.data
    x2 = bndbox.getElementsByTagName('xmax')[0].firstChild.data
    y1 = bndbox.getElementsByTagName('ymin')[0].firstChild.data
    y2 = bndbox.getElementsByTagName('ymax')[0].firstChild.data

    width = int(width)
    height = int(height)
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    result = [cla,(width,height),(x1,y1),(x2,y2)]
    return result

if __name__ == '__main__':
    path = './train'
    names = os.listdir(path)
    lst = []
    i=0
    f = open(path+'train.lst','w')
    for name in names:
        if name.endswith('.xml'):
            result = xmlDecode(path+name)
            img_name = path+name.replace('xml','jpg')
            lst_tmp =str(i)+'\t4'+'\t5'+'\t'+str(result[1][0])+'\t'+str(result[1][1])+'\t'\
            +str(result[0])+'\t'\
            +str(result[2][0]/result[1][0])+'\t'+str(result[2][1]/result[1][1])+'\t'\
            +str(result[3][0]/result[1][0])+'\t'+str(result[3][1]/result[1][1])+'\t'\
            +img_name+'\n'
            f.write(lst_tmp)
            i+=1
    f.close()




