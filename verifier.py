from z3 import *
from my_ast import *

# x = Int('x')
# y = Int('y')
# solve(x > 3, y < 10, x + 2*y == 7)

# Assignment
# {P} V := E {Q}
# P -> Q[E/V]

#     subst : Expr -> Var -> Expr.
#     subst e x e' means substitute all occurrences of x with e' inside of e
#     subst (Plus e1 e2) x e'   = Plus (subst e1 x e') (subst e2 x e')
#     subst (Var y) x e'
#     if y== x then e' else Var y

p, q = Bools('p q')
demorgan = And(p, q) == Not(Or(Not(p), Not(q)))
print(demorgan)

def prove(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        print("proved")
    else:
        print("failed to prove")

print("Proving demorgan...")
prove(demorgan)

def subst(e1, var, e2):
    pass

# def generate_assignment():
#     pass

# Conditionals
# {P} IF S THEN C1 ELSE C2 {Q}
# {P and S} C1 {Q}
# {P and not S} C2 {Q}
# def generate_conditional():
#     pass

# Sequencing

# If Cn is NOT an assignment:
# {P} C1; ... Cn-1; {R} Cn {Q}
# {P} C1 ... Cn-1 {R}
# {R} Cn {Q}

# If Cn is an assignment
# {P} C1; ...;Cn-1; V := E {Q}
# {P} C1; ...;Cn-1 {Q[E/V]}
# def generate_sequencing():
#     pass
