import json
import os, shutil
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
    jsondir = 'bbox'
    img_dir = 'out'
    jsonfiles = os.walk((os.path.join(root,jsondir)))

    for jr, jd, jfs in jsonfiles:
        for jf in jfs:
            # print(os.path.join(jr,jf))
            with open(os.path.join(jr,jf), 'r') as load_f:
                pred_dict = json.load(load_f)
                # print(pred_dict)
                lbs = pred_dict['labels']# the type of label: string
                # print(lbs)

                new_xml = pred_dict['img_name'].split('.')[-2]+'.xml'
                img_name = pred_dict['img_name']
                boxes = pred_dict['bbox']
                img = cv2.imread(os.path.join(root,img_dir,img_name))
                img_size = img.shape
                print (img_name,img_size)

                # create a new xml file
                src = os.path.join(root,xmldir,template)
                des = os.path.join(root,xmldir,new_xml)

                copyfile(src, des)

                # edit file
                tree = ET.parse(des)
                x_root = tree.getroot()

                x_file_name = x_root.find("filename")
                x_file_name.text = img_name
                x_size = x_root.find('size')
                x_width = x_size.find('width')
                x_width.text = str(img_size[1])
                x_height = x_size.find('height')
                x_height.text = str(img_size[0])

                if lbs:
                    obj0 = x_root.find('object')
                    lb_name = obj0.find('name')
                    lb_name.text = str(lbs[0])
                    bndbox = obj0.find('bndbox')
                    for i in range(4):
                        bndbox[i].text = str(boxes[0][i])

                    for bi in range(1,len(lbs)):
                        dup_obj = copy.deepcopy(obj0)
                        x_root.append(dup_obj)
                        lb_name = dup_obj.find('name')
                        lb_name.text = str(lbs[bi])
                        bndbox = dup_obj.find('bndbox')
                        for i in range(4):
                            bndbox[i].text = str(boxes[bi][i])

                else: x_root.remove(x_root.find('object'))
                tree.write(des)


if __name__ == '__main__':
    directory = "voc_ann"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory, "does not exist, created one!")
    else:
        print(directory, "already exists. ")

    exists = os.path.isfile('./voc_ann/tmp.xml')
    if exists:
        print("tmp.xml file already exist.")
    else:
        newPath = shutil.copy('tmp.xml', './voc_ann')
        print("tmp.xml file is not in voc_ann, move it in, path is", newPath) 
    _main()
