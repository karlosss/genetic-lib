from .interfaces import MutationPreventer


class EliteMutationPreventer(MutationPreventer):
    def __init__(self, elite_count_fn):
        self.elite_count_fn = elite_count_fn

    def get_elite_count(self):
        return self.elite_count_fn()

    def __call__(self, population):
        count = self.get_elite_count()
        elite = population[:count]
        del population[:count]
        return elite


class NoMutationPreventer(EliteMutationPreventer):
    def __init__(self):
        super().__init__(lambda: 0)
