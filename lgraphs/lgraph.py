from lgraphs.vertex import Vertex
from lgraphs.arc import Arc
class LGraph:
    def __init__(self,brackets =[['(',')'],['[',']']]):
        self.__vertexes = {}
        self.__arcs= {}
        self.__brackets = brackets
    def add_arc(self,start_vertex,end_vertex,label='',bracket_trace='',key = None):
        flag = 0 if bracket_trace == '' else 1
        for b in self.__brackets:
            if bracket_trace in b:
                flag = 0
                break
        if flag:
            raise NameError('Incorrect brackets')
        if key:
            if key in self.__arcs:
                raise NameError(f'Arc with key "{key}" already exists')
        else:
            key = f'{len(self.__arcs) + 1}' ## need some ajustments kere, cause 2 then none will make an error
        if start_vertex in self.__vertexes.keys():
            self.__vertexes[start_vertex].out_arcs.add(key)
        else:
            self.__vertexes[start_vertex] = Vertex(start_vertex)
            self.__vertexes[start_vertex].out_arcs.add(key)
        if end_vertex in self.__vertexes.keys():
            self.__vertexes[end_vertex].in_arcs.add(key)
        else:
            self.__vertexes[end_vertex] = Vertex(end_vertex)
            self.__vertexes[end_vertex].in_arcs.add(key)

        self.__arcs[key]= Arc(key,self.__vertexes[start_vertex],self.__vertexes[end_vertex],label, bracket_trace)
    def add_vertex(self,name = None):
        if name:
            if name in self.__vertexes.keys():
                raise NameError(f'Vertex with name "{name}" already exists.')
            else:
                new_name = name
        else:
            new_name = f'{len(self.__vertexes) + 1}'
        self.__vertexes[new_name] = Vertex(new_name)

    def remove_arc(self,key):
        self.__arcs[key].remove_arc()
        self.__arcs.pop(key)
    def remove_vertex(self,name):
        j = self.__vertexes[name].in_arcs.copy()
        for i in j:
            self.__arcs[i].remove_arc()
            self.__arcs.pop(i)
        j = self.__vertexes[name].out_arcs.copy()
        for i in j:
            self.__arcs[i].remove_arc()
            self.__arcs.pop(i)
        self.__vertexes.pop(name)
    def __str__(self):
        res = "Vertexes: \n"
        for b in self.__vertexes.keys():
            res += b + ' ' + str(self.__vertexes[b])
        res += "\nArcs:\n"
        for a, c in self.__arcs.items():
            res += str(c) + '\n'
        return res
    def generate_from_grammar(self, inGrammar):
        #inGrammar must be a list of string rules. I concider makig a special class for this purposes
        #but it may be so small, that it seems to me that we can handle it right here
        for inString in inGrammar:
            pass
            #here i need to parse each grammar rule with regexp, to cath all non terminals from it


