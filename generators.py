from random import randint

from genetic.gene import Gene
from genetic.interfaces import InitPopGenerator


class SuddenDeathException(Exception):
    pass


class SolutionEnforcingInitPopGenerator(InitPopGenerator):
    def __init__(self, pop_size, non_solution_handler):
        self.pop_size = pop_size
        self.fitness_calculator = None
        self.non_solution_handler = non_solution_handler

    def set_fitness_calculator(self, fc):
        self.fitness_calculator = fc
        self.non_solution_handler.set_fitness_calculator(fc)

    def generate_gene(self):
        raise NotImplementedError

    def handle_non_solution(self, gene):
        return self.non_solution_handler(gene)

    def __call__(self):
        ret = []

        while len(ret) < self.pop_size:
            gene = self.generate_gene()
            gene.fitness = self.fitness_calculator(gene)
            try:
                gene = self.handle_non_solution(gene)
            except SuddenDeathException:
                continue
            ret.append(gene)
        return ret


class IntegerGeneInitPopGenerator(SolutionEnforcingInitPopGenerator):
    def __init__(self, pop_size,  non_solution_handler, gene_size, range_from, range_to):
        super().__init__(pop_size, non_solution_handler)
        self.gene_size = gene_size
        self.range_from = range_from
        self.range_to = range_to

    def generate_gene(self):
        g = Gene()
        for _ in range(self.gene_size):
            g.append(randint(self.range_from, self.range_to))
        return g


class BinaryGeneInitPopGenerator(IntegerGeneInitPopGenerator):
    def __init__(self, pop_size, non_solution_handler, gene_size):
        super().__init__(pop_size, non_solution_handler, gene_size, 0, 1)
