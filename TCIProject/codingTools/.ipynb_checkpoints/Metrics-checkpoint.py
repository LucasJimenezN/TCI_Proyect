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
        error = 0
        for z in range(self.original_image_components):
            for y in range(self.original_image_rows):
                for x in range(self.original_image_columns):
                    error += (self.original_image[z][y][x] - self.reconstructed_image[z][y][x]) * (self.original_image[z][y][x] - self.reconstructed_image[z][y][x])                
        
    
        self.MSE = error / (self.original_image_components * self.original_image_rows * self.original_image_columns)

        if self.MSE == 0: self.PSNR = "Infinity"
        else:
            self.PSNR = "PSNR calculation is pending of being programmed"
    