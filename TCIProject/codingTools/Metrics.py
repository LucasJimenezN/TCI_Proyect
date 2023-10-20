import sys
import os

from .utils import *

#object to quantize/dequantize input data
class Metrics:
    
    #constructor. 
    def __init__(self, original_image, reconstructed_image):
        self.original_image = original_image
        self.reconstructed_image = reconstructed_image
        self.MSE = 0
        self.PSNR = 0
        self.PAE_data = 0
        
        self.original_image_components = original_image.shape[0]
        self.original_image_rows = original_image.shape[1]
        self.original_image_columns = original_image.shape[2]
        
        self.reconstructed_image_components = reconstructed_image.shape[0]
        self.reconstructed_image_rows = reconstructed_image.shape[1]
        self.reconstructed_image_columns = reconstructed_image.shape[2]
        
        #DIMENSIONS OF BOTH IMAGES NEED TO BE VALIDATED
    
    #Check the geometry of the images to be compared
    def check_geometry(self):
        pass
    
    #compute metrics    
    def compute(self):
        pass
    
    def PAE(self):
        # PAE(I, IQ) = max |xij - xij^|
        max_value = None
        for z in range(self.original_image_components):
            for y in range(self.original_image_rows):
                for x in range(self.original_image_columns):
                    value = self.original_image[z][y][x] - self.reconstructed_image[z][y][x]
                    if max_value == None:
                        max_value = value
                    elif max_value < value:
                        max_value = value
        self.PAE_data = max_value
