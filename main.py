from caching.cache_manager import CacheManager

cache_manager = CacheManager()
cache_manager.put("name", "Divyesh")
cache_manager.put("user_id", "e938ru2983rf0")
cache_manager.put("class", "Distinction")
cache_manager.get("name")
cache_manager.get("fingerprint")
cache_manager.get("class")