# LRU Cache
import time
from caching.logger import log_status

class Node:
    def __init__(self, key, value, next = None, prev = None):
        self.key = key
        self.value = value
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_at_front(self, node: Node):
        if node.prev is not None and node.next is not None:
            self.remove_node(node)
        node.next = self.head.next
        node.next.prev = node
        self.head.next = node
        node.prev = self.head

    def remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def remove_from_back(self):
        node:Node = self.tail.prev
        self.remove_node(node)
        return node

class CacheManager:
    def __init__(self, capacity = 50):
        self.capacity = capacity
        self.cache = {}
        self.list = LinkedList()

    def get(self, key):
        if key not in self.cache:
            log_status(time.time(), key, "get", "miss")
            return None
        node = self.cache[key]
        self.list.insert_at_front(node)
        log_status(time.time(), key, "get", "hit")
        return node.value

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.list.insert_at_front(node)
        else:
            if len(self.cache) >= self.capacity:
                removed_node = self.list.remove_from_back()
                del self.cache[removed_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self.list.insert_at_front(new_node)
        log_status(time.time(), key, "set")
