class CacheManager:
    def __init__(self):
        self.cache = {}

    def get(self, key, params):
        return self.cache.get((key, frozenset(params.items())))

    def set(self, key, params, value):
        self.cache[(key, frozenset(params.items()))] = value
        
    def clear(self):
        self.cache.clear()