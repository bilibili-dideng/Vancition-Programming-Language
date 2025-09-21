from typing import List, Optional, Union, Dict, Tuple
from dataclasses import dataclass
from lexer import Token, TokenType, Lexer

# AST Node Definitions
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
    top_level_statements: List['Statement'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.functions is None:
            self.functions = []
        if self.top_level_statements is None:
            self.top_level_statements = []

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
    module_name: str = ""  # Module name
    alias: str = ""  # Import alias, for import xxx using xxx syntax
    using: bool = False  # Whether to use alias import

@dataclass
class BreakStatement(Statement):
    pass

@dataclass
class ContinueStatement(Statement):
    pass

@dataclass
class ForStatement(Statement):
    variable: Optional[str] = None  # For for (item in collection)
    iterable: Optional['Expression'] = None  # For for (item in collection)
    init: Optional['Expression'] = None  # For traditional for loop
    condition: Optional['Expression'] = None  # For traditional for loop
    update: Optional['Expression'] = None  # For traditional for loop
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
class MultiAssignmentExpression(Expression):
    variables: list = None
    value: Expression = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.variables is None:
            self.variables = []

@dataclass
class CallExpression(Expression):
    function: Union[str, 'LambdaExpression'] = ""
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
class TupleExpression(Expression):
    elements: List['Expression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.elements is None:
            self.elements = []

@dataclass
class TryStatement(Statement):
    try_body: List[Statement] = None
    catch_body: Optional[List[Statement]] = None
    exception_var: Optional[str] = None
    exception_type: Optional[str] = None  # New: specify exception type to catch
    finally_body: Optional[List[Statement]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.try_body is None:
            self.try_body = []
        if self.catch_body is None:
            self.catch_body = None
        if self.finally_body is None:
            self.finally_body = None

@dataclass
class ThrowStatement(Statement):
    expression: Optional['Expression'] = None

@dataclass
class LambdaExpression(Expression):
    parameters: List[str] = None
    body: 'Expression' = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.parameters is None:
            self.parameters = []

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

@dataclass
class SwitchStatement(Statement):
    expression: 'Expression' = None
    cases: List['CaseStatement'] = None
    default_case: Optional[List[Statement]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.cases is None:
            self.cases = []
        if self.default_case is None:
            self.default_case = None

@dataclass
class CaseStatement(ASTNode):
    value: 'Expression' = None
    body: List[Statement] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.body is None:
            self.body = []

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
        top_level_statements = []  # Store top-level statements (like import)
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token and self.current_token.type == TokenType.FUNC:
                functions.append(self.parse_function())
            elif self.current_token and self.current_token.type == TokenType.IMPORT:
                # Collect top-level import statements
                top_level_statements.append(self.parse_import_statement())
            else:
                # Handle other top-level statements (like expression statements)
                if self.current_token and self.current_token.type != TokenType.EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        top_level_statements.append(stmt)
                else:
                    break
        
        # Return program with both functions and top-level statements
        return Program(
            functions=functions,
            top_level_statements=top_level_statements
        )
    
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
            # Check for colon after right brace (only needed in certain contexts)
            if self.current_token and self.current_token.type == TokenType.RBRACE and self.peek_token() and self.peek_token().type == TokenType.COLON:
                # Skip colon after right brace (used for if-else and while statements)
                if self.peek_token() and self.peek_token().type == TokenType.COLON:
                    self.advance()  # Skip RBRACE
                    self.advance()  # Skip COLON
                    break
        
        return statements
    
    def parse_statement(self) -> Statement:
        # Save current token position for error reporting
        start_token = self.current_token

        if self.current_token.type == TokenType.FUNC:
            # Support nested function definitions
            return self.parse_function()
        elif self.current_token.type == TokenType.RETURN:
            stmt = self.parse_return_statement()
        elif self.current_token.type == TokenType.IF:
            stmt = self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            stmt = self.parse_while_statement()
        elif self.current_token.type == TokenType.FOR:
            stmt = self.parse_for_statement()
        elif self.current_token.type == TokenType.SWITCH:
            stmt = self.parse_switch_statement()
        elif self.current_token.type == TokenType.TRY:
            stmt = self.parse_try_statement()
        elif self.current_token.type == TokenType.THROW:
            stmt = self.parse_throw_statement()
        elif self.current_token.type == TokenType.DEFINE:
            # Handle define statement: define variableName;
            self.advance()  # Consume 'define'
            if self.current_token.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected identifier after 'define' at line {start_token.line if start_token else 0}")
            var_name = self.current_token.value
            self.advance()
            
            # Check for semicolon
            if self.current_token.type != TokenType.SEMICOLON:
                raise SyntaxError(f"Expected semicolon after 'define {var_name}' at line {start_token.line if start_token else 0}")
            self.advance()
            
            # Create an assignment expression with anytion value
            left = Identifier(name=var_name)
            right = Identifier(name="anytion")
            expr = BinaryExpression(left=left, operator='=', right=right)
            stmt = ExpressionStatement(expression=expr)
            stmt.line = start_token.line
            stmt.column = start_token.column
        elif self.current_token.type == TokenType.IMMUT:
            # Handle immut statement: immut variableName = value;
            self.advance()  # Consume 'immut'
            if self.current_token.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected identifier after 'immut' at line {start_token.line if start_token else 0}")
            var_name = self.current_token.value
            self.advance()
            
            if self.current_token.type != TokenType.ASSIGN:
                raise SyntaxError(f"Expected '=' after 'immut {var_name}' at line {start_token.line if start_token else 0}")
            self.advance()
            
            # Parse the value expression
            value = self.parse_expression()
            
            # Check for semicolon
            if self.current_token.type != TokenType.SEMICOLON:
                raise SyntaxError(f"Expected semicolon after 'immut {var_name} = ...' at line {start_token.line if start_token else 0}")
            self.advance()
            
            # Create an assignment expression with special metadata for immut
            left = Identifier(name=var_name)
            expr = BinaryExpression(left=left, operator='=', right=value)
            expr.is_constant = True  # Mark as constant
            stmt = ExpressionStatement(expression=expr)
            stmt.line = start_token.line
            stmt.column = start_token.column
        elif self.current_token.type == TokenType.BREAK:
            self.advance()
            stmt = BreakStatement()
            # break statement also needs semicolon or newline
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            elif self.current_token and self.current_token.type == TokenType.NEWLINE:
                self.advance()
            # break statement can be without semicolon (in certain contexts)
            
        elif self.current_token.type == TokenType.CONTINUE:
            self.advance()
            stmt = ContinueStatement()
            # continue statement also needs semicolon or newline
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            elif self.current_token and self.current_token.type == TokenType.NEWLINE:
                self.advance()
            # continue statement can be without semicolon (in certain contexts)
        elif self.current_token.type == TokenType.IMPORT:
            stmt = self.parse_import_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Check if it's function call or assignment
            stmt = self.parse_expression_statement()
        elif self.current_token.type == TokenType.SYSTEM:
            # Handle calls like System.print
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
        
        # Allow statements to end with semicolon or newline
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon or newline after return statement at line {self.current_token.line if self.current_token else 0}")
        
        return ReturnStatement(value=value)
    
    def parse_try_statement(self) -> TryStatement:
        self.consume_with_filename(TokenType.TRY)
        self.consume_with_filename(TokenType.LBRACE)
        
        try_body = self.parse_statements()
        self.consume_with_filename(TokenType.RBRACE)
        
        catch_body = None
        exception_var = None
        exception_type = None
        
        if self.current_token and self.current_token.type == TokenType.CATCH:
            self.advance()
            
            # Support new catch syntax: catch ([exception_type]) as [variable] {}
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                self.consume_with_filename(TokenType.LPAREN)
                
                # Parse exception type (optional)
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                    exception_type = self.consume_with_filename(TokenType.IDENTIFIER).value
                
                self.consume_with_filename(TokenType.RPAREN)
                
                # Parse "as" keyword and variable name
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "as":
                    self.advance()  # Consume "as"
                    exception_var = self.consume_with_filename(TokenType.IDENTIFIER).value
            else:
                # Backward compatibility: catch {}
                exception_var = None
                exception_type = None
            
            self.consume_with_filename(TokenType.LBRACE)
            catch_body = self.parse_statements()
            self.consume_with_filename(TokenType.RBRACE)
        
        finally_body = None
        if self.current_token and self.current_token.type == TokenType.FINALLY:
            self.advance()
            self.consume_with_filename(TokenType.LBRACE)
            finally_body = self.parse_statements()
            self.consume_with_filename(TokenType.RBRACE)
        
        return TryStatement(try_body=try_body, catch_body=catch_body, finally_body=finally_body, 
                         exception_var=exception_var, exception_type=exception_type)
    
    def parse_throw_statement(self) -> ThrowStatement:
        self.consume_with_filename(TokenType.THROW)
        expression = self.parse_expression()
        
        # Allow statement to end with semicolon or newline
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        
        return ThrowStatement(expression=expression)
    
    def parse_if_statement(self) -> IfStatement:
        self.consume_with_filename(TokenType.IF)
        condition = self.parse_expression()
        self.consume_with_filename(TokenType.LBRACE)
        
        then_body = self.parse_statements()
        self.consume_with_filename(TokenType.RBRACE)
        
        else_body = None
        # Handle else-if and else parts
        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE_IF:
            # Handle multiple else-if
            current_if = None
            while self.current_token and self.current_token.type == TokenType.ELSE_IF:
                self.advance()  # Consume else-if
                else_if_condition = self.parse_expression()
                self.consume_with_filename(TokenType.LBRACE)
                else_if_body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                
                # Create if statement
                new_if = IfStatement(
                    condition=else_if_condition, 
                    then_body=else_if_body, 
                    else_body=None
                )
                
                if current_if is None:
                    current_if = new_if
                else:
                    # Link new if statement to previous one's else part
                    current_if.else_body = [new_if]
                    current_if = new_if
            
            # Check if there's else part
            if self.current_token and self.current_token.type == TokenType.ELSE:
                self.advance()  # Consume else
                self.consume_with_filename(TokenType.LBRACE)
                final_else_body = self.parse_statements()
                self.consume_with_filename(TokenType.RBRACE)
                current_if.else_body = final_else_body
            
            else_body = [current_if] if current_if else None
            
        elif self.current_token and self.current_token.type == TokenType.ELSE:
            # Regular else (no longer supports else if syntax)
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
        
        # Parse three forms of for loop:
        # 1. for (init; condition; update) { body }
        # 2. for (item in array) { body }
        # 3. for (key, value in dict) { body }
        
        self.consume_with_filename(TokenType.LPAREN)
        
        # Check if it's range loop syntax
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.value == 'in':
                # for (item in collection) syntax
                self.advance()  # Consume 'in'
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
                # Traditional for loop: for (init; condition; update)
                # Rollback and parse initialization
                self.position -= 1  # Rollback
                self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
                
                # Parse initialization statement
                init = None
                if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                    init = self.parse_expression()
                self.consume_with_filename(TokenType.SEMICOLON)
                
                # Parse condition
                condition = None
                if self.current_token and self.current_token.type != TokenType.SEMICOLON:
                    condition = self.parse_expression()
                self.consume_with_filename(TokenType.SEMICOLON)
                
                # Parse update
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
            # Traditional for loop: for (; condition; update) or for (;;)
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
    
    def parse_switch_statement(self) -> SwitchStatement:
        """Parse switch statement"""
        self.consume_with_filename(TokenType.SWITCH)
        expression = self.parse_expression()
        self.consume_with_filename(TokenType.LBRACE)
        
        cases = []
        default_case = None
        
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            self.skip_newlines()
            
            if self.current_token and self.current_token.type == TokenType.CASE:
                self.advance()  # Consume 'case'
                case_value = self.parse_expression()
                self.consume_with_filename(TokenType.COLON)
                
                case_body = []
                # Parse case statement body until next case, default, or right brace
                while (self.current_token and 
                       self.current_token.type not in (TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE) and
                       self.current_token.type != TokenType.EOF):
                    if self.current_token.type == TokenType.NEWLINE:
                        self.advance()
                        continue
                    case_body.append(self.parse_statement())
                
                cases.append(CaseStatement(value=case_value, body=case_body))
                
            elif self.current_token and self.current_token.type == TokenType.DEFAULT:
                self.advance()  # Consume 'default'
                self.consume_with_filename(TokenType.COLON)
                
                default_body = []
                # Parse default statement body until next case or right brace
                while (self.current_token and 
                       self.current_token.type not in (TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE) and
                       self.current_token.type != TokenType.EOF):
                    if self.current_token.type == TokenType.NEWLINE:
                        self.advance()
                        continue
                    default_body.append(self.parse_statement())
                
                default_case = default_body
                
            else:
                self.advance()  # Skip unknown token
        
        self.consume_with_filename(TokenType.RBRACE)
        
        return SwitchStatement(expression=expression, cases=cases, default_case=default_case)
    
    def parse_import_statement(self) -> ImportStatement:
        self.consume_with_filename(TokenType.IMPORT)
        
        # Get module name (identifier), support folder.module format
        module_name = ""
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            module_name = self.current_token.value
            self.advance()
            
            # Support folder.module format
            while self.current_token and self.current_token.type == TokenType.DOT:
                self.advance()
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                    module_name += "." + self.current_token.value
                    self.advance()
                else:
                    raise SyntaxError(f"Expected identifier after dot in import statement at line {self.current_token.line if self.current_token else 0}")
        else:
            raise SyntaxError(f"Import statement expects module name at line {self.current_token.line if self.current_token else 0}")
        
        # Check for using alias syntax
        alias = ""
        using = False
        if self.current_token and self.current_token.type == TokenType.USING:
            using = True
            self.advance()
            if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                alias = self.current_token.value
                self.advance()
            else:
                raise SyntaxError(f"Expected alias name after 'using' in import statement at line {self.current_token.line if self.current_token else 0}")
        
        # Allow statements to end with semicolon or newline
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon or newline after import statement at line {self.current_token.line if self.current_token else 0}")
        
        return ImportStatement(module_name=module_name, alias=alias, using=using)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        
        # Allow statement to end with semicolon
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
        else:
            raise SyntaxError(f"Expected semicolon after expression at line {self.current_token.line if self.current_token else 0}")
        
        return ExpressionStatement(expression=expr)
    
    def parse_expression(self) -> Expression:
        expr = self.parse_assignment()
        # Add line/column info to expression
        if hasattr(expr, 'line') and expr.line == 0 and self.current_token:
            expr.line = self.current_token.line
            expr.column = self.current_token.column
        return expr
    
    def parse_assignment(self) -> Expression:
        # First try to parse a multi-variable assignment (a, b, c = value)
        # Check if we have identifiers separated by commas followed by assignment
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            # Look ahead to see if there's a comma after this identifier
            position = self.position
            temp_tokens = []
            temp_tokens.append(self.current_token)
            position += 1
            
            # Count how many consecutive identifier, comma pairs we have
            while position < len(self.tokens) and self.tokens[position].type == TokenType.COMMA and position + 1 < len(self.tokens) and self.tokens[position + 1].type == TokenType.IDENTIFIER:
                temp_tokens.append(self.tokens[position])  # Comma
                temp_tokens.append(self.tokens[position + 1])  # Next identifier
                position += 2
            
            # Check if after this sequence there's an assignment operator
            if position < len(self.tokens) and self.tokens[position].type == TokenType.ASSIGN:
                # This is a multi-variable assignment
                variables = []
                # Replay the token consumption
                for i in range(0, len(temp_tokens), 2):
                    var_name = temp_tokens[i].value
                    self.advance()  # Consume identifier
                    if i + 1 < len(temp_tokens):
                        self.advance()  # Consume comma
                
                # Consume assignment operator
                self.advance()
                
                # Parse the value expression
                value = self.parse_assignment()
                
                # Recreate the identifiers list
                variables = [Identifier(name=temp_tokens[i].value) for i in range(0, len(temp_tokens), 2)]
                
                return MultiAssignmentExpression(variables=variables, value=value)
        
        # If not a multi-variable assignment, parse regular assignment
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
                # Power operation should be right-associative, so recursively call parse_power
                right = self.parse_power()
            elif self.current_token.type == TokenType.POWER3:
                operator = '^3'
                self.advance()
                right = Literal(value=3)  # Cube
            else:  # POWERX
                operator = self.current_token.value
                # Extract numeric part
                power_num = int(operator[1:])  # Remove ^ symbol
                self.advance()
                right = Literal(value=power_num)
            
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_equality(self) -> Expression:
        left = self.parse_bitwise_or()
        
        while self.current_token and self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.current_token.value
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            self.advance()
            right = self.parse_bitwise_or()
            binary_expr = BinaryExpression(left=left, operator=operator, right=right)
            binary_expr.line = line
            binary_expr.column = column
            left = binary_expr
        
        return left
    
    def parse_comparison(self) -> Expression:
        left = self.parse_term()
        
        while self.current_token and self.current_token.type in (TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self.current_token.value
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            self.advance()
            right = self.parse_term()
            binary_expr = BinaryExpression(left=left, operator=operator, right=right)
            binary_expr.line = line
            binary_expr.column = column
            left = binary_expr
        
        return left
    
    def parse_term(self) -> Expression:
        left = self.parse_factor()
        
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            self.advance()
            right = self.parse_factor()
            binary_expr = BinaryExpression(left=left, operator=operator, right=right)
            binary_expr.line = line
            binary_expr.column = column
            left = binary_expr
        
        return left
    
    def parse_factor(self) -> Expression:
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.value
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            self.advance()
            right = self.parse_unary()
            binary_expr = BinaryExpression(left=left, operator=operator, right=right)
            binary_expr.line = line
            binary_expr.column = column
            left = binary_expr
        
        return left
    
    def parse_unary(self) -> Expression:
        if self.current_token and self.current_token.type in (TokenType.MINUS, TokenType.PLUS, TokenType.NOT):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression(operator=operator, operand=operand)
        
        return self.parse_power()  # Modified: parse power operation first
    
    def parse_postfix(self) -> Expression:
        expr = self.parse_primary()
        
        while self.current_token:
            if self.current_token.type == TokenType.LPAREN:
                self.advance()
                arguments = []
                keyword_arguments = {}
                
                # Parse parameter list
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    # Check if it's named parameter (identifier : expression)
                    if (self.current_token.type == TokenType.IDENTIFIER and 
                        self.peek_token() and self.peek_token().type == TokenType.COLON):
                        # Named parameter
                        param_name = self.current_token.value
                        self.advance()  # Consume parameter name
                        self.advance()  # Consume colon
                        param_value = self.parse_expression()
                        keyword_arguments[param_name] = param_value
                    else:
                        # Positional parameter
                        arguments.append(self.parse_expression())
                    
                    while self.current_token and self.current_token.type == TokenType.COMMA:
                        self.advance()
                        # Continue parsing parameters, check if it's named parameter
                        if (self.current_token.type == TokenType.IDENTIFIER and 
                            self.peek_token() and self.peek_token().type == TokenType.COLON):
                            # Named parameter
                            param_name = self.current_token.value
                            self.advance()  # Consume parameter name
                            self.advance()  # Consume colon
                            param_value = self.parse_expression()
                            keyword_arguments[param_name] = param_value
                        else:
                            # Positional parameter
                            arguments.append(self.parse_expression())
                
                self.consume_with_filename(TokenType.RPAREN)
                
                if isinstance(expr, Identifier):
                    expr = CallExpression(function=expr.name, arguments=arguments, keyword_arguments=keyword_arguments)
                elif isinstance(expr, MemberExpression):
                    expr = CallExpression(function=f"{expr.object}.{expr.property}", arguments=arguments, keyword_arguments=keyword_arguments)
                elif isinstance(expr, LambdaExpression):
                    # Support immediate invocation of anonymous functions, e.g. (lambda x, y -> x + y)(3, 4)
                    expr = CallExpression(function=expr, arguments=arguments, keyword_arguments=keyword_arguments)
                else:
                    raise SyntaxError(f"Invalid function call: expected Identifier or MemberExpression, but got {type(expr).__name__}")
            
            elif self.current_token.type == TokenType.DOT:
                self.advance()
                if self.current_token and (self.current_token.type == TokenType.IDENTIFIER or self.current_token.type == TokenType.PRINT or self.current_token.type == TokenType.INPUT):
                    property_name = self.current_token.value
                    self.advance()
                    
                    if isinstance(expr, Identifier):
                        expr = MemberExpression(object=expr.name, property=property_name)
                    elif isinstance(expr, MemberExpression):
                        # Support chained calls, like System.out.print
                        expr = MemberExpression(object=f"{expr.object}.{expr.property}", property=property_name)
                    else:
                        raise SyntaxError(f"Invalid member access")
                else:
                    raise SyntaxError(f"Expected identifier after '.'")
            elif self.current_token.type == TokenType.LBRACKET:
                # Handle subscript access, like a[0], a["key"]
                self.advance()  # Consume '['
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
        
        elif self.current_token.type == TokenType.LAMBDA:
            return self.parse_lambda_expression()
        
        elif self.current_token.type == TokenType.LPAREN:
            return self.parse_tuple_expression()
        
        elif self.current_token.type == TokenType.DIVIDE:
            # Handle division operator
            operator = self.current_token.value
            self.advance()
            return Identifier(name=operator)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.value}")
    
    def parse_lambda_expression(self) -> LambdaExpression:
        """Parse lambda expression: lambda x, y -> x + y"""
        self.consume_with_filename(TokenType.LAMBDA)
        
        parameters = []
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            parameters.append(self.consume_with_filename(TokenType.IDENTIFIER).value)
            
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
                parameters.append(self.consume_with_filename(TokenType.IDENTIFIER).value)
        
        self.consume_with_filename(TokenType.ARROW)
        body = self.parse_expression()
        
        return LambdaExpression(parameters=parameters, body=body)
    
    def parse_array_expression(self) -> Expression:
        """Parse array expression [item1, item2, ...]"""
        self.consume_with_filename(TokenType.LBRACKET)
        elements = []
        
        # Check empty array []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            
            # Parse remaining elements
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # Consume comma
                if self.current_token and self.current_token.type != TokenType.RBRACKET:
                    elements.append(self.parse_expression())
        
        self.consume_with_filename(TokenType.RBRACKET)
        return ArrayExpression(elements=elements)
    
    def parse_tuple_expression(self) -> Expression:
        """Parse tuple expression (item1, item2, ...)"""
        self.consume_with_filename(TokenType.LPAREN)
        elements = []
        
        # Check empty tuple ()
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            elements.append(self.parse_expression())
            
            # Parse remaining elements
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # Consume comma
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    elements.append(self.parse_expression())
        
        self.consume_with_filename(TokenType.RPAREN)
        
        # If only one element and no comma, return the element itself (not tuple)
        # This supports immediate invocation of anonymous functions like (lambda x -> x + 1)(5)
        if len(elements) == 1:
            return elements[0]
        
        return TupleExpression(elements=elements)
    
    def parse_dict_expression(self) -> Expression:
        """Parse dictionary expression {key1: value1, key2: value2, ...}"""
        self.consume_with_filename(TokenType.LBRACE)
        entries = []  # Use list to store key-value pairs
        
        # Skip initial newline (if any)
        self.skip_newlines()
        
        # Check empty dictionary {}
        if self.current_token and self.current_token.type != TokenType.RBRACE:
            key = self.parse_expression()
            self.consume_with_filename(TokenType.COLON)
            value = self.parse_expression()
            entries.append((key, value))  # Store as tuple
            
            # Parse remaining key-value pairs
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # Consume comma
                self.skip_newlines()  # Skip newline
                if self.current_token and self.current_token.type != TokenType.RBRACE:
                    key = self.parse_expression()
                    self.consume_with_filename(TokenType.COLON)
                    value = self.parse_expression()
                    entries.append((key, value))  # Store as tuple
        
        self.skip_newlines()  # Skip final newline
        self.consume_with_filename(TokenType.RBRACE)
        return DictExpression(entries=entries)

def main():
    # Test parser
    code = '''
func main() {
    System.print("Hello World!"):
}
'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAST Structure:")
    for func in ast.functions:
        print(f"Function: {func.name}")
        for stmt in func.body:
            print(f"  Statement: {type(stmt).__name__}")
            if hasattr(stmt, 'expression'):
                print(f"    Expression: {type(stmt.expression).__name__}")
                if hasattr(stmt.expression, 'function'):
                    print(f"    Function: {stmt.expression.function}")
                if hasattr(stmt.expression, 'arguments'):
                    print(f"    Arguments: {len(stmt.expression.arguments)}")
                    for i, arg in enumerate(stmt.expression.arguments):
                        print(f"      Argument {i}: {type(arg).__name__}")

if __name__ == "__main__":
    main()