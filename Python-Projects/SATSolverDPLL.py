# I think it works (hopefully)

import copy


class Literal:
    def __init__(self, name, negated):
        self.name = name
        self.value = None
        self.negated = negated

    def truthy(self):
        if self.value is not None:
            return self.value != self.negated

    def __str__(self):
        return ("¬" if self.negated else "") + f"({self.name}, {str(self.value)})"


class SubClause:
    def __init__(self, *args):
        self.literals = list(args)

    def __str__(self):
        return " ∨ ".join(str(literal) for literal in self.literals)


class Clause:
    def __init__(self, *args):
        self.subclauses = list(args)

    def __str__(self):
        return " ∧ ".join("(" + str(subclause) + ")" for subclause in self.subclauses)


def DPLL(clause):
    print(clause)
    while True:
        for i, subclause in enumerate(clause.subclauses):
            if len(subclause.literals) == 1:
                unit = subclause.literals[0]
                unit.value = True
                newClause = []
                for j, subclause2 in enumerate(clause.subclauses):
                    if i != j:
                        if any((literal.name == unit.name) and (literal.negated == unit.negated) for literal in subclause2.literals):
                            continue
                        newSubClause = []
                        for literal in subclause2.literals:
                            if literal.name == unit.name and literal.negated == (not unit.negated):
                                continue
                            newSubClause.append(literal)
                        newClause.append(SubClause(*newSubClause))
                break
        else:
            break
        clause = copy.deepcopy(Clause(*newClause))

    literalDict = {}
    for subclause in clause.subclauses:
        for literal in subclause.literals:
            if literal.name not in literalDict:
                literalDict[literal.name] = [literal]
            else:
                literalDict[literal.name].append(literal)

    for literal in literalDict:
        literalDict[literal] = (all(l.negated for l in literalDict[literal]) or not any(l.negated for l in literalDict[literal])) and len(literalDict[literal]) > 1

    newClause = []
    for subclause in clause.subclauses:
        valid = True
        for literal in subclause.literals:
            if literalDict[literal.name]:
                valid = False
                break
        if valid:
            newClause.append(subclause)

    clause = copy.deepcopy(Clause(*newClause))

    print(clause)

    if not clause:
        return True

    valid = True
    for subclause in clause.subclauses:
        seenTruthy = False
        for literal in subclause.literals:
            if literal.truthy() or literal.truthy() is None:
                if literal.truthy():
                    seenTruthy = True
                break
        else:
            return False
        if not seenTruthy:
            valid = False

    if valid:
        return True

    backtrackLiteral = None
    for subclause in clause.subclauses:
        for literal in subclause.literals:
            if literal.value is None:
                backtrackLiteral = literal.name
                break

    clauseLeft = copy.deepcopy(clause)
    for subclause in clauseLeft.subclauses:
        for literal in subclause.literals:
            if literal.name == backtrackLiteral:
                literal.value = True

    clauseRight = copy.deepcopy(clause)
    for subclause in clauseRight.subclauses:
        for literal in subclause.literals:
            if literal.name == backtrackLiteral:
                literal.value = False

    return DPLL(clauseLeft) or DPLL(clauseRight)


print(
    DPLL(
        Clause(
            SubClause(
                Literal("A", True),
                Literal("B", True),
            ),
            SubClause(
                Literal("A", False),
                Literal("C", True),
            )
        )
    )
)

