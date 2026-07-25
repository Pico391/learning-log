import random
x = random.randint(1,100)
z = 0
while True:
    y = float(input("猜猜我想的是什么"))
    if x == y:
        print("you are right")
        
    elif x > y :
        z += 1
        if z <= 5:
                 print("you need a bigger answer,the chance still have ",7-z,"times")
        elif z >= 5:
                 print("you need a bigger answer,the chance still have ",7-z,"time")
    elif x < y:
        z += 1
        if z <= 5:
            print("you need a smaller answer,the chance still have ",7-z,"times")
        if z >= 5:
            print("you need a smaller answer,the chance still have ",7-z,"time")
        if z == 7:
            print("you are loser,the answer is",x)
            break
        
    
