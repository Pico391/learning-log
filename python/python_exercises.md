# Python 练习册 v2

> 配合小甲鱼《零基础学Python》课程使用  
> 题目全新，不重复 QClaw 版本  
> 重点强化：第3章运算符易错点、第5-6章循环与break/continue  
> 结合机械电子工程实际场景

---

## 使用说明

- 先自己想，别急着看答案（答案在每章最后，可折叠）
- 敲代码运行，报错就读错误信息，那是最好的老师
- 带 [易错] 标记的题，是你之前踩过坑的地方，重点做
- 带专业] 标记的题，和机械电子相关，提前感受
- 每题做完在前面打 [x]

---

## 第1章：print 与基础

### 知识点

- `print()` 输出，`\n` 换行，`end=""` 不换行
- 注释用 `#`
- 字符串可用单引号或双引号

### 练习 1-1：开机欢迎语

写一段代码，运行后输出：

```
============================
  实习备战 Day 1 - 开始！
  目标：6个月后去深圳
============================
```

### 练习 1-2：不换行输出

用 `print()` 的 `end` 参数，让三个 print 输出在同一行：

```
机械 电子 工程
```

### 练习 1-3：打印分割线

写一个程序，打印 20 个 `-` 组成的分割线（提示：`"-" * 20`）。

---

## 第2章：变量与数据类型

### 知识点

- 变量赋值：`name = "pico"`
- 类型：`int` `float` `str` `bool`
- `type()` 查类型，`int()` `float()` `str()` 类型转换
- input() 返回的永远是字符串

### 练习 2-1：专业信息卡

创建变量存储你的信息，然后打印：

```python
name = "pico"
school = "天水师范大学"
major = "机械电子工程"
goal = "深圳实习"
# 用 print 和 f-string 打印一张信息卡
```

### [易错] 练习 2-2：input 的陷阱

下面这段代码，用户输入 18，打印出来的是什么类型？怎么修？

```python
age = input("输入年龄：")
# 用户输入 18
print(age + 1)  # 这里会报错吗？为什么？
```

### 练习 2-3：类型转换

用户输入一个温度（摄氏度），程序转换成华氏度并打印。  
公式：华氏度 = 摄氏度 * 1.8 + 32

### [专业] 练习 2-4：齿轮转速

已知电机转速 3000 rpm，齿轮减速比 1:30，输出轴转速是多少？  
创建变量计算并打印（结果应该是 100 rpm）。

---

## 第3章：运算符（重点章节）

### 知识点

- 算术：`+ - * / // % **`
- 比较：`== != > < >= <=`（注意 `==` 是比较，`=` 是赋值）
- 逻辑：`and or not`

### [易错] 练习 3-1：== 还是 = ？

判断下面每行代码对不对，对的写运行结果，错的说明为什么：

```python
# 第1行
x = 10
print(x == 10)

# 第2行
y = 5
if y = 5:       # 这行对吗？
    print("y是5")

# 第3行
a = 3
b = 3
print(a == b)

# 第4行
score = 85
print(score = 90)  # 这行对吗？
```

### 练习 3-2：取余运算

- 100 除以 7 的余数是多少？用代码算
- 判断一个数是奇数还是偶数（提示：`n % 2`）

### [专业] 练习 3-3：传感器阈值判断

温度传感器读数 `temp = 28.5`，设定阈值：

- 低于 25：正常
- 25-35：偏高
- 35 以上：报警

用比较运算符和逻辑运算符写判断代码。

### 练习 3-4：布尔表达式练习

不用 if，直接打印下面表达式的值（True 或 False）：

```python
age = 18
has_id = True

print(age >= 18)              # ?
print(age >= 18 and has_id)   # ?
print(age < 18 or has_id)     # ?
print(not has_id)             # ?
```

先猜结果，再运行验证。

### [易错] 练习 3-5：短路逻辑

下面代码打印什么？先想再运行：

```python
print(0 and 5)    # ?
print(3 and 5)    # ?
print(0 or 5)     # ?
print(3 or 5)     # ?
```



---

## 第4章：条件判断

### 知识点

```python
if 条件:
    执行
elif 条件2:
    执行
else:
    执行
```

注意冒号 `:` 不能少，缩进必须一致

### 练习 4-1：成绩等级（新版本）

输入成绩，输出等级和评语：

