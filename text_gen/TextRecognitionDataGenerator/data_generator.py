import os
import random as rnd
import math
import cv2
import numpy as np

from skimage.util import random_noise

from PIL import Image, ImageFilter, ImageColor, ImageFont, ImageDraw


import computer_text_generator
import background_generator
import distorsion_generator
try:
    import handwritten_text_generator
except ImportError as e:
    print('Missing modules for handwritten text generation.')


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(cls, index, text, font, out_dir, size, extension, skewing_angle, random_skew, blur, random_blur, background_type, distorsion_type, distorsion_orientation, is_handwritten, name_format, width, alignment, text_color, orientation, space_width, margins, fit):
    
        num_zero = 6 - len(str(index))
        image_name = '{}.{}'.format('0'*num_zero+str(index),extension)
    
    
        file = open("bb_result.txt","a+")
        file.write("\n"+image_name.split(".")[0] + " " +text.replace(" ", ""))
        file.close
        
        
        image = None

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

#        print("margins is :" , margins)

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image = handwritten_text_generator.generate(text, text_color, fit)
        else:
            image = computer_text_generator.generate(text, font, text_color, size, orientation, space_width, fit)

        random_angle = rnd.randint(0-skewing_angle, skewing_angle)

        rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img # Mind = blown
        elif distorsion_type == 1:
            distorted_img = distorsion_generator.sin(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        elif distorsion_type == 2:
            distorted_img = distorsion_generator.cos(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        else:
            distorted_img = distorsion_generator.random(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        if orientation == 0:
            new_width = int(distorted_img.size[0] * (float(size - vertical_margin) / float(distorted_img.size[1])))
            resized_img = distorted_img.resize((new_width, size - vertical_margin), Image.ANTIALIAS)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
        # Vertical text
        elif orientation == 1:
            new_height = int(float(distorted_img.size[1]) * (float(size - horizontal_margin) / float(distorted_img.size[0])))
            resized_img = distorted_img.resize((size - horizontal_margin, new_height), Image.ANTIALIAS)
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background = background_generator.gaussian_noise(background_height, background_width)
        elif background_type == 1:
            background = background_generator.plain_white(background_height, background_width)
        elif background_type == 2:
            background = background_generator.quasicrystal(background_height, background_width)
        else:
            background = background_generator.picture(background_height, background_width)

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size
#        print("resized_img.size is : ", resized_img.size)

        if alignment == 0 or width == -1:
            background.paste(resized_img, (margin_left, margin_top), resized_img)
        elif alignment == 1:
            background.paste(resized_img, (int(background_width / 2 - new_text_width / 2), margin_top), resized_img)
        
            x0 = int(background_width / 2 - new_text_width / 2 )
            y0 = margin_top
            x1 = x0 + resized_img.size[0]
            y1 = y0 + resized_img.size[1]
            
            number =int((len(text)+1)/2)
#            print("digits number in text is : ", number)
#            print("text is : ", text)
            angle = math.radians(random_angle)
#            print("random_angle is ", random_angle)
#digit_width = int(((x1-x0)/number)*(1+0.005*(number)))
            digit_width = int(((x1-x0)/number)*(1+0.01*(number)))
        
            
            for i in range(number):
                x00 = x0 + i * digit_width + 1*(i - 0.5*number)
                x11 = x0 + (i+1) * (digit_width)
                txt_draw = ImageDraw.Draw(background)
    
                x_center = 0.5 * background.size[0]
                y_center = 0.5 * background.size[1]
                
                # test
                rx0 = x00
                ry0 = (y0-y_center)*math.cos(angle) - (x00-x_center)*math.sin(angle) + y_center
                
                rx1 = x11
                ry1 = (y1-y_center)*math.cos(angle) - (x11-x_center)*math.sin(angle) + y_center

            
#                rx0 = (x00-x_center)*math.cos(angle) + (y0-y_center)*math.sin(angle) + x_center
#                ry0 = (y0-y_center)*math.cos(angle) - (x00-x_center)*math.sin(angle) + y_center
#
#                rx1 = (x11-x_center)*math.cos(angle) + (y1-y_center)*math.sin(angle) + x_center
#                ry1 = (y1-y_center)*math.cos(angle) - (x11-x_center)*math.sin(angle) + y_center

                # the rotated bounding box for each digit is (rx0,ry0,rx1,ry1)
############################### txt_draw.rectangle((rx0,ry0,rx1,ry1), fill=None, outline=None, width=1)
                # print("the rotated bounding box for each digit is ", rx0,ry0,rx1,ry1)

                file = open("bb_result.txt","a+")
#                file.write("\nbbox coordinates : x_min: "+ str(rx0) +" y_min: "+str(ry0)+" x_max: "+ str(rx1)+" y_max: "+str(ry1))
                file.write(" "+ str(rx0)+" " + str(ry0)+" " +str(rx1)+" "+str(ry1))
                file.close
        
        else:
            background.paste(resized_img, (background_width - new_text_width - margin_right, margin_top), resized_img)

                
        
        ##################################
        # Apply gaussian blur #
        ##################################
        
        final_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else rnd.randint(0, blur))
            )
        )
        
        
       


        # Save the image
        final_image.convert('RGB').save(os.path.join(out_dir, image_name))
        final_img_copy =np.array(final_image.convert('RGB'))

        
        file = open("bb_result.txt","a+")
        file.write(" "+str(final_img_copy.shape[1])+" "+str(final_img_copy.shape[0]))
        file.close




