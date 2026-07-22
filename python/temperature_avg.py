# 温度采集 - 循环版本
# 练习目标：用 for 循环 + 累加器模式采集5次温度并求平均

total = 0  # 累加器，先归零

for i in range(5):
    temp = float(input(f"请输入第{i+1}次温度: "))
    total += temp  # 每次把新温度加到 total 里

average = total / 5
print(f"5次平均温度: {average}")
