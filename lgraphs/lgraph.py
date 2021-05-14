from lgraphs.vertex import Vertex
from lgraphs.arc import Arc
import re
import copy


class LGraph:
    def __init__(self, brackets=None):
        if brackets is None:
            brackets = (('(', ')'), ('[', ']'))
        self.__vertexes = {}
        self.__arcs = {}
        self.__brackets = brackets
        # we need to create a scheme of program structure.
        # we need to have a special form for L-graph core
        # basing on core, we can check for consistency of l-graph
        # this is a task of checking for empty language
        # we may check for determinative l-graph, search for algorithm is needed
        # we need concatenation
        # we may also try SAGE

        self.__start_vertexes = []
        self.__finish_vertexes = []

    def add_arc(self, start_vertex, end_vertex, label='', bracket_trace='', key=None):
        flag = 0 if bracket_trace == '' else 1
        for b in self.__brackets:
            for bb in b:
                if bb in bracket_trace:
                    flag = 0
                    break
        if flag:
            raise NameError('Incorrect brackets')
        if key:
            if key in self.__arcs:
                raise NameError(f'Arc with key "{key}" already exists')
        else:
            key = f'{len(self.__arcs) + 1}'  # need some ajustments here, cause 2 then none will make an error
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

        self.__arcs[key] = Arc(key, self.__vertexes[start_vertex], self.__vertexes[end_vertex], label, bracket_trace)

    def add_vertex(self, name=None):
        if name:
            if name in self.__vertexes.keys():
                raise NameError(f'Vertex with name "{name}" already exists.')
            else:
                new_name = name
        else:
            new_name = f'{len(self.__vertexes) + 1}'
        self.__vertexes[new_name] = Vertex(new_name)

    def remove_arc(self, key):
        self.__arcs[key].remove_arc()
        self.__arcs.pop(key)

    def remove_vertex(self, name):
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
        res += "Start_Vertexes: \n"
        for b in self.__start_vertexes:
            res += b + '\n'
        res += "Finish_Vertexes: \n"
        for b in self.__finish_vertexes:
            res += b + '\n'
        return res

    def set_start(self, name):
        if name in self.__vertexes.keys():
            self.__start_vertexes.append(name)
        else:
            raise NameError(f'No vertex with name "{name}"')

    def set_finish(self, name):
        if name in self.__vertexes.keys():
            self.__finish_vertexes.append(name)
        else:
            raise NameError(f'No vertex with name "{name}"')

    def remove_start(self, name):
        if name in self.__start_vertexes:
            self.__start_vertexes.remove(name)
        else:
            raise NameError(f'No start vertex with name "{name}"')

    def remove_finish(self, name):
        if name in self.__finish_vertexes:
            self.__finish_vertexes.remove(name)
        else:
            raise NameError(f'No finish vertex with name "{name}"')

    def solve(self, in_string, arc_trace=False, vertex_trace=False):
        current_vertex_name = self.__start_vertexes[0]
        # current_vertex = self.__vertexes[current_vertex_name]
        brackets_path = [[], []]
        path, arc_path = self.__solve_one(in_string, current_vertex_name, brackets_path)
        if arc_trace:
            return path
        if vertex_trace:
            return arc_path
        if len(path) == 0:
            return False
        else:
            return True

    def __solve_one(self, in_string, vertex_key, old_brackets_path):
        if vertex_key in self.__finish_vertexes and len(in_string) == 0 and len(old_brackets_path[0]) == 0 and len(old_brackets_path[1]) == 0:
            return [vertex_key], []
        # brackets_path[0] for first type of brackets
        # brackets_path[1] for the second
        current_vertex = self.__vertexes[vertex_key]
        path = []
        arc_trace = []
        for cur in current_vertex.out_arcs:
            # we check conditions whether an arc is suitable for us
            flag_to_check = False

            brackets_path = copy.deepcopy(old_brackets_path)
            # copy is needed to copy nested list correctly
            new_string = ""
            if len(in_string) == 0:
                if self.__arcs[cur].label == '':
                    flag_to_check = True
                    new_string = in_string
                else:
                    continue
            else:
                if self.__arcs[cur].label == in_string[0] or self.__arcs[cur].label == '':
                    flag_to_check = True
                    if self.__arcs[cur].label == in_string[0]:
                        new_string = in_string[1:]
                    else:
                        new_string = in_string
            # we checked all conditions when the ark may be suitable for us to go further.
            if flag_to_check:
                new_current_vertex = self.__arcs[cur].end
                current_brackets = self.__arcs[cur].brackets
                first_brackets = ''
                second_brackets = ''
                if len(current_brackets) > 0:
                    # first open brackets
                    res = current_brackets.find(self.__brackets[0][0])
                    if res != -1:
                        if len(current_brackets) > res:
                            if current_brackets[res+1:res+2].isnumeric():
                                first_brackets = current_brackets[res:res+2]
                            else:
                                first_brackets = current_brackets[res]
                        else:
                            first_brackets = current_brackets[res]
                    elif current_brackets.find(self.__brackets[0][1]) != -1:
                        # first close brackets
                        res = current_brackets.find(self.__brackets[0][1])
                        if res != -1:
                            if len(current_brackets) > res:
                                if current_brackets[res + 1:res + 2].isnumeric():
                                    first_brackets = current_brackets[res:res + 2]
                                else:
                                    first_brackets = current_brackets[res]
                            else:
                                first_brackets = current_brackets[res]
                    else:
                        first_brackets = ''
                    # second open brackets
                    res = current_brackets.find(self.__brackets[1][0])
                    if res != -1:
                        if len(current_brackets) > res:
                            if current_brackets[res + 1:res + 2].isnumeric():
                                second_brackets = current_brackets[res:res + 2]
                            else:
                                second_brackets = current_brackets[res]
                        else:
                            second_brackets = current_brackets[res]
                    elif current_brackets.find(self.__brackets[1][1]) != -1:
                        # second close brackets
                        res = current_brackets.find(self.__brackets[1][1])
                        if res != -1:
                            if len(current_brackets) > res:
                                if current_brackets[res + 1:res + 2].isnumeric():
                                    second_brackets = current_brackets[res:res + 2]
                                else:
                                    second_brackets = current_brackets[res]
                            else:
                                second_brackets = current_brackets[res]
                    else:
                        second_brackets = ''
                    # The following parts helps track the resolving process
                    # print()
                    # print(cur)
                    # print(current_brackets)
                    # print(brackets_path)
                    # print('first brackets: ', first_brackets)
                    # print('second brackets: ', second_brackets)

                # if bracket is opening we add it
                # should revise the whole bracket check
                if self.__brackets[0][0] in first_brackets:
                    brackets_path[0].append(first_brackets)

                elif self.__brackets[0][1] in first_brackets:
                    if len(brackets_path[0]) > 0:
                        if self.__brackets[0][0] in brackets_path[0][len(brackets_path[0])-1]:
                            # brackets_path[0][len(brackets_path[0])-1] means the last added bracket
                            # if bracket is closing we try to close it
                            if brackets_path[0][len(brackets_path[0])-1][1:] == first_brackets[1:]:
                                brackets_path[0].pop()
                                # some kind of index check
                            else:
                                continue
                            # check for index is made after brackets are categorised
                        else:
                            continue
                    else:
                        continue
                # print(cur)
                # the same for the second type of the brackets
                if self.__brackets[1][0] in second_brackets:
                    brackets_path[1].append(second_brackets)
                elif self.__brackets[1][1] in second_brackets:
                    if len(brackets_path[1]) > 0:
                        if self.__brackets[1][0] in brackets_path[1][len(brackets_path[1])-1]:
                            if brackets_path[1][len(brackets_path[1]) - 1][1:] == second_brackets[1:]:
                                brackets_path[1].pop()
                                # some kind of index check
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                new_path, new_arc_trace = self.__solve_one(new_string, new_current_vertex.name, brackets_path)
                # print(new_path)
                if len(new_path) > 0:
                    path = [vertex_key]
                    arc_trace = [cur]
                    path.extend(new_path)
                    arc_trace.extend(new_arc_trace)
                    break
                # here we combine our path, and if it is not empty, it's good. if it is empty -> no path
        return path, arc_trace

    def cycles(self):  # cycles without duplicates
        cycle_res = self.__cycle_detection()
        res = [list(i) for i in {*[tuple(sorted(i)) for i in cycle_res]}]
        return res

    def __cycle_detection(self):  # all cycles
        cycles = []
        for cur in self.__vertexes.keys():
            path = []
            self.__cycle_depth_search(cur, [], path)
            if len(path) > 0:
                cycles.extend(path)
        res = cycles
        return res

    def __cycle_depth_search(self, vertex_name, path, accumulator):
        current_vertex = self.__vertexes[vertex_name]
        new_path = path.copy()
        if len(path) > 0:
            if vertex_name == path[0]:
                return new_path
        if vertex_name in path:
            return []
        new_path.append(vertex_name)
        for cur in current_vertex.out_arcs:
            only_new_path = self.__cycle_depth_search(self.__arcs[cur].end.name, new_path, accumulator)
            if len(only_new_path) > 0:
                accumulator.append(only_new_path)
        return []

    def __arc_cycle_detection(self):  # returns list of all lists of cycling arcs
        cycles = self.__cycle_detection()
        arc_cy = []
        for cy in cycles:
            cur_cycle = []
            for ind in range(len(cy)):
                # print(self.__vertexes[cy[ind]].in_arcs)
                new_arc = self.__vertexes[cy[ind]].in_arcs.intersection(self.__vertexes[cy[ind-1]].out_arcs)
                # print(new_arc)
                for ar in new_arc:
                    cur_cycle.append(ar)
                # print(cur_cycle)
            arc_cy.append(cur_cycle)
        return arc_cy

    def arc_cycles(self):
        cycle = self.__arc_cycle_detection()
        res = [list(i) for i in {*[tuple(sorted(i)) for i in cycle]}]
        return res

    def generate_from_grammar(self, in_grammar):
        # inGrammar must be a list of string rules. I concider makig a special class for this purposes
        # but it may be so small, that it seems to me that we can handle it right here
        bracket_counter = 1
        finish_vertex_flag = True
        for inString in in_grammar:
            # inString = "P->S@"
            res = re.search("->", inString)
            if res is None:
                raise TypeError('Incorrect grammar')
            left_part = inString[:res.start()]  # label of the rule
            right_part = inString[res.end():]  # what we need to do
            vertex_counter = 1
            current_vertex = f'{left_part}_beg'
            end_vertex = f'{left_part}_end'
            begin_vertex = current_vertex

            for position, symbol in enumerate(right_part):
                # here we need to add an edge, if it is upper - than make 2 separate edjes and go forward
                if symbol == '|':
                    current_vertex = f'{left_part}_beg'
                    continue  # does not work, need to count symbol position
                if symbol.isupper():
                    new_vertex = f'{symbol}_beg'
                    self.add_arc(current_vertex, new_vertex, '', f'({bracket_counter}')
                    current_vertex = f'{symbol}_end'
                    if right_part.endswith(symbol):
                        new_vertex = end_vertex
                    elif right_part[position+1] == '|':
                        new_vertex = end_vertex
                    else:
                        new_vertex = f'{left_part}{vertex_counter}'
                        vertex_counter += 1
                    self.add_arc(current_vertex, new_vertex, '', f'){bracket_counter}')
                    current_vertex = new_vertex
                    bracket_counter += 1
                else:
                    if right_part.endswith(symbol):
                        new_vertex = end_vertex
                    elif right_part[position+1] == '|':
                        new_vertex = end_vertex
                    else:
                        new_vertex = f'{left_part}{vertex_counter}'
                        vertex_counter += 1
                    self.add_arc(current_vertex, new_vertex, symbol, '')
                    current_vertex = new_vertex
            if finish_vertex_flag:
                finish_vertex_flag = False
                self.set_start(begin_vertex)
                self.set_finish(end_vertex)

    def set_brackets(self, brackets):
        if isinstance(tuple, brackets):
            for brace in brackets:
                if isinstance(tuple, brace):
                    self.__brackets = brackets
                    return
        raise TypeError('Incorrect brackets')

    def core(self, paired, neutral):
        cycles = self.arc_cycles()
        # define cycle type
        paired_cycles = set()
        neutral_cycles = set()
        for cycle in cycles:
            flag = 1
            for cur_arc in cycle:
                if self.__arcs[cur_arc].brackets != '':
                    for item in cycle:
                        paired_cycles.add(item)
                    flag = 0
                    break
            if flag:
                for item in cycle:
                    neutral_cycles.add(item)

        neutral_arcs = dict.fromkeys(neutral_cycles, neutral)
        paired_arcs = dict.fromkeys(paired_cycles, paired)
        begin_vertex = self.__start_vertexes[0]
        path = self.__core_depth(begin_vertex, paired_arcs, neutral_arcs, [[], []], [])
        return path

    def __core_depth(self, vertex_key, paired, neutral, old_brackets_path, path_res):
        if vertex_key in self.__finish_vertexes and len(old_brackets_path[0]) == 0 and len(old_brackets_path[1]) == 0:
            new_path_res = copy.deepcopy(path_res)
            new_path_res.append(vertex_key)
            return new_path_res
        current_vertex = self.__vertexes[vertex_key]
        path = []
        for cur in current_vertex.out_arcs:
            # we check conditions whether an arc is suitable for us
            new_path_res = copy.deepcopy(path_res)
            flag_to_check = False
            brackets_path = copy.deepcopy(old_brackets_path)
            new_neutral = copy.copy(neutral)
            new_paired = copy.copy(paired)
            if cur in new_neutral.keys():
                if new_neutral[cur] > 0:
                    flag_to_check = True
                    new_neutral[cur] -= 1
            elif cur in new_paired.keys():
                if new_paired[cur] > 0:
                    flag_to_check = True
                    new_paired[cur] -= 1
            else:
                flag_to_check = True
            # copy is needed to copy nested list correctly
            # we checked all conditions when the ark may be suitable for us to go further.
            if flag_to_check:
                new_current_vertex = self.__arcs[cur].end
                current_brackets = self.__arcs[cur].brackets
                first_brackets = ''
                second_brackets = ''
                if len(current_brackets) > 0:
                    # first open brackets
                    res = current_brackets.find(self.__brackets[0][0])
                    if res != -1:
                        if len(current_brackets) > res:
                            if current_brackets[res + 1:res + 2].isnumeric():
                                first_brackets = current_brackets[res:res + 2]
                            else:
                                first_brackets = current_brackets[res]
                        else:
                            first_brackets = current_brackets[res]
                    elif current_brackets.find(self.__brackets[0][1]) != -1:
                        # first close brackets
                        res = current_brackets.find(self.__brackets[0][1])
                        if res != -1:
                            if len(current_brackets) > res:
                                if current_brackets[res + 1:res + 2].isnumeric():
                                    first_brackets = current_brackets[res:res + 2]
                                else:
                                    first_brackets = current_brackets[res]
                            else:
                                first_brackets = current_brackets[res]
                    else:
                        first_brackets = ''
                    # second open brackets
                    res = current_brackets.find(self.__brackets[1][0])
                    if res != -1:
                        if len(current_brackets) > res:
                            if current_brackets[res + 1:res + 2].isnumeric():
                                second_brackets = current_brackets[res:res + 2]
                            else:
                                second_brackets = current_brackets[res]
                        else:
                            second_brackets = current_brackets[res]
                    elif current_brackets.find(self.__brackets[1][1]) != -1:
                        # second close brackets
                        res = current_brackets.find(self.__brackets[1][1])
                        if res != -1:
                            if len(current_brackets) > res:
                                if current_brackets[res + 1:res + 2].isnumeric():
                                    second_brackets = current_brackets[res:res + 2]
                                else:
                                    second_brackets = current_brackets[res]
                            else:
                                second_brackets = current_brackets[res]
                    else:
                        second_brackets = ''
                if self.__brackets[0][0] in first_brackets:
                    brackets_path[0].append(first_brackets)

                elif self.__brackets[0][1] in first_brackets:
                    if len(brackets_path[0]) > 0:
                        if self.__brackets[0][0] in brackets_path[0][len(brackets_path[0]) - 1]:
                            # brackets_path[0][len(brackets_path[0])-1] means the last added bracket
                            # if bracket is closing we try to close it
                            if brackets_path[0][len(brackets_path[0]) - 1][1:] == first_brackets[1:]:
                                brackets_path[0].pop()
                                # some kind of index check
                            else:
                                continue
                            # check for index is made after brackets are categorised
                        else:
                            continue
                    else:
                        continue
                # the same for the second type of the brackets
                if self.__brackets[1][0] in second_brackets:
                    brackets_path[1].append(second_brackets)
                elif self.__brackets[1][1] in second_brackets:
                    if len(brackets_path[1]) > 0:
                        if self.__brackets[1][0] in brackets_path[1][len(brackets_path[1]) - 1]:
                            if brackets_path[1][len(brackets_path[1]) - 1][1:] == second_brackets[1:]:
                                brackets_path[1].pop()
                                # some kind of index check
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue

                new_path_res.append(vertex_key)
                new_path = self.__core_depth(new_current_vertex.name, new_paired, new_neutral, brackets_path, new_path_res)
                # trying to get consistent flat list regardless of recursion direction
                if len(new_path) > 0:
                    if len(path) > 0:
                        if isinstance(path[0], list):
                            path.append(new_path)
                        else:
                            if isinstance(new_path[0], list):
                                path_x = path
                                path = new_path
                                path.append(path_x)
                            else:
                                path_x = [path]
                                path = path_x
                                path.append(new_path)
                    else:
                        path.extend(new_path)
        return path
