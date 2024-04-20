def foo(x):
    if x == 0: return False
    if x == 1: return True
    if x == 2: return False

x = False
x += foo(1)
print(x)
x += foo(0)
print(x)