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

# ===== 每日任务数据（24周×7天，每天4-6条带时间估计的详细任务）=====
DAILY_TASKS = {
    # ========== 第一阶段：基础巩固 (W1-W8) ==========
    1: {
        "goal": "Python复习1-5章+CAD基础+GitHub",
        "days": [
            {"focus": "Python运算符+GitHub", "tasks": ["【25min】看小甲鱼第3章视频回顾运算符(重点:== vs =)", "【15min】IDLE练习:写5个比较表达式,打印True/False", "【25min】看小甲鱼第5章视频回顾while循环语法", "【15min】写3个while:计数1-10/累加1-100/猜数字", "【20min】登录GitHub确认learning-log仓库正常"]},
            {"focus": "条件分支+CAD入门", "tasks": ["【25min】看小甲鱼第4章条件分支视频", "【15min】练习:写成绩等级判断(if/elif/else)", "【30min】看大梦老师CAD第1集:界面认识", "【20min】CAD练习:画线/矩形/圆,熟悉命令", "【10min】Git提交"]},
            {"focus": "break语句+CAD精确绘图", "tasks": ["【25min】看小甲鱼第6章break视频", "【20min】做练习册v2 break专项前2题", "【30min】看大梦老师CAD第2集:精确绘图", "【15min】CAD:用绝对坐标画100x50矩形", "【10min】Git提交"]},
            {"focus": "continue语句+CAD极轴", "tasks": ["【25min】看小甲鱼第6章continue视频", "【20min】做练习册v2 continue专项后2题", "【25min】CAD:用极轴追踪画45度斜线", "【15min】CAD:画圆弧和椭圆", "【10min】Git提交"]},
            {"focus": "循环实战+CAD相切圆", "tasks": ["【30min】用循环重写温度采集题(列表存储+遍历)", "【25min】试写九九乘法表(嵌套循环,卡住就问)", "【25min】CAD:画3个相切圆", "【10min】Git提交"]},
            {"focus": "本周复习+图层", "tasks": ["【30min】复习本周Python:重做练习册错题", "【30min】CAD:重画轴承座(带图层分层)", "【15min】整理本周笔记", "【10min】Git提交所有代码"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息/灵活机动", "【20min】预习Python第7章列表(看视频前半段)", "【5min】看看GitHub绿色格子"]},
        ]
    },
    2: {
        "goal": "Python第7章列表+CAD修剪/标注(TRIM/HATCH/DIMLINEAR)",
        "days": [
            {"focus": "列表入门", "tasks": ["【25min】看小甲鱼第7章列表基础(创建/索引)", "【15min】IDLE练习:创建3个列表,用索引访问", "【15min】练习:列表切片[1:3],[-2:]", "【10min】Git提交"]},
            {"focus": "列表增删改+CAD", "tasks": ["【25min】学append/insert/remove/pop", "【15min】练习:对列表做10次增删改操作", "【30min】看大梦老师CAD:TRIM命令", "【10min】Git提交"]},
            {"focus": "列表遍历+CAD修剪", "tasks": ["【20min】学for循环遍历列表", "【15min】练习:遍历列表求和/求最大值", "【25min】CAD练习:TRIM修剪多余线段(画十字再修剪)", "【10min】Git提交"]},
            {"focus": "列表嵌套+CAD填充", "tasks": ["【20min】学嵌套列表(矩阵)", "【15min】练习:创建3x3矩阵,遍历打印", "【25min】CAD练习:HATCH填充剖面线", "【10min】Git提交"]},
            {"focus": "综合练习+CAD标注", "tasks": ["【25min】用列表重写学生成绩管理(存多个成绩)", "【25min】CAD练习:DIMLINEAR线性标注", "【10min】Git提交"]},
            {"focus": "本周复习+轴承座标注", "tasks": ["【25min】复习列表所有操作", "【30min】CAD:给轴承座加完整标注(尺寸+粗糙度)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习Python第8章元组", "【5min】看看本周代码量"]},
        ]
    },
    3: {
        "goal": "Python元组/字典/集合+CAD三视图练习",
        "days": [
            {"focus": "元组", "tasks": ["【25min】学元组:不可变序列", "【15min】练习:元组打包/解包", "【15min】练习:元组vs列表对比(哪些操作不行)", "【10min】Git提交"]},
            {"focus": "字典入门+CAD主视图", "tasks": ["【25min】学字典:键值对", "【15min】练习:创建字典,访问/修改/删除", "【30min】CAD:画简单零件主视图", "【10min】Git提交"]},
            {"focus": "字典进阶+CAD", "tasks": ["【20min】学字典遍历/嵌套", "【15min】练习:用字典存学生信息并遍历", "【25min】CAD:继续完善主视图", "【10min】Git提交"]},
            {"focus": "集合+CAD俯视图", "tasks": ["【20min】学集合:去重/交并差", "【15min】练习:集合运算(交集/并集/差集)", "【25min】CAD:画俯视图", "【10min】Git提交"]},
            {"focus": "综合+CAD左视图", "tasks": ["【25min】用字典+列表写通讯录(增删改查)", "【25min】CAD:画左视图,完成三视图", "【10min】Git提交"]},
            {"focus": "三视图复习", "tasks": ["【25min】CAD:检查三视图对应关系(长对正/高平齐/宽相等)", "【20min】复习元组/字典/集合", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习Python第9章函数", "【5min】整理本周笔记"]},
        ]
    },
    4: {
        "goal": "Python函数/OOP入门(类/对象/__init__)+CAD出图",
        "days": [
            {"focus": "函数", "tasks": ["【25min】学函数定义/参数/返回值", "【20min】练习:写5个函数(加法/判断奇偶/求最大值/格式化输出/计算BMI)", "【10min】Git提交"]},
            {"focus": "OOP入门", "tasks": ["【25min】学类和对象概念", "【20min】学__init__方法", "【15min】练习:写一个Dog类(name/age属性)", "【10min】Git提交"]},
            {"focus": "OOP属性方法", "tasks": ["【20min】学实例属性/类属性", "【20min】学实例方法", "【15min】练习:给Dog加bark()和sit()方法", "【10min】Git提交"]},
            {"focus": "OOP+CAD出图", "tasks": ["【20min】练习:写Student类(name/scores/avg方法)", "【30min】CAD:学习布局出图/打印设置", "【10min】Git提交"]},
            {"focus": "CAD出图+Git", "tasks": ["【25min】CAD:打印设置练习(比例/图框/标题栏)", "【20min】整理GitHub仓库README", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习OOP概念(类/对象/属性/方法)", "【25min】用类重写之前的练习(如通讯录用类封装)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习继承和封装", "【5min】看看GitHub提交记录"]},
        ]
    },
    5: {
        "goal": "Python OOP进阶(继承/封装)+异常处理",
        "days": [
            {"focus": "继承", "tasks": ["【25min】学继承:子类/父类", "【20min】练习:Dog继承Animal", "【10min】Git提交"]},
            {"focus": "多态+封装", "tasks": ["【25min】学多态和封装", "【20min】练习:写继承体系(Animal->Dog/Cat)", "【10min】Git提交"]},
            {"focus": "异常处理", "tasks": ["【25min】学try/except/finally", "【20min】练习:处理除零/索引越界/键错误", "【10min】Git提交"]},
            {"focus": "自定义异常+CAD", "tasks": ["【20min】学raise/自定义异常", "【30min】CAD:复杂零件图练习(齿轮毛坯)", "【10min】Git提交"]},
            {"focus": "综合练习", "tasks": ["【35min】用OOP+异常写银行账户系统(存取款/透支异常)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习OOP+异常", "【20min】整理代码注释", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习文件I/O", "【5min】整理笔记"]},
        ]
    },
    6: {
        "goal": "Python文件I/O+模块+CAD复杂零件图(暑假收官)",
        "days": [
            {"focus": "文件读写", "tasks": ["【25min】学open/read/write/close", "【20min】练习:写txt文件(写入3行再读回)", "【10min】Git提交"]},
            {"focus": "with语句+CAD", "tasks": ["【20min】学with自动关闭", "【15min】练习:with写文件", "【25min】CAD:画复杂零件(阶梯轴)", "【10min】Git提交"]},
            {"focus": "模块导入", "tasks": ["【20min】学import/from import", "【15min】学自己写模块(把函数拆到单独py文件)", "【10min】Git提交"]},
            {"focus": "CAD复杂零件", "tasks": ["【30min】CAD:画法兰盘完整图", "【20min】标注齐全(尺寸+公差+粗糙度)", "【10min】Git提交"]},
            {"focus": "暑假总结", "tasks": ["【25min】写暑假学习总结(Markdown)", "【20min】整理GitHub仓库结构", "【10min】Git提交"]},
            {"focus": "项目巩固", "tasks": ["【30min】用文件I/O+OOP写小型项目(记账本:存取记录到文件)", "【10min】Git提交"]},
            {"focus": "开学前启动C", "tasks": ["【25min】装Dev-C++/VSCode,看翁恺C第1集", "【20min】写第一个hello.c并编译运行", "【15min】准备开学物品", "【10min】Git提交"]},
        ]
    },
    7: {
        "goal": "C语言入门(翁恺课程)+开学报到调整时间表",
        "days": [
            {"focus": "开学报到", "tasks": ["【全天】报到/安顿宿舍", "【30min】认识同学和辅导员", "【30min】了解课程表和教室"]},
            {"focus": "C语言入门", "tasks": ["【20min】装Dev-C++或VSCode", "【25min】看翁恺C语言第1集", "【15min】写第一个hello.c并编译运行", "【10min】Git提交"]},
            {"focus": "C基础语法", "tasks": ["【25min】看翁恺第2集:变量/数据类型", "【20min】练习:声明int/float/char变量并printf打印", "【10min】Git提交"]},
            {"focus": "C输入输出", "tasks": ["【25min】看翁恺第3集:printf/scanf", "【20min】练习:scanf读入两数求和并输出", "【10min】Git提交"]},
            {"focus": "调整时间表", "tasks": ["【20min】按课表调整每日学习时间", "【15min】确定每天2-3小时学习窗口(如晚7-10点)", "【10min】Git提交"]},
            {"focus": "C运算符", "tasks": ["【25min】学C运算符(和Python对比:&&/||/!等)", "【20min】练习:算术/关系/逻辑运算各5题", "【30min】C++初探:看一节C++简介(对比C的变化)", "【10min】Git提交"]},
            {"focus": "休息+复习", "tasks": ["【自由】休息", "【25min】复习本周C内容", "【20min】C++初探:类与对象(对比C结构体,看翁恺/C++教程)", "【10min】整理笔记"]},
        ]
    },
    8: {
        "goal": "C控制流/函数/数组+Python迷你项目(学生成绩管理系统)",
        "days": [
            {"focus": "C控制流", "tasks": ["【25min】学C的if/for/while(对比Python语法差异)", "【20min】练习:for循环打印1-100,while求1-100和", "【10min】Git提交"]},
            {"focus": "C函数", "tasks": ["【25min】学C函数定义/调用/声明", "【20min】练习:写计算器函数(加减乘除4个函数)", "【10min】Git提交"]},
            {"focus": "C数组", "tasks": ["【25min】学C一维数组", "【20min】练习:数组冒泡排序", "【10min】Git提交"]},
            {"focus": "Python项目", "tasks": ["【35min】用OOP写学生成绩管理系统(增删改查)", "【10min】Git提交"]},
            {"focus": "项目完善", "tasks": ["【30min】完善成绩管理系统:加文件存储+异常处理", "【10min】Git提交"]},
            {"focus": "阶段总结", "tasks": ["【25min】第一阶段总结(梳理已学知识)", "【20min】整理所有代码和笔记", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习C指针(翁恺指针章节简介)", "【5min】看看GitHub总提交数"]},
        ]
    },
    # ========== 第二阶段：核心技能 (W9-W16) ==========
    9: {
        "goal": "C指针基础(&和*运算符/指针与数组)",
        "days": [
            {"focus": "指针概念", "tasks": ["【25min】学什么是指针(内存地址概念)", "【20min】学&取地址运算符,打印变量地址", "【10min】Git提交"]},
            {"focus": "指针使用", "tasks": ["【25min】学*解引用运算符", "【20min】练习:用指针读写变量值", "【10min】Git提交"]},
            {"focus": "指针与数组", "tasks": ["【25min】学数组名=首元素指针", "【20min】练习:用指针遍历数组", "【10min】Git提交"]},
            {"focus": "指针运算", "tasks": ["【25min】学指针加减法(p+1指向下一元素)", "【20min】练习:指针比较和算术运算", "【10min】Git提交"]},
            {"focus": "指针练习", "tasks": ["【25min】做10道指针练习题", "【20min】写swap函数(交换两个变量)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习指针基础(&/*/指针与数组)", "【20min】画内存示意图(变量/指针/数组关系)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习指针进阶(指针数组/函数指针)", "【5min】整理笔记"]},
        ]
    },
    10: {
        "goal": "C指针进阶+动态内存(malloc/calloc/free)",
        "days": [
            {"focus": "指针数组", "tasks": ["【25min】学指针数组和数组指针(区别!)", "【20min】练习:用指针数组做字符串排序", "【10min】Git提交"]},
            {"focus": "函数指针", "tasks": ["【25min】学函数指针概念和语法", "【20min】练习:用函数指针写回调(如qsort比较函数)", "【10min】Git提交"]},
            {"focus": "多级指针", "tasks": ["【25min】学二级指针", "【20min】练习:用二级指针操作二维数组", "【10min】Git提交"]},
            {"focus": "动态内存", "tasks": ["【25min】学malloc/calloc/free", "【20min】练习:动态分配数组(malloc+输入+输出+free)", "【10min】Git提交"]},
            {"focus": "内存管理", "tasks": ["【25min】学内存泄漏检测(常见错误)", "【20min】练习:动态二维数组(分配+使用+释放)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习指针进阶", "【20min】写综合指针程序(如动态通讯录)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习结构体", "【5min】整理笔记"]},
        ]
    },
    11: {
        "goal": "C结构体/文件I/O+买Arduino UNO套件",
        "days": [
            {"focus": "结构体", "tasks": ["【25min】学struct定义和使用", "【20min】练习:学生结构体(姓名/年龄/成绩)", "【10min】Git提交"]},
            {"focus": "typedef+结构体指针", "tasks": ["【20min】学typedef(给结构体起别名)", "【20min】学结构体指针(->运算符)", "【15min】练习:用指针操作结构体", "【10min】Git提交"]},
            {"focus": "C文件I/O", "tasks": ["【25min】学fopen/fread/fwrite/fclose", "【20min】练习:文件复制程序", "【10min】Git提交"]},
            {"focus": "买Arduino", "tasks": ["【30min】淘宝买Arduino UNO套件(80-120元)", "【15min】等快递期间复习C结构体", "【10min】Git提交"]},
            {"focus": "综合练习", "tasks": ["【35min】用结构体+文件写通讯录(存到文件,重启可读回)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习结构体和文件I/O", "【15min】整理本周笔记", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习Arduino(太极创客网站看入门)", "【5min】期待套件到达"]},
        ]
    },
    12: {
        "goal": "Arduino入门(Blink/数字I/O/模拟输入)",
        "days": [
            {"focus": "Arduino环境", "tasks": ["【20min】装Arduino IDE", "【20min】连UNO板,跑Blink(LED闪烁)", "【15min】了解IDE界面和基本操作", "【10min】Git提交Arduino代码"]},
            {"focus": "数字I/O", "tasks": ["【25min】学pinMode/digitalWrite/digitalRead", "【25min】练习:按键控制LED开关", "【10min】Git提交"]},
            {"focus": "模拟输入", "tasks": ["【25min】学analogRead(0-1023)", "【25min】练习:电位器调LED亮度(map函数)", "【10min】Git提交"]},
            {"focus": "串口通信", "tasks": ["【25min】学Serial.begin/Serial.print", "【20min】练习:串口打印传感器值(每秒一次)", "【10min】Git提交"]},
            {"focus": "太极创客网课", "tasks": ["【30min】看太极创客Arduino教程", "【20min】跟着做实验", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习Arduino基础(数字/模拟/串口)", "【20min】整理代码和电路图(手绘或拍照)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习传感器(HC-SR04/DHT11数据手册)", "【5min】整理笔记"]},
        ]
    },
    13: {
        "goal": "Arduino传感器(超声波HC-SR04/温湿度DHT11)+舵机SG90",
        "days": [
            {"focus": "超声波测距", "tasks": ["【25min】接HC-SR04超声波模块(trig/echo)", "【25min】写测距代码,串口显示距离(cm)", "【10min】Git提交"]},
            {"focus": "温湿度", "tasks": ["【20min】装DHT库(库管理器搜索安装)", "【25min】接DHT11,读取温湿度并串口输出", "【10min】Git提交"]},
            {"focus": "舵机控制", "tasks": ["【20min】学Servo库(Servo.h)", "【25min】用SG90做转动实验(0-180度扫描)", "【10min】Git提交"]},
            {"focus": "综合实验", "tasks": ["【30min】超声波测距+舵机联动(距离<10cm就转舵机)", "【10min】Git提交"]},
            {"focus": "数据记录", "tasks": ["【25min】温湿度定时采集(每5秒一次)", "【15min】串口输出CSV格式数据(便于复制到Excel)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习传感器(接线/代码/原理)", "【20min】整理电路图(拍照或手绘)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习LCD1602和电机驱动L298N", "【5min】整理笔记"]},
        ]
    },
    14: {
        "goal": "Arduino进阶(LCD/电机驱动L298N/PWM)+智能温控风扇项目",
        "days": [
            {"focus": "LCD显示", "tasks": ["【25min】接LCD1602(I2C模块,4根线)", "【25min】显示Hello World和传感器数据", "【10min】Git提交"]},
            {"focus": "电机驱动", "tasks": ["【25min】学L298N驱动板接线(IN1/IN2/ENA/电机)", "【25min】控制直流电机正反转", "【10min】Git提交"]},
            {"focus": "PWM调速", "tasks": ["【25min】学analogWrite/PWM原理(0-255)", "【20min】练习:PWM控制电机转速(由慢到快)", "【10min】Git提交"]},
            {"focus": "温控风扇", "tasks": ["【30min】DHT11测温->PWM控风扇(温度高转速快)", "【10min】Git提交"]},
            {"focus": "项目完善", "tasks": ["【25min】加LCD显示温度和转速档位", "【20min】加阈值报警(温度>35度蜂鸣器响)", "【10min】Git提交"]},
            {"focus": "项目文档", "tasks": ["【25min】写项目README(功能/接线图/代码说明)", "【20min】录演示视频(手机拍即可)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习电路基础(欧姆定律)", "【5min】整理笔记"]},
        ]
    },
    15: {
        "goal": "电子电路基础(欧姆定律/基尔霍夫/元件识别)+SolidWorks入门",
        "days": [
            {"focus": "欧姆定律", "tasks": ["【25min】学V=IR(电压=电流x电阻)", "【20min】练习:计算串联/并联电阻", "【10min】Git提交笔记"]},
            {"focus": "基尔霍夫", "tasks": ["【25min】学KVL(电压定律)/KCL(电流定律)", "【20min】练习:节点分析简单电路", "【10min】Git提交"]},
            {"focus": "元件识别", "tasks": ["【25min】学电阻/电容/电感/二极管识别", "【20min】练习:读色环电阻(4环/5环各5个)", "【10min】Git提交"]},
            {"focus": "SolidWorks入门", "tasks": ["【25min】装SolidWorks(学生教育版)", "【25min】学草图绘制(直线/圆/矩形/约束)", "【10min】Git提交"]},
            {"focus": "SolidWorks拉伸", "tasks": ["【25min】学拉伸/旋转特征", "【25min】画一个简单零件3D(长方体打孔)", "【10min】Git提交"]},
            {"focus": "本周复习", "tasks": ["【25min】复习电路基础(V=IR/KVL/KCL)", "【20min】整理元件识别表(电阻色环/电容标称)", "【10min】Git提交"]},
            {"focus": "休息+预习", "tasks": ["【自由】休息", "【20min】预习PCB设计(立创EDA)", "【5min】整理笔记"]},
        ]
    },
    16: {
        "goal": "PCB设计入门(立创EDA)+阶段总结",
        "days": [
            {"focus": "立创EDA入门", "tasks": ["【25min】注册立创EDA(在线版)", "【25min】学原理图绘制(放元件/连线/标号)", "【10min】Git提交"]},
            {"focus": "PCB布局", "tasks": ["【25min】学PCB布局/布线规则", "【25min】画LED闪烁板原理图(555或Arduino)", "【10min】Git提交"]},
            {"focus": "PCB完善", "tasks": ["【20min】加丝印/焊盘", "【20min】导出Gerber文件", "【15min】了解打样流程(嘉立创免费打样)", "【10min】Git提交"]},
            {"focus": "阶段总结", "tasks": ["【25min】总结第二阶段(学了什么/做了什么)", "【20min】整理GitHub仓库(分类:Python/C/Arduino/CAD)", "【10min】Git提交"]},
            {"focus": "项目规划", "tasks": ["【25min】规划第三阶段项目(智能环境监测站)", "【20min】列硬件清单(还需要买什么模块)", "【10min】Git提交"]},
            {"focus": "代码整理", "tasks": ["【25min】整理所有代码(加注释/分文件夹)", "【20min】写文档(每个项目的README)", "【10min】Git提交"]},
            {"focus": "休息+准备", "tasks": ["【自由】休息", "【20min】准备项目材料(确认硬件齐全)", "【5min】期待项目阶段"]},
        ]
    },
    # ========== 第三阶段：项目与求职 (W17-W24) ==========
    17: {
        "goal": "项目规划(智能环境监测站:Arduino+传感器+LCD+SD卡+Python可视化)",
        "days": [
            {"focus": "需求文档", "tasks": ["【30min】写需求文档:功能(温湿度/光照采集+LCD显示+SD卡存储+串口上传)", "【15min】确定技术路线(Arduino下位机+Python上位机)", "【10min】Git提交"]},
            {"focus": "硬件确认", "tasks": ["【20min】确认传感器/SD卡/LCD齐全(缺少的淘宝下单)", "【25min】画系统框图(手绘或draw.io)", "【10min】Git提交"]},
            {"focus": "软件架构", "tasks": ["【25min】设计代码架构(分模块:采集/显示/存储/通信)", "【20min】画数据流图(传感器->Arduino->串口->Python)", "【10min】Git提交"]},
            {"focus": "数据格式", "tasks": ["【20min】设计CSV存储格式(时间戳,温度,湿度,光照)", "【20min】设计串口通信协议(数据帧:起始符+数据+校验)", "【15min】Git提交"]},
            {"focus": "开发计划", "tasks": ["【25min】制定3周开发时间表(W18硬件/W19上位机/W20完善)", "【15min】分配每天具体任务", "【10min】Git提交"]},
            {"focus": "环境搭建", "tasks": ["【25min】搭开发环境(Arduino库安装/Python包安装)", "【20min】测试各传感器模块能正常读数", "【10min】Git提交"]},
            {"focus": "休息+准备", "tasks": ["【自由】休息", "【20min】复习项目相关代码(Arduino传感器/Python串口)", "【5min】准备开始编码"]},
        ]
    },
    18: {
        "goal": "项目硬件实现(组装+传感器代码+数据记录)",
        "days": [
            {"focus": "硬件组装", "tasks": ["【30min】组装电路(面包板/杜邦线,按框图接线)", "【20min】接好所有传感器(DHT11/光敏/SD卡/LCD)", "【10min】拍照记录接线"]},
            {"focus": "传感器代码", "tasks": ["【25min】写温湿度采集代码(DHT11)", "【20min】写光照采集代码(光敏电阻analogRead)", "【10min】Git提交"]},
            {"focus": "LCD显示", "tasks": ["【25min】LCD显示实时数据(温湿度/光照值)", "【15min】加滚动显示(数据多时轮播)", "【10min】Git提交"]},
            {"focus": "SD卡记录", "tasks": ["【25min】写SD卡数据存储(SPI库)", "【20min】CSV格式定时记录(每分钟一条)", "【10min】Git提交"]},
            {"focus": "数据校验", "tasks": ["【25min】测试数据完整性(读SD卡CSV验证)", "【15min】处理异常值(传感器读失败时记录ERROR)", "【10min】Git提交"]},
            {"focus": "联调测试", "tasks": ["【30min】全系统联调(采集->显示->存储->串口)", "【15min】修复bug", "【10min】Git提交"]},
            {"focus": "休息+整理", "tasks": ["【自由】休息", "【20min】整理代码(加注释)", "【5min】准备上位机开发"]},
        ]
    },
    19: {
        "goal": "Python上位机(串口pyserial+matplotlib绘图)+文档+演示视频",
        "days": [
            {"focus": "串口通信", "tasks": ["【25min】学pyserial库(pip install pyserial)", "【25min】读Arduino串口数据并打印", "【10min】Git提交"]},
            {"focus": "数据解析", "tasks": ["【25min】解析串口数据(按协议拆分字段)", "【20min】存入列表(时间/温度/湿度/光照)", "【10min】Git提交"]},
            {"focus": "matplotlib绘图", "tasks": ["【25min】学matplotlib基础(折线图)", "【25min】实时绘制温湿度曲线(动画更新)", "【10min】Git提交"]},
            {"focus": "UI界面", "tasks": ["【25min】用tkinter做简单UI(窗口+图表区+数据表)", "【20min】显示图表+实时数据表格", "【10min】Git提交"]},
            {"focus": "项目文档", "tasks": ["【25min】写README文档(功能/硬件清单/使用说明/截图)", "【15min】写使用说明(如何接线/如何运行)", "【10min】Git提交"]},
            {"focus": "演示视频", "tasks": ["【25min】录项目演示视频(手机拍,3-5分钟)", "【15min】上传B站或存本地", "【10min】Git提交"]},
            {"focus": "休息+整理", "tasks": ["【自由】休息", "【20min】整理项目(检查代码/文档)", "【5min】准备作品集"]},
        ]
    },
    20: {
        "goal": "项目完善+GitHub作品集(GitHub Pages主页)",
        "days": [
            {"focus": "代码优化", "tasks": ["【25min】优化代码结构(拆分模块/去掉冗余)", "【20min】加详细注释(每个函数写docstring)", "【10min】Git提交"]},
            {"focus": "README完善", "tasks": ["【25min】写专业README(项目简介/功能/截图/GIF演示)", "【15min】加安装和使用说明", "【10min】Git提交"]},
            {"focus": "GitHub Pages", "tasks": ["【25min】开启GitHub Pages(Settings->Pages)", "【25min】设计个人主页框架(HTML/CSS)", "【10min】Git提交"]},
            {"focus": "主页内容", "tasks": ["【25min】写自我介绍(教育背景/技能栈/项目)", "【20min】展示项目(截图+链接+描述)", "【10min】Git提交"]},
            {"focus": "项目展示", "tasks": ["【25min】在主页展示环境监测站项目", "【20min】加演示视频链接(B站或YouTube)", "【10min】Git提交"]},
            {"focus": "最终检查", "tasks": ["【25min】检查所有链接有效", "【15min】测试主页在不同浏览器显示正常", "【10min】Git提交"]},
            {"focus": "休息+准备", "tasks": ["【自由】休息", "【20min】准备写简历(看优秀简历模板)", "【5min】整理作品集"]},
        ]
    },
    21: {
        "goal": "简历制作+自我介绍练习",
        "days": [
            {"focus": "简历框架", "tasks": ["【25min】确定简历结构(一页纸:基本信息/教育/技能/项目/经历)", "【20min】写基本信息+教育背景", "【10min】Git提交"]},
            {"focus": "技能描述", "tasks": ["【25min】写技能清单(Python/C/AutoCAD/Arduino/SolidWorks)", "【20min】突出项目经验(环境监测站)", "【10min】Git提交"]},
            {"focus": "项目描述", "tasks": ["【25min】用STAR法则写项目(情境/任务/行动/结果)", "【20min】量化成果(如'采集1万+数据点/实时绘图/3模块联动')", "【10min】Git提交"]},
            {"focus": "简历完善", "tasks": ["【25min】润色语言(简洁有力,动词开头)", "【20min】调整排版(导出PDF,一页纸)", "【10min】Git提交"]},
            {"focus": "自我介绍", "tasks": ["【25min】写1分钟自我介绍稿(背景+技能+项目+为什么想来)", "【20min】对着镜子练3遍(录音回听)", "【10min】Git提交"]},
            {"focus": "模拟面试", "tasks": ["【25min】准备常见面试问题(为什么选这个专业/最大的困难等)", "【20min】找人模拟面试(或自问自答录视频)", "【10min】Git提交"]},
            {"focus": "休息+准备", "tasks": ["【自由】休息", "【20min】准备投递(注册招聘平台)", "【5min】整理简历终稿"]},
        ]
    },
    22: {
        "goal": "公司调研+开始投递(BOSS直聘/实习僧,目标10-15家)",
        "days": [
            {"focus": "注册平台", "tasks": ["【20min】注册BOSS直聘/实习僧", "【20min】完善个人资料(教育/技能/项目)", "【20min】上传简历PDF"]},
            {"focus": "公司调研", "tasks": ["【25min】调研汇川/英威腾/长盈精密/立讯精密等10家", "【20min】整理目标公司清单(Excel:公司/岗位/要求/薪资)", "【10min】记录岗位要求"]},
            {"focus": "投递Day1", "tasks": ["【30min】投3-5家保底方向(CAD绘图/生产工艺,远程优先)", "【20min】写打招呼话术(简短有力:我是谁+会什么+想做什么)", "【10min】记录投递"]},
            {"focus": "投递Day2", "tasks": ["【30min】投3-5家嵌入式方向(Arduino/C开发)", "【20min】针对岗位调整简历(突出相关技能)", "【10min】记录投递"]},
            {"focus": "投递Day3", "tasks": ["【25min】投2-3家Python/硬件测试方向", "【20min】跟进之前投递(发消息问进度)", "【10min】记录投递"]},
            {"focus": "投递总结", "tasks": ["【25min】整理投递清单(公司/岗位/日期/状态)", "【20min】准备面试(复习技术知识)", "【10min】Git提交进度"]},
            {"focus": "休息+准备", "tasks": ["【自由】休息", "【20min】准备面试(看面经)", "【5min】整理投递记录"]},
        ]
    },
    23: {
        "goal": "面试准备(技术面+行为面)+持续投递",
        "days": [
            {"focus": "技术面C", "tasks": ["【25min】复习C常考:指针/内存/结构体(手写代码)", "【25min】准备代码题:手写swap/strlen/strcpy/冒泡排序", "【10min】Git提交"]},
            {"focus": "技术面Python", "tasks": ["【25min】复习Python常考:列表/字典/OOP/装饰器", "【25min】准备代码题:反转字符串/列表去重/字典排序", "【10min】Git提交"]},
            {"focus": "技术面Arduino", "tasks": ["【25min】复习Arduino/传感器知识(pinMode/analogRead/PWM)", "【25min】准备项目讲解(5分钟:需求/方案/实现/难点)", "【10min】Git提交"]},
            {"focus": "行为面准备", "tasks": ["【25min】学STAR法则回答行为面问题", "【25min】准备8个故事:困难/合作/学习/失败/领导/创新/时间管理/自我驱动", "【10min】Git提交"]},
            {"focus": "模拟面试", "tasks": ["【30min】模拟技术面(自问自答,录音回听)", "【20min】模拟行为面(STAR故事练习)", "【10min】Git提交"]},
            {"focus": "持续投递", "tasks": ["【25min】再投5家(拓展新公司/新岗位)", "【20min】跟进入投递状态(回复HR消息)", "【10min】Git提交"]},
            {"focus": "休息+复盘", "tasks": ["【自由】休息", "【25min】复盘模拟面试(找薄弱点)", "【5min】整理笔记"]},
        ]
    },
    24: {
        "goal": "积极求职+寒假面试,目标拿到实习offer",
        "days": [
            {"focus": "积极面试", "tasks": ["【全天】参加所有面试机会", "【30min】面完立即复盘(记录问题和回答)", "【10min】Git提交"]},
            {"focus": "持续投递", "tasks": ["【30min】持续投递不放弃(每天投3-5家)", "【20min】拓展新岗位(小红书/牛客/脉脉找机会)", "【10min】Git提交"]},
            {"focus": "面试改进", "tasks": ["【25min】根据面试反馈改进薄弱点", "【25min】加强练习(手写代码/项目讲解)", "【10min】Git提交"]},
            {"focus": "寒假准备", "tasks": ["【25min】准备去深圳/广州(订车票/找住宿)", "【20min】找住宿(青旅/短租/同学借住)", "【10min】Git提交"]},
            {"focus": "积极求职", "tasks": ["【25min】主动联系HR(发消息/打电话问进度)", "【20min】争取面试机会(表达强烈意愿)", "【10min】Git提交"]},
            {"focus": "目标达成", "tasks": ["【30min】拿到offer!确认入职细节(时间/薪资/地点/住宿)", "【20min】回复offer接受邮件", "【10min】Git提交"]},
            {"focus": "庆祝+总结", "tasks": ["【自由】庆祝拿到offer!", "【25min】总结6个月历程(写博客或发B站)", "【10min】更新GitHub(加实习经历)"]},
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
    days = week_data.get("days", [])
    if dow < len(days):
        today_task = days[dow]
    else:
        today_task = {"focus": "灵活安排", "tasks": ["复习巩固", "Git提交"]}
    week_goal = week_data.get("goal", "按计划学习")

    quote = QUOTES[day_num % len(QUOTES)]

    # 计算今日总时长
    total_min = 0
    for task in today_task.get("tasks", []):
        import re
        m = re.search(r'【(\d+)min】', task)
        if m:
            total_min += int(m.group(1))
    hours = total_min // 60
    mins = total_min % 60
    time_str = f"{hours}小时{mins}分钟" if hours > 0 else f"{mins}分钟"

    # 标题
    title = f"Day{day_num} | W{week_num} {phase_name} | {today_task.get('focus', '学习')}"

    # 正文
    desp = f"""## {date_str} | 第{week_num}周/24 | {phase_name} | 总进度 {pct}%

---

### 本周目标
{week_goal}

---

### 今日重点: {today_task.get('focus', '学习')}
> 预计学习时长: {time_str} | 共{len(today_task.get('tasks', []))}项任务

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
