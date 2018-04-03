''' Handles tokenizing input text through the Lexer class '''
from exceptions import ForthException


class Token:
    ''' A token from the lexer '''

    def __init__(self, word, isstringliteral=False):
        ''' Create a new token with `text` as the value '''
        self.word = word
        self.isstringliteral = isstringliteral

    def __repr__(self):
        ''' Get a String representing the token '''
        if self.isstringliteral:
            return "StringLiteral( " + self.word + " )"
        return "Token( " + self.word + " )"
    

class Lexer:
    ''' Handles tokenization of input text '''
    whitespace = [' ', '\n', '\t', '\r']

    def __init__(self, input):
        ''' Create a new Lexer to tokenize `input` '''
        self.input = input
        self.index = 0
        self.length = len(input)

    def __iter__(self):
        ''' Get an iter over the tokens produced by this Lexer '''
        return self
    
    def __next__(self):
        ''' Get the next token in the iteration '''
        token = self.next_token()
        if token:
           return token
        raise StopIteration 

    def __curr(self):
        ''' Helper method to get the current character '''
        return self.input[self.index]
    
    def __has_more(self):
        ''' Helper method to check if there are more characters to parse '''
        return self.index < self.length
    
    def __has_chars(self, text):
        ''' Helper method to check if a sequence of characters is at the current index of input '''
        remainder = self.length - self.index

        if remainder < len(text):
            return False
        
        return self.input[self.index : self.index + len(text)] == text
    
    def __take_until(self, check=lambda c: true):
        ''' Helper method to collect characters from the input until a criteria `check` is matched '''
        value = ''
        while self.__has_more() and not check(self.__curr()):
            value += self.__curr()
            self.index += 1
        return value
    
    def __skip_whitespace(self):
        ''' Helper method to consume input while they are whitespace characters '''
        self.__take_until(lambda c: not c in self.whitespace)
    
    def __parse_string(self):
        ''' Helper method to consume and return input until a trailing " is found '''
        # Skip the ." and space
        self.index += 3
        text = self.__take_until(lambda c: c == '"')
        if not self.__curr() == '"':
            raise ForthException('Incomplete string')
        self.index += 1
        return Token(text, True)
    
    def __parse_comment(self):
        ''' Helper method to consume input until a trailing ) is found '''
        self.__take_until(lambda c: c == ')')
        if not self.__curr() == ')':
            raise ForthException('Incomplete comment')
        self.index += 1
    
    def __parse_token(self):
        ''' Helper method to consume and return input until whitespace is found '''
        if not self.__has_more():
            return None
        return Token(self.__take_until(lambda c: c in self.whitespace))
    
    def next_token(self):
        ''' Get the next token from input. Will return Token or StringLiteral for tokens and None for end of input. '''
        if not self.__has_more():
            return None
        
        self.__skip_whitespace()
        
        if self.__has_chars('." '):
            return self.__parse_string()
        elif self.__has_chars('('):
            self.__parse_comment()
            return self.next_token()
        else:
            return self.__parse_token()
