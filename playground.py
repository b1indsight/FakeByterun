import dis

test = "def x(y):   return y + 1"

code = compile(test, '<string>', "exec")

print("code is", code.co_code)
for x in code.co_code:
    print(dis.opname[x])