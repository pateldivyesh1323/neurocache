from caching.cache_manager import CacheManager

cache_manager = CacheManager()
cache_manager.set("name", "Divyesh")
cache_manager.set("user_id", "e938ru2983rf0")
cache_manager.set("class", "Distinction")
cache_manager.get("name")
cache_manager.get("fingerprint")
cache_manager.get("class")