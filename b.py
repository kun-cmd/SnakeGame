b = 100
def a():
    global b
    b = 10
def c():
    print(b)
a()
c()