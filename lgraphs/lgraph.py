from lgraphs.vertex import Vertex
from lgraphs.arc import Arc
import re
class LGraph:
    def __init__(self,brackets =[['(',')'],['[',']']]):
        self.__vertexes = {}
        self.__arcs= {}
        self.__brackets = brackets
        self.__start_vertexes = {}
        self.__finish_vertexes = {}
    def add_arc(self,start_vertex,end_vertex,label='',bracket_trace='',key = None):
        flag = 0 if bracket_trace == '' else 1
        for b in self.__brackets:
            for bb in b:
                if bb in bracket_trace :
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
    def set_start(self,name):
        if name in self.__vertexes.keys():
            self.__start_vertexes[name] = 1
        else:
            raise NameError(f'No vertex with name "{name}"')
    def set_finish(self,name):
        if name in self.__vertexes.keys():
            self.__finish_vertexes[name] = 1
        else:
            raise NameError(f'No vertex with name "{name}"')
    def generate_from_grammar(self, inGrammar):
        #inGrammar must be a list of string rules. I concider makig a special class for this purposes
        #but it may be so small, that it seems to me that we can handle it right here
        bracket_counter = 1
        for inString in inGrammar:
            #inString = "P->S@"
            res = re.search("->",inString)
            if res == None:
                raise TypeError('Incorrect grammar')
            left_part = inString[:res.start()] #label of the rule
            right_part = inString[res.end():] # what we need to do
            vertex_counter =1
            current_vertex = f'{left_part}_beg'
            end_vertex = f'{left_part}_end'
            for position, symbol in enumerate(right_part):
            #here we need to add an edge, if it is upper - than make 2 separate edjes and go forward
                if symbol == '|':
                    current_vertex =f'{left_part}_beg'
                    continue #does not work, need to count symbol position
                if symbol.isupper():
                    new_vertex = f'{symbol}_beg'
                    self.add_arc(current_vertex,new_vertex,'',f'({bracket_counter}')
                    current_vertex= f'{symbol}_end'
                    if right_part.endswith(symbol):
                        new_vertex=end_vertex
                    elif right_part[position+1]=='|':
                        new_vertex=end_vertex
                    else: # need to replace concrete brackets with variable
                        new_vertex = f'{left_part}{vertex_counter}'
                        vertex_counter+=1
                    self.add_arc(current_vertex,new_vertex,'',f'){bracket_counter}')
                    current_vertex=new_vertex
                    bracket_counter+=1
                else:
                    if right_part.endswith(symbol):
                        new_vertex=end_vertex
                    elif right_part[position+1]=='|' :
                        new_vertex=end_vertex
                    else:
                        new_vertex= f'{left_part}{vertex_counter}'
                        vertex_counter+=1
                    self.add_arc(current_vertex,new_vertex,symbol,'')
                    current_vertex = new_vertex


            #here i need to parse each grammar rule with regexp, to cath all non terminals from it


