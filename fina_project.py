#coding:gbk
'''
作者：梁鹤逸
'''
#确定需要的变量
import os, sys
import jieba, codecs, math
import jieba.posseg as pseg
names={}##姓名字典
relationships={}##关系字典
line_Names = []##每段人物关系
#文本中实体识别
jieba.load_userdict("C:\\Users\\dell\\Desktop\\python综合项目\\Introduction to key people.txt")##加载字典
##C:\\Users\\dell\\Desktop\\python综合项目\\黎明破晓的街道.txt
with codecs.open("C:\\Users\\dell\\Desktop\\python综合项目\\黎明破晓的街道.txt", "r") as f:
    for line in f.readlines():
        poss=pseg.cut(line)##分词并返回该词词性
        line_Names.append([])##为新读入的一段添加人物名称列表
        for w in poss:
            if w.flag != "nr" or len(w.word) < 2:
                continue##当分词长度小于2或该词词性不为nr时认为该词不为人名
            line_Names[-1].append(w.word)##为当前段的环境增加一个人物
            if names.get(w.word) is None:
                names[w.word]=0
                relationships[w.word]={}
            names[w.word]+=1##该人物出现次数+1
#根据识别结果构建网络
for line in line_Names:##对于每一段
    for name1 in line:
        for name2 in line:##每段中的任意两个人
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:##若两人尚未同时出现则新建项
                relationships[name1][name2]= 1
            else:
                relationships[name1][name2]=relationships[name1][name2]+1##两人共同出现次数加 1
#将已经建好的names和relationships输出到文本，
#以方便 gephi 可视化处理。
#输出边的过程中可以过滤可能是冗余的边，
#这里假设共同出现次数少于10次的是冗余边，
#则在输出时跳过这样的边。
#输出的节点集合保存为 busan_node.txt ，
#边集合保存为 busan_edge.node 。
with codecs.open("C:\\Users\\dell\\Desktop\\python综合项目\\黎明破晓的街道_node.csv", "w", "gbk") as f:
    f.write("Id Label Weight\r\n")
    for name, times in names.items():
        f.write(name + " " + name + " " + str(times) + "\r\n")
with codecs.open("C:\\Users\\dell\\Desktop\\python综合项目\\黎明破晓的街道_edge.csv", "w", "gbk") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 10:
               f.write(name+" "+v+" "+str(w)+"\r\n")
