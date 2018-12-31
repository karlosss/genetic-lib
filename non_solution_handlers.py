from genetic.generators import SuddenDeathException
from genetic.interfaces import NonSolutionHandler


class SuddenDeathNonSolutionHandler(NonSolutionHandler):
    def __call__(self, gene):
        raise SuddenDeathException


class DoNothingNonSolutionHandler(NonSolutionHandler):
    def __call__(self, gene):
        return gene