- 90+：A 优秀
- 80-89：B 良好
- 60-79：C 及格
- 60以下：D 需努力

### [专业] 练习 4-2：电机控制逻辑

根据用户输入的命令，控制电机：

- 输入 "start"：打印"电机启动"
- 输入 "stop"：打印"电机停止"
- 输入 "reverse"：打印"电机反转"
- 其他：打印"无效命令"

### 练习 4-3：BMI 计算

输入身高体重，计算 BMI（体重/身高^2），输出体型：

- <18.5 偏瘦
- 18.5-24 正常
- 24-28 偏胖
-

### [易错] 练习 4-4：嵌套判断陷阱

下面代码有 bug，运行结果不对，找出来并修复：

```python
score = 75
if score >= 60:
    print("及格")
    if score >= 90:
        print("优秀")
else:
    print("不及格")
    if score >= 80:    # 这行逻辑有问题吗？
        print("良好")
```

### 练习 4-5：闰年判断（进阶）

输入年份判断闰年。规则：能被4整除且不能被100整除，或能被400整除。  
额外要求：加上输入验证，年份必须是正整数，否则提示"请输入有效年份"。

---

## 第5章：循环

### 知识点

```python
while 条件:       # 条件为True就一直执行
    循环体

for 变量 in range(开始, 结束, 步长):
    循环体
```

### 练习 5-1：倒计时

用 while 循环打印 10 到 1 的倒计时，最后打印"发射！"。

### 练习 5-2：累加（新版本）

用 for 循环计算 1 到 50 所有奇数的和。  
（提示：`range(1, 51, 2)`）

### [易错] 练习 5-3：死循环陷阱

下面代码会无限循环，为什么？怎么修？

```python
i = 0
while i < 10:
    print(i)
# 缺了什么？
```

### [易错] 练习 5-4：循环变量作用域

下面代码打印什么？先想再运行：

```python
for i in range(3):
    for j in range(3):
        print(f"i={i}, j={j}")
```

问题：内层循环每次结束时，j 的值是多少？i 什么时候变？

### [专业] 练习 5-5：传感器数据平均

模拟采集 5 次温度数据（用 input 输入），计算平均值并打印。  
（提示：需要一个变量累加，最后除以 5）

### 练习 5-6：乘法表（新格式）

打印一个"左下三角"乘法表：

```
1
2 4
3 6 9
4 8 12 16
...
9 18 27 36 45 54 63 72 81
```

### 练习 5-7：猜数字加强版

系统随机生成 1-100 的数，用户猜，提示大小，猜对为止。  
额外要求：限制最多猜 7 次，7 次没猜中就打印"失败了，答案是X"。

```python
import random
secret = random.randint(1, 100)
# 你的代码（用到 while + 计数器 + if）
```

---

## 第6章：break 和 continue（你正在学的重点）

### 知识点

- `break`：立刻跳出整个循环，不再执行
- `continue`：跳过本次剩余代码，直接进入下一轮循环
- 两者都可以用在 while 和 for 里

### [易错] 练习 6-1：break vs continue 对比

先猜每段代码打印什么，再运行验证：

```python
# 代码A：用 break
for i in range(1, 11):
    if i == 5:
        break
    print(i)
print("---")

# 代码B：用 continue
for i in range(1, 11):
    if i == 5:
        continue
    print(i)
print("---")
```

问题：A 和 B 分别打印到几？5 打印了吗？为什么不同？

### 练习 6-2：跳过3的倍数

打印 1 到 30，跳过所有 3 的倍数（3、6、9...），用 continue。

### 练习 6-3：找到就停

从 100 开始往上找，找到第一个能被 7 和 9 同时整除的数，打印出来并退出循环。  
（答案应该是 126）

### 练习 6-4：密码锁

预设密码 "python123"：

- 用户最多输入 3 次密码
- 输对了立刻打印"解锁成功"并退出（用 break）
- 输错了继续，3 次都用完打印"账户锁定"

```python
password = "python123"
for i in range(3):
    user_input = input("输入密码：")
    # 你的代码
```

### [专业] 练习 6-5：温度监控

模拟温度持续监控：用 while True 循环，每次让用户输入温度：

- 温度 >= 50：打印"过热警告！强制停机"，用 break 退出
- 温度 < 50：打印"温度正常，继续监控"
- 输入 "q"：正常退出监控

