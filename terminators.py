from genetic.interfaces import Terminator


class GenerationCountTerminator(Terminator):
    def __init__(self, generation_limit):
        self.generation_limit = generation_limit

    def __call__(self, population, generation_cnt):
        return generation_cnt >= self.generation_limit


class NoImprovementTerminator(Terminator):
    def __init__(self, generation_limit):
        self.generation_limit = generation_limit
        self._best_fitness = None
        self._generation_cnt = 0

    def __call__(self, population, generation_cnt):
        if self._best_fitness is None or population[0].fitness > self._best_fitness:
            self._best_fitness = population[0].fitness
            self._generation_cnt = 0
        else:
            self._generation_cnt += 1

        return self._generation_cnt >= self.generation_limit


class FitnessDegenerationTerminator(Terminator):
    def __init__(self, population_percentage_limit, fitness_threshold=0.0):
        self.population_percentage_limit = population_percentage_limit
        self.fitness_threshold = fitness_threshold

    def _num_best_fitness(self, population):
        best = population[0].fitness
        cnt = 0
        for item in population:
            if (best - item.fitness)/best < self.fitness_threshold:
                cnt += 1
            else:
                break
        return cnt

    def __call__(self, population, generation_cnt):
        return self._num_best_fitness(population) / len(population) >= self.population_percentage_limit
