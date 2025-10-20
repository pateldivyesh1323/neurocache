# LRU Cache
import time
from caching.logger import log_status
from ml.predictor import ReusePredictor

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
    def __init__(self, session, capacity = 5, use_ml_eviction = True):
        self.capacity = capacity
        self.cache = {}
        self.list = LinkedList()
        self.session = session
        self.key_stats = {}
        self.use_ml_eviction = use_ml_eviction
        self.predictor = ReusePredictor() if use_ml_eviction else None
    
    def get(self, key):
        if key not in self.cache:
            self.log_event(key, "get", "miss")
            return None
        node = self.cache[key]
        self.list.insert_at_front(node)
        self.log_event(key, "get", "hit")
        return node.value

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.list.insert_at_front(node)
        else:
            if len(self.cache) >= self.capacity:
                if self.use_ml_eviction and self.predictor.model is not None:
                    removed_node = self._evict_ml_based()
                else:
                    removed_node = self.list.remove_from_back()
                del self.cache[removed_node.key]
                del self.key_stats[removed_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self.list.insert_at_front(new_node)
        self.log_event(key, "set")


    def _evict_ml_based(self):
        now = time.time()
        min_reuse_prob = float('inf')
        evict_node = None
        
        for key, node in self.cache.items():
            stats = self.key_stats[key]
            time_since = now - stats["last_access"] if stats["last_access"] else 0
            access_count = stats["access_count"]
            
            reuse_prob = self.predictor.predict_reuse_probability(time_since, access_count)
            
            if reuse_prob < min_reuse_prob:
                min_reuse_prob = reuse_prob
                evict_node = node
        
        if evict_node:
            self.list.remove_node(evict_node)
        else:
            evict_node = self.list.remove_from_back()
        
        return evict_node

    def log_event(self, key, event, status = ""):
        now = time.time()
        stats = self.key_stats.get(key, {"access_count": 0, "last_access": None})

        if stats["last_access"] is None:
            time_since_last_access = None
        else:
            time_since_last_access = now - stats["last_access"]

        stats["access_count"] += 1
        stats["last_access"] = now
        self.key_stats[key] = stats

        log_status(self.session, now, key, event, status, time_since_last_access, stats["access_count"])
        return stats
        