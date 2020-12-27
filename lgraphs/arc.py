from lgraphs.vertex import Vertex
class Arc:
    def __init__(self, key, start_vertex: Vertex , end_vertex: Vertex, label = '',bracket_trace=''):
        self.__label = label
        self.__key = key
        self.__brackets = bracket_trace
        self.__start_vertex = start_vertex
        self.__end_vertex = end_vertex
        self.__next_arcs = end_vertex.out_arcs
        #start_vertex.out_arcs.add(self.__key)
        #end_vertex.in_arcs.add(self.__key)

    def __eq__(self, other):
        return (isinstance(self, type(other))
                and self.__key == other.__key
                and self.__start_vertex == other.__start_vertex
                and self.__end_vertex == other.__end_vertex
                and self.__label == other.__label
                )
    def __str__(self):
        res = f'From {self.__start_vertex.name} to {self.__end_vertex.name}, with {self.__label},{self.__brackets}'
        res += f' next arcs: {self.__next_arcs}'
        return res
    def remove_arc(self):
        self.__start_vertex.out_arcs.discard(self.__key)
        self.__end_vertex.in_arcs.discard(self.__key)

    @property
    def start(self):
        return self.__start_vertex

    @property
    def end(self):
        return self.__end_vertex

    @property
    def label(self):
        return self.__label


