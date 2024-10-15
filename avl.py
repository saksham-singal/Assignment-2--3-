from node import Node
from object import Object
def comp_None(node_1,node_2):
    if node_1.id<node_2.id:
        return -1
    elif node_1.id==node_2.id:
        return 0
    else:
        return 1

def comp_b(node_1, node_2):    
    if node_1.id<node_2.id:
        return -1
    elif node_1.id>node_2.id:
        return 1
    else:
        if node_1.value<node_2.value:
            return -1
        elif node_1.value>node_2.value:
            return 1
        else:
            return 0
def comp_y(node_1, node_2):
    if node_1.id<node_2.id:
        return -1
    elif node_1.id>node_2.id:
        return 1
    else:
        if node_1.value>node_2.value:
            return -1
        elif node_1.value<node_2.value:
            return 1
        else:
            return 0
def comp_r(node_1, node_2):
    if node_1.id>node_2.id:
        return -1
    elif node_1.id<node_2.id:
        return 1
    else:
        if node_1.value<node_2.value:
            return -1
        elif node_1.value>node_2.value:
            return 1
        else:
            return 0
def comp_g(node_1, node_2):
    if node_1.id>node_2.id:
        return -1
    elif node_1.id<node_2.id:
        return 1
    else:
        if node_1.value>node_2.value:
            return -1
        elif node_1.value<node_2.value:
            return 1
        else:
            return 0

class AVLTree:
    def __init__(self, compare_function=comp_None):
        self._root = None
        self._size = 0
        self.comparator = compare_function

    def insert(self, id, value):
        node = Node(id, value)
        self._root = self._insert_recursive(self._root, node)

    def _insert_recursive(self, root, node):
        if root is None:
            self._size += 1
            return node
        comp = self.comparator(node, root)
        if comp < 0:
            root.left = self._insert_recursive(root.left, node)
        elif comp > 0:
            root.right = self._insert_recursive(root.right, node)
        else:
            raise KeyError(f"Duplicate key (id: {node.id}, value: {node.value}) cannot be inserted.")
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance_value = self.get_balance_value(root)
        if balance_value > 1 and self.comparator(node, root.left) < 0:
            return self.right_rotate(root)
        if balance_value < -1 and self.comparator(node, root.right) > 0:
            return self.left_rotate(root)
        if balance_value > 1 and self.comparator(node, root.left) > 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance_value < -1 and self.comparator(node, root.right) < 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def delete(self, id, value=None):
        node = Node(id, value if value is not None else -1e9)  
        self._root = self._delete(self._root, node)

    def _delete(self, root, node):
        if root is None:
            raise KeyError(f"Key (id: {node.id}, value: {node.value}) not found in the tree.")
        comp = self.comparator(node, root)
        if comp < 0:
            root.left = self._delete(root.left, node)
        elif comp > 0:
            root.right = self._delete(root.right, node)
        else:
            if root.left is None:
                temp = root.right
                root = None
                self._size -= 1
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                self._size -= 1
                return temp
            temp = self.leftmost_node(root.right)
            root.id = temp.id
            root.value = temp.value
            root.right = self._delete(root.right, temp)
        if root is None:
            return root
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance_value = self.get_balance_value(root)
        if balance_value > 1 and self.get_balance_value(root.left) >= 0:
            return self.right_rotate(root)
        if balance_value > 1 and self.get_balance_value(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance_value < -1 and self.get_balance_value(root.right) <= 0:
            return self.left_rotate(root)
        if balance_value < -1 and self.get_balance_value(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def search(self, id, value=None):
        node = self.search_node(self._root, Node(id, value if value is not None else None))
        return node.value if node else None

    def search_node_deletion(self, id, value=None):
        return self.search_node(self._root, Node(id, value if value is not None else None))

    def search_node(self, root, node):
        if root is None:
            return None
        comp = self.comparator(node, root)
        if comp == 0:
            return root
        elif comp < 0:
            return self.search_node(root.left, node)
        else:
            return self.search_node(root.right, node)

    def inorder_traversal(self):
        nodes = []
        self._inorder_traversal_list(self._root, nodes)
        return nodes

    def _inorder_traversal_list(self, node, nodes):
        if node:
            self._inorder_traversal_list(node.left, nodes)
            nodes.append(node)
            self._inorder_traversal_list(node.right, nodes)

    def desired(self, size):
        suitable_node = self._desired(self._root, size)
        return suitable_node.value if suitable_node else None

    def _desired(self, root, size):   
        if root is None:
            return None
        poss = None
        while root is not None:
            if root.id>=size:
                poss = root
                root = root.left
            else:
                root = root.right
        return poss      
    def greatest_key(self):
        node = self._greatest(self._root)
        return node.id if node else None
    def greatest_value(self):
        node = self._greatest(self._root)
        return node.value 
    def _greatest(self, root):
        if root is None:
            return None
        if root.right is None:
            return root
        while root.right:
            root = root.right
        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance_value(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def leftmost_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def rightmost_node(self, root):
        current = root
        while current.right:
            current = current.right
        return current

    def set_comparator(self, compare_function):
        self.comparator = compare_function

    def __len__(self):
        return self._size




        
        
        