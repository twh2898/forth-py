from exceptions import CompileException


class Body:
    def __init__(self, parent=None):
        self.parent = parent
        self.body = []

    def take(self, token):
        self.body.append(token)

    def finish(self):
        def run(state):
            state.act_all(self.body)
        if self.parent:
            self.parent.body.append(run)
        else:
            return run

    def __repr__(self):
        return 'Body (parent=' + repr(self.parent) + ') [' + ', '.join([repr(b) for b in self.body]) + ']'


class IfBlock(Body):
    def __init__(self, parent=None):
        Body.__init__(self, parent)
        self.el = []
        self.inbody = True

    def take(self, token):
        if token.word == 'then':
            return False
        elif token.word == 'else':
            if not self.inbody:
                raise CompileException('Already in else block')
            self.inbody = False
        elif self.inbody:
            self.body.append(token)
        else:
            self.el.append(token)
        return True

    def finish(self):
        def run(state):
            n1 = state.istack.pop()
            if n1 != 0:
                state.act_all(self.body)
            else:
                state.act_all(self.el)
        if self.parent:
            if type(self.parent) == IfBlock and not self.parent.inbody:
                self.parent.el.append(run)
            else:
                self.parent.body.append(run)
        else:
            return run


class DoBlock(Body):

    def take(self, token):
        if token.word == 'loop':
            return False
        else:
            self.body.append(token)
        return True

    def finish(self):
        def run(state):
            n1 = state.istack.pop()
            n2 = state.istack.pop()
            for i in range(n1, n2):
                state.on('i', lambda s: s.istack.push(i))
                state.act_all(self.body)
        return run


class BeginBlock(Body):

    def take(self, token):
        if token.word == 'until':
            return False
        else:
            self.body.append(token)
        return True

    def finish(self):
        def run(state):
            while True:
                state.act_all(self.body)
                if state.istack.pop() != 0:
                    return
        return run


class Compile:
    def __init__(self):
        self.name = None
        self.code = []
        self.tree = None

    def take(self, token):
        if not self.name:
            if token.isstringliteral:
                raise CompileException('Expected name, not string')
            self.name = token.word
        else:
            if token.word == 'if':
                self.tree = IfBlock(self.tree)
            elif token.word == 'do':
                self.tree = DoBlock(self.tree)
            elif token.word == 'begin':
                self.tree = BeginBlock(self.tree)
            elif self.tree:
                if not self.tree.take(token):
                    if self.tree.parent:
                        self.tree.finish()
                    else:
                        self.code.append(self.tree.finish())
                    self.tree = self.tree.parent
            else:
                self.code.append(token)

    def finish(self, state):
        code = self.code
        def run(state):
            state.act_all(code)
        state.dict[self.name] = run
