x = float(input("请输入您的分数 "))
if x >= 90:
    print("Good")
elif 90 > x >= 80:
    print("batter")
elif 79 >= x >= 60:
    print("pass")
elif 0 >= x > 60:
    print("no pass")
else:
    print("请输入数字")
