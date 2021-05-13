class Vertex:
    def __init__(self, name=''):
        self.__name = name
        self.in_arcs = set()  # we need them to check consistency if we are deleting a vertex
        self.out_arcs = set()  # we need them to update arcs if we are adding a new one

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.name == other.name

    def __str__(self):
        res = f'In: {self.in_arcs}, out: {self.out_arcs}\n'
        return res

    def rename(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name
