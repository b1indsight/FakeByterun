''' try execute 
    a = 10
    while a:
        a = a - 1
        print a
'''
import dis
#import pyvm

what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),
                     ("STORE_NAME", 0),
                     ("LOAD_NAME", 0),
                     ("POP_JUMP_IF_FALSE", -1),
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_NOT_POP", None),
                     ("JUMP", 3),
                     ("NOP", None)],
    "numbers": [10, -1],
    "names": ["a"]}

def d(x):
    return x

def test(c):
    def e(x):
        return x + 1
    a = d(c)
    b = 1
    return a + b + e(1)

if __name__ == "__main__":
    #interpreter = pyvm.Interpreter()
    #interpreter.run_code(what_to_execute)
    #print(list(interpreter.LOAD_NAME.__code__.co_code))
    #print(dis.dis(interpreter.LOAD_NAME))
    print(dis.dis(test))
    tmp = {}
    tmp = dis.dis(test)
    for x in dis.get_instructions(test): 
        print(x)