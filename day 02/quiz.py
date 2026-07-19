def ask_que(Question, correct_ans):
    given_ans = input(Question)
    if given_ans.lower() == correct_ans.lower():
        print("bitch you got that right !!!! ")
        return 1
    else :
        print("just do moonwalk lil bro cuz you got it wrong")
        return 0
Questions = [("What is 2+2 ","4"),("what is 2+3 ", "5"),("what is 3+3 ", "6"),("what is 4+3 ", "7"),("what is 5+ 3", "8")]
score = 0 
for question,answer in Questions:
    score += ask_que(question,answer)

print(f"My dear sir, you got {score} out of 5!!!! all thanks to claude , my god and my religion :)")
