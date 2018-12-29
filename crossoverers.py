from random import sample, randint, random

from genetic.gene import Gene
from genetic.interfaces import Crossoverer


class TwoParentCrossoverer(Crossoverer):
    def __init__(self, num_offspring_fn):
        self.num_offspring_fn = num_offspring_fn

    def get_num_offsprings(self):
        return self.num_offspring_fn()

    def crossover(self, gene_length, parents):
        raise NotImplementedError

    def __call__(self, parents, population):
        ret = []
        gene_length = len(population[0])

        cnt = 0
        while cnt < len(population):
            par = sample(parents, 2)
            for _ in range(self.get_num_offsprings()):
                g = self.crossover(gene_length, par)
                ret.append(g)
                cnt += 1

        return ret


class MultiPointCrossoverer(TwoParentCrossoverer):
    def __init__(self, point_cnt_fn, num_offspring_fn):
        super().__init__(num_offspring_fn)
        self.point_cnt_fn = point_cnt_fn

    def get_point_cnt(self):
        return self.point_cnt_fn()

    def crossover(self, gene_length, parents):
        points = sample(range(gene_length - 1), self.get_point_cnt())
        current_parent = randint(0, 1)
        g = Gene()
        for i in range(gene_length):
            g[i] = parents[current_parent][i]
            if i in points:
                current_parent = (current_parent + 1) % 2
        return g


class OnePointCrossoverer(MultiPointCrossoverer):
    def __init__(self, num_offspring_fn):
        super().__init__(lambda: 1, num_offspring_fn)


class UniformCrossoverer(TwoParentCrossoverer):
    def __init__(self, num_offspring_fn, first_parent_probability_fn=lambda: 0.5):
        super().__init__(num_offspring_fn)
        self.first_parent_probability_fn = first_parent_probability_fn

    def get_first_parent_probability(self):
        return self.first_parent_probability_fn()

    def crossover(self, gene_length, parents):
        g = Gene()
        for i in range(gene_length):
            g[i] = parents[0][i] if random() < self.get_first_parent_probability() else parents[1][i]
        return g
