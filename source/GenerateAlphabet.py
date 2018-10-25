result = ""
for i in range(0, 127-32):
    result += "\"" + chr(i+32) + "\":" + str(i) + ", "
print(result)