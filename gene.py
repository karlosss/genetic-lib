class Gene(list):
    def __init__(self, null_val=None):
        self._null_val = null_val
        self.fitness = None
        self.age = 0
        super().__init__()

    def __setitem__(self, key, value):
        for i in range(len(self), key + 1):
            self.append(self._null_val)
        if self[key] != value:
            self.fitness = None
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        if item >= len(self):
            return self._null_val
        return super().__getitem__(item)

    def __hash__(self):
        h = 0
        for item in self:
            h = (h + hash(item)) % 2147483647
        return h

    def __repr__(self):
        return "<Fit={}, Age={}, Gene={}>".format(self.fitness, self.age, super().__repr__())

    def __str__(self):
        return self.__repr__()
