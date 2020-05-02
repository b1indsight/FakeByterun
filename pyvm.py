class Interpreter:

    def __init__(self):
        self.pc = 0
        self.stack = []
        self.enviornment = {}

    def NOP(self):
        pass

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

    def PRINT_NOT_POP(self):
        print(self.stack[-1])

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

    def jump(self, jump):
        self.pc = jump

    def JUMP(self, jump):
        self.jump(jump)

    def POP_JUMP_IF_FALSE(self, jump):
        val = self.stack.pop()
        if val:
            self.stack.append(val)
            return
        else:
            self.jump(jump)
            

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]
        while not (self.pc == -1 or self.pc >= len(instructions)):
            instruction, argument = instructions[self.pc]
            self.pc += 1
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument:
                bytecode_method(argument)
            else:
                bytecode_method()
            