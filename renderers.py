from .interfaces import Renderer


class NullRenderer(Renderer):
    def append(self, population, generation_cnt):
        pass

    def write(self):
        pass


class FileRenderer(Renderer):
    def __init__(self, file):
        self.file = file
        self._f = open(self.file, "w")

    def __del__(self):
        self._f.close()

    def get_file_handle(self):
        return self._f

    def append(self, population, generation_cnt):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError


class WolframPlotRenderer(FileRenderer):
    def __init__(self, file):
        super().__init__(file)
        self.min = []
        self.max = []
        self.med = []

    def append(self, population, generation_cnt):
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