### 练习 6-6：找出第一个质数

用循环从 50 开始往后找，找到第一个质数就打印并退出。  
（提示：需要嵌套循环，内层判断是否质数，外层找到就 break）

### [易错] 练习 6-7：continue 的坑

下面代码想跳过偶数只打印奇数，但结果是死循环，为什么？怎么修？

```python
i = 0
while i < 10:
    if i % 2 == 0:
        continue
    print(i)
    i += 1
```

### 练习 6-8：简易菜单系统

写一个循环菜单程序：

```
===== 菜单 =====
1. 开始
2. 设置
3. 帮助
4. 退出
===============
```

- 输入 1/2/3 打印对应内容
- 输入 4 用 break 退出
- 输入其他提示"无效选项"并继续循环

---

## 第7章：列表（预习）

### 知识点

```python
lst = [1, 2, 3]
lst.append(4)      # 尾部添加
lst.insert(0, 0)   # 指定位置插入
lst.remove(2)      # 删除指定值
lst[0]             # 按索引取值（从0开始）
len(lst)           # 长度
lst[-1]            # 最后一个
```

### [专业] 练习 7-1：传感器数据列表

创建一个列表存 7 天的温度数据，然后：

- 打印最高温、最低温、平均温
- 把超过 35 度的找出来打印"高温预警"

### 练习 7-2：购物清单

写一个循环程序管理购物清单：

- 输入 "add 物品名"：添加到列表
- 输入 "del 物品名"：从列表删除
- 输入 "show"：打印所有物品
- 输入 "quit"：退出

---

## 第8章：元组与字符串（预习）

### 练习 8-1：坐标点

用元组存储三个坐标点，遍历打印每个点的 x 和 y。

### 练习 8-2：字符串反转

用户输入一个字符串，不用 `[::-1]`，用循环把它反转输出。  
（比如输入 "hello"，输出 "olleh"）

---

## 第9章：字典（预习）

### [专业] 练习 9-1：零件库存

用字典管理零件库存：

```python
inventory = {
    "螺丝": 100,
    "螺母": 80,
    "轴承": 25,
    "电机": 10
}
```

功能：查询零件、补充库存、库存不足时预警（<20 打印"需要采购"）。

---

## 第10章：函数（预习）

### 练习 10-1：温度转换函数

写一个函数 `celsius_to_fahrenheit(c)`，摄氏转华氏。

### [专业] 练习 10-2：齿轮传动比函数

写一个函数 `calc_output_speed(motor_rpm, ratio)`，输入电机转速和减速比，返回输出转速。

### 练习 10-3：判断质数函数

写一个函数 `is_prime(n)`，返回 True 或 False。然后用它打印 1-100 所有质数。

---

## 综合练习

### [专业] 综合-1：简易数据采集器

模拟一个传感器数据采集系统：

1. 循环让用户输入温度数据（输入 q 退出）
2. 所有数据存到列表里
3. 退出后打印：数据个数、最高值、最低值、平均值
4. 如果有超过 40 度的数据，打印"检测到异常高温"

用到的知识：while、break、列表、if、函数

### 综合-2：实习倒计时

写一个程序：

1. 用 input 输入今天日期（或用代码获取，选做）
2. 目标日期是 2027-01-04
3. 计算还剩多少天
4. 打印鼓励语，比如"距离珠三角实习还有 XX 天，加油！"

---

## 参考答案

<details>

<summary>第1章答案</summary>

**练习 1-1：**

```python
print("=" * 28)
print("  实习备战 Day 1 - 开始！")
print("  目标：6个月后去深圳")
print("=" * 28)
```

**练习 1-2：**

```python
print("机械", end=" ")
print("电子", end=" ")
print("工程")
```

**练习 1-3：**

```python
print("-" * 20)
```

</details>

<details>

<summary>第2章答案</summary>

**练习 2-1：**

```python
name = "pico"
school = "天水师范大学"
major = "机械电子工程"
goal = "深圳实习"

print(f"姓名：{name}")
print(f"学校：{school}")
print(f"专业：{major}")
print(f"目标：{goal}")
```

**练习 2-2：**

```python
# input 返回的是字符串，"18" + 1 会报 TypeError
# 修复：转成整数
age = int(input("输入年龄："))
print(age + 1)  # 现在输出 19
```

**练习 2-3：**

