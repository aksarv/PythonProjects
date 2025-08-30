"""
From an explanation on GeeksforGeeks (the very final bit is not done)
"""

import copy

transactions = [("E", "K", "M", "N", "O", "Y"), ("D", "E", "K", "N", "O", "Y"), ("A", "E", "K", "M"), ("K", "M", "Y"), ("C", "E", "I", "K", "O", "O")]

frequencies = {}

for t in transactions:
    for i in t:
        if i not in frequencies:
            frequencies[i] = 1
        else:
            frequencies[i] += 1

minimum_support = 3

frequent_pattern = {}

for i, f in frequencies.items():
    if f > minimum_support:
        frequent_pattern[i] = f

ordered_items = []
for t in transactions:
    t1 = []
    for i in frequent_pattern.keys():
        if i in t:
            t1.append(i)
    ordered_items.append(tuple(t1))


class Node:
    def __init__(self, item):
        self.item = item
        self.count = 0
        self.children = []


root = Node(None)
for t in ordered_items:
    curr = copy.deepcopy(root)
    for i in t:
        for child in curr.children:
            if child.item == i:
                curr = child
                curr.count += 1
                break
        else:
            curr.children.append(Node(i))
            curr = curr.children[-1]


conditional_patterns = {x: [] for x in frequent_pattern}


def get_count(curr, item, path=[]):
    if curr.item == item:
        conditional_patterns[item].append([path[1:], curr.count])
    else:
        for child in curr.children:
            get_count(child, item, path=path + [curr.item])


def max_similar_prefix(l):
    prefix = ""
    for i in range(max(len(x) for x in l)):
        try:
            if len(set([e[i] for e in l])) > 1:
                return prefix
        except IndexError:
            return prefix
        prefix += l[0][i]


for x in frequent_pattern:
    get_count(root, x)

for i, p in conditional_patterns.items():
    conditional_patterns[i].append(sum(x[1] for x in conditional_patterns[i]))
    conditional_patterns[i].append(max_similar_prefix([x[0] for x in conditional_patterns[i][:-1]]))


