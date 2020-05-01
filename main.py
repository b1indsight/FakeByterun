# try execute 7 + 5 + 5
import dis

what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),  # the first number
                     ("LOAD_VALUE", 1),  # the second number
                     ("ADD_TWO_VALUES", None),
                     ("LOAD_VALUE", 1),
                     ("STORE_NAME", 0),
                     ("LOAD_NAME", 0),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5],
    "names": ["a", "b"]}

class Interpreter:
    def __init__(self):
        self.stack = []
        self.enviornment = {}

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def LOAD_NAME(self, name):
        self.stack.append(self.enviornment.get(name))
    
    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.enviornment[name] = val

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def parse_argument(self, instruction, argument, what_to_execute):
        """ Understand what the argument to each instruction means."""
        numbers = ["LOAD_VALUE"]
        names = ["LOAD_NAME", "STORE_NAME"]

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument:
                bytecode_method(argument)
            else:
                bytecode_method()

if __name__ == "__main__":
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
    print(list(interpreter.LOAD_NAME.__code__.co_code))
    print(dis.dis(interpreter.LOAD_NAME))
    print(dis.opname[124])