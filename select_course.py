# -*- coding: utf-8 -*-
# @Time    : 2020-03-01 18:02
# @Author  : lcp and ybn
# @FileName: select_course.py
# @Usage: 抢课软件（仅限哈工程!）
# code
import getopt
import os
import random
import ssl
import sys
import time

import requests
from bs4 import BeautifulSoup
from requests import session

# 配置requests
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

# 默认配置
_username = "2017061124"
_password = -1
halt_time = 10
bi_xiu_classes = {

}
xuan_xiu_classes = {
    #"MATLAB与科学计算": "201920202012725",
    "区块链技术": "201920202012578"
}
gong_xuan_classes = {
    "创新创业领导力": "201920202007592",
    "经济学百年": "201920202007597",
    "创新创业工程实践": "201920202007614",
    "大学生创业基础（网络）": "201920202007622",
    "创践-大学生创新创业实务（网络）": "201920202007623",
    "设计创意生活（网络）": "201920202007624"
}
kua_zhuan_ye_classes = {

}
xuan_ke_oper_urls = [
    "https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/bxxkOper",  # 必修选课
    "https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/xxxkOper",  # 选修选课
    "https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/fawxkOper",  # 跨专业选课
    "https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper"  # 公选课选课
]

os.system("cls")

opts, args = getopt.getopt(sys.argv[1:], '-u:-p:-t:', ['username=', 'password=', 'halt_time='])
# print(opts)
for opt_name, opt_value in opts:
    if opt_name in ('-u', '--username'):
        _username = opt_value
        # print(opt_value)
    if opt_name in ('-p', '--password'):
        _password = opt_value
        # print(opt_value)
    if opt_name in ('-t', '--halt_time'):
        halt_time = opt_value
if _password == -1:
    print("未输入密码且无默认密码，程序退出！")
    sys.exit(0)

print("*****************************")
print("请选择抢课大类的序号:")
print("1.必修课程(待完成)")
print("2.选修课程")
print("3.跨专业选课(待完成)")
print("4.公选课选课")
print("*****************************")

choice = input("请输入序号:")

os.system("cls")
if choice == "1":
    print("您选择了必修课程大类!")
    Online_classes = bi_xiu_classes
if choice == "2":
    print("您选择了选修课程大类!")
    Online_classes = xuan_xiu_classes
if choice == "3":
    print("您选择了跨专业选课大类!")
    Online_classes = kua_zhuan_ye_classes
if choice == "4":
    print("您选择了公选课课程大类!")
    Online_classes = gong_xuan_classes

if len(Online_classes) == 0:
    os.system("cls")
    print("没有设置课程信息映射字典，程序退出!")
    exit(1)

xuan_ke_url = xuan_ke_oper_urls[int(choice) - 1]



print("正在为{}抢以下课程(5秒后开始):".format(_username))
print("*****************************")
for i in Online_classes.keys():
    print(i)
print("*****************************")

time.sleep(5)
os.system("cls")
print("开始抢课", "\n")

login_url = "https://cas-443.wvpn.hrbeu.edu.cn/cas/login?service=https%3A%2F%2Fwvpn.hrbeu.edu.cn%2Fusers%2Fauth%2Fcas%2Fcallback%3Furl"
dir_url = "https://cas-443.wvpn.hrbeu.edu.cn/cas/login?service=https%3A%2F%2Fehome.wvpn.hrbeu.edu.cn%2Fcas"
login_data = {
    'username': _username,
    'password': _password,
    '_eventId': 'submit',
    'submit': '登 录'
}

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4056.0 Safari/537.36 Edg/82.0.432.3"
}

s = session()

# 这是{times:0}不知道什么的转换
cookie = {
    'MESSAGE_TICKET': "%7B%22times%22%3A0%7D"
}

# 获取原生网页，便于获取原生cookie
r = s.get(login_url, headers=header, cookies=cookie, verify=False)

# 将hidden的内容输入data
soup = BeautifulSoup(r.text, 'html.parser')
hidden_data = soup.find_all(type='hidden')
for input in hidden_data:
    name = input['name']
    value = input['value']
    login_data[name] = value
    # print(name + " " + value)

# 登录统一认证
r = s.post(dir_url, headers=header, cookies=cookie, data=login_data, verify=False)

# 首先进入办事中心
affair_center_url = "https://one.wvpn.hrbeu.edu.cn/taskcenter/workflow/index"
r = s.get(affair_center_url, headers=header, verify=False)
# 进入业务办理确认界面（需要此界面cookies!）
r = s.get("https://one.wvpn.hrbeu.edu.cn/infoplus/form/BKKBCX-XS/start", headers=header, verify=False)
# 进入课表查询
r = s.get("https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xskb/xskb_list.do", headers=header, verify=False)

# 进入选课界面
# https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/bxxkOper   必修选课
# https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/xxxkOper   选修选课
# https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/fawxkOper  跨专业选课
# https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper    公选课选课

choose_course_url = "https://edusys.wvpn.hrbeu.edu.cn/jsxsd/xsxk/xsxk_index.do?jx0502zbid=A3E5508792C848F1B862359B430FF22A"
r = s.get(choose_course_url, headers=header, verify=False)

# halt_time = 10
is_complete = False
false_judge_dict = {
    "选课失败：此课堂选课人数已满！": False,
    "选课失败：当前教学班已选择！": True,
    "选课失败：此课程已选！": True
}
select_list = [False for i in range(len(Online_classes))]

round = 1

try:
    while is_complete is False:
        print("******************** 第 {} 轮 ********************".format(round))
        # 在运行过程中，只要有一门没有抢到，则会变为False
        is_complete = True
        for index, [key, value] in enumerate(Online_classes.items()):
            # 已经抢到的课程不会再抢
            if select_list[index] is True:
                continue
            r = s.post(xuan_ke_url, data={"jx0404id": value})
            return_data = r.text

            return_data = return_data.replace("false", "False")
            return_data = return_data.replace("true", "True")
            return_data = eval(return_data)

            print("正在请求\"{}\"，结果是:{}".format(key, r.text))

            if return_data["success"] is True:
                select_list[index] = True
            else:
                select_list[index] = false_judge_dict[return_data["message"]]

                # 如果false，且未抢到课，标志位设置为False
                if false_judge_dict[return_data["message"]] is False:
                    is_complete = False
                else:
                    # 如果false，但是是你已经抢到了这门课，则实际已完成
                    select_list[index] = True

            time.sleep(random.random() * halt_time)

        round = round + 1
    print("\n\n全部课程抢课完毕!!!")
except Exception as e:
    print(e)
finally:
    # 即使keyboardInterrupt也能看抢课结果
    print("抢课小结:")
    for index, course in enumerate(Online_classes.keys()):
        print(f'{course}\t\t{"完成" if select_list[index] else "未完成"}')
        
    print("\n\n\n")
