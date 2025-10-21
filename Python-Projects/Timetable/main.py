from data import *
from random import randint, choice, random
from copy import deepcopy

timetable = [
    [{r: None for r in rooms} for _ in range(7)] for __ in range(5)
]


class InfiniteGenerator:
    def __init__(self, l):
        self.l = l
        self.pointer = 0

    def get(self):
        res = self.l[self.pointer]
        self.pointer += 1
        self.pointer %= len(self.l)
        return res


class_lessons = {**y7_class_lessons, **y8_class_lessons, **y9_class_lessons, **y10_class_lessons, **y11_class_lessons, **y12_class_lessons, **y13_class_lessons}
subject_classes = y7_subject_classes
for s in [y8_subject_classes, y9_subject_classes, y10_subject_classes, y11_subject_classes, y12_subject_classes, y13_subject_classes]:
    for subject in s.keys():
        if subject in subject_classes:
            subject_classes[subject] = subject_classes[subject] + s[subject]
        else:
            subject_classes[subject] = s[subject]

class_subjects = dict((tuple(v), k) for k, v in subject_classes.items())

classes = list(class_lessons.keys())
gen = InfiniteGenerator(classes)

for day in timetable:
    for period in day:
        for room in period.keys():
            period[room] = gen.get()


def get_subject(cls):
    for c in class_subjects.keys():
        if cls in c:
            return class_subjects[c]


def fitness(tt):
    score = 0
    lessons_count = {}
    for day in tt:
        for period in day:
            for room in period.keys():
                sub = get_subject(period[room])
                if period[room] is not None and room not in subject_room[sub]:
                    score -= 1
                if period[room] in lessons_count:
                    lessons_count[period[room]] += 1
                else:
                    lessons_count[period[room]] = 1

    for lesson, count in lessons_count.items():
        if lesson is not None:
            score -= abs(count - class_lessons[lesson]) ** 2

    return score


def mutate(tt1):
    tt = deepcopy(tt1)
    rand = randint(1, 4)
    if rand == 1:
        day, period, room = randint(0, 4), randint(0, 6), choice(rooms)
        day1, period1, room1 = randint(0, 4), randint(0, 6), choice(rooms)
        while day == day1 and period == period1 and room == room1:
            day1, period1, room1 = randint(0, 4), randint(0, 6), choice(rooms)
        tt[day][period][room], tt[day1][period1][room1] = tt[day1][period1][room1], tt[day][period][room]
    elif rand == 2:
        day, period, room = randint(0, 4), randint(0, 6), choice(rooms)
        tt[day][period][room] = None
    elif rand == 3:
        day, period, room = randint(0, 4), randint(0, 6), choice(rooms)
        tt[day][period][room] = choice(classes)
    return tt


# I tried adding a small chance of accepting a worse fitness as a sort of simulated annealing approach but it didn't really work
epochs = 100000
best_tt = deepcopy(timetable)
best_fitness = -float("inf")
for i in range(epochs):
    new_tt = mutate(best_tt)
    if i % 100 == 0:
        print(str(round(i / epochs * 100, 2)) + f"%\tBest Fitness: {best_fitness}\tCurrent Fitness: {fitness(new_tt)}")
    if fitness(new_tt) > best_fitness:
        best_tt = new_tt
        best_fitness = fitness(new_tt)

print(best_tt)
