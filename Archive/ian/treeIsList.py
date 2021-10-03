class Leaf(int):
    pass

class Tree(list):
    def append(self, item):
        assert type(item) in (Tree, Leaf)
        super().append(item)

class InfTree(list):
    def append(self, item):
        assert type(item) is InfTree
        super().append(item)

a = InfTree()
a.append(a)
print(a)

b = Tree()
b.append(Leaf(3))
b.append(b)
print(b)

d = Tree()
d.append(Leaf(4))
c = Tree()
c.append(d)
c.append(Leaf(5))
print(c)
