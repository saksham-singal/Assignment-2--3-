from bin import Bin
from avl import *
from node import Node
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bins = AVLTree()
        self.objects = AVLTree(comp_None)
        self.bins_blue = AVLTree(comp_b)
        self.bins_yellow = AVLTree(comp_y)
        self.bins_red = AVLTree(comp_r)
        self.bins_green = AVLTree(comp_g)
        self.object_to_bin = AVLTree(comp_None)

    def add_bin(self, bin_id, capacity):
        self.bins.insert(bin_id,Bin(bin_id,capacity))
        self.bins_blue.insert(capacity, bin_id)
        self.bins_green.insert(capacity, bin_id)
        self.bins_yellow.insert(capacity, bin_id)
        self.bins_red.insert(capacity, bin_id)
     
    def add_object(self, object_id, size, color): 
        object_to_add=Object(object_id,size,color)
        found_bin = None
        if color == Color.BLUE:
            found_bin_id = self.bins_blue.desired(size)
        elif color == Color.GREEN:
            found_bin_id = self.bins_blue.greatest_value()
        elif color == Color.YELLOW:
            found_bin_id = self.bins_yellow.desired(size)
        elif color == Color.RED:
            found_bin_id = self.bins_yellow.greatest_value()    
        
        if found_bin_id is None or self.bins_blue.greatest_key() < size or self.bins_yellow.greatest_key() < size:
            raise NoBinFoundException()
        found_bin = self.bins.search(found_bin_id)
        
        self.bins_yellow.delete(found_bin.capacity, found_bin.bin_id)
        self.bins_red.delete(found_bin.capacity, found_bin.bin_id)
        self.bins_blue.delete(found_bin.capacity, found_bin.bin_id)
        self.bins_green.delete(found_bin.capacity, found_bin.bin_id)
        found_bin.add_object(object_to_add)
        self.add_deleted_bin(found_bin)
        self.object_to_bin.insert(object_id, found_bin.bin_id)

    def delete_object(self, object_id):
        bin_id = self.object_to_bin.search(object_id)
        if bin_id is None:
            return None
        bin = self.bins.search(bin_id)
        former_capacity = bin.capacity
        bin.remove_object(object_id)
        latter_capacity = bin.capacity
        self.object_to_bin.delete(object_id)
        self.bins_blue.delete(former_capacity, bin_id)
        self.bins_red.delete(former_capacity, bin_id)
        self.bins_green.delete(former_capacity, bin_id)
        self.bins_yellow.delete(former_capacity, bin_id)
        self.bins_red.insert(latter_capacity, bin_id)
        self.bins_green.insert(latter_capacity, bin_id)
        self.bins_blue.insert(latter_capacity, bin_id)
        self.bins_yellow.insert(latter_capacity, bin_id)
       
    def bin_info(self, bin_id):
        bin = self.bins.search(bin_id)
        if not bin:
            raise NoBinFoundException()
        info=bin.get_info()
        return info   
        
    def object_info(self, object_id):
        bin_id_node = self.object_to_bin.search(object_id)
        if bin_id_node is None:
            return None
        return bin_id_node
    
    def add_deleted_bin(self, found_bin: Bin):
        self.bins_yellow.insert(found_bin.capacity, found_bin.bin_id)
        self.bins_red.insert(found_bin.capacity, found_bin.bin_id)
        self.bins_blue.insert(found_bin.capacity, found_bin.bin_id)
        self.bins_green.insert(found_bin.capacity, found_bin.bin_id)
     
    
    