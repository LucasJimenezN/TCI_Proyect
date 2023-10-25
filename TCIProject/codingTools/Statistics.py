import sys
import os
import math

from .utils import *

#object to compute statistics of the input data
class statistics:
    
    #constructor. 
    def __init__(self, image):
        self.image = image
        self.entropy = 0
        self.max_value = None
        self.min_value = None
        self.dynamic_range = 0
        
        self.image_components = image.shape[0]
        self.image_rows = image.shape[1]
        self.image_columns = image.shape[2]
        self.counter = self.image_components * self.image_rows * self.image_columns
    
    def calculate_max(self, pixel_value):
        if self.max_value == None:
            self.max_value = pixel_value
        else:
            if self.max_value < pixel_value:
                self.max_value = pixel_value
            
    def calculate_min(self, pixel_value):
        if self.min_value == None:
            self.min_value = pixel_value
        else:
            if self.min_value > pixel_value:
                self.min_value = pixel_value
    
    #compute metrics    
    def compute_entropy(self):
   
        histogram = {}
        #histogram[self.image[z][y][x]]
        #TO BE IMPLEMENTED

        for z in range(self.image_components):
            for y in range(self.image_rows):
                for x in range(self.image_columns):                                    
                    pixel_value = self.image[z][y][x]
                    self.calculate_max(pixel_value)
                    self.calculate_min(pixel_value)
                    if pixel_value in histogram:
                        histogram[pixel_value] += 1
                    else:
                        histogram[pixel_value] = 1

        # Probability
        for count in histogram.values():
            probability = count / self.counter
            prob_entropy = probability * math.log2(probability)
            
            self.entropy -= prob_entropy

        return self.entropy
    
