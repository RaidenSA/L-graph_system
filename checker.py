from L_graph_system.src.L_graph_system import LGraph
from L_graph_system.src.L_graph_system.lgraph import save_graph, load_graph
import unittest


c = LGraph()
# c.add_vertex('a')
# .add_vertex('b')
c.add_arc('a', 'a', 'a', '(')
c.add_arc('a', 'b', 'b', ')')
c.add_arc('b', 'b', 'b', ')')
c.add_arc('b', 'c', 'c')
# c.remove_arc('4')
# c.remove_vertex('b')
# print(c)

d = LGraph()
d.generate_from_grammar(['P->S@', 'S->aSb|dA', 'A->dA|e'])
#print(d)

k = LGraph()
k.generate_from_grammar(['S->aA|b', 'A->aS|b'])
#print(k)
s = "ab"
#print(k.solve(s))
#print(k.solve(s, arc_trace=True))
#print(k.solve(s, vertex_trace=True))
#print()
#print(k.cycles())
#print(k.arc_cycles())
#print()

constructed = LGraph()
constructed.add_arc('0','1','=','')
constructed.add_arc('1','1','a','[')
constructed.add_arc('1','2','b',']')
constructed.add_arc('2','2','b',']')
constructed.set_start('0')
constructed.set_finish('2')
#print('Pre-constructed C-f L-graph:')
#print(constructed)
s ="ab"
#print(constructed.next_vertexes('0', set()))
#print(constructed.solve(s))
#print(constructed.cycles())
#print(constructed.core(0,2))

constructed2 = LGraph()
constructed2.add_arc('1','1','a','[')
constructed2.add_arc('1','2','b','(]')
constructed2.add_arc('2','2','b','(]')
constructed2.add_arc('2','3','c',')')
constructed2.add_arc('3','3','c',')')
constructed2.set_start('1')
constructed2.set_finish('3')
#print('Pre-constructed C-d L-graph:')
#print(constructed2)
s ="abc"
#print(constructed2.solve(s))

multiply6 = LGraph()
multiply6.add_arc('1','1','I','[1')  # 1
multiply6.add_arc('1','2','x','')  # 2
multiply6.add_arc('2','2','I','[2')  # 3
multiply6.add_arc('2','3','=','')  # 4
multiply6.add_arc('3','4','','(1')  # 5
multiply6.add_arc('4','4','I','(0]2')  # 6
multiply6.add_arc('4','5','',']1')  # 7
multiply6.add_arc('5','5','','[2)0')  # 8
multiply6.add_arc('5','3','',')1')  # 9
multiply6.add_arc('3','6','','')  # 10
multiply6.add_arc('6','6','',']2')  # 11
multiply6.set_start('1')
multiply6.set_finish('6')
#print(multiply6.next_vertexes('1',set()))
multiply6.remove_arc('5')
#print(multiply6.dead_ends())
#print(multiply6.unattainable())
s='IIxII=IIII'
#print('Strange multiply:')
#print(multiply6.solve(s))
#print(['1'] in [['1'],['2']])
#print(multiply6.cycles())
#print(multiply6.core(0,1))

for_reduction = LGraph()
for_reduction.add_arc('0','1','a','(')
#for_reduction.add_arc('1','1','a','')
for_reduction.add_arc('1','2','',')')
#for_reduction.add_arc('2','3','a','')
print(for_reduction)
save_graph(for_reduction,"tmp")
print("3")
ddd =load_graph("tmp")
print(ddd)
#print(for_reduction)
#for_reduction.reduction()
#print(for_reduction)

#f = LGraph()
#f.generate_from_grammar(['S->Ab', 'A->aA|e'])
#print(f)
#f.reduction()
#print(f)
#print(f.type_def())
#print(f.is_context_free())