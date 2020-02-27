
class Order:

    def __init__(self, con):
        self.con = con

    def mert(self, l):
        m = Ordert(con=self.con, l=l)
        return m



class Ordert:
    def __init__(self, con, l):
        self.con = con
        self.l = l
        self.lister = [1, 4, 6]

    def listlist(self, jert):
        return self.lister.append(jert)

    def __call__(self):
        return self.lister

    def order_b(self, id):
        self.lister.append(id)
        return self.lister


p = Order(45)
# for n in p.mert():
    # print(n)
print(p.mert(56)())
print(p.mert(56).order_b(657567))
# print(p.mert(1))
# print(type(p.mert().con))
# for n in Order(45).mert():

# print(p.mert())


