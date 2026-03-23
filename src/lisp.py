import math
import operator as op

# Types
Symbol = str
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Nil    = None
Exp    = (Atom, list)

# Atom type.
# We either get a number, or a Symbol. Floats do not exist (they do, I lied).
def atom(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

# Output buffer that print and other STDIO goes to. 
# We need this because we cannot give the user
# IO using STDIO so we "fake" STDIO with this buffer.
class OutputBuffer:
    def __init__(self):
        self.lines = []

    def write(self, *args):
        self.lines.append(" ".join(map(str, args)))

    def get_output(self):
        return "\n".join(self.lines)

# Env type.
# This is a class so we can have scope.
# SICP style!
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    
    def find(self, var):
        return self if (var in self) else self.outer.find(var)

# Init global env
# Very cool, very nice.
def std_env(output) -> Env:
    env = Env()
    env.update(vars(math))

    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '<': op.lt,
        '>': op.gt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'do': lambda *x: x[-1],
        'list': lambda *x: List(x),
        'is?': op.is_,
        'exp': pow,
        'map': map,
        'max': max,
        'min': min,
        'first': lambda x: x[0],
        'second': lambda x: x[1],
        'eq?': op.eq,
        'list?': lambda x: isinstance(x, List),
        'num?':  lambda x: isinstance(x, Number),
        'nil?':  lambda x: x == [],
        'func?': callable,
        'sym?': lambda x: isinstance(x, Symbol),
        'print': lambda *x: output.write(*x),
        'round': round,
    })
    return env

# Pure function
# Takes in the code
# Returns the AST
def tokenize(expr: str) -> Exp:
    return expr.replace("(", " ( ").replace(")", " ) ").split()

# Pure function; takes in the tokens
# Returns AST
def read(tokens: list) -> Exp:
    if (len(tokens) == 0):
        raise SyntaxError('Unexpected EOF') # TODO: error handling?
    
    # We pop because pop removes from tokens! pop pop popcorn
    token = tokens.pop(0)

    if (token == '('):
        L = []
        while tokens[0] != ')':
            # Recursion!
            L.append(read(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('Unexpected \')\'')
    else:
        return atom(token)

def parse(program: str) -> Exp:
    return read(tokenize(program))

# Impure function
# Takes in the expression and the environment
# Evaluates expressions and mutates state
def eval(expr: Exp, env: Env):
    if isinstance(expr, Symbol):
        return env[expr]

    if isinstance(expr, Number):
        return expr

    if expr[0] == 'if':
        (_, test, conseq, alt) = expr
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)

    elif expr[0] == 'define' or expr[0] == 'def':
        (_, symbol, exp) = expr
        env[symbol] = eval(exp, env)
    
    else:
        func = eval(expr[0], env)
        args = [eval(arg, env) for arg in expr[1:]]
        return func(*args)
