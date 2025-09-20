import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Iterator

class TokenType(Enum):
    # 关键字
    FUNC = 'FUNC'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    RETURN = 'RETURN'
    SYSTEM = 'SYSTEM'
    PRINT = 'PRINT'
    INPUT = 'INPUT'
    IMPORT = 'IMPORT'
    
    # 标识符和字面量
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    
    # 运算符
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
    
    # 逻辑运算符
    AND = 'AND'          # &
    OR = 'OR'            # |
    NOT = 'NOT'          # !
    XOR = 'XOR'          # ^^
    
    # 位运算符
    BITWISE_AND = 'BITWISE_AND'    # &
    BITWISE_OR = 'BITWISE_OR'      # |
    BITWISE_XOR = 'BITWISE_XOR'    # ^^
    LEFT_SHIFT = 'LEFT_SHIFT'      # <<
    RIGHT_SHIFT = 'RIGHT_SHIFT'    # >>
    
    # 幂运算符
    POWER = 'POWER'      # ^
    POWER3 = 'POWER3'    # ^3
    POWERX = 'POWERX'    # ^x (x为数字)
    
    # 复合数据结构
    LBRACKET = 'LBRACKET'     # [ 数组开始
    RBRACKET = 'RBRACKET'     # ] 数组结束
    BREAK = 'BREAK'           # break 语句
    CONTINUE = 'CONTINUE'     # continue 语句 
    
    # 布尔常量
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    
    # 控制流
    ELSE_IF = 'ELSE_IF'      # else-if
    FOR = 'FOR'              # for循环
    
    # 分隔符
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEMICOLON = 'SEMICOLON'
    DOT = 'DOT'
    COMMA = 'COMMA'
    COLON = 'COLON'
    
    # 特殊
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
        
        # 关键字映射
        self.keywords = {
            'func': TokenType.FUNC,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'else-if': TokenType.ELSE_IF,  # 添加else-if支持
            'while': TokenType.WHILE,
            'for': TokenType.FOR,          # 添加for循环支持
            'return': TokenType.RETURN,
            'System': TokenType.SYSTEM,
            'print': TokenType.PRINT,
            'input': TokenType.INPUT,
            'import': TokenType.IMPORT,
            'true': TokenType.TRUE,        # 添加布尔常量
            'false': TokenType.FALSE,      # 添加布尔常量
            'break': TokenType.BREAK,      # 添加break语句
            'continue': TokenType.CONTINUE,  # 添加continue语句
        }
        
        # 单字符标记映射
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
            '%': TokenType.MODULO,     # 添加取模运算符
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '=': TokenType.ASSIGN,
            '&': TokenType.AND,
            '|': TokenType.OR,
            '!': TokenType.NOT,
            '^': TokenType.POWER,
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
        """跳过续行符（反斜杠 + 换行符）"""
        while self.current_char() == '\\' and self.peek_char() == '\n':
            self.advance()  # 跳过反斜杠
            self.advance()  # 跳过换行符
            self.skip_whitespace()  # 跳过新行后的空白字符
    
    def read_string(self) -> str:
        value = ''
        self.advance()  # 跳过开头的双引号
        
        while self.current_char() != '"' and self.current_char() != '\0':
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
                elif escape_char == '"':
                    value += '"'
                else:
                    value += escape_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()  # 跳过结尾的双引号
        
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
            self.skip_line_continuation()  # 跳过续行符
            
            if self.current_char() == '\0':
                break
            
            line = self.line
            column = self.column
            
            # 处理换行
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
                self.advance()
                continue
            
            # 处理字符串
            if self.current_char() == '"':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue
            
            # 处理数字
            if self.current_char().isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
                continue
            
            # 处理标识符和关键字
            if self.current_char().isalpha() or self.current_char() == '_':
                value = self.read_identifier()
                
                # 特殊处理else-if关键字
                if value == 'else' and self.current_char() == '-' and self.peek_char() == 'i' and self.peek_char(2) == 'f':
                    self.advance()  # 消费 -
                    self.advance()  # 消费 i
                    self.advance()  # 消费 f
                    self.tokens.append(Token(TokenType.ELSE_IF, 'else-if', line, column))
                    continue
                
                token_type = self.keywords.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # 处理注释
            if self.current_char() == '|':
                # 单行注释: | xxxx
                next_char = self.peek_char()
                if next_char != '\\' and next_char != '*':
                    while self.current_char() != '\n' and self.current_char() != '\0':
                        self.advance()
                    continue
                
                # 多行注释: |\ xxxxx\nxxxx /|
                if next_char == '\\':
                    self.advance()  # 跳过 |
                    self.advance()  # 跳过 \
                    while self.current_char() != '\0':
                        if self.current_char() == '/' and self.peek_char() == '|':
                            self.advance()  # 跳过 /
                            self.advance()  # 跳过 |
                            break
                        self.advance()
                    continue
                
                # 文档注释: |*\n * xx:xx\n * xx:xx\n*|
                if next_char == '*':
                    self.advance()  # 跳过 |
                    self.advance()  # 跳过 *
                    while self.current_char() != '\0':
                        if self.current_char() == '*' and self.peek_char() == '|':
                            self.advance()  # 跳过 *
                            self.advance()  # 跳过 |
                            break
                        self.advance()
                    continue
            
            # 处理双字符运算符
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
            
            if self.current_char() == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, column))
                self.advance()
                self.advance()
                continue
            
            # 处理位移运算符
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
            
            # 处理异或运算符
            if self.current_char() == '^' and self.peek_char() == '^':
                self.tokens.append(Token(TokenType.BITWISE_XOR, '^^', line, column))
                self.advance()
                self.advance()
                continue
            
            # 处理单字符标记
            if self.current_char() in self.single_char_tokens:
                # 特殊处理幂运算符 ^
                if self.current_char() == '^':
                    # 检查是否是异或 ^^
                    if self.peek_char() == '^':
                        self.tokens.append(Token(TokenType.BITWISE_XOR, '^^', line, column))
                        self.advance()
                        self.advance()
                        continue
                    
                    # 检查是否是 ^3 (立方)
                    if self.peek_char() == '3':
                        self.tokens.append(Token(TokenType.POWER3, '^3', line, column))
                        self.advance()
                        self.advance()
                        continue
                    
                    # 检查是否是 ^数字 (x次方)
                    if self.peek_char().isdigit() and self.peek_char() != '0':  # ^0 没有意义
                        power_num = ''
                        self.advance()  # 跳过 ^
                        while self.current_char().isdigit():
                            power_num += self.current_char()
                            self.advance()
                        self.tokens.append(Token(TokenType.POWERX, f'^{power_num}', line, column))
                        continue
                    
                    # 默认是 ^2 (平方)
                    self.tokens.append(Token(TokenType.POWER, '^', line, column))
                    self.advance()
                    continue
                
                # 其他单字符标记
                token_type = self.single_char_tokens[self.current_char()]
                self.tokens.append(Token(token_type, self.current_char(), line, column))
                self.advance()
                continue
            
            # 未知字符
            raise SyntaxError(f"未知字符 '{self.current_char()}' 在第 {line} 行，第 {column} 列")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

def main():
    # 测试词法分析器
    code = '''
func main() {
    System.print("Hello World!")
}
'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("词法分析结果:")
    for token in tokens:
        print(f"{token.type.value}: '{token.value}' (第 {token.line} 行，第 {token.column} 列)")

if __name__ == "__main__":
    main()