```python
celsius = float(input("输入摄氏温度："))
fahrenheit = celsius * 1.8 + 32
print(f"华氏温度：{fahrenheit}")
```

**练习 2-4：**

```python
motor_rpm = 3000
ratio = 30
output_rpm = motor_rpm / ratio
print(f"输出轴转速：{output_rpm} rpm")
```

</details>

<details>

<summary>第3章答案</summary>

**练习 3-1：**

```python
# 第1行：对，打印 True（== 是比较）
x = 10
print(x == 10)  # True

# 第2行：错！y = 5 是赋值不是比较，if 里要用 ==
# 修复：if y == 5:

# 第3行：对，打印 True
a = 3
b = 3
print(a == b)  # True

# 第4行：错！score = 90 是赋值，print 里不能用赋值
# 修复：print(score == 90)  会打印 False
```

**练习 3-2：**

```python
print(100 % 7)  # 2

n = int(input("输入一个数："))
if n % 2 == 0:
    print("偶数")
else:
    print("奇数")
```

**练习 3-3：**

```python
temp = 28.5
if temp < 25:
    print("正常")
elif temp >= 25 and temp <= 35:
    print("偏高")
else:
    print("报警")
```

**练习 3-4：**

```python
age = 18
has_id = True
print(age >= 18)              # True
print(age >= 18 and has_id)   # True
print(age < 18 or has_id)     # True
print(not has_id)             # False
```

**练习 3-5：**

```python
# and：两边都真返回右边，有假返回第一个假值
print(0 and 5)    # 0（0 是假值）
print(3 and 5)    # 5（都真，返回右边）
# or：有真返回第一个真值，都假返回最后一个
print(0 or 5)     # 5
print(3 or 5)     # 3
```

</details>

<details>

<summary>第4章答案</summary>

**练习 4-1：**

```python
score = float(input("输入成绩："))
if score >= 90:
    print("A 优秀")
elif score >= 80:
    print("B 良好")
elif score >= 60:
    print("C 及格")
else:
    print("D 需努力")
```

**练习 4-2：**

```python
cmd = input("输入命令(start/stop/reverse)：")
if cmd == "start":
    print("电机启动")
elif cmd == "stop":
    print("电机停止")
elif cmd == "reverse":
    print("电机反转")
else:
    print("无效命令")
```

**练习 4-4：**

```python
# 问题：else 分支里 score < 60，不可能 >= 80，所以"良好"永远不会打印
# 这是逻辑错误。如果想在 80-89 显示良好，应该放在主判断里
score = 75
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**练习 4-5：**

```python
year_str = input("输入年份：")
if not year_str.isdigit():
    print("请输入有效年份")
else:
    year = int(year_str)
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(f"{year} 是闰年")
    else:
        print(f"{year} 不是闰年")
```

</details>

<details>

<summary>第5章答案</summary>

**练习 5-1：**

```python
i = 10
while i >= 1:
    print(i)
    i -= 1
print("发射！")
```

**练习 5-2：**

```python
total = 0
for i in range(1, 51, 2):
    total += i
print(f"1到50奇数之和：{total}")  # 625
```

**练习 5-3：**

```python
# 死循环原因：i 永远是 0，没有 i += 1
# 修复：
i = 0
while i < 10:
    print(i)
    i += 1
```

**练习 5-4：**

```python
# 打印：
# i=0, j=0
# i=0, j=1
# i=0, j=2
# i=1, j=0
# ...
# 内层循环结束时 j=2
# i 在内层循环全部跑完后才 +1
for i in range(3):
    for j in range(3):
        print(f"i={i}, j={j}")
```

**练习 5-5：**

```python
total = 0
for i in range(5):
    temp = float(input(f"输入第{i+1}次温度："))
    total += temp
average = total / 5
print(f"平均温度：{average}")
```

**练习 5-6：**

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(i * j, end=" ")
    print()
```

**练习 5-7：**

```python
import random
secret = random.randint(1, 100)
count = 0
while count < 7:
    guess = int(input("猜一个数(1-100)："))
    count += 1
    if guess == secret:
        print(f"恭喜！{count}次猜中")
        break
    elif guess > secret:
        print("太大了")
    else:
        print("太小了")
else:
    print(f"失败了，答案是{secret}")
```

</details>

<details>

<summary>第6章答案（重点）</summary>

**练习 6-1：**

