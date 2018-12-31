class InitPopGenerator:
    def __call__(self):
        raise NotImplementedError


class Mutator:
    def __call__(self, population):
        raise NotImplementedError


class FitnessCalculator:
    def __call__(self, gene):
        raise NotImplementedError


class Crossoverer:
    def __call__(self, parents, population):
        raise NotImplementedError


class Terminator:
    def __call__(self, population, best, generation_cnt):
        raise NotImplementedError


class Selector:
    def __call__(self, population, count=None):
        raise NotImplementedError


class MutationPreventer:
    def __call__(self, population):
        raise NotImplementedError


class NonSolutionHandler:
    def __init__(self):
        self.fitness_calculator = None

    def set_fitness_calculator(self, fc):
        self.fitness_calculator = fc

    def calculate_fitness(self, gene):
        gene.fitness = self.fitness_calculator(gene)

    def __call__(self, gene):
        raise NotImplementedError


class Renderer:
    def append(self, population, generation_cnt):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError
