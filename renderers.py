from .interfaces import Renderer


class FileRenderer(Renderer):
    class _Print:
        def write(self, s):
            print(s)

    def __init__(self, file):
        self.file = file
        self._f = open(self.file, "w") if file else None

    def __del__(self):
        if self.file:
            self._f.close()

    def get_file_handle(self):
        if self.file:
            return self._f
        return self._Print()

    def append(self, population, best, generation_cnt):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError


class WolframPlotRenderer(FileRenderer):
    def __init__(self, file=None):
        super().__init__(file)
        self.min = []
        self.max = []
        self.med = []

    def append(self, population, best, generation_cnt):
        self.min.append([generation_cnt, population[-1].fitness])
        self.max.append([generation_cnt, population[0].fitness])
        self.med.append([generation_cnt, population[len(population)//2].fitness])

    def write(self):
        wrt = 'ListLinePlot[{\n'

        wrt += '{'
        for i in range(len(self.min)-1):
            wrt += '{{{}, {}}}, '.format(*self.min[i])
        wrt += '{{{}, {}}}'.format(*self.min[-1])
        wrt += '},\n'

        wrt += '{'
        for i in range(len(self.max) - 1):
            wrt += '{{{}, {}}}, '.format(*self.max[i])
        wrt += '{{{}, {}}}'.format(*self.max[-1])
        wrt += '},\n'

        wrt += '{'
        for i in range(len(self.med) - 1):
            wrt += '{{{}, {}}}, '.format(*self.med[i])
        wrt += '{{{}, {}}}'.format(*self.med[-1])
        wrt += '}'

        wrt += '},\n'
        wrt += 'AxesLabel->{"Generation", "Fitness"},\n'
        wrt += 'PlotLegends->{"Min", "Max", "Med"}]\n'

        self.get_file_handle().write(wrt)


class StdoutRenderer(Renderer):
    def append(self, population, best, generation_cnt):
        print("Generation: {}, best: {}".format(generation_cnt, best))

    def write(self):
        pass


class DetailedStdoutRenderer(Renderer):
    def append(self, population, best, generation_cnt):
        minimum = population[-1].fitness
        maximum = population[0].fitness
        median = population[len(population) // 2].fitness
        print("Generation: {}, max: {}, min: {}, med: {}, best: {}".format(
            generation_cnt, maximum, minimum, median, best))

    def write(self):
        pass
