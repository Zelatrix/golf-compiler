from abc import ABC, abstractmethod
# from my_ast import Integer, Float, Chars, String, Boolean

# The Type class implements the abstract base class
# The syntax is the equivalent of something like
"""
abstract class Type {
    // methods implemented by all subclasses
    // of Type go here
} 
"""

class Type: # (ABC):
    # @abstractmethod
    def get_type(self):
        return type(self)

# The following classes are all subclasses of Type
class Integer(Type):
    pass

class Float(Type):
    pass

class Char(Type):
    pass

class Boolean(Type):
    pass

class String(Type):
    pass

def main():
    i = Integer()
    f = Float()
    c = Char()
    b = Boolean()
    s = String()

    print(i.get_type())
    print(f.get_type())
    print(c.get_type())
    print(b.get_type())
    print(s.get_type())

main()