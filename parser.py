from typing import List, Optional, Union, Dict, Tuple
from dataclasses import dataclass
from lexer import Token, TokenType, Lexer

# AST节点定义
@dataclass
class ASTNode:
    line: int = 0
    column: int = 0
    
    def __post_init__(self):
        if not hasattr(self, 'line'):
            self.line = 0
        if not hasattr(self, 'column'):
            self.column = 0

@dataclass
class Program(ASTNode):
    functions: List['FunctionDef'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.functions is None:
            self.functions = []

@dataclass
class FunctionDef(ASTNode):
    name: str = ""
    parameters: List[str] = None
    body: List['Statement'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.parameters is None:
            self.parameters = []
        if self.body is None:
            self.body = []

@dataclass
class Statement(ASTNode):
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: 'Expression' = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.expression is None:
            self.expression = None

@dataclass
class ReturnStatement(Statement):
    value: Optional['Expression'] = None

@dataclass
class IfStatement(Statement):
    condition: 'Expression' = None
    then_body: List[Statement] = None
    else_body: Optional[List[Statement]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.then_body is None:
            self.then_body = []
        if self.else_body is None:
            self.else_body = None

@dataclass
class WhileStatement(Statement):
    condition: 'Expression' = None
    body: List[Statement] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.body is None:
            self.body = []

@dataclass
class ImportStatement(Statement):
    module_name: str = ""

@dataclass
class BreakStatement(Statement):
    pass

@dataclass
class ContinueStatement(Statement):
    pass

@dataclass
class ForStatement(Statement):
    variable: Optional[str] = None  # 用于 for (item in collection)
    iterable: Optional['Expression'] = None  # 用于 for (item in collection)
    init: Optional['Expression'] = None  # 用于传统 for 循环
    condition: Optional['Expression'] = None  # 用于传统 for 循环
    update: Optional['Expression'] = None  # 用于传统 for 循环
    body: List[Statement] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.body is None:
            self.body = []

@dataclass
class Expression(ASTNode):
    pass

@dataclass
class BinaryExpression(Expression):
    left: 'Expression' = None
    operator: str = ""
    right: 'Expression' = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.left is None:
            self.left = None
        if self.right is None:
            self.right = None

@dataclass
class UnaryExpression(Expression):
    operator: str = ""
    operand: 'Expression' = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.operand is None:
            self.operand = None

@dataclass
class CallExpression(Expression):
    function: str = ""
    arguments: List['Expression'] = None
    keyword_arguments: Dict[str, 'Expression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.arguments is None:
            self.arguments = []
        if self.keyword_arguments is None:
            self.keyword_arguments = {}

@dataclass
class MemberExpression(Expression):
    object: str = ""
    property: str = ""

@dataclass
class Identifier(Expression):
    name: str = ""

@dataclass
class Literal(Expression):
    value: Union[str, int, float, bool] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.value is None:
            self.value = 0

@dataclass
class ArrayExpression(Expression):
    elements: List['Expression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.elements is None:
            self.elements = []

@dataclass
class DictExpression(Expression):
    entries: List[Tuple['Expression', 'Expression']] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.entries is None:
            self.entries = []

@dataclass
class IndexExpression(Expression):
    object: 'Expression' = None
    index: 'Expression' = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.object is None:
            self.object = None
        if self.index is None:
            self.index = None

class Parser:
    def __init__(self, tokens: List[Token], filename: str = "<file>"):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
        self.filename = filename
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def consume(self, token_type: TokenType, filename: str = "<file>") -> Token:
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            # Get current position information
            line = self.current_token.line if self.current_token else 1
            column = self.current_token.column if self.current_token else 1
            
            # Friendly error descriptions
            if token_type == TokenType.COLON:
                expected_desc = "colon (:)"
            elif token_type == TokenType.SEMICOLON:
                expected_desc = "semicolon (;)"
            elif token_type == TokenType.LBRACE:
                expected_desc = "left brace ({)"
            elif token_type == TokenType.RBRACE:
                expected_desc = "right brace (})"
            elif token_type == TokenType.LPAREN:
                expected_desc = "left parenthesis"
            elif token_type == TokenType.RPAREN:
                expected_desc = "right parenthesis"
            elif token_type == TokenType.IDENTIFIER:
                expected_desc = "identifier"
            elif token_type == TokenType.STRING:
                expected_desc = "string"
            elif token_type == TokenType.NUMBER:
                expected_desc = "number"
            else:
                expected_desc = f"{token_type.value}"
            
            # Current actual content
            if not self.current_token:
                actual_desc = "end of file"
            elif self.current_token.type == TokenType.NEWLINE:
                actual_desc = "newline"
            elif self.current_token.type == TokenType.EOF:
                actual_desc = "end of file"
            else:
                actual_desc = f"'{self.current_token.value}'"
            
            # Generate error message with file info
            error_msg = f"Syntax Error: {expected_desc} expected, found {actual_desc}"
            
            # Print error with file location and pointer
            print(f"Error: {error_msg}")
            print(f"  --> {filename}:{line}:{column}")
            
            # Add helpful hints
            hints = []
            if token_type == TokenType.COLON:
                hints.append("In Vanction language, every statement must end with a colon (:)")
            elif token_type == TokenType.RBRACE:
                hints.append("Check if code blocks are properly closed")
            elif token_type == TokenType.RPAREN:
                hints.append("Check if function call parentheses are balanced")
            
            if hints:
                print(f"Hint: {hints[0]}")
            
            # Add visual pointer to error location
            if self.current_token and self.current_token.type != TokenType.EOF:
                # Create a pointer line showing the error location
                pointer_line = " " * (column - 1) + "^^^^"
                print(f"{pointer_line}")
            
            raise SyntaxError(error_msg)
    
    def consume_with_filename(self, token_type: TokenType) -> Token:
        """Wrapper to use filename from parser instance"""
        return self.consume(token_type, self.filename)
    
    def skip_newlines(self):
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        functions = []
        top_level_statements = []  # 存储顶级语句（如import）
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token and self.current_token.type == TokenType.FUNC:
                functions.append(self.parse_function())
            elif self.current_token and self.current_token.type == TokenType.IMPORT:
                # 收集顶级import语句
                top_level_statements.append(self.parse_import_statement())
            else:
                self.advance()
        
        # 如果有顶级语句，创建或修改main函数来包含它们
        if top_level_statements:
            # 查找是否已有main函数
            main_func = None
            for func in functions:
                if func.name == "main":
                    main_func = func
                    break
            
            if main_func:
                # 如果已有main函数，在函数体开头插入顶级语句
                main_func.body = top_level_statements + main_func.body
            else:
                # 如果没有main函数，创建一个新的main函数
                main_func = FunctionDef(
                    name="main",
                    parameters=[],
                    body=top_level_statements
                )
                functions.insert(0, main_func)  # 将main函数放在最前面
        
        return Program(functions=functions)
    
    def parse_function(self) -> FunctionDef:
        func_token = self.consume_with_filename(TokenType.FUNC)
        name_token = self.consume_with_filename(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.consume_with_filename(TokenType.LPAREN)
        parameters = []
        
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            parameters.append(self.consume_with_filename(TokenType.IDENTIFIER).value)
            
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
                parameters.append(self.consume_with_filename(TokenType.IDENTIFIER).value)
        
        self.consume_with_filename(TokenType.RPAREN)
        self.consume_with_filename(TokenType.LBRACE)
        
        body = self.parse_statements()
        
        self.consume_with_filename(TokenType.RBRACE)
        
        # Create function with line/column info
        func_def = FunctionDef(name=name, parameters=parameters, body=body)
        func_def.line = func_token.line
        func_def.column = func_token.column
        
        return func_def
    
    def parse_statements(self) -> List[Statement]:
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token and self.current_token.type != TokenType.RBRACE:
                statements.append(self.parse_statement())
            # 检查右大括号后的冒号（仅在某些上下文中需要）
            if self.current_token and self.current_token.type == TokenType.RBRACE and self.peek_token() and self.peek_token().type == TokenType.COLON:
                # 跳过右大括号后的冒号（用于if-else和while语句）
                if self.peek_token() and self.peek_token().type == TokenType.COLON:
                    self.advance()  # 跳过RBRACE
                    self.advance()  # 跳过COLON
                    break
        
        return statements
    
    def parse_statement(self) -> Statement:
        # Save current token position for error reporting
        start_token = self.current_token
        
        if self.current_token.type == TokenType.RETURN:
            stmt = self.parse_return_statement()
        elif self.current_token.type == TokenType.IF:
            stmt = self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            stmt = self.parse_while_statement()
        elif self.current_token.type == TokenType.FOR:
            stmt = self.parse_for_statement()
        elif self.current_token.type == TokenType.BREAK:
            self.advance()
            stmt = BreakStatement()
        elif self.current_token.type == TokenType.CONTINUE:
            self.advance()
            stmt = ContinueStatement()
        elif self.current_token.type == TokenType.IMPORT:
            stmt = self.parse_import_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            # 检查是否是函数调用或赋值
            stmt = self.parse_expression_statement()
        elif self.current_token.type == TokenType.SYSTEM:
            # 处理 System.print 这样的调用
            stmt = self.parse_expression_statement()
        else:
            stmt = self.parse_expression_statement()
        
        # Set line/column info for the statement
        if start_token and stmt:
            stmt.line = start_token.line
            stmt.column = start_token.column
            
        return stmt
    
    def parse_return_statement(self) -> ReturnStatement:
        self.consume_with_filename(TokenType.RETURN)
        
        value = None
        if self.current_token.type != TokenType.SEMICOLON and self.current_token.type != TokenType.NEWLINE:
            value = self.parse_expression()
        
        # 允许语句以分号或换行符结尾
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon or newline after return statement at line {self.current_token.line if self.current_token else 0}")
        
        return ReturnStatement(value=value)
    
    def parse_if_statement(self) -> IfStatement:
        self.consume_with_filename(TokenType.IF)
        condition = self.parse_expression()
        self.consume_with_filename(TokenType.LBRACE)
        
        then_body = self.parse_statements()
        self.consume_with_filename(TokenType.RBRACE)
        
        else_body = None
        # 处理else-if和else部分
        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE_IF:
            # 处理多个else-if
            current_if = None
            while self.current_token and self.current_token.type == TokenType.ELSE_IF:
                self.advance()  # 消费else-if
                else_if_condition = self.parse_expression()
                self.consume_with_filename(TokenType.LBRACE)
                else_if_body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                
                # 创建if语句
                new_if = IfStatement(
                    condition=else_if_condition, 
                    then_body=else_if_body, 
                    else_body=None
                )
                
                if current_if is None:
                    current_if = new_if
                else:
                    # 将新的if语句链接到前一个的else部分
                    current_if.else_body = [new_if]
                    current_if = new_if
            
            # 检查是否有else部分
            if self.current_token and self.current_token.type == TokenType.ELSE:
                self.advance()  # 消费else
                self.consume_with_filename(TokenType.LBRACE)
                final_else_body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                current_if.else_body = final_else_body
            
            else_body = [current_if] if current_if else None
            
        elif self.current_token and self.current_token.type == TokenType.ELSE:
            # 普通else（不再支持else if语法）
            self.advance()
            self.consume_with_filename(TokenType.LBRACE)
            else_body = self.parse_statements()
            self.consume_with_filename(TokenType.RBRACE)
        
        return IfStatement(condition=condition, then_body=then_body, else_body=else_body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.consume_with_filename(TokenType.WHILE)
        condition = self.parse_expression()
        self.consume_with_filename(TokenType.LBRACE)
        
        body = self.parse_statements()
        self.consume_with_filename(TokenType.RBRACE)
        
        return WhileStatement(condition=condition, body=body)
    
    def parse_for_statement(self) -> ForStatement:
        self.consume_with_filename(TokenType.FOR)
        
        # 解析for循环的三种形式：
        # 1. for (init; condition; update) { body }
        # 2. for (item in array) { body }
        # 3. for (key, value in dict) { body }
        
        self.consume_with_filename(TokenType.LPAREN)
        
        # 检查是否是范围循环语法
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.value == 'in':
                # for (item in collection) 语法
                self.advance()  # 消费 'in'
                iterable = self.parse_expression()
                self.consume_with_filename(TokenType.RPAREN)
                self.consume_with_filename(TokenType.LBRACE)
                body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                
                return ForStatement(
                    variable=var_name,
                    iterable=iterable,
                    body=body
                )
            else:
                # 传统for循环：for (init; condition; update)
                # 回退并解析初始化
                self.position -= 1  # 回退
                self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
                
                # 解析初始化语句
                init = None
                if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                    init = self.parse_expression()
                self.consume_with_filename(TokenType.SEMICOLON)
                
                # 解析条件
                condition = None
                if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                    condition = self.parse_expression()
                self.consume_with_filename(TokenType.SEMICOLON)
                
                # 解析更新
                update = None
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    update = self.parse_expression()
                self.consume_with_filename(TokenType.RPAREN)
                
                self.consume_with_filename(TokenType.LBRACE)
                body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                
                return ForStatement(
                    init=init,
                    condition=condition,
                    update=update,
                    body=body
                )
        else:
            # 传统for循环：for (; condition; update) 或 for (;;)
            init = None
            if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                init = self.parse_expression()
            self.consume_with_filename(TokenType.SEMICOLON)
            
            condition = None
            if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                condition = self.parse_expression()
            self.consume_with_filename(TokenType.SEMICOLON)
            
            update = None
            if self.current_token and self.current_token.type != TokenType.RPAREN:
                update = self.parse_expression()
            self.consume_with_filename(TokenType.RPAREN)
            
            self.consume_with_filename(TokenType.LBRACE)
            body = self.parse_statements()
            self.consume_with_filename(TokenType.RBRACE)
            
            return ForStatement(
                init=init,
                condition=condition,
                update=update,
                body=body
            )
    
    def parse_import_statement(self) -> ImportStatement:
        self.consume_with_filename(TokenType.IMPORT)
        
        # 获取模块名（标识符）
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            module_name = self.current_token.value
            self.advance()
        else:
            raise SyntaxError(f"Import statement expects module name at line {self.current_token.line if self.current_token else 0}")
        
        # 允许语句以分号或换行符结尾
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon or newline after import statement at line {self.current_token.line if self.current_token else 0}")
        
        return ImportStatement(module_name=module_name)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        
        # 允许语句以分号或换行符结尾
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon or newline after expression at line {self.current_token.line if self.current_token else 0}")
        
        return ExpressionStatement(expression=expr)
    
    def parse_expression(self) -> Expression:
        expr = self.parse_assignment()
        # Add line/column info to expression
        if hasattr(expr, 'line') and expr.line == 0 and self.current_token:
            expr.line = self.current_token.line
            expr.column = self.current_token.column
        return expr
    
    def parse_assignment(self) -> Expression:
        left = self.parse_logical_or()
        
        if self.current_token and self.current_token.type == TokenType.ASSIGN:
            self.advance()
            right = self.parse_assignment()
            return BinaryExpression(left=left, operator='=', right=right)
        
        return left
    
    def parse_logical_or(self) -> Expression:
        left = self.parse_logical_and()
        
        while self.current_token and (self.current_token.type == TokenType.OR or 
                                     (self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == 'or')):
            operator = '||' if self.current_token.type == TokenType.OR else self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_logical_and(self) -> Expression:
        left = self.parse_equality()
        
        while self.current_token and (self.current_token.type == TokenType.AND or 
                                     (self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == 'and')):
            operator = '&&' if self.current_token.type == TokenType.AND else self.current_token.value
            self.advance()
            right = self.parse_equality()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_bitwise_or(self) -> Expression:
        left = self.parse_bitwise_xor()
        
        while self.current_token and self.current_token.type == TokenType.BITWISE_OR:
            operator = '|'
            self.advance()
            right = self.parse_bitwise_xor()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_bitwise_xor(self) -> Expression:
        left = self.parse_bitwise_and()
        
        while self.current_token and self.current_token.type == TokenType.BITWISE_XOR:
            operator = '^^'
            self.advance()
            right = self.parse_bitwise_and()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_bitwise_and(self) -> Expression:
        left = self.parse_shift()
        
        while self.current_token and self.current_token.type == TokenType.BITWISE_AND:
            operator = '&'
            self.advance()
            right = self.parse_shift()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_shift(self) -> Expression:
        left = self.parse_comparison()
        
        while self.current_token and self.current_token.type in (TokenType.LEFT_SHIFT, TokenType.RIGHT_SHIFT):
            operator = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_power(self) -> Expression:
        left = self.parse_postfix()
        
        while self.current_token and self.current_token.type in (TokenType.POWER, TokenType.POWER3, TokenType.POWERX):
            if self.current_token.type == TokenType.POWER:
                operator = '^'
                self.advance()
                # 幂运算应该是右结合的，所以递归调用parse_power
                right = self.parse_power()
            elif self.current_token.type == TokenType.POWER3:
                operator = '^3'
                self.advance()
                right = Literal(value=3)  # 立方
            else:  # POWERX
                operator = self.current_token.value
                # 提取数字部分
                power_num = int(operator[1:])  # 去掉^符号
                self.advance()
                right = Literal(value=power_num)
            
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_equality(self) -> Expression:
        left = self.parse_bitwise_or()
        
        while self.current_token and self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.current_token.value
            self.advance()
            right = self.parse_bitwise_or()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_comparison(self) -> Expression:
        left = self.parse_term()
        
        while self.current_token and self.current_token.type in (TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_term(self) -> Expression:
        left = self.parse_factor()
        
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_factor(self) -> Expression:
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_unary(self) -> Expression:
        if self.current_token and self.current_token.type in (TokenType.MINUS, TokenType.PLUS, TokenType.NOT):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression(operator=operator, operand=operand)
        
        return self.parse_power()  # 修改：先解析幂运算
    
    def parse_postfix(self) -> Expression:
        expr = self.parse_primary()
        
        while self.current_token:
            if self.current_token.type == TokenType.LPAREN:
                self.advance()
                arguments = []
                keyword_arguments = {}
                
                # 解析参数列表
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    # 检查是否是命名参数 (identifier : expression)
                    if (self.current_token.type == TokenType.IDENTIFIER and 
                        self.peek_token() and self.peek_token().type == TokenType.COLON):
                        # 命名参数
                        param_name = self.current_token.value
                        self.advance()  # 消费参数名
                        self.advance()  # 消费冒号
                        param_value = self.parse_expression()
                        keyword_arguments[param_name] = param_value
                    else:
                        # 位置参数
                        arguments.append(self.parse_expression())
                    
                    while self.current_token and self.current_token.type == TokenType.COMMA:
                        self.advance()
                        # 继续解析参数，检查是否是命名参数
                        if (self.current_token.type == TokenType.IDENTIFIER and 
                            self.peek_token() and self.peek_token().type == TokenType.COLON):
                            # 命名参数
                            param_name = self.current_token.value
                            self.advance()  # 消费参数名
                            self.advance()  # 消费冒号
                            param_value = self.parse_expression()
                            keyword_arguments[param_name] = param_value
                        else:
                            # 位置参数
                            arguments.append(self.parse_expression())
                
                self.consume_with_filename(TokenType.RPAREN)
                
                if isinstance(expr, Identifier):
                    expr = CallExpression(function=expr.name, arguments=arguments, keyword_arguments=keyword_arguments)
                elif isinstance(expr, MemberExpression):
                    expr = CallExpression(function=f"{expr.object}.{expr.property}", arguments=arguments, keyword_arguments=keyword_arguments)
                else:
                    raise SyntaxError(f"无效的函数调用")
            
            elif self.current_token.type == TokenType.DOT:
                self.advance()
                if self.current_token and (self.current_token.type == TokenType.IDENTIFIER or self.current_token.type == TokenType.PRINT or self.current_token.type == TokenType.INPUT):
                    property_name = self.current_token.value
                    self.advance()
                    
                    if isinstance(expr, Identifier):
                        expr = MemberExpression(object=expr.name, property=property_name)
                    elif isinstance(expr, MemberExpression):
                        # 支持链式调用，如 System.out.print
                        expr = MemberExpression(object=f"{expr.object}.{expr.property}", property=property_name)
                    else:
                        raise SyntaxError(f"无效的 member 访问")
                else:
                    raise SyntaxError(f"期望标识符在 '.' 后")
            elif self.current_token.type == TokenType.LBRACKET:
                # 处理下标访问，如 a[0], a["key"]
                self.advance()  # 消费 '['
                index_expr = self.parse_expression()
                self.consume_with_filename(TokenType.RBRACKET)
                expr = IndexExpression(object=expr, index=index_expr)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> Expression:
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            if '.' in value:
                return Literal(value=float(value))
            else:
                return Literal(value=int(value))
        
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return Literal(value=value)
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            return Identifier(name=name)
        
        elif self.current_token.type == TokenType.SYSTEM:
            name = self.current_token.value
            self.advance()
            return Identifier(name=name)
        
        elif self.current_token.type == TokenType.PRINT:
            name = self.current_token.value
            self.advance()
            return Identifier(name=name)
        
        elif self.current_token.type == TokenType.INPUT:
            name = self.current_token.value
            self.advance()
            return Identifier(name=name)
        
        elif self.current_token.type == TokenType.LBRACKET:
            return self.parse_array_expression()
        
        elif self.current_token.type == TokenType.LBRACE:
            return self.parse_dict_expression()
        
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.consume_with_filename(TokenType.RPAREN)
            return expr
        
        elif self.current_token.type == TokenType.DIVIDE:
            # 处理除法运算符
            operator = self.current_token.value
            self.advance()
            return Identifier(name=operator)
        else:
            raise SyntaxError(f"意外的标记: {self.current_token.value}")
    
    def parse_array_expression(self) -> Expression:
        """解析数组表达式 [item1, item2, ...]"""
        self.consume_with_filename(TokenType.LBRACKET)
        elements = []
        
        # 检查空数组 []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            
            # 解析剩余的元素
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # 消费逗号
                if self.current_token and self.current_token.type != TokenType.RBRACKET:
                    elements.append(self.parse_expression())
        
        self.consume_with_filename(TokenType.RBRACKET)
        return ArrayExpression(elements=elements)
    
    def parse_dict_expression(self) -> Expression:
        """解析字典表达式 {key1: value1, key2: value2, ...}"""
        self.consume_with_filename(TokenType.LBRACE)
        entries = []  # 使用列表存储键值对
        
        # 跳过初始的换行符（如果有）
        self.skip_newlines()
        
        # 检查空字典 {}
        if self.current_token and self.current_token.type != TokenType.RBRACE:
            key = self.parse_expression()
            self.consume_with_filename(TokenType.COLON)
            value = self.parse_expression()
            entries.append((key, value))  # 存储为元组
            
            # 解析剩余的键值对
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # 消费逗号
                self.skip_newlines()  # 跳过换行符
                if self.current_token and self.current_token.type != TokenType.RBRACE:
                    key = self.parse_expression()
                    self.consume_with_filename(TokenType.COLON)
                    value = self.parse_expression()
                    entries.append((key, value))  # 存储为元组
        
        self.skip_newlines()  # 跳过最后的换行符
        self.consume_with_filename(TokenType.RBRACE)
        return DictExpression(entries=entries)

def main():
    # 测试解析器
    code = '''
func main() {
    System.print("Hello World!"):
}
'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAST 结构:")
    for func in ast.functions:
        print(f"函数: {func.name}")
        for stmt in func.body:
            print(f"  语句: {type(stmt).__name__}")
            if hasattr(stmt, 'expression'):
                print(f"    表达式: {type(stmt.expression).__name__}")
                if hasattr(stmt.expression, 'function'):
                    print(f"    函数: {stmt.expression.function}")
                if hasattr(stmt.expression, 'arguments'):
                    print(f"    参数: {len(stmt.expression.arguments)}")
                    for i, arg in enumerate(stmt.expression.arguments):
                        print(f"      参数 {i}: {type(arg).__name__}")

if __name__ == "__main__":
    main()