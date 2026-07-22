#input string 

s = str(input("enter a sentence: "))
words = s.split()
new_words = []

for word in words:
    #SHIT I FORGOT
    new_words.append(word[0].upper()+word[1:-1].lower()+word[-1].upper()) 

result = " ".join(new_words)
#then print??