from avl import AVLTree
from exceptions import NoBinFoundException

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects = AVLTree()

    def __lt__(self, other):
        return self.capacity < other.capacity
    
    def __gt__(self, other):
        return self.capacity > other.capacity

    def __eq__(self, other):
        return self.capacity == other.capacity

    def add_object(self, object):
            self.objects.insert(object.object_id, object)
            self.capacity-=object.size
       

    def remove_object(self, object_id):
        object = self.objects.search(object_id)
        self.capacity += object.size
        self.objects.delete(object_id)
    def get_info(self):
        return (self.capacity, [object.value.object_id for object in self.objects.inorder_traversal()])
