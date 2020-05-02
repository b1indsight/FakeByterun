''' try execute 
    a = 10
    while a:
        a = a - 1
        print a
'''
import dis
import pyvm

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


if __name__ == "__main__":
    interpreter = pyvm.Interpreter()
    interpreter.run_code(what_to_execute)
    print(list(interpreter.LOAD_NAME.__code__.co_code))
    print(dis.dis(interpreter.LOAD_NAME))
    print(dis.opname[124])