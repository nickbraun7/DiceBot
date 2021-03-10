#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class roll:
    def __init__(self, dice):
        self.num = int(dice[0]) #number of dice
        self.die = int(dice[1]) #value of dice
        self.mod = dice[2] if dice[2] else "" #modifier

        self.ls = [] #list of all dice rolls
        self.total = 0 #total of dice rolls
        self.crit = "" #conditional for specific events

    def dnd(self):
        if self.die == 20:
            x = random.randint(1, self.die)
            self.ls.append(str(x))
            self.total += x

            if x == 20:
                self.crit = " - ***CRITICAL SUCCESS***"
            elif x == 1:
                self.crit = " - ***CRITICAL FAILURE***"
        else:
            for i in range(self.num):
                x = random.randint(1, self.die)
                self.ls.append(str(x))
                self.total += x

        if self.mod:
            sym = self.mod[0]
            val = int(self.mod[1:])
            self.total += val if sym == "+" else -val

        return self.total, self.mod, self.ls, self.crit

    def shadow_run(self):
        g_total = 0 #total for zeros
        for i in range(self.num):
            x = random.randint(1, 6)
            self.ls.append(str(x))

            if x >= 5:
                self.total += 1
            elif x == 1:
                g_total += 1

        if g_total > (self.num / 2):
            self.crit = " - ***GLITCH***"

        return self.total, "", self.ls, self.crit

    def tephra(self):
        while True:
            x = random.randint(1, 12)
            self.ls.append(str(x))
            self.total += x
            
            if x != 12:
                break

        if self.total == 1:
            self.crit = " - ***FAIL***"

        if self.mod:
            sym = self.mod[0]
            val = int(self.mod[1:])

            if self.crit:
                if sym == "-":
                    self.total -= val
            else:
                self.total += val if sym == "+" else -val

        return self.total, self.mod, self.ls, self.crit

    def switch(self, case):
        games = {
            "DnD": self.dnd,
            "Shadow Run": self.shadow_run,
            "Tephra": self.tephra,
            }
        return games[case]()
