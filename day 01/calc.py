def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiplication(a,b):
    return a*b
def divide(a,b):
    return a/b
choice = input("opertion: +,-,*,/  ? ")
a= int(input("first number: "))
b= int(input("second number: "))
if choice == "+":
    answer = add(a,b)
    print(answer)
if choice == "-":
    answer = subtract(a,b)
    print(answer)
if choice == "*":
    answer = multiplication(a,b)
    print(answer)
if choice == "/":
    answer = divide(a,b)
    print(answer)
