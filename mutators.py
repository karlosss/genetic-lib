from random import sample, random, shuffle

from .interfaces import Mutator


class ProbabilityMutator(Mutator):
    def __init__(self, mutation_probability_fn):
        super().__init__()
        self.mutation_probability_fn = mutation_probability_fn

    def get_mutation_probability(self):
        return self.mutation_probability_fn()

    def __call__(self, population):
        raise NotImplementedError


class RandomResettingMutator(ProbabilityMutator):
    def __init__(self, allowed_values, mutation_probability_fn):
        self.allowed_values = allowed_values
        super().__init__(mutation_probability_fn)

    def get_random_replacement(self, not_this):
        return sample(self.allowed_values.difference({not_this}), 1)[0]

    def __call__(self, population):
        for gene in population:
            for i in range(len(gene)):
                if random() < self.get_mutation_probability():
                    gene[i] = self.get_random_replacement(gene[i])
        return population


class BitFlipMutator(RandomResettingMutator):
    def __init__(self, mutation_probability_fn):
        super().__init__({0, 1}, mutation_probability_fn)


class GreedyImprovementBitFlipMutator(Mutator):
    def __init__(self, individual_mutation_probability_fn):
        self.individual_mutation_probability_fn = individual_mutation_probability_fn
        super().__init__()

    def get_individual_mutation_probability(self):
        return self.individual_mutation_probability_fn()

    def __call__(self, population):
        for gene in population:
            if random() > self.individual_mutation_probability_fn():
                continue
            repeat = True
            old_fitness = self.calculate_fitness(gene)
            while repeat:
                repeat = False
                arr = [i for i in range(len(gene))]
                shuffle(arr)
                for i in arr:
                    if gene[i] == 0:
                        gene[i] = 1
                    else:
                        gene[i] = 0
                    new_fitness = self.calculate_fitness(gene)
                    if old_fitness >= new_fitness:
                        gene.fitness = old_fitness
                        if gene[i] == 0:
                            gene[i] = 1
                        else:
                            gene[i] = 0
                    else:
                        old_fitness = new_fitness
                        repeat = True
        return population
