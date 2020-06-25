import dis

test = """a = 1 
b = a + 1"""

code = compile(test, '<string>', "exec")

print("code is", code.co_code)
print(code.co_code[10])
dis.dis(code)
