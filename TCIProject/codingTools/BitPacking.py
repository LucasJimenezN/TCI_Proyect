import sys
import os

from .utils import *
from .binary_file_output import *
from .binary_file_input import *

#object to manipulate a output binary file
class BitPacking:
    
    #constructor. 
    def __init__(self, file_name, image_data):
        self.file_name = file_name
        self.image_data = image_data
        self.components = image_data.shape[0]
        self.rows = image_data.shape[1]
        self.columns = image_data.shape[2]
        self.size_of_coded_file = 0

    def coding(self):
        BFO = binary_file_output(self.file_name)
        BFO.open_binay_file_output()
        #TO BE IMPLEMENTED

        # Write header information
        BFO.write_value(self.components, 32)  # 32-bit integer
        BFO.write_value(self.rows, 32)      # 32-bit integer
        BFO.write_value(self.columns, 32)   # 32-bit integer
        
        # Write image data
        for i in range(self.components):
            for j in range(self.rows):
                for k in range(self.columns):
                    value = self.image_data[i, j, k]
                    BFO.write_value(value, 32)  # 32-bit integer
                    self.size_of_coded_file += 4  # 4 bytes per value

        # Close the binary file
        BFO.close_binary_file_output()
        
    def decoding(self):
        BFI = binary_file_input(self.file_name)
        BFI.open_binay_file_input()
        #TO BE IMPLEMENTED

        # Read header information
        components = BFI.read_value(32)  # 32-bit integer
        rows = BFI.read_value(32)        # 32-bit integer
        columns = BFI.read_value(32)     # 32-bit integer
        
        # Initialize an array to store the decoded image
        decoded_image = np.zeros((components, rows, columns), dtype=np.int32)
        
        # Read image data
        for i in range(components):
            for j in range(rows):
                for k in range(columns):
                    value = BFI.read_value(32)  # 32-bit integer
                    decoded_image[i, j, k] = value

        # Close the binary file
        BFI.close_binary_file_input()

        return decoded_image
        
