from random import randint

from genetic.gene import Gene
from genetic.interfaces import InitPopGenerator


class IntegerGeneInitPopGenerator(InitPopGenerator):
    def __init__(self, gene_size, pop_size, range_from, range_to):
        self.gene_size = gene_size
        self.pop_size = pop_size
        self.range_from = range_from
        self.range_to = range_to

    def __call__(self):
        ret = []
        for _ in range(self.pop_size):
            gene = Gene()
            for __ in range(self.gene_size):
                gene.append(randint(self.range_from, self.range_to))
            ret.append(gene)
        return ret


class BinaryGeneInitPopGenerator(IntegerGeneInitPopGenerator):
    def __init__(self, gene_size, pop_size):
        super().__init__(gene_size, pop_size, 0, 1)
