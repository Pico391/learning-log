#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task_engine.py - 动态每日任务引擎（共享模块）

读取：
  1. Git 提交活跃度（各方向文件夹最近 N 天提交次数 + 断更天数）
  2. mastery_tracking.md 掌握度（可选，本地有则更准，云端无则跳过）

生成：
  当天个性化任务（focus + tasks[]），每天基于真实进度不同。
  供 daily_mission.html（本地 bat 刷新）与 daily_push.py（云端推送）共用。

用法：
  python task_engine.py --repo <仓库路径> --mastery <掌握度md> --html <面板html>
  不带 --html 则只打印 JSON。
"""

import subprocess
import os
import re
import json
import sys
import datetime

START_DATE = datetime.date(2026, 7, 21)
TOTAL_WEEKS = 24

# 仓库内各方向对应的顶层文件夹
GIT_DIRS = {
    "Python": "python",
    "CAD": "cad",
    "C": "c-language",
    "Arduino": "arduino",
}

# 技能任务池：每个方向一串递进任务 (关键词, 完整任务串含【xxmin】)
# 顺序即难度/进度顺序；mastery 未完成项会优先匹配关键词
SKILL_POOL = {
    "Python": [
        ("嵌套循环", "【25min】Python：练 QClaw 错题——反向打印数字（while + x%10 取个位、x//10 砍位）①打印1~10 ②九九乘法表（嵌套 for），这两道你之前卡过"),
        ("累加器", "【20min】Python：写累加器——用户输入数字累加、输 q 退出打印总和（x = x + y，别写成 x==x+y，这是你踩过的坑）"),
        ("for列表", "【25min】Python：练列表——创建 fruits 列表，打印第2/4个、最后2个，append 加西瓜、insert 插草莓、del 删香蕉（python_exercises 第7章）"),
        ("分支", "【20min】Python：练 if-elif——成绩评级（>=90 A / >=80 B / >=60 C / 否则 D）+ 判断闰年（QClaw 你问过的题）"),
        ("函数", "【25min】Python：定义函数 max_of_two / calculate(a,b,op) 加减乘除 / is_prime 判素数（python_exercises 第12章）"),
        ("字符串", "【20min】Python：字符串——输入一句话转大小写、统计某字母次数、凯撒密码偏移一位（python_exercises 第9章）"),
    ],
    "CAD": [
        ("尺寸标注", "【25min】CAD：给轴承图补尺寸标注 DIM（直径/半径/长度），练出图规范（你 8/1 画的轴承座）"),
        ("齿轮", "【30min】CAD：画齿轮——CIRCLE 外圆 + ARRAY 环形阵列 20 个齿 + TRIM 修顺"),
        ("六角螺母", "【20min】CAD：POLYGON 画六边形 + 中心螺纹孔 + 倒角 CHAMFER（QClaw 练习8 进阶）"),
        ("法兰盘", "【25min】CAD：画法兰盘——外圆直径100 + 内孔30 + ARRAY 阵列4个均布螺栓孔（QClaw 练习8，你画过）"),
        ("阶梯轴实战", "【30min】CAD：实际画出阶梯轴（矩形拼 + MIRROR 镜像，之前说不会，今天攻克）"),
        ("剖视图", "【35min】CAD：画轴承座剖视图，加剖面线 HATCH（QClaw 练习7 轴承座升级）"),
        ("导出图片", "【10min】CAD：把今天画的图导出 JPG/PNG，存 GitHub 当作品"),
    ],
    "C": [
        ("环境", "【20min】C：配环境写 hello.c，gcc 编译运行（翁恺第1讲）"),
        ("变量类型", "【25min】C：变量/数据类型/printf，对比 Python"),
        ("运算符", "【25min】C：算术/关系/逻辑运算符，注意 &&/||/! 与 Python 不同"),
        ("条件", "【25min】C：if/else + switch 分支"),
        ("循环", "【30min】C：while/for 循环，对比 Python 缩进；练你 QClaw 错题——找第一个被7整除的数（计数器 i 必须放循环外！）"),
        ("函数", "【25min】C：函数定义、参数传递（值传递）"),
    ],
    "Arduino": [
        ("Blink", "【30min】Arduino：装 IDE，烧录 Blink 让板载 LED 闪"),
        ("数字IO", "【25min】Arduino：用按钮/数字口控 LED，学 pinMode/digitalWrite"),
        ("传感器", "【30min】Arduino：接 DHT11 温度传感器，串口打印读数"),
        ("温控风扇", "【40min】Arduino：做温控风扇小项目（传感器 + 判断 + 电机）"),
    ],
}

GIT_COMMIT = ["git"]


def _run_git(repo, args, timeout=30):
    try:
        r = subprocess.run(
            GIT_COMMIT + ["-C", repo] + args,
            capture_output=True, text=True, timeout=timeout,
        )
        return r.stdout
    except Exception:
        return ""


def analyze_git(repo, days=30):
    """返回 {方向: {count, last, days_since}}"""
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    res = {}
    for d, folder in GIT_DIRS.items():
        # 该方向提交涉及的文件数
        out = _run_git(repo, ["log", f"--since={since}", "--name-only",
                                "--pretty=format:", "--", folder + "/"])
        count = sum(1 for l in out.splitlines()
                    if l.strip().startswith(folder + "/"))
        # 该方向最近提交日期
        ld = _run_git(repo, ["log", "-1", "--format=%ad", "--date=short",
                               "--", folder + "/"]).strip()
        last = None
        days_since = 999
        if ld:
            try:
                last = datetime.date.fromisoformat(ld)
                days_since = (datetime.date.today() - last).days
            except Exception:
                pass
        res[d] = {"count": count, "last": ld, "days_since": days_since}
    return res


def _classify(title):
    if "Python" in title:
        return "Python"
    if "CAD" in title:
        return "CAD"
    if "C 语言" in title or title.strip().startswith("C "):
        return "C"
    if "Arduino" in title:
        return "Arduino"
    return None


def read_mastery(path):
    """解析 mastery_tracking.md，返回 {方向: [未完成项文本]}"""
    if not path or not os.path.exists(path):
        return {}
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return {}
    result = {}
    cur = None
    for line in txt.splitlines():
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            cur = _classify(m.group(1))
            if cur:
                result.setdefault(cur, [])
            else:
                cur = None
            continue
        if cur:
            m2 = re.match(r"^- \[ \] (.+)$", line)
            if m2:
                result[cur].append(m2.group(1))
    return result


def get_week_num(now=None):
    now = now or datetime.date.today()
    diff = (now - START_DATE).days // 7
    return max(1, min(TOTAL_WEEKS, diff + 1))


def next_task_for(direction, mastery_map, git_info, used=None):
    pool = SKILL_POOL.get(direction, [])
    if not pool:
        return None
    # 1) mastery 未完成项优先匹配关键词
    if direction in mastery_map:
        for unf in mastery_map[direction]:
            for kw, text in pool:
                if kw in unf and text not in (used or set()):
                    return text
    # 2) 否则按 git 活跃度取索引
    cnt = git_info.get(direction, {}).get("count", 0)
    idx = min(cnt, len(pool) - 1)
    for off in range(len(pool)):
        j = (idx + off) % len(pool)
        if pool[j][1] not in (used or set()):
            return pool[j][1]
    return None


def generate_today(repo, mastery_path=None, now=None):
    now = now or datetime.date.today()
    week = get_week_num(now)
    git = analyze_git(repo)
    mastery = read_mastery(mastery_path)

    def prio(d):
        base = 0
        if d == "C" and week >= 6:
            base += 6
        if d == "Arduino" and week >= 10:
            base += 6
        if d == "Python" and week <= 8:
            base += 3
        if d == "CAD":
            base += 2
        base += git.get(d, {}).get("count", 0) * 1.2
        ds = git.get(d, {}).get("days_since", 999)
        if 0 < ds <= 2:  # 近 2 天在练，优先延续
            base += 3
        if 5 < ds < 999:  # 断更惩罚（999=未知，不惩罚）
            base -= 4
        return base

    dirs = ["Python", "CAD", "C", "Arduino"]
    ranked = sorted(dirs, key=prio, reverse=True)
    main, second = ranked[0], ranked[1]

    tasks = []
    used = set()
    t1 = next_task_for(main, mastery, git, used)
    if t1:
        used.add(t1)
        tasks.append(t1)
    t2 = next_task_for(main, mastery, git, used)
    if t2:
        used.add(t2)
        tasks.append(t2)

    ds2 = git.get(second, {}).get("days_since", 999)
    if 5 < ds2 < 999:
        tasks.append(f"【15min】提醒：{second} 已 {ds2} 天没提交，捡回 1 道基础题保持手感")
    else:
        t3 = next_task_for(second, mastery, git, used)
        if t3:
            tasks.append(t3)

    tasks.append("【10min】Git：把今天作品 add/commit/push 到 learning-log（保持绿格子）")

    focus = f"{main} 为主 · 动态生成（基于你的提交与掌握度）"
    return {
        "date": now.isoformat(),
        "focus": focus,
        "tasks": tasks,
        "week": week,
        "generated_by": "dynamic",
        "main": main,
        "second": second,
    }


def to_markdown(data):
    title = "📅 " + data["date"] + " 今日任务（动态生成）"
    lines = ["**" + data["focus"] + "**", "", "今日任务："]
    for i, t in enumerate(data["tasks"], 1):
        lines.append(f"{i}. {t}")
    lines.append("")
    lines.append("> 根据你的 GitHub 提交活跃度与掌握度追踪自动生成，每天不同。")
    return title, "\n".join(lines)


MARKER = "/*__DYNAMIC_TASK__*/"


def _extract_balanced(content, prefix):
    """从 content 里 prefix 之后提取配平的 {...} JSON 字符串。"""
    idx = content.find(prefix)
    if idx < 0:
        return None
    i = content.find("{", idx)
    if i < 0:
        return None
    depth = 0
    for j in range(i, len(content)):
        if content[j] == "{":
            depth += 1
        elif content[j] == "}":
            depth -= 1
            if depth == 0:
                return content[i:j + 1]
    return None


def write_html_dynamic(html_path, data):
    """把当天任务写入 HTML 的 DYNAMIC_TASKS（按日期 map），保留其它日期的任务不覆盖。"""
    date_key = (data.get("date") or
                __import__("datetime").date.today().isoformat())
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    tasks_map = {}
    # 读取已有的按日期任务 map（兼容旧版单条 DYNAMIC_TASK）
    obj = _extract_balanced(content, "window.DYNAMIC_TASKS =")
    if obj is not None:
        try:
            tasks_map = json.loads(obj)
        except Exception:
            tasks_map = {}
    else:
        obj2 = _extract_balanced(content, "window.DYNAMIC_TASK =")
        if obj2 is not None:
            try:
                old = json.loads(obj2)
                if "date" in old:
                    tasks_map[old["date"]] = old
            except Exception:
                pass
    tasks_map[date_key] = data
    new_block = ("window.DYNAMIC_TASKS = "
                 + json.dumps(tasks_map, ensure_ascii=False)
                 + ";\n" + MARKER)
    # 定位待替换的旧块（兼容单条 / 旧单条 / 仅占位符）
    start = content.find("window.DYNAMIC_TASKS =")
    prefix = "window.DYNAMIC_TASKS ="
    if start < 0:
        start = content.find("window.DYNAMIC_TASK =")
        prefix = "window.DYNAMIC_TASK ="
    if start >= 0:
        i = content.find("{", start)
        depth = 0
        end = i
        for j in range(i, len(content)):
            if content[j] == "{":
                depth += 1
            elif content[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        k = end
        while k < len(content) and content[k] in " ;\t\n\r":
            k += 1
        while content[k:k + 20].startswith("/*__DYNAMIC_TASK__*/"):
            k += 20
        old_block = content[start:k]
        content = content[:start] + new_block + content[k:]
    elif MARKER in content:
        content = content.replace(MARKER, new_block, 1)
    else:
        content = content.replace("</body>",
                                   "<script>" + new_block + "</script></body>", 1)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    import argparse
    p = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    p.add_argument("--repo",
                   default=os.path.dirname(here),
                   help="learning-log 仓库路径")
    p.add_argument("--mastery", default=None, help="mastery_tracking.md 路径")
    p.add_argument("--html", default=None, help="daily_mission.html 路径")
    args = p.parse_args()

    data = generate_today(args.repo, args.mastery)
    if args.html:
        write_html_dynamic(args.html, data)
        print("HTML 动态任务已写入:", args.html)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
