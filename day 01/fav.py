animes = ["One Piece", "Tokyo Ghoul", "Attack on Titan", "Rezero", "Classroom of the elite"]
food = ["Roti", "Dal", "eggs", "soyabean", "oats"]
musics = ["Montagem Supersonic", "dia delecia", "salvatore", "i will survive", "twin tribes- monolith"]
keywords = ["Self control", "discipline", "efficient","adaptable", "No attachements"]
names = ["rei","ram", "rem", "rajeev", "rin"]

print(animes[0], animes[4])
print(food[0], food[4])
print(musics[0], musics[4])
print(keywords[0], keywords[4])
print(names[0], names[4])
 
print(len(animes))
print(len(food))
print(len(keywords))
print(len(musics))
print(len(names))

animes.append("Evangelion")
food.append("chicken")
musics.append("fenomenal")
keywords.append("read books")
names.append("Reinhard")
 
print(animes)
print(food)
print(musics)
print(keywords)
print(names)

countdown = len(animes) 
for i in range(countdown):
    temp_anime = animes[i]
    print(f"{i +1 }. {temp_anime}")

count = 5 
while count != 0:
    print(count)
    count -= 1

print("lets go!!!!! claude my lovee")
