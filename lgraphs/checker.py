from lgraph import LGraph
import re

c = LGraph()
#c.add_vertex('a')
#.add_vertex('b')
c.add_arc('a','a', 'a','(')
c.add_arc('a','b', 'b',')')
c.add_arc('b','b','b',')')
c.add_arc('b','c','c')
#c.remove_arc('4')
#c.remove_vertex('b')
#print(c)

d = LGraph()
d.generate_from_grammar(['P->S@','S->aSb|dA','A->dA|e'])
print(d)

k = LGraph()
k.generate_from_grammar(['S->aA|b','A->aA|a'])
#k.set_start("S_beg")
#k.set_finish("S_end")
#k.set_finish("A_end")
print(k)
print(k.solve("aaaa"))
#z ="d"
#print(len(z[1:]))




