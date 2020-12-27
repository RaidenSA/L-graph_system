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
print(c)
