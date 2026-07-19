number = int(input("number?"))
if number > 0:
    print("positive number")
elif number == 0 :
    print("number is 0")
elif number<0:
    print("negative thingy")
else :
    print("what did you put inside hm?")
i = number%2
if i==0:
    print("even")
else:
    print("badshit crazy odd")