import lib.maes

class Test:
    def __init__(self):
        self.val = 0

def testfunc(val):
    val.val=1

test = Test()

testfunc(test)
print(test.val)