```python
# 代码A (break)：打印 1 2 3 4，遇到5直接退出，5不打印
# 代码B (continue)：打印 1 2 3 4 6 7 8 9 10，跳过5但继续循环

# break = 彻底跳出循环
# continue = 只跳过这一次，循环继续
```

**练习 6-2：**

```python
for i in range(1, 31):
    if i % 3 == 0:
        continue
    print(i, end=" ")
```

**练习 6-3：**

```python
n = 100
while True:
    if n % 7 == 0 and n % 9 == 0:
        print(n)  # 126
        break
    n += 1
```

**练习 6-4：**

```python
password = "python123"
for i in range(3):
    user_input = input("输入密码：")
    if user_input == password:
        print("解锁成功")
        break
else:
    print("账户锁定")
```

**练习 6-5：**

```python
while True:
    temp = input("输入温度(q退出)：")
    if temp == "q":
        print("监控结束")
        break
    temp = float(temp)
    if temp >= 50:
        print("过热警告！强制停机")
        break
    else:
        print("温度正常，继续监控")
```

**练习 6-6：**

```python
n = 50
while True:
    is_prime = True
    for i in range(2, n):
        if n % i == 0:
            is_prime = False
            break
    if is_prime:
        print(f"找到质数：{n}")  # 53
        break
    n += 1
```

**练习 6-7：**

```python
# 死循环原因：i=0 时是偶数，continue 跳过了 i += 1
# 所以 i 永远是 0，永远偶数，永远 continue
# 修复：把 i += 1 放到 continue 之前
i = 0
while i < 10:
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1
```

**练习 6-8：**

```python
while True:
    print("===== 菜单 =====")
    print("1. 开始  2. 设置  3. 帮助  4. 退出")
    choice = input("请选择：")
    if choice == "1":
        print("系统启动")
    elif choice == "2":
        print("设置中...")
    elif choice == "3":
        print("这是帮助信息")
    elif choice == "4":
        print("再见")
        break
    else:
        print("无效选项")
```

</details>

<details>

<summary>第7章答案</summary>

**练习 7-1：**

```python
temps = [26.5, 28.0, 33.2, 36.1, 30.5, 29.0, 31.8]
print(f"最高温：{max(temps)}")
print(f"最低温：{min(temps)}")
print(f"平均温：{sum(temps) / len(temps):.1f}")
for t in temps:
    if t > 35:
        print(f"高温预警：{t}")
```

</details>

<details>

<summary>综合练习答案</summary>

**综合-1：**

```python
data = []
while True:
    user_input = input("输入温度(q结束)：")
    if user_input == "q":
        break
    temp = float(user_input)
    data.append(temp)

print(f"采集了 {len(data)} 个数据")
print(f"最高：{max(data)}")
print(f"最低：{min(data)}")
print(f"平均：{sum(data) / len(data):.1f}")

for t in data:
    if t > 40:
        print(f"检测到异常高温：{t}")
```

**综合-2：**

```python
from datetime import date

today = date.today()
target = date(2027, 1, 4)
days_left = (target - today).days
print(f"距离珠三角实习还有 {days_left} 天，加油！")
```

</details>

---

## 进度追踪

做完一章打个勾：

- [ ] 第1章 print与基础
- [ ] 第2章 变量与类型
- [ ] 第3章 运算符（重点）
- [ ] 第4章 条件判断
- [ ] 第5章 循环
- [ ] 第6章 break和continue（当前重点）
- [ ] 第7章 列表（预习）
- [ ] 第8章 元组与字符串（预习）
- [ ] 第9章 字典（预习）
- [ ] 第10章 函数（预习）
- [ ] 综合-1 数据采集器
- [ ] 综合-2 实习倒计时

---

## 易错点速查表

| 你踩过的坑        | 正确写法               | 记忆口诀                         |
| ------------ | ------------------ | ---------------------------- |
| `=` 当比较用     | `==` 才是比较          | 一个等号赋值，两个等号比较                |
| 循环不递增        | while 里记得 `i += 1` | 循环体里必须有让条件变假的代码              |
| continue 死循环 | continue 前先递增      | continue 跳过的是后面的全部代码，包括 i+=1 |
| input 不转换    | `int(input(...))`  | input 返回的永远是字符串              |

---

*做完这份练习册，你的 Python 基础就比大多数大一新生扎实了。遇到不会的随时问！*
