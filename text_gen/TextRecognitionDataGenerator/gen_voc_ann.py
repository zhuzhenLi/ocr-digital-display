import json
import os, shutil, glob
from shutil import copyfile
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET
import cv2
import copy
import os

def _main():
    template = 'tmp.xml'
    root = ''
    xmldir = 'voc_ann'
    img_dir = 'out'
    bbox = 'bb_result.txt'
    
    listoflines= list()
    
    with open(bbox, "r") as openfile:
        for line in openfile:
            if line != "\n" :
                listoflines.append(line.strip())

    print(len(listoflines))

    for i in range (len(listoflines)) :
        each_list = listoflines[i].split()
        new_xml = each_list[0] +'.xml'

        # create a new xml file
        src = os.path.join(root,xmldir,template)
        des = os.path.join(root,xmldir,new_xml)
        copyfile(src, des)
        
        # edit file
        tree = ET.parse(des)
        x_root = tree.getroot()

        x_file_name = x_root.find("filename")
        x_file_name.text = each_list[0]+".png"

        x_size = x_root.find('size')
        x_width = x_size.find('width')
        x_width.text = str(each_list[-2])
        x_height = x_size.find('height')
        x_height.text = str(each_list[-1])


        
        obj0 = x_root.find('object')
        lb_name = obj0.find('name')
        lb_name.text = str(each_list[1][0])
        bndbox = obj0.find('bndbox')
        for i in range(4):
            bndbox[i].text = str(each_list[i+2])

        for bi in range(1,len(each_list[1])):
            dup_obj = copy.deepcopy(obj0)
            x_root.append(dup_obj)
            lb_name = dup_obj.find('name')
            lb_name.text = str(each_list[1][bi])
            bndbox = dup_obj.find('bndbox')
            for j in range(4):
                bndbox[j].text = str(each_list[bi*4+2+j])
                
        tree.write(des)


if __name__ == '__main__':
    directory = "voc_ann"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory, "does not exist, created one!")
    else:
        print(directory, "already exists. Clear it!")
        files = glob.glob(directory+"/*")
        for f in files:
            os.remove(f)


    exists = os.path.isfile('./voc_ann/tmp.xml')
    if exists:
        print("tmp.xml file already exist.")
    else:
        newPath = shutil.copy('tmp.xml', './voc_ann')
        print("tmp.xml file is not in voc_ann, move it in, path is", newPath) 
    _main()
