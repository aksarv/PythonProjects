"""
Very simple but surprisingly relatively good story generator
"""

import os
import random

books = []

for f in os.listdir("path/to/archive (2)"):
    if f.endswith(".txt"):
        books.append(open("path/to/archive (2)/" + f, "r").read().split())

words = {}

for book in books:
    for i in range(len(book) - 2):
        wds = (book[i], book[i + 1])
        next = book[i + 2]
        if wds not in words:
            words[wds] = [next]
        else:
            words[wds].append(next)

start = random.choice(list(words.keys()))
while not start[0].isalpha() or not start[0][0].isupper():
    start = random.choice(list(words.keys()))

story = list(start)
count = 0
max_count = 20
while count < max_count:
    story.append(random.choice(words[(story[-2], story[-1])]))
    if story[-1].endswith("."):
        count += 1

print(" ".join(story))
