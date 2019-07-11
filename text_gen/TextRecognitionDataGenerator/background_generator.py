#%matplotlib inline
import cv2
import math
import os, sys, time
import random as rnd
import numpy as np
import random


import mxnet as mx
from mxnet import autograd, gluon, image, init, nd
from mxnet.gluon import data as gdata, loss as gloss, utils as gutils

from skimage.util import random_noise


from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps, ImageFile

def gaussian_noise(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((height, width)) * 255

    # We add gaussian noise
    cv2.randn(image, 235, 10)

    return Image.fromarray(image).convert('RGBA')

def plain_white(height, width):
    """
        Create a plain white background
    """

    return Image.new("L", (width, height), 255).convert('RGBA')

def quasicrystal(height, width):
    """
        Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
    """

    image = Image.new("L", (width, height))
    pixels = image.load()

    frequency = rnd.random() * 30 + 20 # frequency
    phase = rnd.random() * 2 * math.pi # phase
    rotation_count = rnd.randint(10, 20) # of rotations

    for kw in range(width):
        y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
        for kh in range(height):
            x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
            z = 0.0
            for i in range(rotation_count):
                r = math.hypot(x, y)
                a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                z += math.cos(r * math.sin(a) * frequency + phase)
            c = int(255 - round(255 * z / rotation_count))
            pixels[kw, kh] = c # grayscale
    return image.convert('RGBA')

def randomColor(image):
    
    random_factor = np.random.randint(0, 40) / 10.  # 随机因子
    color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
    random_factor = np.random.randint(10, 40) / 10.  # 随机因子
    brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
    random_factor = np.random.randint(10, 40) / 10.  # 随机因1子
    contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
    random_factor = np.random.randint(0, 40) / 10.  # 随机因子
    return ImageEnhance.Sharpness(contrast_image).enhance(random_factor)  # 调整图像锐度

def picture(height, width):
    """
        Create a background with a picture
    """

    pictures = os.listdir('./background')

    if len(pictures) > 0:
        pic = Image.open('./background/' + pictures[rnd.randint(0, len(pictures) - 1)])
        
       
        list = [0, 1]
        boolean1= random.choice(list)
        boolean2= random.choice(list)
        if(boolean1):
             # add random noise to random number of pictures
            picture = np.array(pic)
            cv2.randn(picture, (picture[0][0]),(20,20,20,0))
            pic = Image.fromarray(picture).convert('RGBA')

        if(boolean2):
            # add random color on random number of pictures
            pic= randomColor(pic)
        


        if pic.size[0] < width:
            pic = pic.resize([width, int(pic.size[1] * (width / pic.size[0]))], Image.ANTIALIAS)
        elif pic.size[1] < height:
            pic.thumbnail([int(pic.size[0] * (height / pic.size[1])), height], Image.ANTIALIAS)

        if (pic.size[0] == width):
            x = 0
        else:
            x = rnd.randint(0, pic.size[0] - width)
        if (pic.size[1] == height):
            y = 0
        else:
            y = rnd.randint(0, pic.size[1] - height)
        
        
        

        pic_result = pic.crop(
                              (
                               x,
                               y,
                               x + width,
                               y + height,
                               )
                              )
                              
                              # pic_result = random_noise(image=pic_result, mode = "gaussian", clip = True, mean=0.0, var=0.01)
                              
                              #cv2.randn(pic_result, (50,50,50), (50,50,50))

        
        return pic_result
    else:
        raise Exception('No images where found in the background folder!')
