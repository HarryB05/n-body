"""
Stack data structure for tree traversal.
"""


class Stack:
    """Simple stack implementation using a list."""
    
    def __init__(self):
        """Initialize an empty stack."""
        self.inList = []
        
    def push(self, v):
        """Push an element onto the stack."""
        self.inList.append(v)

    def pop(self):
        """Pop and return the top element from the stack."""
        if len(self.inList) == 0:
            raise Exception("Popping from an empty stack")
        return self.inList.pop()
    
    def isEmpty(self):
        """Check if the stack is empty."""
        return len(self.inList) == 0
    
    def size(self):
        """Return the size of the stack."""
        return len(self.inList)

    def toArray(self):
        """Return the stack as an array."""
        return self.inList
    
    def __str__(self):
        return str(self.inList)

