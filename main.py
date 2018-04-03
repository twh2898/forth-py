from lexer import Lexer
from util import Stack, Memory
from compile import Compile
from predefs import ons
from exceptions import ForthException, CompileException

    
def isInt(token):
    try:
        int(token)
        return True
    except ValueError:
        return False


def isFloat(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


class State:
    def __init__(self):
        self.istack = Stack()
        self.rstack = Stack()
        self.fstack = Stack()
        self.memory = Memory()
        self.lex = None
        self.dict = {}
        self.compile = None

    def on(self, word, action):
        self.dict[word] = action

    def act_all(self, tokens):
        for token in tokens:
            if callable(token):
                token(self)
            elif type(token) == type([]):
                self.act_all(token)
            else:
                self.act(token)

    def act(self, token):
        word = token.word
        if word == ':':
            if self.compile:
                print('Already in compile mode!')
                return False
            self.compile = Compile()
        elif word == ';':
            if not self.compile:
                print('Not in compile mode!')
                return False
            self.compile.finish(self)
            self.compile = None
        elif self.compile:
            try:
                self.compile.take(token)
            except CompileException as e:
                print(e)
                self.compile = None
        elif word == 'variable':
            if self.lex:
                name = next(self.lex)
                if name.isstringliteral:
                    raise ForthException('Expected name, not string')
                name = name.word
                index = self.memory.create_var(name)
                self.on(name, lambda s: s.istack.push(index))
            else:
                raise ForthException("No name variable name given")
        elif word == 'constant':
            if self.lex:
                name = next(self.lex)
                if name.isstringliteral:
                    raise ForthException('Expected name, not string')
                name = name.word
                n1 = self.istack.pop()
                self.on(name, lambda s: s.istack.push(n1))
            else:
                raise ForthException("No name variable name given")
        elif isInt(word):
            self.istack.push(int(word))
        elif isFloat(word):
            self.fstack.push(float(word))
        elif token.isstringliteral:
            print(word, end='')
        elif word in self.dict:
            self.dict[word](self)
        else:
            raise ForthException('Unknown Token: ' + word)
        return True

    def parse_text(self, text):
        self.lex = iter(Lexer(text))
        for token in self.lex:
            if not self.act(token):
                self.lex = None
                return False
        self.lex = None
        return True
        

def main():
    state = State()
    ons(state)
    try:
        while True:
            text = input('> ')
            try:
                if state.parse_text(text):
                    print(' ok')
                else:
                    return
            except ForthException as e:
                print(e)
    except KeyboardInterrupt:
        print("Exiting!")


if __name__ == '__main__':
    main()
