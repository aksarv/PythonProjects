class Rule:
    def __init__(self, curr_state, curr_symbol, next_state, write_symbol, direction):
        self.curr_state = curr_state
        self.curr_symbol = curr_symbol
        self.next_state = next_state
        self.write_symbol = write_symbol
        self.direction = direction

    def show_rule(self):
        return f"(S{self.curr_state}, {(self.curr_symbol if self.curr_symbol != '' else '□')}) → (S{self.next_state}, {(self.write_symbol if self.write_symbol != '' else '□')}, {self.direction})"


class TuringMachine:
    def __init__(self, init_state, tape, init_pos, rules):
        self.state = init_state
        self.tape = tape
        self.tape_pos = init_pos
        self.rules = rules

    def run(self):
        run = True
        while run:
            #self.show_state()
            for rule in self.rules:
                #print("Checking rule", rule.show_rule())
                if rule.curr_state == self.state:
                    if 0 <= self.tape_pos < len(self.tape):
                        pass
                    elif self.tape_pos < 0:
                        self.tape = [""] * (-self.tape_pos) + self.tape
                        self.tape_pos -= self.tape_pos
                    else:
                        self.tape.extend([""] * (self.tape_pos - (len(self.tape) - 1)))
                    symbol = self.tape[self.tape_pos]
                    #print("Read a", symbol)
                    #print("The rule's symbol expected", rule.curr_symbol)
                    if (symbol == "" and rule.curr_symbol == "") or (symbol.isnumeric() and int(symbol) == rule.curr_symbol):
                        if rule.next_state == "HaltPositive":
                            return 1
                        elif rule.next_state == "HaltNegative":
                            return 0
                        self.tape[self.tape_pos] = rule.write_symbol
                        #print("Wrote a", rule.write_symbol)
                        self.state = rule.next_state
                        if rule.direction == "L":
                            #print("Moved left")
                            self.tape_pos -= 1
                        elif rule.direction == "R":
                            #print("Moved right")
                            self.tape_pos += 1
                        break
                        #print("Did not match this rule")

    def show_state(self):
        print("Current State:", self.state)
        print(" ".join([str(x) for x in self.tape]))
        print(" " * 2 * self.tape_pos + "^")


# Count even number of 1s
machine = TuringMachine(0, list("011"), 0,
                        [
                            Rule(0, 0, 0, 0, "R"),
                            Rule(0, 1, 1, 1, "R"),
                            Rule(0, "", "HaltPositive", "", "R"),
                            Rule(1, 0, 1, 0, "R"),
                            Rule(1, 1, 0, 1, "R"),
                            Rule(1, "", "HaltNegative", "", "R")
                        ])

result = machine.run()

if result == 0:
    print("Not an even number of 1s")
else:
    print("Even number of 1s")
