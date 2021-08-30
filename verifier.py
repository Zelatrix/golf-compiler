from z3 import *
import nltk.sem.logic

# Assignment
# {P} V := E {Q}
# P -> Q[E/V]
def generate_assignment():
    pass

# Conditionals
# {P} IF S THEN C1 ELSE C2 {Q}
# {P and S} C1 {Q}
# {P and not S} C2 {Q}
def generate_conditional():
    pass

# Sequencing

# If Cn is NOT an assignment:
# {P} C1; ... Cn-1; {R} Cn {Q}
# {P} C1 ... Cn-1 {R}
# {R} Cn {Q}

# If Cn is an assignment
# {P} C1; ...;Cn-1; V := E {Q}
# {P} C1; ...;Cn-1 {Q[E/V]}
def generate_sequencing():
    pass
