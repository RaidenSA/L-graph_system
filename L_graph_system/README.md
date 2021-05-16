This is an universal l-graph system.
It shall be my pleasure if you use it in your projects.
# Contents

This project includes 3 main modules, each containing it's named class.
The main module is lgraph.py, which provides us with an access
to LGraph class and save and load operations.

## LGraph

The main class. To make a proper L-graph, you should make an object of it.

### Properties

___vertexes:{vertex_name:String :: vertex:Vertex}___

___arcs:{arc_key:String :: arc:Arc}___

___start_vertexes:set(vertex_name:String)___

___finish_vertexes:set(vertex_name)___

___brackets:((open:String,close:String),(open2:String, close2:String))___

### Methods

___add_arc(start_vertex:String, finish_vertex:String, label:String, bracket_label:String, key='':String)___
This method allows us to add a new arc to the graph with corresponding values. If one of the vertexes does not exist in the graph, 
it will create a new one.

___add_vertex(vertex_name:String)___ 
This method creates a new vertex in the graph

___remove(arc_name:String)___
This method removes selected arc from the graph and it's components

___remove(vertex_name:String)___
This method removes selected vertex __and__ all arcs it was bind to

___set_start(vertex_name:String)___
Adds the selected vertex to the starting vertexes

___set_finish(vertex_name:String)___
Adds the selected vertex to the finish vertexes 

___remove_start(arc_name:String)___
Removes the selected vertex from starting vertexes

___remove_finish(vertex_name:String)___
Removes the selected vertex from finish vertexes

___set_brackets(brackets:((),()))___
Allows to use another set of brackets. Must be special type.

___solve(string:String,vertex_path=False,arc_path=False)___
Returns True or False whether string belongs to the language of the L-graph, or not.
If vertex_vath is set to True, returns correct label path as list or empty list if string does not belog to the language.
Arc_path does the same thing with path of arcs instead of vertexes. 

___cycles():list(list(vertex_name:String))___
Searches for cylces in the graph. Returns a list of lists, each containing vertexes from the corresponding cycle.

___arc_cycles():list(list(arc_key:String))___
Does the same thing as ___cycles()___, but returns arcs.

___generate_from_grammar(in_grammar:list(grammar_rule:String))___
Must be used with empty L-graph. Builds L-graph which represents language, equivalent to the language of the grammar.

___type_def():String___
Returns 'regular', 'context-free' or 'recursively_enumerable' depending on L-graph class.

___is_regular():Boolean___
True if L-graph is regular

___is_context_free():Boolean___
True if L-graph is context-free

___core(paired_number, neutral_number):list(list(vertex_name:String))___
Returns list of successful paths with restricted number of cycles. 

___merge(another_graph:LGraph)___
Restructurises the graph to represent 2 L-graphs in 1.

___dead_ends():list(vertex_names:String)___
Returns a set of vertexes, from which no finish vertexes can be reached.

___unattainable():list(vertex_names:String)___
Returns a set of vertexes, which can not be reached from start  vertexes.

___remove_unusable()___
Removes all vertexes present in dead ends and unattainable sets.

___reduction()___
Restructurises L-graph to be more compact.

## Vertex

class of graph vertexes

### Properties
___name:String___

___out_arcs:set()___

___in_arcs:set()___

### Methods:

___rename(new_name:String)___

## Arc

class of graph arcs

### Properties

___key:String___

___label:String___

___brackets:String___

___start:Vertex___

___end:Vertex___

___next_arcs:set(String)___

### Methods:

___remove_arc()___

___set_label(new_label:String)___

___set_brackets(new_brackets:String)___