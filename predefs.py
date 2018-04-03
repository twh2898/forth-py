from math import floor

TRUE = -1
FALSE = 0

def ons(state):
    def n_printstack(state):
        print(state.istack.pop(), end = ' ')
    state.on('.', n_printstack)

    def n_stackdump(state):
        for val in state.istack.stack:
            print(val, end=' ')
        print('<- Top', end=' ')
    state.on('.s', n_stackdump)

    def n_addition(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 + n1)
    state.on('+', n_addition)

    def n_subtraction(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 - n1)
    state.on('-', n_subtraction)

    def n_multiplication(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 * n1)
    state.on('*', n_multiplication)
    
    def n_division(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 / n1)
    state.on('/', n_division)
    
    def n_divmod(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 % n1)
        state.istack.push(n2 / n1)
    state.on('/mod', n_divmod)
    
    def n_mod(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n2 % n1)
    state.on('mod', n_mod)
    
    def n_equal(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(TRUE if n2 == n1 else FALSE)
    state.on('=', n_equal)

    def n_lessthan(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(TRUE if n2 < n1 else FALSE)
    state.on('<', n_lessthan)

    def n_greaterthan(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(TRUE if n2 > n1 else FALSE)
    state.on('>', n_greaterthan)
    
    def n_and(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(TRUE if n2 and n1 else FALSE)
    state.on('and', n_and)

    def n_or(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(TRUE if n2 or n1 else FALSE)
    state.on('or', n_or)

    def n_invert(state):
        n1 = state.istack.pop()
        state.istack.push(FALSE if n1 else TRUE)
    state.on('invert', n_invert)
    
    def n_emit(state):
        n1 = state.istack.pop()
        c = int(n1)
        print(chr(c), end='')
    state.on('emit', n_emit)
    
    def n_swap(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.istack.push(n1)
        state.istack.push(n2)
    state.on('swap', n_swap)
    
    def n_dup(state):
        n1 = state.istack.peek()
        state.istack.push(n1)
    state.on('dup', n_dup)
    
    def n_over(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        state.stac.push(n2)
        state.stac.push(n1)
        state.stac.push(n2)
    state.on('over', n_over)
    
    def n_rot(state):
        n1 = state.istack.pop()
        n2 = state.istack.pop()
        n3 = state.istack.pop()
        state.istack.push(n2)
        state.istack.push(n1)
        state.istack.push(n3)
    state.on('rot', n_rot)
    
    def n_drop(state):
        state.istack.pop()
    state.on('drop', n_drop)
    
    def n_varwrite(state):
        addr = state.istack.pop()
        addr = int(addr)
        val = state.istack.pop()
        state.memory.set_val(addr, val)
    state.on('!', n_varwrite)

    def n_varread(state):
        addr = state.istack.pop()
        addr = int(addr)
        state.istack.push(state.memory.get_val(addr))
    state.on('@', n_varread)
    
    def n_allot(state):
        n1 = state.istack.pop()
        state.memory.allot(n1)
    state.on('allot', n_allot)

    def n_words(state):
        for word in state.dict:
            print(word)
    state.on('words', n_words)

    def n_rin(state):
        self.rstack.push(self.istack.pop())
    state.on('>r', n_rin)
    
    def n_rout(state):
        self.istack.push(self.rstack.pop())
    state.on('r>', n_rout)

    def n_rcpy(state):
        self.istack.push(self.rstack.peek())
    state.on('r@', n_rcpy)
    state.on('R@', n_rcpy)
    
    # TODO key

    state.parse_text(': cells 1 * ;')
    state.parse_text(': cr 10 emit ;')
    state.parse_text(': space 32 emit ;')
    state.parse_text(': 0= 0 = ;')
    state.parse_text(': 0< 0 < ;')
    state.parse_text(': 0> 0 > ;')
    state.parse_text(': 2dup over over ;')
    state.parse_text(': 1+ 1 + ;')
    state.parse_text(': 1- 1 - ;')
    state.parse_text(': 2+ 2 + ;')
    state.parse_text(': 2- 2 - ;')
    state.parse_text(': 2* 2 * ;')
    state.parse_text(': 2/ 2 / ;')
    state.parse_text(': negate -1 * ;')
    state.parse_text(': ? @ . ;')
    state.parse_text(': +! dup @ rot + swap ! ;')

    # TODO spaces ?dup abs min max
