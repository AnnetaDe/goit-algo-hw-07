class Tree_bi:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
        self.heigt = 1
        self._children = []
    def add_child(self, child):
        if self.left is None:
            self.left = child
        elif self.right is None:
            self.right = child
       
            
            
        self._children.append(child)    
   
        
tree = Tree_bi(1)


      
    



print(tree)