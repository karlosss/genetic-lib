from bisect import bisect_left
from copy import deepcopy
from random import sample, randint

from genetic.interfaces import Selector


class CountSelector(Selector):
    def __init__(self, elitism_fn, count_fn=None):
        self.count_fn = count_fn
        self.elitism_fn = elitism_fn

    def get_count(self):
        count = self.count_fn()
        if count < 2:
            raise ValueError("Impossible to create the next generation with less than 2 parents.")
        return count

    def get_elitism(self):
        return self.elitism_fn()

    def choose_parent_id(self, population):
        raise NotImplementedError

    def __call__(self, population, count=None):
        count = count or self.get_count()
        elitism = self.get_elitism()
        if elitism > count:
            elitism = count
        if count > len(population):
            count = len(population)

        pop = deepcopy(population)
        pop.sort(key=lambda x: x.fitness)

        if elitism != 0:
            ret = pop[-elitism:]
            del pop[-elitism:]
        else:
            ret = []

        for _ in range(count - elitism):
            ret.append(pop.pop(self.choose_parent_id(pop)))

        return ret


class TournamentSelector(CountSelector):
    def __init__(self, tournament_size_fn, elitism_fn, count_fn=None):
        super().__init__(elitism_fn, count_fn)
        self.tournament_size_fn = tournament_size_fn

    def get_tournament_size(self):
        return self.tournament_size_fn()

    def choose_parent_id(self, population):
        ids = sample(range(len(population)), self.get_tournament_size())
        return max(ids, key=lambda x: population[x].fitness)


class AgeSelector(CountSelector):
    def __init__(self, elitism_fn, count_fn=None):
        super().__init__(elitism_fn, count_fn)

    def choose_parent_id(self, population):
        ids = [i for i in range(len(population))]
        return max(ids, key=lambda x: -population[x].age)


class RouletteSelector(CountSelector):
    def choose_parent_id(self, population):
        cumulative_probs = [0]

        for item in reversed(population):
            if item.fitness > 0:
                cumulative_probs.append(cumulative_probs[-1]+item.fitness)

        rnd = randint(cumulative_probs[0], cumulative_probs[-1])
        i = bisect_left(cumulative_probs, rnd)
        return len(population) - i
