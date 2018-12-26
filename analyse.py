#!/usr/bin/env python
# encoding: utf-8


import os
import sys
import jieba
import math


names = {}
relationships = {}
line_names = []


names_set = set()
with open('dict.txt', 'r') as f:
    for line in f:
        word = line.strip()
        if word != '' and word not in names_set:
            names_set.add(word)

# check
print(names_set)


jieba.load_userdict("dict.txt")
with open('lang_ya_bang.txt', 'r') as f:
    for line in f:
        line = jieba.cut(line)
        line_names_temp = []
        for word in line:
            if word in names_set:
                line_names_temp.append(word)
                if names.get(word) is None:
                    names[word] = 1
                    relationships[word] = {}
                else:
                    names[word] += 1
        if len(line_names_temp) != 0:
            line_names.append(line_names_temp)

# check
for name, times in names.items():
    print(name, times)


for line in line_names:
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] = relationships[name1][name2] + 1


with open('node.csv', 'w') as f:
    f.write('Id Label Weight\n')
    for name, times, in names.items():
        f.write('{} {} {}\n'.format(name, name, str(times)))


with open('edge.csv', 'w') as f:
    f.write('Source Target Weight\n')
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write('{} {} {}\n'.format(name, v, str(w)))

