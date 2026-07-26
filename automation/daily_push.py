# -*- coding: utf-8 -*-
"""
每日学习提醒 - 云端微信推送脚本
通过 GitHub Actions 每天定时运行，推送到 pico 的微信
电脑关了也能推送，因为跑在 GitHub 的云服务器上
"""
import urllib.request
import urllib.parse
import json
import os
import sys
from datetime import datetime, date, timedelta

# ===== 配置 =====
START_DATE = date(2026, 7, 21)
TOTAL_WEEKS = 24

# ===== 每日任务数据 =====
# 每周7天的具体任务，比之前的"每周3个任务"细化到每天
# 结构: WEEKS[周号-1]["days"][0-6] = {"focus": 重点, "tasks": [任务列表]}
DAILY_TASKS = {
    # ========== 第一阶段：基础巩固 (W1-W8) ==========
    1: {
        "goal": "Python复习第1-5章 + CAD基础 + 注册GitHub账号",
        "days": [
            {"focus": "Python复习 + GitHub", "tasks": ["复习小甲鱼第3章运算符(== vs =)", "复习第5章while循环", "注册GitHub账号，创建learning-log仓库"]},
            {"focus": "Python复习 + CAD", "tasks": ["复习小甲鱼第4章条件分支", "看大梦老师CAD第1-2集", "画轴承座轮廓图(不用图层)"]},
            {"focus": "Python第6章 + CAD", "tasks": ["学小甲鱼第6章break", "做练习册v2第6章前4题", "CAD练习: 精确坐标画矩形和圆"]},
            {"focus": "Python第6章 + CAD", "tasks": ["学小甲鱼第6章continue", "做练习册v2第6章后4题", "CAD练习: 用极轴追踪画45度线"]},
            {"focus": "循环实战 + CAD", "tasks": ["用循环重写温度采集题", "试写九九乘法表(卡住就问)", "CAD练习: 画3个相切圆"]},
            {"focus": "本周复习 + Git", "tasks": ["复习本周Python内容", "重画轴承座(带图层分层)", "Git提交所有练习代码"]},
            {"focus": "休息 + 预习", "tasks": ["休息/灵活机动", "预习Python第7章列表", "看看GitHub绿色格子"]},
        ]
    },
    2: {
        "goal": "Python第7章列表 + CAD修剪/标注(TRIM/HATCH/DIMLINEAR)",
        "days": [
            {"focus": "Python列表入门", "tasks": ["学小甲鱼第7章列表基础", "练习: 创建列表/索引/切片", "Git提交"]},
            {"focus": "列表操作", "tasks": ["学列表增删改: append/insert/remove/pop", "做10道列表练习题", "Git提交"]},
            {"focus": "列表遍历 + CAD", "tasks": ["用for循环遍历列表", "CAD练习: TRIM修剪多余线段", "Git提交"]},
            {"focus": "列表嵌套 + CAD", "tasks": ["学嵌套列表(矩阵)", "CAD练习: HATCH填充剖面线", "Git提交"]},
            {"focus": "综合练习 + CAD", "tasks": ["用列表重写学生成绩管理", "CAD练习: DIMLINEAR线性标注", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习列表所有操作", "CAD: 给轴承座加完整标注", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息/灵活机动", "预习Python第8章元组", "看看本周代码量"]},
        ]
    },
    3: {
        "goal": "Python元组/字典/集合 + CAD三视图练习",
        "days": [
            {"focus": "元组", "tasks": ["学元组: 不可变序列", "练习: 元组打包/解包", "Git提交"]},
            {"focus": "字典入门", "tasks": ["学字典: 键值对", "练习: 创建/访问/修改字典", "Git提交"]},
            {"focus": "字典进阶 + CAD", "tasks": ["学字典遍历/嵌套", "CAD: 画简单零件主视图", "Git提交"]},
            {"focus": "集合", "tasks": ["学集合: 去重/交并差", "练习: 集合运算", "Git提交"]},
            {"focus": "综合 + CAD", "tasks": ["用字典+列表写通讯录", "CAD: 画俯视图", "Git提交"]},
            {"focus": "三视图 + 复习", "tasks": ["CAD: 画左视图，完成三视图", "复习元组/字典/集合", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息/灵活机动", "预习Python第9章函数", "整理本周笔记"]},
        ]
    },
    4: {
        "goal": "Python OOP入门(类/对象/__init__) + CAD出图 + Git首次提交",
        "days": [
            {"focus": "函数复习", "tasks": ["学函数定义/参数/返回值", "练习: 写5个函数", "Git提交"]},
            {"focus": "OOP入门", "tasks": ["学类和对象概念", "学__init__方法", "练习: 写一个Dog类", "Git提交"]},
            {"focus": "OOP属性方法", "tasks": ["学实例属性/类属性", "学实例方法", "练习: 给Dog加方法", "Git提交"]},
            {"focus": "OOP + CAD", "tasks": ["练习: 写一个Student类", "CAD: 学习布局出图", "Git提交"]},
            {"focus": "CAD出图 + Git", "tasks": ["CAD: 打印设置/出图练习", "整理GitHub仓库README", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习OOP概念", "用类重写之前的练习", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息/灵活机动", "预习继承和封装", "看看GitHub提交记录"]},
        ]
    },
    5: {
        "goal": "Python OOP进阶(继承/封装) + 异常处理",
        "days": [
            {"focus": "继承", "tasks": ["学继承: 子类/父类", "练习: Dog继承Animal", "Git提交"]},
            {"focus": "多态 + 封装", "tasks": ["学多态和封装", "练习: 写继承体系", "Git提交"]},
            {"focus": "异常处理", "tasks": ["学try/except/finally", "练习: 处理各种异常", "Git提交"]},
            {"focus": "自定义异常 + CAD", "tasks": ["学raise/自定义异常", "CAD: 复杂零件图练习", "Git提交"]},
            {"focus": "综合练习", "tasks": ["用OOP+异常写银行账户系统", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习OOP+异常", "整理代码注释", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息/灵活机动", "预习文件I/O", "整理笔记"]},
        ]
    },
    6: {
        "goal": "Python文件I/O + 模块 + CAD复杂零件图(暑假收官)",
        "days": [
            {"focus": "文件读写", "tasks": ["学open/read/write/close", "练习: 读写txt文件", "Git提交"]},
            {"focus": "with语句", "tasks": ["学with自动关闭", "练习: with写文件", "Git提交"]},
            {"focus": "模块导入", "tasks": ["学import/from import", "学自己写模块", "Git提交"]},
            {"focus": "CAD复杂零件", "tasks": ["CAD: 画复杂零件完整图", "标注齐全(尺寸+公差)", "Git提交"]},
            {"focus": "暑假总结", "tasks": ["写暑假学习总结", "整理GitHub仓库", "Git提交"]},
            {"focus": "项目巩固", "tasks": ["用文件I/O+OOP写小型项目", "Git提交"]},
            {"focus": "休息 + 准备开学", "tasks": ["休息", "准备开学物品", "预习C语言"]},
        ]
    },
    7: {
        "goal": "C语言入门(翁恺课程) + 开学报到调整时间表",
        "days": [
            {"focus": "开学报到", "tasks": ["报到/安顿宿舍", "认识同学和辅导员", "了解课程表"]},
            {"focus": "C语言入门", "tasks": ["装Dev-C++或VSCode", "看翁恺C语言第1集", "写第一个hello.c", "Git提交"]},
            {"focus": "C基础语法", "tasks": ["看翁恺第2集: 变量/数据类型", "练习: 声明变量并打印", "Git提交"]},
            {"focus": "C输入输出", "tasks": ["看翁恺第3集: printf/scanf", "练习: 计算两数之和", "Git提交"]},
            {"focus": "调整时间表", "tasks": ["按课表调整每日学习时间", "确定每天2-3小时学习窗口", "Git提交"]},
            {"focus": "C运算符", "tasks": ["学C运算符(和Python对比)", "练习: 算术/关系/逻辑运算", "Git提交"]},
            {"focus": "休息 + 复习", "tasks": ["休息", "复习本周C内容", "整理笔记"]},
        ]
    },
    8: {
        "goal": "C控制流/函数/数组 + Python迷你项目(学生成绩管理系统)",
        "days": [
            {"focus": "C控制流", "tasks": ["学C的if/for/while(对比Python)", "练习: 写循环程序", "Git提交"]},
            {"focus": "C函数", "tasks": ["学C函数定义/调用", "练习: 写计算器函数", "Git提交"]},
            {"focus": "C数组", "tasks": ["学C一维数组", "练习: 数组排序", "Git提交"]},
            {"focus": "Python项目", "tasks": ["用OOP写学生成绩管理系统", "功能: 增删改查+文件存储", "Git提交"]},
            {"focus": "项目完善", "tasks": ["完善成绩管理系统", "加异常处理和输入验证", "Git提交"]},
            {"focus": "阶段总结", "tasks": ["第一阶段总结", "整理所有代码和笔记", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习C指针", "看看GitHub总提交数"]},
        ]
    },
    # ========== 第二阶段：核心技能 (W9-W16) ==========
    9: {
        "goal": "C指针基础(&和*运算符/指针与数组)",
        "days": [
            {"focus": "指针概念", "tasks": ["学什么是指针", "学&取地址运算符", "Git提交"]},
            {"focus": "指针使用", "tasks": ["学*解引用运算符", "练习: 指针读写变量", "Git提交"]},
            {"focus": "指针与数组", "tasks": ["学数组名=指针", "练习: 用指针遍历数组", "Git提交"]},
            {"focus": "指针运算", "tasks": ["学指针加减法", "练习: 指针比较", "Git提交"]},
            {"focus": "指针练习", "tasks": ["做10道指针练习题", "写交换函数(swap)", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习指针基础", "画内存示意图", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习指针进阶", "整理笔记"]},
        ]
    },
    10: {
        "goal": "C指针进阶 + 动态内存(malloc/calloc/free)",
        "days": [
            {"focus": "指针数组", "tasks": ["学指针数组和数组指针", "练习: 字符串排序", "Git提交"]},
            {"focus": "函数指针", "tasks": ["学函数指针", "练习: 回调函数", "Git提交"]},
            {"focus": "多级指针", "tasks": ["学二级指针", "练习: 二级指针操作", "Git提交"]},
            {"focus": "动态内存", "tasks": ["学malloc/calloc/free", "练习: 动态数组", "Git提交"]},
            {"focus": "内存管理", "tasks": ["学内存泄漏检测", "练习: 动态二维数组", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习指针进阶", "写综合指针程序", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习结构体", "整理笔记"]},
        ]
    },
    11: {
        "goal": "C结构体/文件I/O + 买Arduino UNO套件",
        "days": [
            {"focus": "结构体", "tasks": ["学struct定义和使用", "练习: 学生结构体", "Git提交"]},
            {"focus": "typedef + 结构体指针", "tasks": ["学typedef", "学结构体指针(->)", "Git提交"]},
            {"focus": "C文件I/O", "tasks": ["学fopen/fread/fwrite", "练习: 文件复制", "Git提交"]},
            {"focus": "买Arduino", "tasks": ["淘宝买Arduino UNO套件(80-120元)", "等快递期间复习C", "Git提交"]},
            {"focus": "综合练习", "tasks": ["用结构体+文件写通讯录", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习结构体和文件", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习Arduino", "期待套件到达"]},
        ]
    },
    12: {
        "goal": "Arduino入门(Blink/数字I/O/模拟输入)",
        "days": [
            {"focus": "Arduino环境", "tasks": ["装Arduino IDE", "连UNO板，跑Blink", "Git提交Arduino代码"]},
            {"focus": "数字I/O", "tasks": ["学pinMode/digitalWrite/digitalRead", "练习: 按键控LED", "Git提交"]},
            {"focus": "模拟输入", "tasks": ["学analogRead", "练习: 电位器调LED亮度", "Git提交"]},
            {"focus": "串口通信", "tasks": ["学Serial.begin/Serial.print", "练习: 串口打印传感器值", "Git提交"]},
            {"focus": "太极创客网课", "tasks": ["看太极创客Arduino教程", "跟着做实验", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习Arduino基础", "整理代码和电路图", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习传感器", "整理笔记"]},
        ]
    },
    13: {
        "goal": "Arduino传感器(超声波HC-SR04/温湿度DHT11) + 舵机SG90",
        "days": [
            {"focus": "超声波测距", "tasks": ["接HC-SR04", "写测距代码，串口显示距离", "Git提交"]},
            {"focus": "温湿度", "tasks": ["装DHT库", "接DHT11，读取温湿度", "Git提交"]},
            {"focus": "舵机控制", "tasks": ["学Servo库", "用SG90做转动实验", "Git提交"]},
            {"focus": "综合实验", "tasks": ["超声波测距+舵机联动", "近了就转舵机", "Git提交"]},
            {"focus": "数据记录", "tasks": ["温湿度定时采集", "串口输出数据", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习传感器", "整理电路图", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习LCD和电机", "整理笔记"]},
        ]
    },
    14: {
        "goal": "Arduino进阶(LCD/电机驱动L298N/PWM) + 智能温控风扇项目",
        "days": [
            {"focus": "LCD显示", "tasks": ["接LCD1602", "显示Hello World和传感器数据", "Git提交"]},
            {"focus": "电机驱动", "tasks": ["学L298N驱动板", "控制直流电机正反转", "Git提交"]},
            {"focus": "PWM调速", "tasks": ["学analogWrite/PWM", "练习: PWM控电机转速", "Git提交"]},
            {"focus": "温控风扇", "tasks": ["DHT11测温→PWM控风扇", "温度高转速快", "Git提交"]},
            {"focus": "项目完善", "tasks": ["加LCD显示温度和转速", "加阈值报警", "Git提交"]},
            {"focus": "项目文档", "tasks": ["写项目README", "录演示视频", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习电路基础", "整理笔记"]},
        ]
    },
    15: {
        "goal": "电子电路基础(欧姆定律/基尔霍夫/元件识别) + SolidWorks入门",
        "days": [
            {"focus": "欧姆定律", "tasks": ["学V=IR", "练习: 计算电路", "Git提交笔记"]},
            {"focus": "基尔霍夫", "tasks": ["学KVL/KCL", "练习: 节点分析", "Git提交"]},
            {"focus": "元件识别", "tasks": ["学电阻/电容/电感/二极管", "练习: 读色环电阻", "Git提交"]},
            {"focus": "SolidWorks入门", "tasks": ["装SolidWorks", "学草图绘制", "Git提交"]},
            {"focus": "SolidWorks拉伸", "tasks": ["学拉伸/旋转", "画一个简单零件3D", "Git提交"]},
            {"focus": "本周复习", "tasks": ["复习电路基础", "整理元件识别表", "Git提交"]},
            {"focus": "休息 + 预习", "tasks": ["休息", "预习PCB设计", "整理笔记"]},
        ]
    },
    16: {
        "goal": "PCB设计入门(立创EDA) + 阶段总结",
        "days": [
            {"focus": "立创EDA入门", "tasks": ["注册立创EDA", "学原理图绘制", "Git提交"]},
            {"focus": "PCB布局", "tasks": ["学PCB布局/布线", "画LED闪烁板", "Git提交"]},
            {"focus": "PCB完善", "tasks": ["加丝印/焊盘", "导出Gerber文件", "Git提交"]},
            {"focus": "阶段总结", "tasks": ["总结第二阶段", "整理GitHub仓库", "Git提交"]},
            {"focus": "项目规划", "tasks": ["规划第三阶段项目", "列硬件清单", "Git提交"]},
            {"focus": "代码整理", "tasks": ["整理所有代码", "写文档", "Git提交"]},
            {"focus": "休息 + 准备", "tasks": ["休息", "准备项目材料", "期待项目阶段"]},
        ]
    },
    # ========== 第三阶段：项目与求职 (W17-W24) ==========
    17: {
        "goal": "项目规划(智能环境监测站：Arduino+传感器+LCD+SD卡+Python可视化)",
        "days": [
            {"focus": "需求文档", "tasks": ["写需求文档: 功能/硬件/技术路线", "Git提交"]},
            {"focus": "硬件确认", "tasks": ["确认传感器/SD卡/LCD齐全", "画系统框图", "Git提交"]},
            {"focus": "软件架构", "tasks": ["设计代码架构", "分模块设计", "Git提交"]},
            {"focus": "数据格式", "tasks": ["设计数据存储格式(CSV)", "设计通信协议", "Git提交"]},
            {"focus": "开发计划", "tasks": ["制定开发时间表", "分配每天任务", "Git提交"]},
            {"focus": "环境搭建", "tasks": ["搭开发环境", "测试各模块", "Git提交"]},
            {"focus": "休息 + 准备", "tasks": ["休息", "准备开始编码", "整理文档"]},
        ]
    },
    18: {
        "goal": "项目硬件实现(组装+传感器代码+数据记录)",
        "days": [
            {"focus": "硬件组装", "tasks": ["组装电路", "接好所有传感器", "拍照记录"]},
            {"focus": "传感器代码", "tasks": ["写温湿度采集代码", "写光照采集代码", "Git提交"]},
            {"focus": "LCD显示", "tasks": ["LCD显示实时数据", "Git提交"]},
            {"focus": "SD卡记录", "tasks": ["写SD卡数据存储", "CSV格式定时记录", "Git提交"]},
            {"focus": "数据校验", "tasks": ["测试数据完整性", "处理异常值", "Git提交"]},
            {"focus": "联调测试", "tasks": ["全系统联调", "修复bug", "Git提交"]},
            {"focus": "休息 + 整理", "tasks": ["休息", "整理代码", "准备上位机"]},
        ]
    },
    19: {
        "goal": "Python上位机(串口pyserial+matplotlib绘图) + 文档 + 演示视频",
        "days": [
            {"focus": "串口通信", "tasks": ["学pyserial", "读Arduino串口数据", "Git提交"]},
            {"focus": "数据解析", "tasks": ["解析串口数据", "存入列表", "Git提交"]},
            {"focus": "matplotlib绘图", "tasks": ["学matplotlib基础", "实时绘制温湿度曲线", "Git提交"]},
            {"focus": "UI界面", "tasks": ["用tkinter做简单UI", "显示图表+数据", "Git提交"]},
            {"focus": "项目文档", "tasks": ["写README文档", "写使用说明", "Git提交"]},
            {"focus": "演示视频", "tasks": ["录项目演示视频", "上传B站或存本地", "Git提交"]},
            {"focus": "休息 + 整理", "tasks": ["休息", "整理项目", "准备作品集"]},
        ]
    },
    20: {
        "goal": "项目完善 + GitHub作品集(GitHub Pages主页)",
        "days": [
            {"focus": "代码优化", "tasks": ["优化代码结构", "加详细注释", "Git提交"]},
            {"focus": "README完善", "tasks": ["写专业README", "加截图和GIF", "Git提交"]},
            {"focus": "GitHub Pages", "tasks": ["开GitHub Pages", "设计个人主页", "Git提交"]},
            {"focus": "主页内容", "tasks": ["写自我介绍", "展示项目和技能", "Git提交"]},
            {"focus": "项目展示", "tasks": ["在主页展示项目", "加演示视频链接", "Git提交"]},
            {"focus": "最终检查", "tasks": ["检查所有链接", "测试主页显示", "Git提交"]},
            {"focus": "休息 + 准备", "tasks": ["休息", "准备写简历", "整理作品集"]},
        ]
    },
    21: {
        "goal": "简历制作 + 自我介绍练习",
        "days": [
            {"focus": "简历框架", "tasks": ["确定简历结构", "写基本信息+教育背景", "Git提交"]},
            {"focus": "技能描述", "tasks": ["写技能清单(Python/C/CAD/Arduino)", "突出项目经验", "Git提交"]},
            {"focus": "项目描述", "tasks": ["用STAR法则写项目", "量化成果", "Git提交"]},
            {"focus": "简历完善", "tasks": ["润色语言", "调整排版", "Git提交"]},
            {"focus": "自我介绍", "tasks": ["写1分钟自我介绍稿", "对着镜子练3遍", "Git提交"]},
            {"focus": "模拟面试", "tasks": ["准备常见问题", "找人模拟面试", "Git提交"]},
            {"focus": "休息 + 准备", "tasks": ["休息", "准备投递", "整理简历"]},
        ]
    },
    22: {
        "goal": "公司调研 + 开始投递(BOSS直聘/实习僧，目标10-15家)",
        "days": [
            {"focus": "注册平台", "tasks": ["注册BOSS直聘/实习僧", "完善个人资料", "上传简历"]},
            {"focus": "公司调研", "tasks": ["调研汇川/英威腾/长盈精密等", "整理目标公司清单", "记录岗位要求"]},
            {"focus": "投递Day1", "tasks": ["投3-5家保底方向(CAD/工艺)", "写打招呼话术", "记录投递"]},
            {"focus": "投递Day2", "tasks": ["投3-5家嵌入式方向", "针对岗位调整简历", "记录投递"]},
            {"focus": "投递Day3", "tasks": ["投2-3家Python/硬件测试", "跟进之前投递", "记录投递"]},
            {"focus": "投递总结", "tasks": ["整理投递清单", "准备面试", "Git提交进度"]},
            {"focus": "休息 + 准备", "tasks": ["休息", "准备面试", "整理投递记录"]},
        ]
    },
    23: {
        "goal": "面试准备(技术面+行为面) + 持续投递",
        "days": [
            {"focus": "技术面C", "tasks": ["复习C常考: 指针/内存/结构体", "准备代码题", "Git提交"]},
            {"focus": "技术面Python", "tasks": ["复习Python常考: 列表/字典/OOP", "准备代码题", "Git提交"]},
            {"focus": "技术面Arduino", "tasks": ["复习Arduino/传感器知识", "准备项目讲解", "Git提交"]},
            {"focus": "行为面准备", "tasks": ["学STAR法则", "准备8个故事", "Git提交"]},
            {"focus": "模拟面试", "tasks": ["模拟技术面", "模拟行为面", "Git提交"]},
            {"focus": "持续投递", "tasks": ["再投5家", "跟进入投递状态", "Git提交"]},
            {"focus": "休息 + 复盘", "tasks": ["休息", "复盘模拟面试", "整理笔记"]},
        ]
    },
    24: {
        "goal": "积极求职 + 寒假面试，目标拿到实习offer",
        "days": [
            {"focus": "积极面试", "tasks": ["参加所有面试机会", "面完立即复盘", "Git提交"]},
            {"focus": "持续投递", "tasks": ["持续投递不放弃", "拓展新岗位", "Git提交"]},
            {"focus": "面试改进", "tasks": ["根据反馈改进", "加强薄弱点", "Git提交"]},
            {"focus": "寒假准备", "tasks": ["准备去深圳/广州", "找住宿", "Git提交"]},
            {"focus": "积极求职", "tasks": ["主动联系HR", "争取面试机会", "Git提交"]},
            {"focus": "目标达成", "tasks": ["拿到offer!", "确认入职细节", "Git提交"]},
            {"focus": "庆祝 + 总结", "tasks": ["庆祝拿到offer!", "总结6个月历程", "更新GitHub"]},
        ]
    },
}

PHASE_NAMES = {1: "基础巩固", 2: "核心技能", 3: "项目与求职"}
WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

QUOTES = [
    "学校牌子改不了，但技能深度、项目质量、投递数量你能控制。",
    "每天Git提交一次，绿色格子是面试官会看的坚持证据。",
    "小公司不卡大一，要的是'能干活、便宜、愿意学'。",
    "AutoCAD是第一优先，面试必问。用中望CAD学完全没问题。",
    "先去供应链中小企业实习，曲线进大厂。",
    "6个月后你的简历要有：Python+C+Arduino+CAD+项目+GitHub。",
    "比别人早半年起步，这就是你的优势。",
    "哪怕一行代码也要每天提交。",
    "嵌套循环=外层像时针走一格，内层像分针转一圈。",
    "循环的价值：用同一段代码重复执行，不用复制粘贴。",
]

PHASE_EMOJI = {1: "Phase1", 2: "Phase2", 3: "Phase3"}


def get_week_num():
    """计算当前是第几周"""
    today = date.today()
    diff = (today - START_DATE).days
    if diff < 0:
        return 1
    return diff // 7 + 1


def get_day_of_week():
    """返回今天是周几(0=周一, 6=周日)"""
    return date.today().weekday()


def get_phase(week_num):
    """根据周数返回阶段号"""
    if week_num <= 8:
        return 1
    elif week_num <= 16:
        return 2
    else:
        return 3


def build_message():
    """构建推送消息"""
    week_num = get_week_num()
    if week_num > TOTAL_WEEKS:
        week_num = TOTAL_WEEKS
    if week_num < 1:
        week_num = 1

    phase = get_phase(week_num)
    phase_name = PHASE_NAMES[phase]
    dow = get_day_of_week()
    weekday = WEEKDAY_NAMES[dow]

    today = datetime.now()
    date_str = f"{today.month}月{today.day}日 {weekday}"
    day_num = (date.today() - START_DATE).days + 1
    pct = min(100, round((week_num / TOTAL_WEEKS) * 100))

    # 获取今日任务
    week_data = DAILY_TASKS.get(week_num, {})
    today_task = week_data.get("days", [{}])[dow] if dow < len(week_data.get("days", [])) else {"focus": "灵活安排", "tasks": ["复习巩固", "Git提交"]}
    week_goal = week_data.get("goal", "按计划学习")

    quote = QUOTES[day_num % len(QUOTES)]

    # 标题
    title = f"Day{day_num} | W{week_num} {phase_name} | {today_task.get('focus', '学习')}"

    # 正文
    desp = f"""## {date_str} | 第{week_num}周/24 | {phase_name} | 总进度 {pct}%

---

### 本周目标
{week_goal}

---

### 今日重点: {today_task.get('focus', '学习')}

"""
    for i, task in enumerate(today_task.get("tasks", ["按计划学习"]), 1):
        desp += f"{i}. {task}\n"

    # 周末加额外提醒
    if dow >= 5:
        desp += f"""
---
### 周末特别提醒
- 周末时间多，可以多花2小时做项目
- 复习本周内容，查漏补缺
- 整理笔记和代码，保持GitHub仓库整洁

"""

    desp += f"""---
### 每日提醒
- 每天至少 Git 提交一次（哪怕一行代码）
- CAD 是面试第一优先，Python 第二
- 目标：汇川/英威腾/长盈精密/立讯精密等供应链企业
- 小公司不卡大一，要的是"能干活、便宜、愿意学"

---
### {quote}

---
> 完成任务后在桌面任务面板打卡！明天见

*WorkBuddy Cloud - GitHub Actions Auto Push*
"""

    return title, desp


def send_push(key, title, desp):
    """通过Server酱推送到微信"""
    url = f"https://sctapi.ftqq.com/{key}.send"
    data = urllib.parse.urlencode({"title": title, "desp": desp}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode("utf-8"))
    return result


def main():
    # 从环境变量读取 key（GitHub Actions 用），回退到本地配置文件
    key = os.environ.get("SERVERCHAN_KEY", "").strip()

    if not key:
        # 本地模式：读配置文件
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_paths = [
            os.path.join(script_dir, "serverchan_config.json"),
            os.path.join(os.path.dirname(script_dir), ".workbuddy", "serverchan_config.json"),
            os.path.join(os.path.expanduser("~"), "WorkBuddy", "2026-07-21-00-58-04", ".workbuddy", "serverchan_config.json"),
        ]
        for cp in config_paths:
            if os.path.exists(cp):
                with open(cp, "r", encoding="utf-8") as f:
                    config = json.load(f)
                key = config.get("serverchan_key", "")
                break

    if not key:
        print("ERROR: No SERVERCHAN_KEY found in env or config files")
        return 1

    # 构建消息
    title, desp = build_message()

    print(f"Pushing: {title}")
    print(f"Content length: {len(desp)} chars")

    # 发送
    try:
        result = send_push(key, title, desp)
        if result.get("code") == 0 and result.get("data", {}).get("error") == "SUCCESS":
            print("Push SUCCESS! Message sent to WeChat.")
            return 0
        else:
            print(f"Push FAILED: {result}")
            return 1
    except Exception as e:
        print(f"Push ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
