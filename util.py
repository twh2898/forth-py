from exceptions import ForthException


class Memory:
    def __init__(self):
        self.memory = []
        self.vars = {}
        self.used = 0
    
    def allot(self, sz=1):
        index = self.used
        self.used += sz
        for _ in range(sz):
            self.memory.append(0)
        return index
    
    def create_var(self, name):
        if name in self.vars:
            raise ForthException('Variable already exists ' + name)
        index = self.allot()
        self.vars[name] = index
        return index
    
    def get_var(self, name):
        if not name in self.vars:
            raise ForthException('No variable named ' + name)
        return self.vars[name]
    
    def get_val(self, addr):
        if addr < 0 or addr >= self.used:
            raise ForthException('Address out of bounds ' + repr(addr))
        return self.memory[addr]

    def set_val(self, addr, val):
        if addr < 0 or addr >= self.used:
            raise ForthException('Address out of bounds ' + repr(addr))
        self.memory[addr] = val


class Stack:
    def __init__(self):
        self.stack = []
        self.length = 0
    
    def is_empty(self):
        return self.length == 0

    def peek(self, level=1):
        if level > self.length:
            raise ForthException('Stack underflow')
        return self.stack[-level]
    
    def push(self, item):
        self.stack.append(item)
        self.length += 1
    
    def pop(self):
        if self.is_empty():
            raise ForthException('Stack underflow')
        self.length -= 1
        return self.stack.pop()
