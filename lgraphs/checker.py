from lgraph import LGraph


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
print(d)

k = LGraph()
k.generate_from_grammar(['S->aA|b', 'A->aS|b'])
print(k)
s = "ab"
print(k.solve(s))
print(k.solve(s, arc_trace=True))
print(k.solve(s, vertex_trace=True))
print()
print(k.cycles())
print(k.arc_cycles())
print()

constructed = LGraph()
constructed.add_arc('1','1','a','[')
constructed.add_arc('1','2','b',']')
constructed.add_arc('2','2','b',']')
constructed.set_start('1')
constructed.set_finish('2')
print('Pre-constructed C-f L-graph:')
print(constructed)
s='aabb'
print(s[1:])
print(s[1:3]) #printed 1 and 2
print(constructed.solve(s))
