#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Anliu

import os,sys,json,time
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  #环境变量
sys.path.append(BASE_DIR)
from atm import atm

goods_list = {
    "1":{"icar":280000},
    "2":{"ipad":6888},
    "3":{"iphone":5888},
    "4":{"mihone":1999},
    "5":{"mi fan":19},
    "6":{"hong mi":999},
    "7":{"hat":9},
    "8":{"pen":7},
    "9":{"wrap":38}
}
curr_user = '' #当前用户
goods = []  #购物车列表

def print_goodslist():
    '''
    实现打印商品列表功能。
    :return:
    '''

    print("Supermarket Goods List:")
    print("\t%-7s%-10s%-10s" %("商品号","商品名","价格"))
    for i in goods_list:
        for j in goods_list[i]:
            print("\t%-10s%-13s%-13s"%(i,j,goods_list[i][j]),end='\n')


def showcar(data):
    '''
    打印购物车列表
    :param data: 商品列表
    :return: 购物车结算金额
    '''

    print("你的购物车列表：")
    sum = 0
    for i in data:
        for j in i:
            print("商品名：%-10s  价格：%s元" % (j, i[j]))
            sum += i[j]
    print("\t\t\t\t合计：%s元" % sum)
    return int(sum)

#高阶+嵌套

def auth(data):   # data = curr_user
    '''
    购物车装饰器，实现认证用户功能，记录登录状态，重复购物不用再次输入账号
    :param data: 被装饰函数的内存地址对象。
    :return: out_wrapper内存地址对象
    '''

    def out_wrapper(func):    #  func = shopcat

        def wrapper(*args,**kwargs):    # var = name

            if data == '':
                username = input("Enter you username:").strip()
                passwd = input("Enter you password:").strip()
                if os.path.isfile(BASE_DIR + '/accounts/'+username+'.json'):  #首先从用户列表中查找是否存在该用户
                    with open(BASE_DIR + '/accounts/'+username+'.json', 'r') as f:
                        user = json.load(f)
                        print(user)
                    if username == user["username"] and passwd == user["password"]:
                        func(*args, **kwargs)  # shopcat(name)
                        return username  #返回登录用户
                    else:print("password is wrong,exit");exit(2)
                else:print("user is not exest,exit");exit(1)
            else:
                func(*args, **kwargs)
                return curr_user  # 返回登录用户
        return wrapper
    return out_wrapper


@auth(curr_user)   #@auth(curr_user)   ==> shopcat(curr_user) = auth(shopcat)(curr_user)
                   #shopcat = auth(shopcat)  ===> out_wrapper(shopcat)
                   #shopcat = wrapper  ===> shopcat(name) ===>wrapper(name)
def shopcar(name): #调运被装饰函数，本质是在调运装饰器，从装饰入手分析
    '''
    实现构造购物车功能
    :param name: 商品名
    :return: null
    '''

    goods.append(name)
    #return username

#shopcar("aaa")

def writelog(filename,lines):
    '''
    构造日志实现上品列表添加，用户名当文件名
    :param filename: 用户名
    :param lines: 商品列表
    :return:
    '''

    with open(filename,'a',encoding='utf8') as f:
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        for i in lines:
            for j in i:
                f.write("%s 购买：%-10s  价格：%s元\n" % (curr_time,j, i[j]))

def man_shop():
    '''
    商品选择
    :return:
    '''

    while True:
        print_goodslist()
        choise = input("请选择你要购买的商品号（按q返回上一层,c查看购物车）：").strip()
        if choise and choise in goods_list:
            global curr_user #定义为全局变量，目的用户输入一次账号就记住了
            curr_user = shopcar(goods_list[choise])  #usermame--->shopcat的返回值
            if curr_user:print("加入购物车成功")
        elif choise == 'q':break
        elif choise == 'c':
            bill = showcar(goods)
            step2 = input("结算按1，取消按2：")
            if step2 == "1":
                if curr_user != '':  #判断购物车为空时，第一次没有用户登录
                    k = atm.api_payment(curr_user, bill)  # 调用atm接口扣款
                    if k != "fail":
                        writelog(BASE_DIR + '/logs/' + curr_user + '.log', goods)  # 记录购物清单日志
                        with open(BASE_DIR + '/logs/' + curr_user + '.log','a',encoding='utf8') as f:
                            f.write("\t\t\t\t\t你目前的余额：%s\n" %k)
                        goods.clear()  # 结账成功清空购物车
                    break
                else:
                    print("购物车为空，请购买商品后再结算。")
        else:
            print("你选择的商品不存在，请重新选择:")




