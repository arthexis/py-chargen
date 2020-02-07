
class Trait(int):
    def __new__(cls, val=0, limit=5):
        self = int.__new__(cls, val)
        self.limit = limit
        return self

    def __add__(self, other):
        result = min(int(self) + int(other), self.limit)
        return Trait(result, limit=self.limit)

    def __sub__(self, other):
        result = max(int(self) - int(other), 0)
        return Trait(result, limit=self.limit)
