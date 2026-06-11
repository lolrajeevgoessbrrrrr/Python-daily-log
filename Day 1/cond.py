age = 19

if age >= 18:
    print("adult")
elif age >= 13:
    print("teenager")
else:
    print("child")

# Combining conditions
score = 59
has_studied = True

if score >= 90:
    print("excellent")
elif score >= 60 and has_studied:
    print("good — keep going")
elif score < 60 or not has_studied:
    print("needs work")
else:
    print("average")

# Checking membership in a list
animes = ["One Piece", "Tokyo Ghoul", "Attack on Titan"]

user_input = input("Name an anime: ")

if user_input in animes:
    print("good taste")
else:
    print("not on the list")