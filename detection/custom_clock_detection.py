from __future__ import absolute_import, division
from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
import numpy as np
from scipy.misc import imread, imsave, imresize
import mxnet as mx

import os, time
######################################################################
# Load a pretrained model
# -------------------------
#
# Let's get an SSD model trained with 512x512 images on Pascal VOC
# dataset with ResNet-50 V1 as the base model. By specifying
# ``pretrained=True``, it will automatically download the model from the model
# zoo if necessary. For more pretrained models, please refer to
# :doc:`../../model_zoo/index`.

#net = './number_train_result/ssd_300_vgg16_atrous_voc_0230_0.9997.params'

#net = model_zoo.ssd_300_vgg16_atrous_custom(classes=['zero', 'one', 'two','three', 'four','five','six','seve','eight','nine'], pretrained_base=True)
#net.hybridize()
#print(net)

#net(mx.nd.ones(shape=(1,3,300,300)))
#net.export('symbol.json', 0)
#net.load_parameters('./number_train_result/ssd_300_vgg16_atrous_voc_0230_0.9997.params')
net =model_zoo.get_model(name='ssd_300_vgg16_atrous_voc', pretrained = False, root ='./number_train_result2/ssd_300_vgg16_atrous_voc_best.params')
net.load_parameters('./number_train_result2/ssd_300_vgg16_atrous_voc_best.params')
net.collect_params()


print("net is ", net)
######################################################################
# Pre-process an image
# --------------------
#
# Next we download an image, and pre-process with preset data transforms. Here we
# specify that we resize the short edge of the image to 512 px. But you can
# feed an arbitrarily sized image.
#
# You can provide a list of image file names, such as ``[im_fname1, im_fname2,
# ...]`` to :py:func:`gluoncv.data.transforms.presets.ssd.load_test` if you
# want to load multiple image together.
#
# This function returns two results. The first is a NDArray with shape
# `(batch_size, RGB_channels, height, width)`. It can be fed into the
# model directly. The second one contains the images in numpy format to
# easy to be plotted. Since we only loaded a single image, the first dimension
# of `x` is 1.

def save_result(bboxes, scores=None,  labels=None, thresh = None, class_names=None):  

    if labels is not None and not len(bboxes) == len(labels):
        raise ValueError('The length of labels and bboxes mismatch, {} vs {}'
                         .format(len(labels), len(bboxes)))
    if scores is not None and not len(bboxes) == len(scores):
        raise ValueError('The length of scores and bboxes mismatch, {} vs {}'
                         .format(len(scores), len(bboxes)))
                     
                     
    if isinstance(bboxes, mx.nd.NDArray):
        bboxes = bboxes.asnumpy()
    if isinstance(labels, mx.nd.NDArray):
        labels = labels.asnumpy()
    if isinstance(scores, mx.nd.NDArray):
        scores = scores.asnumpy()
                             
    object = {}
    xmin_lst = []
    for i, bbox in enumerate(bboxes):
        
        if scores is not None and scores.flat[i] < thresh:
            continue
        if labels is not None and labels.flat[i] < 0:
            continue
        cls_id = int(labels.flat[i]) if labels is not None else -1
        
     
        if class_names is not None and cls_id < len(class_names):
            class_name = class_names[cls_id]
        else:
            class_name = str(cls_id) if cls_id >= 0 else ''
        score = '{:.3f}'.format(scores.flat[i]) if scores is not None else ''
        
        
        if class_name or score:
            xmin_lst.append(list(bbox))
            object[bbox[0]] = class_name

    # get rid off the situation which bbox is inside a bbox
    sorted_xmin = sorted(xmin_lst, key=lambda x:x[0]) 
    
    waste = []
    for index in range (len(sorted_xmin)):
        if index > 0 and  sorted_xmin[index][2]< sorted_xmin[index-1][2] :
            waste.append(sorted_xmin[index][0])
    
          
    obj_list=[]	
    for elem in sorted(object.items()) :
       if elem[0] not in (waste):
           obj_list.append(elem[1])
    
    
    return obj_list

def detect(name, result_dir):
    print(name)
    im_fname="./digital-clock-dataset/"+name
    #im_fname="./clock/"+name    

    x, img = data.transforms.presets.ssd.load_test(im_fname, short=300)
    print('Shape of pre-processed image:', x.shape)

######################################################################
# Inference and display
# ---------------------
#
# The forward function will return all detected bounding boxes, and the
# corresponding predicted class IDs and confidence scores. Their shapes are
# `(batch_size, num_bboxes, 1)`, `(batch_size, num_bboxes, 1)`, and
# `(batch_size, num_bboxes, 4)`, respectively.
#
# We can use :py:func:`gluoncv.utils.viz.plot_bbox` to visualize the
# results. We slice the results for the first image and feed them into `plot_bbox`:
    class_IDs, scores, bounding_boxes = net(x)
    ax = utils.viz.plot_bbox(img, bounding_boxes[0], scores[0],
                        class_IDs[0], thresh = 0.5, class_names=["zero","one","two","three","four","five","six","seven","eight","nine"])
    
    result=save_result(bounding_boxes[0], scores[0], class_IDs[0], thresh = 0.5,  class_names=["zero","one","two","three","four","five","six","seven","eight","nine"])
    
    digit_dic =	{"zero": "0", "one": "1", "two": "2","three": "3", "four": "4", "five": "5","six": "6", "seven": "7", "eight": "8","nine":"9"}
    result_digit=""
    for digit in result:
        result_digit=result_digit+digit_dic[digit]
      
    ax.text(10, 10, result_digit,color='white', 
        bbox=dict(facecolor='blue', edgecolor='blue'), style='italic', fontsize=20)
    
    
    plt.show()
    plt.savefig("./"+result_dir+"/"+name+"_detection.jpg")
 

now = time.time()
number = 0

#source_dir = "clock"
#result_dir = "clock_detection"

source_dir = "digital-clock-dataset"
result_dir = "ssd_clock_detection"

if not os.path.exists(result_dir):
    os.makedirs(result_dir)
    print(result_dir, "does not exist, create one.")
else:
    filelist = [ f for f in os.listdir(result_dir)]
    print(result_dir, "already exists, clear it.")
 
    for f in filelist:
        os.remove(os.path.join(result_dir, f))

for filename in os.listdir(source_dir):
    if filename.endswith(".PNG") or filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith("JPEG"):
        number = number + 1
        detect(filename, result_dir)
        
later = time.time()
difference = later - now
print("time cost for detecting", number, "images is",difference, "second")
