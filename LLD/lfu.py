class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def add_node(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def pop_tail(self):
        if self.head.next == self.tail:
            return None
        tail_node = self.tail.prev
        self.remove_node(tail_node)
        return tail_node
    
    def is_empty(self):
        return self.head.next == self.tail

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.key_node_map = {}  # Key to node mapping
        self.freq_list_map = {} # Frequency to DoublyLinkedList mapping

    def _update(self, node):
        freq = node.freq
        self.freq_list_map[freq].remove_node(node)
        
        if self.freq_list_map[freq].is_empty():
            del self.freq_list_map[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        
        node.freq += 1
        freq = node.freq
        if freq not in self.freq_list_map:
            self.freq_list_map[freq] = DoublyLinkedList()
        self.freq_list_map[freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.key_node_map:
            return -1
        node = self.key_node_map[key]
        self._update(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        
        if key in self.key_node_map:
            node = self.key_node_map[key]
            node.value = value
            self._update(node)
        else:
            if self.size >= self.capacity:
                lfu_list = self.freq_list_map[self.min_freq]
                removed_node = lfu_list.pop_tail()
                del self.key_node_map[removed_node.key]
                self.size -= 1
            
            new_node = Node(key, value)
            self.key_node_map[key] = new_node
            if 1 not in self.freq_list_map:
                self.freq_list_map[1] = DoublyLinkedList()
            self.freq_list_map[1].add_node(new_node)
            self.min_freq = 1
            self.size += 1

# Example Usage:
lfu = LFUCache(2)

lfu.put(1, 1)
lfu.put(2, 2)
print(lfu.get(1))  # Returns 1
lfu.put(3, 3)      # Evicts key 2 (LFU: 2 and LRU among 2, 1 is 2)
print(lfu.get(2))  # Returns -1 (not found)
print(lfu.get(3))  # Returns 3
lfu.put(4, 4)      # Evicts key 1 (LFU: 1 and 3, LRU among them is 1)
print(lfu.get(1))  # Returns -1 (not found)
print(lfu.get(3))  # Returns 3
print(lfu.get(4))  # Returns 4
