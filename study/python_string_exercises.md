# Python 字符串基础练习（元组之后 · 8-4 任务）

> ⚠️ 本练习册**只用你已会的语法**：变量、`if`、`for` 循环、`print` 多参数、`+` 拼接、`len()`（你从列表就认识了）。
> **不碰** `f-string`、`def` 函数、`enumerate`、`sorted`、字符串方法（`.upper()`/`.count()`/`.find()` 放最后当预览）。
>
> 💡 字符串和元组、列表一样都是**「序列」**——索引 `s[0]`、切片 `s[1:3]`、遍历 `for c in s` 写法**完全一样**。你练元组时已经会了这些，字符串只是把"元素"换成了"字符"，上手极快。

---

## 第 1 题 · 创建与索引

```python
s = "python"
print(s[0])     # 第 1 个字符
print(s[-1])    # 最后一个字符
print(s[1])     # 第 2 个字符
```

**问**：三行分别输出什么？
<details>
<summary>答案</summary>

```
p
n
y
```
`s[0]` 是第一个 `'p'`，`s[-1]` 是最后一个 `'n'`，`s[1]` 是第二个 `'y'`。
</details>

---

## 第 2 题 · 切片（含头不含尾）

```python
s = "hello world"
print(s[0:5])    # 第1到第5个（含头不含尾）
print(s[6:11])   # 第7到第11个
print(s[::2])    # 从头到尾，每隔一个取一个
```

<details>
<summary>答案</summary>

```
hello
world
hlowrd
```
`s[0:5]` 取索引 0~4 → `"hello"`；`s[6:11]` 取 6~10 → `"world"`；`s[::2]` 步长 2 → 取 0,2,4,6,8,10 位置的字符 `h l o w r d`。
</details>

---

## 第 3 题 · 遍历 + 计数（不用 `.count`）

数出 `s = "banana"` 里有几个字母 `'a'`。用 `for` 循环 + 计数器 + `if` 判断。

<details>
<summary>答案 / 提示</summary>

```python
s = "banana"
count = 0
for c in s:
    if c == 'a':
        count = count + 1
print("a 出现了", count, "次")
```
输出：`a 出现了 3 次`

要点：`count = 0` 写在循环**外面**；循环里用 `=` 赋值（不是 `==` 比较）。
</details>

---

## 第 4 题 · 查找某个字符（不用 `in` / `.find`）

`email = "tom@qq.com"`，判断里面有没有 `'@'`。

<details>
<summary>答案 / 提示</summary>

```python
email = "tom@qq.com"
found = "没找到"
for c in email:
    if c == '@':
        found = "找到了"
print(found)
```
输出：`找到了`

要点：先设 `found = "没找到"` 当默认值，循环里一旦碰到 `'@'` 就改成 `"找到了"`。
</details>

---

## 第 5 题 · 拼接（只用 `+`）

姓和名拼成全名。

<details>
<summary>答案 / 提示</summary>

```python
first = "张"
last = "三"
name = first + last
print("全名：", name)
```
输出：`全名： 张三`

要点：字符串用 `+` 拼起来；多个东西一起打印用 `print("全名：", name)` 多参数写法，不用 f-string。
</details>

---

## 第 6 题（选做）· 用 `len` 算长度

`len()` 你从列表就认识了，字符串一样能用。

<details>
<summary>答案 / 提示</summary>

```python
s = "hello"
print("长度是", len(s))
```
输出：`长度是 5`
</details>

---

## 🔍 字符串方法预览（以后正式学再做，现在不要求）

字符串有很多现成方法，能少写循环：
- `s.upper()` → 全大写：`"abc".upper()` 得 `"ABC"`
- `s.count('a')` → 数出现次数：`"banana".count('a')` 得 `3`
- `s.find('@')` → 找位置：`"tom@qq.com".find('@')` 得 `3`
- `'a' in s` → 判断是否包含：`'a' in "banana"` 得 `True`

这些方法很方便，但属于"字符串章节"才系统讲，你**现在的任务不要求用**，先用手写循环把逻辑练熟就行。
