__author__ = 'Administrator'


g = lambda x, y: x*y
print(g(3, 4) )

g = lambda x, y=0, z=0: x+y+z
print(g(3, 4) )


print( (lambda x, y=0, z=0: x+y+z)(3, 4, 5) )