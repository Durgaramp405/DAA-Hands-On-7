import ctypes

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, key, value):
        new_node = Node(key, value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, key):
        
        current = self.head
        while current:
            if current.key == key:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def find(self, key):

        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

class HashTable:
    def __init__(self, initial_capacity=8, hash_function=None):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 0.75
        self.shrink_threshold = 0.25
        self._allocate_table(self.capacity)

        self.hash_function = hash_function or self.default_hash

    def _allocate_table(self, capacity):
        
        self.table = (ctypes.py_object * capacity)()
        for i in range(capacity):
            self.table[i] = DoublyLinkedList()

    def default_hash(self, key):
        
        A = 0.6180339887  
        return int(self.capacity * ((key * A) % 1)) % self.capacity

    def resize(self, new_capacity):
        
        old_table = self.table
        old_capacity = self.capacity

        self.capacity = new_capacity
        self._allocate_table(new_capacity)
        self.size = 0  
    
        for i in range(old_capacity):
            current = old_table[i].head
            while current:
                self.insert(current.key, current.value)
                current = current.next

    def insert(self, key, value):
        
        if self.size >= self.capacity * self.load_factor:
            self.resize(self.capacity * 2)  

        index = self.hash_function(key)
        node = self.table[index].find(key)

        if node:
            node.value = value  
        else:
            self.table[index].insert(key, value)
            self.size += 1

    def remove(self, key):
        
        index = self.hash_function(key)
        if self.table[index].remove(key):
            self.size -= 1
            if self.capacity > 8 and self.size <= self.capacity * self.shrink_threshold:
                self.resize(self.capacity // 2)
            return True
        return False

    def get(self, key):
        
        node = self.table[self.hash_function(key)].find(key)
        return node.value if node else None

    def display(self):
        print("\nHash Table Contents:")
        for i in range(self.capacity):
            print(f"Bucket {i}:", end=" ")
            current = self.table[i].head
            while current:
                print(f"({current.key}: {current.value})", end=" <-> ")
                current = current.next
            print("None")

if __name__ == "__main__":
    ht = HashTable()
    ht.insert(1, 100)
    ht.insert(2, 200)
    ht.insert(3, 300)
    ht.insert(4, 400)
    ht.insert(5, 500)

    ht.display()

    print("\nValue for key 3:", ht.get(3))  

    ht.remove(3)
    print("\nAfter removing key 3:")
    ht.display()

    for i in range(6, 20):
        ht.insert(i, i * 10)
    
    print("\nAfter inserting more elements (resizing happens):")
    ht.display()

