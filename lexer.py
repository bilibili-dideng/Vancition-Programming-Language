import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Iterator

class TokenType(Enum):
    # Keywords
    FUNC = 'FUNC'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    RETURN = 'RETURN'
    SYSTEM = 'SYSTEM'
    PRINT = 'PRINT'
    INPUT = 'INPUT'
    IMPORT = 'IMPORT'
    SWITCH = 'SWITCH'
    CASE = 'CASE'
    DEFAULT = 'DEFAULT'
    TRY = 'TRY'
    CATCH = 'CATCH'
    FINALLY = 'FINALLY'
    THROW = 'THROW'
    LAMBDA = 'LAMBDA'
    USING = 'USING'
    DEFINE = 'DEFINE'
    IMMUT = 'IMMUT'
    
    # Identifiers and literals
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    FORMAT_STRING = 'FORMAT_STRING'  # f"..." strings
    RAW_STRING = 'RAW_STRING'        # $"..." raw strings
    NUMBER = 'NUMBER'
    
    # Operators
    ASSIGN = 'ASSIGN'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'      # %
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    GREATER = 'GREATER'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER_EQUAL = 'GREATER_EQUAL'
    
    # Logical operators
    AND = 'AND'          # &
    OR = 'OR'            # |
    NOT = 'NOT'          # !
    XOR = 'XOR'          # ^^
    
    # Bitwise operators
    BITWISE_AND = 'BITWISE_AND'    # &
    BITWISE_OR = 'BITWISE_OR'      # |
    BITWISE_XOR = 'BITWISE_XOR'    # ^^
    LEFT_SHIFT = 'LEFT_SHIFT'      # <<
    RIGHT_SHIFT = 'RIGHT_SHIFT'    # >>
    
    # Power operators
    POWER = 'POWER'      # ^
    POWER3 = 'POWER3'    # ^3
    POWERX = 'POWERX'    # ^x (x is number)
    
    # Composite data structures
    LBRACKET = 'LBRACKET'     # [ array start
    RBRACKET = 'RBRACKET'     # ] array end
    BREAK = 'BREAK'           # break statement
    CONTINUE = 'CONTINUE'     # continue statement 
    
    # Boolean constants
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    
    # Control flow
    ELSE_IF = 'ELSE_IF'      # else-if
    FOR = 'FOR'              # for loop
    
    # Delimiters
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEMICOLON = 'SEMICOLON'
    DOT = 'DOT'
    COMMA = 'COMMA'
    COLON = 'COLON'
    ARROW = 'ARROW'  # Lambda arrow ->
    
    # Special
    EOF = 'EOF'
    NEWLINE = 'NEWLINE'

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keyword mapping
        self.keywords = {
            'func': TokenType.FUNC,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'else-if': TokenType.ELSE_IF,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'return': TokenType.RETURN,
            'System': TokenType.SYSTEM,
            'print': TokenType.PRINT,
            'input': TokenType.INPUT,
            'import': TokenType.IMPORT,
            'using': TokenType.USING,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'switch': TokenType.SWITCH,
            'case': TokenType.CASE,
            'default': TokenType.DEFAULT,
            'try': TokenType.TRY,
            'catch': TokenType.CATCH,
            'finally': TokenType.FINALLY,
            'throw': TokenType.THROW,
            'lambda': TokenType.LAMBDA,
            'define': TokenType.DEFINE,
            'immut': TokenType.IMMUT,
        }
        
        # Single character token mapping
        self.single_char_tokens = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ';': TokenType.SEMICOLON,
            '.': TokenType.DOT,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,     # Add modulo operator
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '=': TokenType.ASSIGN,
            '&': TokenType.BITWISE_AND,
            '|': TokenType.BITWISE_OR,
            '!': TokenType.NOT,
            '^': TokenType.POWER,
            '->': TokenType.ARROW,     # Lambda arrow
        }
    
    def current_char(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> str:
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() in ' \t\r':
            self.advance()
    
    def skip_line_continuation(self):
        """Skip line continuation (backslash + newline)"""
        while self.current_char() == '\\' and self.peek_char() == '\n':
            self.advance()  # Skip backslash
            self.advance()  # Skip newline
            self.skip_whitespace()  # Skip whitespace after newline
    
    def read_string(self, delimiter: str = '"') -> str:
        value = ''
        self.advance()  # Skip opening quote
        
        while self.current_char() != delimiter and self.current_char() != '\0':
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == delimiter:
                    value += delimiter
                elif escape_char == 'u':  # Unicode escape \uXXXX
                    self.advance()
                    unicode_hex = ''
                    for i in range(4):
                        if self.current_char() in '0123456789abcdefABCDEF':
                            unicode_hex += self.current_char()
                            self.advance()
                        else:
                            break
                    if len(unicode_hex) == 4:
                        try:
                            unicode_char = chr(int(unicode_hex, 16))
                            value += unicode_char
                            continue
                        except ValueError:
                            value += '\\u' + unicode_hex
                    else:
                        value += '\\u' + unicode_hex
                    continue
                else:
                    value += escape_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == delimiter:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_format_string(self, delimiter: str = '"') -> str:
        """Read format string (f"...") with variable substitution"""
        value = ''
        self.advance()  # Skip opening quote
        
        while self.current_char() != delimiter and self.current_char() != '\0':
            if self.current_char() == '{':
                self.advance()  # Skip {
                var_name = ''
                while self.current_char() != '}' and self.current_char() != '\0':
                    var_name += self.current_char()
                    self.advance()
                if self.current_char() == '}':
                    self.advance()  # Skip }
                    value += f'{{{{{var_name.strip()}}}}}'  # Store as {{var}} for later processing
                else:
                    value += '{' + var_name
            elif self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == delimiter:
                    value += delimiter
                elif escape_char == 'u':  # Unicode escape \uXXXX
                    self.advance()
                    unicode_hex = ''
                    for i in range(4):
                        if self.current_char() in '0123456789abcdefABCDEF':
                            unicode_hex += self.current_char()
                            self.advance()
                        else:
                            break
                    if len(unicode_hex) == 4:
                        try:
                            unicode_char = chr(int(unicode_hex, 16))
                            value += unicode_char
                            continue
                        except ValueError:
                            value += '\\u' + unicode_hex
                    else:
                        value += '\\u' + unicode_hex
                    continue
                else:
                    value += escape_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == delimiter:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_raw_string(self, delimiter: str = '"') -> str:
        """Read raw string ($"...") without escape processing"""
        value = ''
        self.advance()  # Skip opening quote
        
        while self.current_char() != delimiter and self.current_char() != '\0':
            value += self.current_char()
            self.advance()
        
        if self.current_char() == delimiter:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> str:
        value = ''
        
        while self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        
        if self.current_char() == '.' and self.peek_char().isdigit():
            value += self.current_char()
            self.advance()
            
            while self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        return value
    
    def read_identifier(self) -> str:
        value = ''
        
        while (self.current_char().isalnum() or self.current_char() == '_') and self.current_char() != '\0':
            value += self.current_char()
            self.advance()
        
        return value
    
    def tokenize(self) -> List[Token]:
        while self.current_char() != '\0':
            self.skip_whitespace()
            self.skip_line_continuation()  # Skip line continuation
            
            if self.current_char() == '\0':
                break
            
            line = self.line
            column = self.column
            
            # Handle newline
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
                self.advance()
                continue
            
            # Handle format string (f"...")
            if self.current_char() == 'f' and (self.peek_char() == '"' or self.peek_char() == "'"):
                delimiter = self.peek_char()
                self.advance()  # Skip f
                value = self.read_format_string(delimiter)
                self.tokens.append(Token(TokenType.FORMAT_STRING, value, line, column))
                continue
            
            # Handle raw string ($"...")
            if self.current_char() == '$' and (self.peek_char() == '"' or self.peek_char() == "'"):
                delimiter = self.peek_char()
                self.advance()  # Skip $
                value = self.read_raw_string(delimiter)
                self.tokens.append(Token(TokenType.RAW_STRING, value, line, column))
                continue
            
            # Handle regular string
            if self.current_char() == '"' or self.current_char() == "'":
                value = self.read_string(self.current_char())
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue
            
            # Handle number
            if self.current_char().isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
                continue
            
            # Handle identifier and keyword
            if self.current_char().isalpha() or self.current_char() == '_':
                value = self.read_identifier()
                
                # Special handling for else-if keyword
                if value == 'else' and self.current_char() == '-' and self.peek_char() == 'i' and self.peek_char(2) == 'f':
                    self.advance()  # Consume -
                    self.advance()  # Consume i
                    self.advance()  # Consume f
                    self.tokens.append(Token(TokenType.ELSE_IF, 'else-if', line, column))
                    continue
                
                token_type = self.keywords.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # Handle double character operators
            if self.current_char() == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, column))
                self.advance()
                self.advance()
                continue
            
            # Add support for logical AND (&&) operator
            if self.current_char() == '&' and self.peek_char() == '&':
                self.tokens.append(Token(TokenType.AND, '&&', line, column))
                self.advance()
                self.advance()
                continue
            
            # Add support for logical OR (||) operator
            if self.current_char() == '|' and self.peek_char() == '|':
                self.tokens.append(Token(TokenType.OR, '||', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, column))
                self.advance()
                self.advance()
                continue
            
            # Handle Lambda arrow operator
            if self.current_char() == '-' and self.peek_char() == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', line, column))
                self.advance()
                self.advance()
                continue
            
            # Handle shift operators
            if self.current_char() == '<' and self.peek_char() == '<':
                self.tokens.append(Token(TokenType.LEFT_SHIFT, '<<', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '>' and self.peek_char() == '>':
                self.tokens.append(Token(TokenType.RIGHT_SHIFT, '>>', line, column))
                self.advance()
                self.advance()
                continue
            
            # Handle XOR operator
            if self.current_char() == '^' and self.peek_char() == '^':
                self.tokens.append(Token(TokenType.BITWISE_XOR, '^^', line, column))
                self.advance()
                self.advance()
                continue
            
            # Handle comments
            if self.current_char() == '|':
                # Single line comment: | xxxx
                next_char = self.peek_char()
                if next_char != '\\' and next_char != '*':
                    while self.current_char() != '\n' and self.current_char() != '\0':
                        self.advance()
                    continue
                
                # Multi-line comment: |\ xxxxx\nxxxx /|
                if next_char == '\\':
                    self.advance()  # Skip |
                    self.advance()  # Skip \
                    while self.current_char() != '\0':
                        if self.current_char() == '/' and self.peek_char() == '|':
                            self.advance()  # Skip /
                            self.advance()  # Skip |
                            break
                        self.advance()
                    continue
                
                # Documentation comment: |*\n * xx:xx\n * xx:xx\n*|
                if next_char == '*':
                    self.advance()  # Skip |
                    self.advance()  # Skip *
                    while self.current_char() != '\0':
                        if self.current_char() == '*' and self.peek_char() == '|':
                            self.advance()  # Skip *
                            self.advance()  # Skip |
                            break
                        self.advance()
                    continue
            
            # Handle single character tokens
            if self.current_char() in self.single_char_tokens:
                # Special handling for power operator ^
                if self.current_char() == '^':
                    # Check if it's XOR ^^
                    if self.peek_char() == '^':
                        self.tokens.append(Token(TokenType.BITWISE_XOR, '^^', line, column))
                        self.advance()
                        self.advance()
                        continue
                    
                    # Check if it's ^3 (cube)
                    if self.peek_char() == '3':
                        self.tokens.append(Token(TokenType.POWER3, '^3', line, column))
                        self.advance()
                        self.advance()
                        continue
                    
                    # Check if it's ^digit (x power)
                    if self.peek_char().isdigit() and self.peek_char() != '0':  # ^0 has no meaning
                        power_num = ''
                        self.advance()  # Skip ^
                        while self.current_char().isdigit():
                            power_num += self.current_char()
                            self.advance()
                        self.tokens.append(Token(TokenType.POWERX, f'^{power_num}', line, column))
                        continue
                    
                    # Default is ^2 (square)
                    self.tokens.append(Token(TokenType.POWER, '^', line, column))
                    self.advance()
                    continue
                
                # Other single character tokens
                token_type = self.single_char_tokens[self.current_char()]
                self.tokens.append(Token(token_type, self.current_char(), line, column))
                self.advance()
                continue
            
            # Unknown character
            raise SyntaxError(f"Unknown character '{self.current_char()}' at line {line}, column {column}")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

def main():
    # Test lexer
    code = '''
func main() {
    System.print("Hello World!")
}
'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("Lexer results:")
    for token in tokens:
        print(f"{token.type.value}: '{token.value}' (Line {token.line}, Column {token.column})")

if __name__ == "__main__":
    main()