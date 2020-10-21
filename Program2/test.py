# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zed
@Version        :  V1.0.0
------------------------------------
@File           :  program1.py
@Description    :  Calculate the Mean and Standard deviation of set of n numbers
@CreateTime     :  2020-10-5 10:16
------------------------------------
@ModifyTime     :
"""
import math


class item(object):
    def __init__(self, data):
        self.data = data
        self.next = None


class SLinkList(object):
    def __init__(self, size=100):
        self.link = [item(None) for i in range(size + 1)]  # 申请size大小的节点空间[0,1,2,...,size]，其中下标0的节点作为头结点
        self.link[0].next = None  # 表示空表
        self.link[0].space = 1  # 指向第一个节点，因为初始化时第一个节点为空闲节点
        i = 1
        while i < size:
            self.link[i].next = i + 1  # 利用空闲节点连成一个新的表，并且头结点的space始终指向下一个空闲的节点
            i += 1
        self.link[i].next = None  # 空闲表尾指向None
        self.length = 0  # 链表长度
        self.rear = 0  # 表尾指针


    def createSLinkList_R(self, data):
        if self.length > 0:  # 非空表无需创建
            print("THIS SLINKLIST IS NOT NULL")
            return
        for each in data:
            if not self.append(each):
                print("CreateR: NO SPACE!")
                return


    def locateElement(self, data):
        i = self.link[0].next
        while i and self.link[i] != data:
            i = self.link[i].next
        return i


    def malloc_SL(self):
        i = self.link[0].space
        if self.link[0].space:
            self.link[0].space = self.link[i].next
        return i


    def free_SL(self, k):
        self.link[k].data = None
        self.link[k].next = self.link[0].space
        self.link[0].space = k


    def append(self, data):
        node_index = self.malloc_SL()
        if not node_index:
            print("Append: NO SPACE!")
            return False
        self.link[node_index].data = data
        self.link[node_index].next = None
        self.link[self.rear].next = node_index
        self.rear = node_index
        self.length += 1
        return node_index


    def traversal(self):
        print("DATA:\t", end='')
        index = self.link[0].next
        while index:
            if self.link[index].next is not None:
                print(self.link[index].data, end=' , ')
            else:
                print(self.link[index].data)
            index = self.link[index].next


    def detail(self):
        print("\nDETAIL:")
        index = self.link[0].next
        count = 1
        while index:
            print("SN:\t%d\tDATA:\t%s\tADDR:\t%d\tNEXT:\t%s" % (count, self.link[index].data, index, str(self.link[index].next)))
            index = self.link[index].next
            count += 1
        print("Length:\t%d\nRear:\t%d\n" % (self.length, self.rear))


    def mean(self):
        length = self.length
        sum = 0
        index = self.link[0].next
        while index:
            sum += self.link[index].data
            index = self.link[index].next
        return sum / length


    def standardDeviation(self):
        avg = self.mean()
        length = self.length
        index = self.link[0].next
        sumMiddle = 0
        while index:
            sumMiddle += (self.link[index].data - avg) ** 2
            index = self.link[index].next
        return math.sqrt(sumMiddle / (length - 1))


if __name__ == '__main__':
    SL = SLinkList()
    inputList = input("INPUT DATA(split with ,) :\t").split(",")
    data_str = [float(inputList[i]) for i in range(len(inputList))]
    SL.createSLinkList_R(data_str)
    SL.traversal()
    while True:
        opt = input("\nInput a number： 1. Calculate Mean 2. Calculate Standard Deviation  3. View the linked list structure 4. Exit\nOPTION:\t")
        if opt == '1':
            print("Mean: %.2f" % SL.mean())
        elif opt == '2':
            print("Standard Deviation %.2f" % SL.standardDeviation())
        elif opt == '3':
            SL.detail()
        elif opt == '4':
            break
        else:
            print("Re-Input a number !")