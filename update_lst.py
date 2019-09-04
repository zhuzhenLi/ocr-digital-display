jpg_path = "./train/"
xml_path = "./train/"

import os
import xml.etree.ElementTree as ET

name = dict()
n=0

def get_objs_label(objs, size):
    label=[]
    global n
    size = [300, 400]
    for i in objs:
        bndbox = i.find("bndbox")
        xmin = bndbox.find("xmin").text
        xmin = float(xmin)/size[0]
        xmax = bndbox.find("xmax").text
        xmax = float(xmax)/size[0]
        ymin = bndbox.find("ymin").text
        ymin = float(ymin)/size[1]
        ymax = bndbox.find("ymax").text
        ymax = float(ymax)/size[1]
        name_idx = i.find("name").text
        if name_idx not in name.keys():
            name[name_idx] = n
            n += 1
        label = [ (name[name_idx] ), (xmin), (ymin) , (xmax) , (ymax) ]
    return label

def get_lst_line(line):
    idx = line.split()[0]
    filename = line.split()[2]
    xmlfile = ET.parse(xml_path+filename.replace("jpg", "xml"))
    width = xmlfile.find("size").find("width").text
    height = xmlfile.find("size").find("height").text
    objs = xmlfile.findall("object")
    position =  get_objs_label(objs, [float(width), float(height)])
    #print(position)
    label = idx + "\t" + "2\t6\t" + str(position[0])+"\t" +str(position[1])+"\t" +str(position[2])+"\t"+str(position[3])+"\t"+str(position[4])+"\t" + "0.0000"+"\t" + filename +"\n"
    return label

with open("data_train.lst") as f:
    while 1:
        line = f.readline()
        if not line:
            break
        label = get_lst_line(line)
        with open("train.lst", "a") as lst:
            lst.write(label)

