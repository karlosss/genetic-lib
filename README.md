# Documentation

## Algorithm Description

The algorithm runs as follows:

```
generate initial population and calculate its fitness
remember the best individual
lock in the population size
repeat forever:
    select immutable individuals
    select parents for next generation (from the whole population)
    cross the parents over, creating a number of offspring equal to the initial population size
    mutate offspring and mutable individuals
    calculate fitness of the population
    check for a new best individual
    select an amount of survivors equal to the initial population size
    advance to the next generation
    check if algorithm should terminate and if yes, return current best individual
```

This main loop is available in `GeneticSolver`. It accepts a lot of parameters in the initializer. Those parameters and their options are described below. Unless stated otherwise, all of them are invoked repeatedly, whenever needed.

## Generators

These serve for generating the initial population.

### `IntegerGeneInitPopGenerator(gene_size, pop_size, range_from, range_to)`

Generates `pop_size` genes, each of `gene_size` long, filled with uniformly random integers from range `range_from` to `range_to`.

### `BinaryGeneInitPopGenerator(gene_size, pop_size)`

Generates `pop_size` genes, each of `gene_size` long, filled with uniformly random bits.

## Fitness Calculator

Interface for calculating the fitness of an individual. A `FitnessCalculator` shall implement `__call__(self, gene)` and return the fitness of the individual specified by the `gene`.

An example of `KnapsackFitnessCalculator` for 0/1 Knapsack problem. Each individual has its fitness equal to the sum of the values. If it exceedes the knapsack capacity, the fitness is negative, according to how much the capacity is exceeded.

```
class KnapsackFitnessCalculator(FitnessCalculator):
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def __call__(self, gene):
        wt = 0
        val = 0

        for i in range(0, len(gene)):
            if gene[i] == 1:
                wt += self.items[i].weight
                val += self.items[i].value

        if wt <= self.capacity:
            return val
        else:
            return self.capacity - wt
```

## Mutation Preventers

These serve for preventing some individuals from being mutated (usually because they are the fittest).

### `EliteMutationPreventer(elite_count_fn)`

This prevents a few fittest individuals from being mutated. The `elite_count_fn` is a function which returns the number of such individuals.

### `NoMutationPreventer()`

This prevents no individuals from being mutated. It technically disables this feature.

## Selectors

These serve for both selecting the parents and the survivors for the next generation.

### `TournamentSelector(tournament_size_fn, elitism_fn, count_fn=None)`

Selects an amount returned by `tournament_size_fn` of not-(yet)-selected at random, then add the fittest among those to the pool of the selected.
`elitism_fn` returns how many fittest individuals shall be selected regardless of the selection process.
`count_fn` returns how many individuals shall be selected (available only for parents, the number of survivors is defined automatically).

### `AgeSelector(elitism_fn, count_fn=None)`

Selects the youngest individuals, regardless of their fitness.
`elitism_fn` returns how many fittest individuals shall be selected regardless of the selection process.
`count_fn` returns how many individuals shall be selected (available only for parents, the number of survivors is defined automatically).

## Crossoverers

These serve for crossing the parents over and producing offspring.

### `OnePointCrossoverer(num_offspring_fn)`

Performs a one-point crossover at a random position. `num_offspring_fn` returns how many offspring shall a pair of parents produce (invoked repeatedly for each pair of parents)

### `MultiPointCrossoverer(point_cnt_fn, num_offspring_fn)`

Performs a multi-point crossover at random positions. `point_cnt_fn` returns the number of points (invoked repeatedly for each pair of parents). `num_offspring_fn` returns how many offspring shall a pair of parents produce (invoked repeatedly for each pair of parents)

### `UniformCrossoverer(num_offspring_fn, first_parent_probability_fn=lambda: 0.5 )`

Performs a uniform crossover. `num_offspring_fn` returns how many offspring shall a pair of parents produce (invoked repeatedly for each pair of parents). `first_parent_probability_fn` returns the probability of the first parent being selected as the source (invoked repeatedly for each pair of parents).

## Mutators

These serve for mutating the population.

### `RandomResettingMutator(allowed_values, mutation_probability_fn)`

Each cell of each gene of the population has a probability returned by `mutation_probability_fn` of being mutated. If a cell is mutated, its value is changed to one from the set of `allowed_values`. The values is always changed, thus e.g. `4` cannot mutate to `4`.

### `BitFlipMutator(mutation_probability_fn)`

Works only for genes consisting of `0`s and `1`s. Each cell of each gene of the population has a probability returned by `mutation_probability_fn` of being mutated. If a cell is mutated, its bit is inverted.

## Terminators

Decide whether the algorithm shall terminate now.

### `GenerationCountTerminator(generation_limit)`

Terminates after `generation_limit` generations.

### `NoImprovementTerminator(generation_limit)`

Terminates after the fitness of the best individual has not improved for `generation_limit` generations.

### `FitnessDegenerationTerminator(population_percentage_limit, fitness_threshold=0.0)`

Terminates after at least `population_percentage_limit` percent of the population has its fitness deviating from the best by no more than `fitness_threshold` percent.

## Renderers

Called after each generation and after the algorithm terminates. Serve for visualizing the progress of the algorithm.

### `NullRenderer()`

Shows nothing.

### `WolframPlotRenderer(file)`

Outputs a code for showing a plot in Wolfram language tp `file`.
