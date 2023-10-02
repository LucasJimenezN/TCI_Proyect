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
        
        min = self.image_data.min()
        max = self.image_data.max()
        needed_bits_to_write = needed_bits(max-min)
        
        BFO.write_value(max,16)
        BFO.write_value(min,16)
        for z in range(self.image_data.shape[0]):
            for y in range(self.image_data.shape[1]):
                for x in range(self.image_data.shape[2]):
                    BFO.write_value(self.image_data[z][y][x],needed_bits_to_write)
        
        self.size_of_coded_file = BFO.size_of_file()
        
        BFO.close_binary_file_output()
        
    def decoding(self):
        BFI = binary_file_input(self.file_name)
        BFI.open_binay_file_input()
        max = int(BFI.read_value(16))
        min = int(BFI.read_value(16))
        print("min ",min)
        print("max ",max)
        needed_bits_to_read = needed_bits(max-min)
        print("needed_bits_to_read ",needed_bits_to_read)
        for z in range(self.image_data.shape[0]):
            for y in range(self.image_data.shape[1]):
                for x in range(self.image_data.shape[2]):
                    self.image_data[z][y][x] = BFI.read_value(needed_bits_to_read)

        
