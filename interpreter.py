from typing import Any, Dict, List, Optional
import os
import sys
from parser import (Program, FunctionDef, Statement, Expression, ExpressionStatement, 
                   ReturnStatement, IfStatement, WhileStatement, ForStatement,
                   BinaryExpression, UnaryExpression, CallExpression, MemberExpression,
                   Identifier, Literal, ArrayExpression, DictExpression, IndexExpression,
                   BreakStatement, ContinueStatement, ImportStatement)

class VanctionRuntimeError(Exception):
    def __init__(self, message: str, file: str = "", line: int = 0, column: int = 0):
        self.file = file
        self.line = line
        self.column = column
        super().__init__(message)

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDef] = {}
    
    def define(self, name: str, value: Any):
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise VanctionRuntimeError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise VanctionRuntimeError(f"Undefined variable: {name}")
    
    def define_function(self, name: str, func: FunctionDef):
        self.functions[name] = func
    
    def get_function(self, name: str) -> FunctionDef:
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise VanctionRuntimeError(f"Undefined function: {name}")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    """break语句异常"""
    pass

class ContinueException(Exception):
    """continue语句异常"""
    pass

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtin_functions()
        self.current_file = ""
    
    def setup_builtin_functions(self):
        # System.print function with end parameter support
        def system_print(*args, **kwargs):
            # 处理命名参数
            end = kwargs.get('end', '\n')  # 默认换行
            
            # 如果没有位置参数但有message命名参数
            if not args and 'message' in kwargs:
                output = str(kwargs['message'])
            elif args:
                # 使用位置参数
                output = ' '.join(str(arg) for arg in args)
            else:
                output = ''
            
            print(output, end=end)
            return None
        
        # System.input function
        def system_input(prompt=""):
            try:
                return input(prompt)
            except (EOFError, KeyboardInterrupt):
                return ""
        
        self.global_env.define("System.print", system_print)
        self.global_env.define("System.input", system_input)
        
        # Other built-in functions
        self.global_env.define("len", len)
        self.global_env.define("str", str)
        self.global_env.define("int", int)
        self.global_env.define("float", float)
        
        # 布尔值常量
        self.global_env.define("true", True)
        self.global_env.define("false", False)
    
    def interpret(self, program: Program, filename: str = ""):
        self.current_file = filename
        
        # First register all functions
        for func in program.functions:
            self.global_env.define_function(func.name, func)
        
        # Find and execute main function
        if "main" in self.global_env.functions:
            main_func = self.global_env.get_function("main")
            try:
                self.execute_function(main_func, [])
            except VanctionRuntimeError as e:
                if not e.file:
                    e.file = filename
                self.print_runtime_error(e)
                return False
            except Exception as e:
                error = VanctionRuntimeError(f"Runtime error: {str(e)}", filename)
                self.print_runtime_error(error)
                return False
        else:
            error = VanctionRuntimeError("Main function not found", filename)
            self.print_runtime_error(error)
            return False
        
        return True
    
    def print_runtime_error(self, error: VanctionRuntimeError):
        """Print runtime error with file, line, and column information"""
        print(f"Runtime Error: {error}")
        if error.file and error.line > 0:
            print(f"  --> \"{error.file}\" {error.line} line {error.column} column")
            # Try to show the line with error
            try:
                with open(error.file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if error.line <= len(lines):
                        line_content = lines[error.line - 1].rstrip()
                        print(f"   {error.line} | {line_content}")
                        # Point to the error position
                        pointer = ' ' * (len(str(error.line)) + 3 + error.column - 1) + '^^^^'
                        print(pointer)
            except:
                pass  # If can't read file, just show the error message
    
    def execute_function(self, func: FunctionDef, arguments: List[Any]) -> Any:
        # Create new function scope
        func_env = Environment(self.global_env)
        
        # Bind arguments
        if len(arguments) != len(func.parameters):
            raise VanctionRuntimeError(
                f"Function {func.name} expects {len(func.parameters)} arguments, got {len(arguments)}",
                self.current_file, func.line if hasattr(func, 'line') else 0, 0
            )
        
        for param, arg in zip(func.parameters, arguments):
            func_env.define(param, arg)
        
        try:
            # Execute function body
            for statement in func.body:
                self.execute_statement(statement, func_env)
            
            # If no return statement, return None
            return None
        except ReturnException as e:
            return e.value
        except VanctionRuntimeError:
            # Re-raise runtime error, keep original error info
            raise
        except Exception as e:
            # Catch other exceptions, provide friendly error message
            raise VanctionRuntimeError(f"Function execution error: {str(e)}", self.current_file)
    
    def execute_statement(self, statement: Statement, env: Environment):
        if isinstance(statement, ExpressionStatement):
            expr = statement.expression
            # Handle assignment expressions
            if isinstance(expr, BinaryExpression) and expr.operator == '=':
                self.evaluate_expression(expr, env)
            else:
                # Regular expression, evaluate but don't print result
                self.evaluate_expression(expr, env)
        
        elif isinstance(statement, ReturnStatement):
            value = None
            if statement.value:
                value = self.evaluate_expression(statement.value, env)
            raise ReturnException(value)
        
        elif isinstance(statement, IfStatement):
            condition = self.evaluate_expression(statement.condition, env)
            
            if self.is_truthy(condition):
                for stmt in statement.then_body:
                    self.execute_statement(stmt, env)
            elif statement.else_body:
                for stmt in statement.else_body:
                    self.execute_statement(stmt, env)
        
        elif isinstance(statement, WhileStatement):
            while self.is_truthy(self.evaluate_expression(statement.condition, env)):
                for stmt in statement.body:
                    self.execute_statement(stmt, env)
        
        elif isinstance(statement, ForStatement):
            self.execute_for_statement(statement, env)
        
        elif isinstance(statement, BreakStatement):
            raise BreakException()
        
        elif isinstance(statement, ContinueStatement):
            raise ContinueException()
        
        elif isinstance(statement, ImportStatement):
            self.execute_import_statement(statement, env)
        
        else:
            raise VanctionRuntimeError(f"Unknown statement type: {type(statement)}", self.current_file)
    
    def execute_for_statement(self, statement: ForStatement, env: Environment):
        """执行for循环语句"""
        if statement.variable and statement.iterable:
            # for (item in collection) 语法
            iterable = self.evaluate_expression(statement.iterable, env)
            
            # 确保iterable是可迭代的
            if isinstance(iterable, list):
                for item in iterable:
                    # 创建新的局部环境，避免污染外部作用域
                    loop_env = Environment(parent=env)
                    loop_env.define(statement.variable, item)
                    
                    try:
                        for stmt in statement.body:
                            self.execute_statement(stmt, loop_env)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
            else:
                raise VanctionRuntimeError(f"Object is not iterable: {type(iterable)}", self.current_file)
        else:
            # 传统 for (init; condition; update) 语法
            # 执行初始化
            if statement.init:
                self.evaluate_expression(statement.init, env)
            
            # 循环执行
            while True:
                # 检查条件
                if statement.condition:
                    condition_value = self.evaluate_expression(statement.condition, env)
                    if not self.is_truthy(condition_value):
                        break
                
                try:
                    # 执行循环体
                    for stmt in statement.body:
                        self.execute_statement(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    pass  # continue直接进入下一轮循环
                
                # 执行更新
                if statement.update:
                    self.evaluate_expression(statement.update, env)
    
    def execute_import_statement(self, statement: ImportStatement, env: Environment):
        """执行import语句，加载并执行模块文件"""
        module_name = statement.module_name
        
        # 构建模块文件路径（当前目录下的 .va 文件）
        module_filename = f"{module_name}.va"
        
        # 如果当前有执行文件，则相对于当前文件目录查找
        if self.current_file and os.path.exists(self.current_file):
            current_dir = os.path.dirname(self.current_file)
            module_path = os.path.join(current_dir, module_filename)
        else:
            # 否则在当前工作目录查找
            module_path = module_filename
        
        # 检查模块文件是否存在
        if not os.path.exists(module_path):
            raise VanctionRuntimeError(f"Module '{module_name}' not found: {module_path}", self.current_file)
        
        try:
            # 读取模块文件内容
            with open(module_path, 'r', encoding='utf-8') as f:
                module_code = f.read()
            
            # 词法分析
            lexer = Lexer(module_code)
            tokens = lexer.tokenize()
            
            # 语法分析
            parser = Parser(tokens, module_path)
            module_ast = parser.parse()
            
            # 创建新的解释器实例来执行模块（避免污染当前环境）
            module_interpreter = Interpreter()
            
            # 在模块环境中执行，但将函数注册到当前全局环境
            for func in module_ast.functions:
                # 将模块函数注册到当前全局环境，使用模块名作为前缀避免命名冲突
                func_name = f"{module_name}.{func.name}"
                
                # 修改函数名称为带模块前缀的版本
                module_func = FunctionDef(
                    name=func_name,
                    parameters=func.parameters,
                    body=func.body,
                    line=func.line,
                    column=func.column
                )
                
                self.global_env.define_function(func_name, module_func)
            
        except Exception as e:
            raise VanctionRuntimeError(f"Error importing module '{module_name}': {str(e)}", self.current_file)
    
    def evaluate_expression(self, expr: Expression, env: Environment) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        
        elif isinstance(expr, Identifier):
            return env.get(expr.name)
        
        elif isinstance(expr, BinaryExpression):
            if expr.operator == '=':
                # Assignment
                if isinstance(expr.left, Identifier):
                    var_name = expr.left.name
                    value = self.evaluate_expression(expr.right, env)
                    # 如果变量已存在，使用set更新；否则使用define创建
                    try:
                        env.set(var_name, value)
                    except VanctionRuntimeError:
                        # 变量不存在，创建新变量
                        env.define(var_name, value)
                    return value
                else:
                    raise VanctionRuntimeError(f"Invalid assignment target: {type(expr.left)}", self.current_file)
            
            left = self.evaluate_expression(expr.left, env)
            right = self.evaluate_expression(expr.right, env)
            
            if expr.operator == '+':
                return left + right
            elif expr.operator == '-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                return left / right
            elif expr.operator == '%':
                return left % right
            elif expr.operator == '^':
                return left ** right
            elif expr.operator == '==':
                return left == right
            elif expr.operator == '!=':
                return left != right
            elif expr.operator == '<':
                return left < right
            elif expr.operator == '>':
                return left > right
            elif expr.operator == '<=':
                return left <= right
            elif expr.operator == '>=':
                return left >= right
            elif expr.operator == '&&':
                return self.is_truthy(left) and self.is_truthy(right)
            elif expr.operator == '||':
                return self.is_truthy(left) or self.is_truthy(right)
            else:
                raise VanctionRuntimeError(f"Unknown binary operator: {expr.operator}", self.current_file)
        
        elif isinstance(expr, CallExpression):
            return self.evaluate_call_expression(expr, env)
        
        elif isinstance(expr, ArrayExpression):
            return [self.evaluate_expression(elem, env) for elem in expr.elements]
        
        elif isinstance(expr, DictExpression):
            result = {}
            for key_expr, value_expr in expr.entries:
                key_val = self.evaluate_expression(key_expr, env)
                value_val = self.evaluate_expression(value_expr, env)
                # 确保键是可哈希的类型
                if not isinstance(key_val, (int, float, str, bool, type(None))):
                    raise VanctionRuntimeError(f"Dictionary key must be a hashable type, got {type(key_val).__name__}", self.current_file)
                result[key_val] = value_val
            return result
        
        elif isinstance(expr, IndexExpression):
            obj = self.evaluate_expression(expr.object, env)
            index = self.evaluate_expression(expr.index, env)
            
            if isinstance(obj, str):
                # 字符串下标访问
                if isinstance(index, int):
                    if 0 <= index < len(obj):
                        return obj[index]
                    else:
                        raise VanctionRuntimeError(f"String index {index} out of range", self.current_file)
                else:
                    raise VanctionRuntimeError(f"String index must be integer, got {type(index).__name__}", self.current_file)
            
            elif isinstance(obj, list):
                # 列表下标访问
                if isinstance(index, int):
                    if 0 <= index < len(obj):
                        return obj[index]
                    else:
                        raise VanctionRuntimeError(f"List index {index} out of range", self.current_file)
                else:
                    raise VanctionRuntimeError(f"List index must be integer, got {type(index).__name__}", self.current_file)
            
            elif isinstance(obj, dict):
                # 字典下标访问
                if index in obj:
                    return obj[index]
                else:
                    raise VanctionRuntimeError(f"Key '{index}' not found in dictionary", self.current_file)
            
            else:
                raise VanctionRuntimeError(f"Cannot index object of type {type(obj).__name__}", self.current_file)
        
        else:
            raise VanctionRuntimeError(f"Unknown expression type: {type(expr)}", self.current_file)
    
    def evaluate_call_expression(self, expression: CallExpression, env: Environment) -> Any:
        function_name = expression.function
        
        # Handle built-in functions and user-defined functions
        if '.' in function_name:
            # First check if it's a user-defined function (like math.add)
            if function_name in self.global_env.functions:
                func = self.global_env.get_function(function_name)
                arguments = [self.evaluate_expression(arg, env) for arg in expression.arguments]
                return self.execute_function(func, arguments)
            else:
                # Try to get from global environment (for built-in functions like System.print)
                try:
                    builtin_func = self.global_env.get(function_name)
                    
                    # 处理位置参数和命名参数
                    arguments = [self.evaluate_expression(arg, env) for arg in expression.arguments]
                    keyword_arguments = {name: self.evaluate_expression(arg, env) 
                                       for name, arg in expression.keyword_arguments.items()}
                    
                    if callable(builtin_func):
                        return builtin_func(*arguments, **keyword_arguments)
                    else:
                        raise VanctionRuntimeError(f"{function_name} is not a callable function", self.current_file)
                except VanctionRuntimeError as e:
                    # Re-throw original error, don't mask it
                    raise e
                except Exception as e:
                    raise VanctionRuntimeError(f"Undefined function: {function_name}", self.current_file)
        else:
            # Regular function call - first check user-defined functions, then built-in functions
            if function_name in self.global_env.functions:
                func = self.global_env.get_function(function_name)
                arguments = [self.evaluate_expression(arg, env) for arg in expression.arguments]
                return self.execute_function(func, arguments)
            else:
                # Check if it's a built-in function (stored as variables)
                try:
                    builtin_func = env.get(function_name)
                    if callable(builtin_func):
                        arguments = [self.evaluate_expression(arg, env) for arg in expression.arguments]
                        return builtin_func(*arguments)
                    else:
                        raise VanctionRuntimeError(f"{function_name} is not a callable function", self.current_file)
                except VanctionRuntimeError:
                    raise VanctionRuntimeError(f"Undefined function: {function_name}", self.current_file)
    
    def is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        else:
            return True