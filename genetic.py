from copy import deepcopy
from random import randint
from signal import signal, SIGINT

from genetic.gene import Gene
from genetic.generators import SuddenDeathException
from genetic.interfaces import Renderer
from genetic.renderers import NullRenderer


class SIGINT_handler:
    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, *args, **kwargs):
        print("---SIGINT received, will terminate---")
        self.SIGINT = True


class GeneticSolver:
    def __init__(self,
                 init_pop_generator,
                 fitness_calculator,
                 parent_selector,
                 crossoverer,
                 mutator,
                 mutation_preventer,
                 non_solution_handler,
                 survivor_selector,
                 terminator,
                 renderer=NullRenderer()):

        self._init_pop_generator = None
        self._fitness_calculator = None
        self._parent_selector = None
        self._crossoverer = None
        self._mutator = None
        self._survivor_selector = None
        self._non_solution_handler = None
        self._terminator = None
        self._mutation_preventer = None

        self._assign_init_param("init_pop_generator", init_pop_generator)
        self._assign_init_param("fitness_calculator", fitness_calculator)
        self._assign_init_param("parent_selector", parent_selector)
        self._assign_init_param("crossoverer", crossoverer)
        self._assign_init_param("mutator", mutator)
        self._assign_init_param("mutation_preventer", mutation_preventer)
        self._assign_init_param("non_solution_handler", non_solution_handler)
        self._assign_init_param("survivor_selector", survivor_selector)
        self._assign_init_param("terminator", terminator)

        self._non_solution_handler.set_fitness_calculator(self._fitness_calculator)

        self._sigint_handler = SIGINT_handler()
        signal(SIGINT, self._sigint_handler.signal_handler)

        if not isinstance(renderer, Renderer):
            raise TypeError("renderer must be a Renderer, not {}.".format(renderer.__class__.__name__))
        self._renderer = renderer

    def _assign_init_param(self, param_name, param):
        if not hasattr(param, "__call__"):
            raise TypeError("{} must be callable.".format(param_name))
        setattr(self, "_{}".format(param_name), param)

    @staticmethod
    def _list_of_genes_check(param_name, param):
        if not isinstance(param, list):
            raise TypeError("{} must return a list of Genes, not a {}.".format(param_name, param.__class__.__name__))
        for item in param:
            if not isinstance(item, Gene):
                raise TypeError("Items in {} list must be Genes, not {}.".format(param_name, item.__class__.__name__))

    def _generate_init_pop(self):
        self._init_pop_generator.set_fitness_calculator(self._fitness_calculator)
        pop = self._init_pop_generator()
        self._list_of_genes_check("init_pop_generator", pop)
        return pop

    def _get_mutation_prevented(self, population):
        elite = self._mutation_preventer(population)
        self._list_of_genes_check("mutation_preventer", elite)
        return elite

    def _select_parents_for_next_generation(self, population):
        next_gen = self._parent_selector(population)
        self._list_of_genes_check("selector", next_gen)
        return next_gen

    def _crossover(self, parents, population):
        co = self._crossoverer(parents, population)
        self._list_of_genes_check("crossoverer", co)
        return co

    def _mutate(self, next_generation):
        mutated = self._mutator(next_generation)
        self._list_of_genes_check("mutator", mutated)
        return mutated

    def _fitness_and_repair(self, next_generation, population):
        pop = None
        for i in range(len(next_generation)):
            next_generation[i].fitness = self._fitness_calculator(next_generation[i])
            try:
                next_generation[i] = self._non_solution_handler(next_generation[i])
            except SuddenDeathException:
                if pop is None:
                    pop = deepcopy(population)
                replacement = pop.pop(randint(0, len(pop)-1))
                next_generation[i] = replacement
        return next_generation

    def _select_survivors(self, next_generation, population_size):
        survivors = self._survivor_selector(next_generation, count=population_size)
        self._list_of_genes_check("survivor_selector", survivors)
        return survivors

    def _terminate(self, population, best, generation_cnt):
        term = self._terminator(population, best, generation_cnt)
        if not isinstance(term, bool):
            raise TypeError("terminator must return a bool, not {}.".format(term.__class__.__name__))
        term = term or self._sigint_handler.SIGINT
        if term:
            self._renderer.write()
        return term

    def _render(self, population, generation_cnt):
        self._renderer.append(population, generation_cnt)

    def run(self):
        # generate initial population
        population = self._generate_init_pop()
        population_size = len(population)

        # find current best
        population.sort(key=lambda x: -x.fitness)
        best = population[0]

        generation_cnt = 0

        # render initial state
        self._render(population, generation_cnt)

        while True:
            # strip the elite off of the population
            elite = self._get_mutation_prevented(population)

            # select parents for the next generation
            parents = self._select_parents_for_next_generation(elite + population)

            # crossover the parents to create offspring
            offspring = self._crossover(parents, elite + population)

            # mutate the next generation candidates
            mutated_offspring = self._mutate(offspring)
            mutated_population = self._mutate(population)

            next_generation_candidates = mutated_offspring + mutated_population

            next_generation = elite + next_generation_candidates

            next_generation = self._fitness_and_repair(next_generation, population)

            # check for a new best
            this_gen_best = max(next_generation, key=lambda x: x.fitness)
            if this_gen_best.fitness > best.fitness:
                best = this_gen_best

            # select survivors
            next_generation = self._select_survivors(next_generation, population_size)
            next_generation.sort(key=lambda x: -x.fitness)

            # check if the sizes of generations match
            if len(next_generation) != population_size:
                raise ValueError("Generation {} size mismatch: required {}, actual {}.".format(
                    generation_cnt+1, population_size, len(next_generation)))

            # advance to the next generation
            generation_cnt += 1
            population = next_generation
            for item in population:
                item.age += 1

            # render current state
            self._render(population, generation_cnt)

            # check if the algorithm terminates
            if self._terminate(population, best, generation_cnt):
                return best
