import sys
import os

from .utils import *

#object to quantize/dequantize input data
class Metrics:
    
    PAE_data = None
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
    
    #Get PAE
    def get_pae(self):
        return self.PAE_data

    #Check the geometry of the images to be compared
    def check_geometry(self):
        pass
    
    #compute metrics    
    def compute(self):
        pass
    
    def calculate_pae(self):
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
        return max_value
    
    def calculate_mse(self):
        # MSE(I,IQ) = (1/Ni*Nj) * |Xij - Xij^|
        equation_1st_part = 1 / (self.original_image_rows * self.original_image_columns)
        sumatori = 0
        for z in range(self.original_image_components):
            for y in range(self.original_image_rows):
                for x in range(self.original_image_columns):
                    sumatori = sumatori + abs(self.original_image[z][y][x] - self.reconstructed_image[z][y][x])
        result = equation_1st_part * sumatori
        self.MSE = result
        return result
    
    def calculate_psnr(self):
        # PSNR(I, IQ) = 10*log10 ( (2^b - 1)^2/MSE )
        mse = self.calculate_mse()
        max_value = None
        for z in range(self.original_image_components):
            for y in range(self.original_image_rows):
                for x in range(self.original_image_columns):
                    if max_value == None:
                        max_value = self.original_image[z][y][x]
                    else:
                        if max_value < self.original_image[z][y][x]:
                            max_value = self.original_image[z][y][x]
        num_bits = math.ceil(math.log2(max_value))
        result = 10 * math.log10((pow(pow(2,num_bits),2))/mse)
        self.PSNR = result
        return result