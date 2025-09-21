from typing import Any, Dict, List, Optional
import os
import sys
from typing import Dict, List, Any, Optional, Callable

from lexer import Lexer
from parser import (Program, FunctionDef, Statement, Expression, ExpressionStatement,
                    ReturnStatement, IfStatement, WhileStatement, ForStatement,
                    BinaryExpression, UnaryExpression, CallExpression, MemberExpression,
                    Identifier, Literal, ArrayExpression, DictExpression, IndexExpression,
                    BreakStatement, ContinueStatement, ImportStatement, Parser,
                    SwitchStatement, CaseStatement, TupleExpression, TryStatement, 
                    ThrowStatement, LambdaExpression, MultiAssignmentExpression)

class VanctionRuntimeError(Exception):
    def __init__(self, message: str, file: str = "", line: int = 0, column: int = 0):
        self.file = file
        self.line = line
        self.column = column
        super().__init__(message)
    
    def __str__(self):
        """Return formatted error message"""
        error_msg = ""
        if self.file and self.line > 0:
            error_msg = "TRACEBACK ERROR:"
            error_msg += f"\nError at --> \"{self.file}\"  | {self.line} line | {self.column} column |"
            # Try to display the error location code line
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if self.line <= len(lines):
                        line_content = lines[self.line - 1].rstrip()
                        error_msg += f"\n{self.line:4} | {line_content}"
                        # Add pointer to error location
                        if self.column > 0:
                            pointer = ' ' * (len(str(self.line)) + 10) + "^" * (self.column - 4)
                            error_msg += f"\n{pointer}\n"
                error_msg += f"Runtime Error: {super().__str__()}"
            except:
                error_msg = f"Runtime Error: {super().__str__()}"  # If cannot read file, only display basic information
        else:
            error_msg = f"Runtime Error: {super().__str__()}"
        return error_msg

class VanctionDivisionByZeroError(VanctionRuntimeError):
    """Division by zero error"""
    def __init__(self, file: str = "", line: int = 0, column: int = 0):
        super().__init__("Division by zero", file, line, column)

class VanctionIndexOutOfRangeError(VanctionRuntimeError):
    """Index out of range error"""
    def __init__(self, index: int, max_index: int, file: str = "", line: int = 0, column: int = 0):
        message = f"Index {index} out of range (valid range: 0-{max_index-1})"
        super().__init__(message, file, line, column)

class VanctionKeyNotFoundError(VanctionRuntimeError):
    """Dictionary key not found error"""
    def __init__(self, key: str, file: str = "", line: int = 0, column: int = 0):
        message = f"Key '{key}' not found in dictionary"
        super().__init__(message, file, line, column)

class VanctionTypeError(VanctionRuntimeError):
    """Type error"""
    def __init__(self, expected_type: str, actual_type: str, file: str = "", line: int = 0, column: int = 0):
        message = f"Expected {expected_type}, got {actual_type}"
        super().__init__(message, file, line, column)

class VanctionUndefinedError(VanctionRuntimeError):
    """Undefined variable or function error"""
    def __init__(self, name: str, type_name: str = "variable", file: str = "", line: int = 0, column: int = 0):
        message = f"Undefined {type_name}: {name}"
        super().__init__(message, file, line, column)

class VanctionFunctionCallError(VanctionRuntimeError):
    """Function call error"""
    def __init__(self, message: str, file: str = "", line: int = 0, column: int = 0):
        super().__init__(message, file, line, column)

class VanctionAnytionError(VanctionRuntimeError):
    """Anytion type error"""
    def __init__(self, file: str = "", line: int = 0, column: int = 0):
        super().__init__("Operation on anytion value", file, line, column)

class VanctionUnassignedError(VanctionRuntimeError):
    """Unassigned type error"""
    def __init__(self, file: str = "", line: int = 0, column: int = 0):
        super().__init__("Operation on unassigned value", file, line, column)

class VanctionImmutableError(VanctionRuntimeError):
    """Immutable variable error"""
    def __init__(self, name: str, file: str = "", line: int = 0, column: int = 0):
        super().__init__(f"Cannot modify immutable variable '{name}'", file, line, column)

class AnytionType:
    """Special type for anytion values (undefined but declared variables)"""
    def __repr__(self):
        return "<anytion>"

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}  # Regular variables
        self.constants: Dict[str, Any] = {}  # Immutable variables
        self.functions: Dict[str, FunctionDef] = {}
    
    def define(self, name: str, value: Any = None, is_constant: bool = False):
        # If no value provided and not a constant, default to AnytionType
        if value is None and not is_constant:
            value = AnytionType()
        
        if is_constant:
            self.constants[name] = value
        else:
            self.variables[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.constants:
            return self.constants[name]
        elif name in self.variables:
            return self.variables[name]
        elif name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise VanctionUndefinedError(name, "variable")
    
    def set(self, name: str, value: Any, file: str = "", line: int = 0, column: int = 0):
        # Check if it's a constant in current environment
        if name in self.constants:
            raise VanctionImmutableError(name, file, line, column)
        
        # Check if it's a constant in parent environment
        if self.parent:
            try:
                # Try to get from parent constants
                if name in self.parent.constants:
                    raise VanctionImmutableError(name, file, line, column)
            except AttributeError:
                pass
        
        # Set regular variable
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value, file, line, column)
        else:
            raise VanctionUndefinedError(name, "variable")
    
    def define_function(self, name: str, func: FunctionDef):
        self.functions[name] = func
    
    def get_function(self, name: str) -> FunctionDef:
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise VanctionUndefinedError(name, "function")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    """break statement exception"""
    pass

class ContinueException(Exception):
    """continue statement exception"""
    pass

class VanctionException(Exception):
    """Vanction exception base class"""
    def __init__(self, message: str, exception_type: str = "Exception"):
        self.exception_type = exception_type
        self.message = message
        self.file = ""
        self.line = 0
        self.column = 0
        super().__init__(message)
    
    def __str__(self):
        """Return formatted error message"""
        error_msg = f"Runtime Error: {self.message}"
        
        if self.file and self.line > 0:
            error_msg += f"\n  --> {self.file}:{self.line}:{self.column}"
            # Try to display the error location code line
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if self.line > 0 and self.line <= len(lines):
                        line_content = lines[self.line - 1].rstrip()
                        error_msg += f"\n{self.line:4} | {line_content}"
                        # Add pointer to error location
                        if self.column > 0:
                            # Calculate pointer position: line number length + " | " length + column position - 1
                            pointer_pos = len(str(self.line)) + 6 + self.column - 1
                            pointer = ' ' * pointer_pos + '^^^^^'
                            error_msg += f"\n{pointer}"
            except:
                pass  # If cannot read file, only display basic information
        return error_msg

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtin_functions()
        self.current_file = ""
    
    def setup_builtin_functions(self):
        # System.print function with end parameter support
        def system_print(*args, **kwargs):
            # Handle named parameters
            end = kwargs.get('end', '\n')
            
            # If no positional arguments but have message named parameter
            if not args and 'message' in kwargs:
                output = str(kwargs['message'])
            elif args:
                # Use positional arguments
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
        
        # Range function implementation
        def range_func(n):
            """Generate a list of integers from 1 to n"""
            if not isinstance(n, int):
                raise VanctionTypeError("integer", type(n).__name__)
            if n < 0:
                raise VanctionRuntimeError(f"range: argument must be non-negative, got {n}")
            return list(range(1, n + 1))
        
        self.global_env.define("System.print", system_print)
        self.global_env.define("System.input", system_input)
        self.global_env.define("range", range_func)
        
        # Other built-in functions
        self.global_env.define("len", len)
        self.global_env.define("str", str)
        self.global_env.define("int", int)
        self.global_env.define("float", float)
        
        # Array operation functions
        def array_append(arr, item):
            """Append element to array end"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            arr.append(item)
            return arr
        
        def array_remove(arr, item):
            """Remove element from array"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            if item in arr:
                arr.remove(item)
            return arr
        
        def array_pop(arr, index=-1):
            """Remove and return element at specified index"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            if len(arr) == 0:
                raise VanctionRuntimeError("Cannot pop from empty array")
            return arr.pop(index)
        
        def array_index(arr, item):
            """Find element index in array"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            try:
                return arr.index(item)
            except ValueError:
                return -1
        
        def array_insert(arr, index, item):
            """Insert element at specified index"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            arr.insert(index, item)
            return arr
        
        def array_clear(arr):
            """Clear all elements from array"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            arr.clear()
            return arr
        
        def array_reverse(arr):
            """Reverse array order"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            arr.reverse()
            return arr
        
        def array_sort(arr):
            """Sort array elements"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            try:
                arr.sort()
                return arr
            except TypeError:
                raise VanctionRuntimeError("Cannot sort array with mixed types")
        
        def array_join(arr, separator=""):
            """Join array elements into string"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            try:
                return separator.join(str(item) for item in arr)
            except TypeError:
                raise VanctionRuntimeError("All elements must be convertible to string")
        
        def array_slice(arr, start=0, end=None):
            """Return array slice"""
            if not isinstance(arr, list):
                raise VanctionTypeError("array", type(arr).__name__)
            if not isinstance(start, int):
                raise VanctionTypeError("integer", type(start).__name__)
            if end is not None and not isinstance(end, int):
                raise VanctionTypeError("integer", type(end).__name__)
            return arr[start:end]
        
        # Register array operation functions
        self.global_env.define("array.append", array_append)
        self.global_env.define("array.insert", array_insert)
        self.global_env.define("array.remove", array_remove)
        self.global_env.define("array.pop", array_pop)
        self.global_env.define("array.reverse", array_reverse)
        self.global_env.define("array.sort", array_sort)
        self.global_env.define("array.join", array_join)
        self.global_env.define("array.slice", array_slice)
        
        # Dictionary operation functions
        def dict_keys(d):
            """Get all keys from dictionary"""
            if not isinstance(d, dict):
                raise VanctionTypeError("dictionary", type(d).__name__)
            return list(d.keys())
        
        def dict_values(d):
            """Get all values from dictionary"""
            if not isinstance(d, dict):
                raise VanctionTypeError("dictionary", type(d).__name__)
            return list(d.values())
        
        def dict_items(d):
            """Get all key-value pairs from dictionary"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_items: argument must be a dictionary", self.current_file)
            return list(d.items())
        
        def dict_has_key(d, key):
            """Check if dictionary contains key"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_has_key: first argument must be a dictionary", self.current_file)
            return key in d
        
        def dict_get(d, key, default=None):
            """Get value from dictionary, return default if key not found"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_get: first argument must be a dictionary", self.current_file)
            return d.get(key, default)
        
        def dict_set(d, key, value):
            """Set key-value pair in dictionary"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_set: first argument must be a dictionary", self.current_file)
            d[key] = value
            return d
        
        def dict_update(d, other):
            """Update dictionary, merge another dictionary"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_update: first argument must be a dictionary", self.current_file)
            if not isinstance(other, dict):
                raise VanctionRuntimeError("dict_update: second argument must be a dictionary", self.current_file)
            d.update(other)
            return d
        
        def dict_pop(d, key, default=None):
            """Remove and return value for specified key"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_pop: first argument must be a dictionary", self.current_file)
            try:
                return d.pop(key)
            except KeyError:
                if default is not None:
                    return default
                raise VanctionRuntimeError(f"dict_pop: key '{key}' not found", self.current_file)
        
        def dict_clear(d):
            """Clear all elements from dictionary"""
            if not isinstance(d, dict):
                raise VanctionRuntimeError("dict_clear: argument must be a dictionary", self.current_file)
            d.clear()
            return d
        
        # Register dictionary operation functions
        self.global_env.define("dict.keys", dict_keys)
        self.global_env.define("dict.values", dict_values)
        self.global_env.define("dict.items", dict_items)
        self.global_env.define("dict.get", dict_get)
        self.global_env.define("dict.set", dict_set)
        self.global_env.define("dict.update", dict_update)
        self.global_env.define("dict.pop", dict_pop)
        self.global_env.define("dict.clear", dict_clear)
        
        # File operation functions
        def file_read(filename, mode="r"):
            """Read file content"""
            if not isinstance(filename, str):
                raise VanctionRuntimeError("file_read: filename must be a string", self.current_file)
            if not isinstance(mode, str):
                raise VanctionRuntimeError("file_read: mode must be a string", self.current_file)
            
            try:
                with open(filename, mode, encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise VanctionRuntimeError(f"file_read: file '{filename}' not found", self.current_file)
            except Exception as e:
                raise VanctionRuntimeError(f"file_read: error reading file '{filename}': {str(e)}", self.current_file)
        
        def file_write(filename, content, mode="w"):
            """Write content to file"""
            if not isinstance(filename, str):
                raise VanctionRuntimeError("file_write: filename must be a string", self.current_file)
            if not isinstance(content, str):
                content = str(content)
            if not isinstance(mode, str):
                raise VanctionRuntimeError("file_write: mode must be a string", self.current_file)
            
            try:
                with open(filename, mode, encoding='utf-8') as f:
                    f.write(content)
                return len(content)
            except Exception as e:
                raise VanctionRuntimeError(f"file_write: error writing file '{filename}': {str(e)}", self.current_file)
        
        def file_exists(filename):
            """Check if file exists"""
            if not isinstance(filename, str):
                raise VanctionRuntimeError("file_exists: filename must be a string", self.current_file)
            return os.path.exists(filename)
        
        def file_delete(filename):
            """Delete file"""
            if not isinstance(filename, str):
                raise VanctionRuntimeError("file_delete: filename must be a string", self.current_file)
            
            try:
                os.remove(filename)
                return True
            except FileNotFoundError:
                raise VanctionRuntimeError(f"file_delete: file '{filename}' not found", self.current_file)
            except Exception as e:
                raise VanctionRuntimeError(f"file_delete: error deleting file '{filename}': {str(e)}", self.current_file)
        
        self.global_env.define("File.read", file_read)
        self.global_env.define("File.write", file_write)
        self.global_env.define("File.exists", file_exists)
        self.global_env.define("File.delete", file_delete)
        
        # Boolean constants
        self.global_env.define("true", True)
        self.global_env.define("false", False)
        
        # Unassigned type
        self.global_env.define("unassigned", None)
        
        # Anytion type - similar to unassigned but distinguishable
        # Use the global AnytionType class
        anytion_instance = AnytionType()
        self.global_env.define("anytion", anytion_instance)
        
        # String operation functions
        def str_contains(s, substring):
            """Check if string contains substring"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.contains: first argument must be a string", self.current_file)
            if not isinstance(substring, str):
                substring = str(substring)
            return substring in s
        
        def str_replace(s, old, new, count=-1):
            """Replace occurrences of substring"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.replace: first argument must be a string", self.current_file)
            if not isinstance(old, str):
                old = str(old)
            if not isinstance(new, str):
                new = str(new)
            if not isinstance(count, int):
                raise VanctionRuntimeError("str.replace: count must be an integer", self.current_file)
            return s.replace(old, new, count if count >= 0 else -1)
        
        def str_split(s, separator=" ", maxsplit=-1):
            """Split string into list"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.split: first argument must be a string", self.current_file)
            if not isinstance(separator, str):
                separator = str(separator)
            if not isinstance(maxsplit, int):
                raise VanctionRuntimeError("str.split: maxsplit must be an integer", self.current_file)
            return s.split(separator, maxsplit if maxsplit >= 0 else -1)
        
        def str_strip(s, chars=None):
            """Remove leading and trailing whitespace or specified characters"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.strip: argument must be a string", self.current_file)
            if chars is not None and not isinstance(chars, str):
                raise VanctionRuntimeError("str.strip: chars must be a string", self.current_file)
            return s.strip(chars)
        
        def str_lower(s):
            """Convert string to lowercase"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.lower: argument must be a string", self.current_file)
            return s.lower()
        
        def str_upper(s):
            """Convert string to uppercase"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.upper: argument must be a string", self.current_file)
            return s.upper()
        
        def str_startswith(s, prefix):
            """Check if string starts with prefix"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.startswith: first argument must be a string", self.current_file)
            if not isinstance(prefix, str):
                prefix = str(prefix)
            return s.startswith(prefix)
        
        def str_endswith(s, suffix):
            """Check if string ends with suffix"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.endswith: first argument must be a string", self.current_file)
            if not isinstance(suffix, str):
                suffix = str(suffix)
            return s.endswith(suffix)
        
        def str_substring(s, start, end=None):
            """Return substring from start to end"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.substring: first argument must be a string", self.current_file)
            if not isinstance(start, int):
                raise VanctionRuntimeError("str.substring: start must be an integer", self.current_file)
            if end is not None and not isinstance(end, int):
                raise VanctionRuntimeError("str.substring: end must be an integer", self.current_file)
            return s[start:end]
        
        def str_find(s, substring, start=0, end=None):
            """Find substring in string"""
            if not isinstance(s, str):
                raise VanctionRuntimeError("str.find: first argument must be a string", self.current_file)
            if not isinstance(substring, str):
                substring = str(substring)
            if not isinstance(start, int):
                raise VanctionRuntimeError("str.find: start must be an integer", self.current_file)
            if end is not None and not isinstance(end, int):
                raise VanctionRuntimeError("str.find: end must be an integer", self.current_file)
            return s.find(substring, start, end)
        
        # Register string operation functions
        self.global_env.define("str.contains", str_contains)
        self.global_env.define("str.replace", str_replace)
        self.global_env.define("str.split", str_split)
        self.global_env.define("str.strip", str_strip)
        self.global_env.define("str.lower", str_lower)
        self.global_env.define("str.upper", str_upper)
        self.global_env.define("str.startswith", str_startswith)
        self.global_env.define("str.endswith", str_endswith)
        self.global_env.define("str.substring", str_substring)
        self.global_env.define("str.find", str_find)
    
    def interpret(self, program: Program, filename: str = ""):
        self.current_file = filename
        
        # First register all functions
        for func in program.functions:
            self.global_env.define_function(func.name, func)
        
        # Execute top-level statements to define global variables
        for stmt in getattr(program, 'top_level_statements', []):
            try:
                self.execute_statement(stmt, self.global_env)
            except VanctionRuntimeError as e:
                if not e.file:
                    e.file = filename
                self.print_runtime_error(e)
                return False
            except VanctionException:
                # Re-raise VanctionException (user-defined exceptions)
                raise
            except Exception as e:
                error = VanctionRuntimeError(f"Runtime error: {str(e)}", filename)
                self.print_runtime_error(error)
                return False
        
        # Force check if main function exists
        if "main" not in self.global_env.functions:
            error = VanctionRuntimeError(f"Error: Main function not found in '{filename}'. Every Vanction program must have a 'func main()' function.", filename)
            self.print_runtime_error(error)
            return False
        
        # Execute main function
        main_func = self.global_env.get_function("main")
        try:
            self.execute_function(main_func, [])
        except VanctionRuntimeError as e:
            if not e.file:
                e.file = filename
            self.print_runtime_error(e)
            return False
        except VanctionException:
            # Re-raise VanctionException (user-defined exceptions), let try-catch handle it
            raise
        except Exception as e:
            error = VanctionRuntimeError(f"Runtime error: {str(e)}", filename)
            self.print_runtime_error(error)
            return False
        
        return True
    
    def interpret_repl(self, program: Program, filename: str = ""):
        """REPL mode: directly execute top-level statements, no main function required"""
        self.current_file = filename
        
        # In REPL mode, directly execute statements in current program
        # Don't cache function definitions, execute content in current AST each time
        try:
            # Traverse all functions in current program, find main function or parameterless function
            for func in program.functions:
                if func.name == "main" or len(func.parameters) == 0:
                    # Directly execute statements in function body, using global environment
                    for statement in func.body:
                        self.execute_statement(statement, self.global_env)
                    break
                
        except VanctionRuntimeError as e:
            if not e.file:
                e.file = filename
            self.print_runtime_error(e)
            return False
        except Exception as e:
            error = VanctionRuntimeError(f"Runtime error: {str(e)}", filename)
            self.print_runtime_error(error)
            return False
        
        return True
    
    def print_runtime_error(self, error: VanctionRuntimeError):
        """Print runtime error with file, line, and column information"""
        # Directly print error object, as it already contains complete formatted information
        print(error)
    
    def execute_function(self, func: FunctionDef, arguments: List[Any], current_env: Environment = None) -> Any:
        """Execute function definition"""
        # Create new local environment
        # Use current_env as parent for nested functions
        parent_env = current_env if current_env else self.global_env
        function_env = Environment(parent=parent_env)
        
        # Bind parameters
        if len(arguments) != len(func.parameters):
            raise VanctionFunctionCallError(f"Function '{func.name}' expects {len(func.parameters)} arguments, got {len(arguments)}")
        
        for param, arg in zip(func.parameters, arguments):
            function_env.define(param, arg)
        
        # Execute function body
        try:
            for stmt in func.body:
                self.execute_statement(stmt, function_env)
            return None  # Default return value
        except ReturnException as e:
            return e.value
    
    def execute_statement(self, statement: Statement, env: Environment):
        """Execute statement"""
        # Handle function definitions first
        if isinstance(statement, FunctionDef):
            env.define_function(statement.name, statement)
            return
        elif isinstance(statement, ExpressionStatement):
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
        
        elif isinstance(statement, SwitchStatement):
            self.execute_switch_statement(statement, env)
        
        elif isinstance(statement, BreakStatement):
            raise BreakException()
        
        elif isinstance(statement, ContinueStatement):
            raise ContinueException()
        
        elif isinstance(statement, ImportStatement):
            self.execute_import_statement(statement, env)
        
        elif isinstance(statement, TryStatement):
            self.execute_try_statement(statement, env)
        
        elif isinstance(statement, ThrowStatement):
            self.execute_throw_statement(statement, env)
        
        else:
            raise VanctionRuntimeError(f"Unknown statement type: {type(statement)}", self.current_file)
    
    def execute_for_statement(self, statement: ForStatement, env: Environment):
        """Execute for loop statement"""
        if statement.variable and statement.iterable:
            # for (item in collection) syntax
            iterable = self.evaluate_expression(statement.iterable, env)
            
            # Ensure iterable is iterable
            if isinstance(iterable, list):
                for item in iterable:
                    # Create new local environment to avoid polluting external scope
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
            # Traditional for (init; condition; update) syntax
            # Execute initialization
            if statement.init:
                self.evaluate_expression(statement.init, env)
            
            # Loop execution
            while True:
                # Check condition
                if statement.condition:
                    condition_value = self.evaluate_expression(statement.condition, env)
                    if not self.is_truthy(condition_value):
                        break
                
                try:
                    # Execute loop body
                    for stmt in statement.body:
                        self.execute_statement(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    pass  # continue directly enters next iteration
                
                # Execute update
                if statement.update:
                    self.evaluate_expression(statement.update, env)
    
    def execute_try_statement(self, statement: TryStatement, env: Environment):
        """Execute try-catch-finally statement"""
        try:
            # Execute try block
            for stmt in statement.try_body:
                self.execute_statement(stmt, env)
        except VanctionException as e:
            # Catch Vanction exceptions (user-defined exceptions)
            if statement.catch_body:
                # Check exception type filtering (if exception type is specified)
                if statement.exception_type:
                    if e.exception_type != statement.exception_type:
                        # Type mismatch, re-throw exception
                        raise
                
                # Create new environment to handle exception variable
                catch_env = Environment(parent=env)
                
                # If there is exception variable, store exception information to variable
                if statement.exception_var:
                    catch_env.define(statement.exception_var, {
                        'type': e.exception_type,
                        'message': e.message
                    })
                
                # Execute catch block
                for stmt in statement.catch_body:
                    self.execute_statement(stmt, catch_env)
        except VanctionRuntimeError as e:
            # Catch Vanction runtime errors (like division by zero, array out of bounds, etc.)
            if statement.catch_body:
                # Check exception type filtering
                if statement.exception_type:
                    # Get exception class name as type
                    actual_type = type(e).__name__
                    if actual_type != statement.exception_type:
                        # Type mismatch, re-throw exception
                        raise
                
                # Create new environment to handle exception variable
                catch_env = Environment(parent=env)
                
                if statement.exception_var:
                    catch_env.define(statement.exception_var, {
                        'type': type(e).__name__,
                        'message': str(e)
                    })
                
                # Execute catch block
                for stmt in statement.catch_body:
                    self.execute_statement(stmt, catch_env)
        except Exception as e:
            # Catch other unexpected exceptions
            if statement.catch_body:
                # Check exception type filtering
                if statement.exception_type:
                    # Only catch when no specific type is specified
                    if statement.exception_type != "RuntimeError":
                        raise
                
                # Create new environment to handle exception variable
                catch_env = Environment(parent=env)
                
                if statement.exception_var:
                    catch_env.define(statement.exception_var, {
                        'type': 'RuntimeError',
                        'message': str(e)
                    })
                
                # Execute catch block
                for stmt in statement.catch_body:
                    self.execute_statement(stmt, catch_env)
        finally:
            # Execute finally block (executes regardless of whether exception occurred)
            if statement.finally_body:
                for stmt in statement.finally_body:
                    self.execute_statement(stmt, env)
    
    def execute_throw_statement(self, statement: ThrowStatement, env: Environment):
        """Execute throw statement"""
        if statement.expression:
            message = self.evaluate_expression(statement.expression, env)
            # Create exception with location information
            exc = VanctionException(str(message), "UserException")
            exc.line = statement.line
            exc.column = statement.column
            exc.file = self.current_file
            raise exc
        else:
            # Create exception with location information
            exc = VanctionException("Exception thrown", "UserException")
            exc.line = statement.line
            exc.column = statement.column
            exc.file = self.current_file
            raise exc
    
    def execute_import_statement(self, statement: ImportStatement, env: Environment):
        """Execute import statement, load and execute module file"""
        module_name = statement.module_name
        alias = statement.alias
        using = statement.using
        
        # Handle module import from folders (e.g., import clo.sd imports sd.va from clo folder)
        # Replace dots in module_name with path separators
        module_path_parts = module_name.split('.')
        if len(module_path_parts) > 1:
            # Last part as filename, previous parts as folder path
            folder_path = os.path.join(*module_path_parts[:-1])
            filename = f"{module_path_parts[-1]}.va"
            module_filename = os.path.join(folder_path, filename)
        else:
            # Regular module import
            module_filename = f"{module_name}.va"
        
        # If current file exists, look relative to current file directory
        if self.current_file and os.path.exists(self.current_file):
            current_dir = os.path.dirname(self.current_file)
            module_path = os.path.join(current_dir, module_filename)
        else:
            # Otherwise look in current working directory
            module_path = module_filename
        
        # Check if module file exists
        if not os.path.exists(module_path):
            raise VanctionRuntimeError(f"Module '{module_name}' not found: {module_path}", self.current_file)
        
        try:
            # Read module file content
            with open(module_path, 'r', encoding='utf-8') as f:
                module_code = f.read()
            
            # Lexical analysis
            lexer = Lexer(module_code)
            tokens = lexer.tokenize()
            
            # Syntax analysis
            parser = Parser(tokens, module_path)
            module_ast = parser.parse()
            
            # Create new interpreter instance to execute module (avoid polluting current environment)
            module_interpreter = Interpreter()
            
            # Execute module and collect its variables and functions
            module_interpreter.interpret(module_ast, module_path)
            
            # Handle import method
            if using and alias:
                # import xxx using yyy syntax - Import all module content directly into alias namespace
                # Create an object containing all module functions and variables
                module_obj = {}
                
                # Add module functions
                for func in module_ast.functions:
                    # Use original function name (without module prefix)
                    func_name = func.name
                    
                    # Save function reference, not copy function definition
                    # This allows correct access to module context when executing the function
                    module_obj[func_name] = func
                
                # Add module variables
                for var_name, var_value in module_interpreter.global_env.variables.items():
                    module_obj[var_name] = var_value
                
                # Define a global variable pointing to the module object
                self.global_env.define(alias, module_obj)
                
                # Also register module functions and variables with alias prefix to global environment, allowing access via both methods
                for func_name, func in module_obj.items():
                    if isinstance(func, FunctionDef):
                        self.global_env.define_function(f"{alias}.{func_name}", func)
                
                for var_name, var_value in module_interpreter.global_env.variables.items():
                    self.global_env.define(f"{alias}.{var_name}", var_value)
            else:
                # Standard import - Use module name as prefix
                # Register module functions to current global environment, using module name as prefix to avoid naming conflicts
                for func in module_ast.functions:
                    # Register module functions to current global environment, use module name as prefix to avoid naming conflicts
                    func_name = f"{module_name}.{func.name}"
                    
                    # Modify function name to module-prefixed version
                    module_func = FunctionDef(
                        name=func_name,
                        parameters=func.parameters,
                        body=func.body,
                        line=func.line,
                        column=func.column
                    )
                    
                    self.global_env.define_function(func_name, module_func)
                
                # Also register module variables to current global environment
                for var_name, var_value in module_interpreter.global_env.variables.items():
                    prefixed_name = f"{module_name}.{var_name}"
                    self.global_env.define(prefixed_name, var_value)
            
        except Exception as e:
            raise VanctionRuntimeError(f"Error importing module '{module_name}': {str(e)}", self.current_file)
    
    def execute_switch_statement(self, statement: SwitchStatement, env: Environment):
        """Execute switch statement"""
        switch_value = self.evaluate_expression(statement.expression, env)
        matched = False
        
        # Iterate through all cases
        for case in statement.cases:
            case_value = self.evaluate_expression(case.value, env)
            
            # Compare switch value and case value
            if switch_value == case_value:
                matched = True
                # Execute case body, catch break exception
                try:
                    for stmt in case.body:
                        self.execute_statement(stmt, env)
                except BreakException:
                    # Encounter break statement, exit switch
                    pass
                break
        
        # If no matching case, execute default
        if not matched and statement.default_case:
            try:
                for stmt in statement.default_case:
                    self.execute_statement(stmt, env)
            except BreakException:
                # Encounter break statement, exit switch
                pass
    
    def evaluate_expression(self, expr: Expression, env: Environment) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        
        elif isinstance(expr, Identifier):
            value = env.get(expr.name)
            # Check if value is of type AnytionType
            if isinstance(value, AnytionType):
                raise VanctionAnytionError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
            return value
        
        elif isinstance(expr, BinaryExpression):
            if expr.operator == '=':
                # Assignment
                if isinstance(expr.left, Identifier):
                    var_name = expr.left.name
                    value = self.evaluate_expression(expr.right, env)
                    # If variable exists, use set to update; otherwise use define to create
                    try:
                        env.set(var_name, value, self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
                    except VanctionImmutableError:
                        # Re-raise immutable error
                        raise
                    except VanctionRuntimeError:
                        # Variable doesn't exist, create new variable
                        # Check if this is a constant assignment
                        is_constant = getattr(expr, 'is_constant', False)
                        env.define(var_name, value, is_constant)
                    return value
                else:
                    raise VanctionRuntimeError(f"Invalid assignment target: {type(expr.left)}", self.current_file)
            
            left = self.evaluate_expression(expr.left, env)
            right = self.evaluate_expression(expr.right, env)
            
            # Check for anytion values
            if isinstance(left, AnytionType) or isinstance(right, AnytionType):
                raise VanctionAnytionError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
            
            # Check for unassigned values (None)
            if left is None or right is None:
                raise VanctionUnassignedError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
            
            if expr.operator == '+':
                return left + right
            elif expr.operator == '-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                if right == 0:
                    raise VanctionDivisionByZeroError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
                return left / right
            elif expr.operator == '%':
                if right == 0:
                    raise VanctionDivisionByZeroError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
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
        
        elif isinstance(expr, MultiAssignmentExpression):
            # Evaluate the right-hand side expression
            value = self.evaluate_expression(expr.value, env)
            
            # Check if value is of type AnytionType
            if isinstance(value, AnytionType):
                raise VanctionAnytionError(self.current_file, getattr(expr, 'line', 0), getattr(expr, 'column', 0))
            
            # Convert single value to list for consistent handling
            if not isinstance(value, (list, tuple)):
                value_list = [value] * len(expr.variables)
            else:
                value_list = list(value)
            
            # Check if number of variables matches number of values
            if len(expr.variables) != len(value_list):
                raise VanctionRuntimeError(f"Number of variables ({len(expr.variables)}) does not match number of values ({len(value_list)})")
            
            # Assign values to variables
            for var, val in zip(expr.variables, value_list):
                var_name = var.name
                # If variable exists, use set to update; otherwise use define to create
                try:
                    env.set(var_name, val, self.current_file, getattr(var, 'line', 0), getattr(var, 'column', 0))
                except VanctionImmutableError:
                    # Re-raise immutable error
                    raise
                except VanctionRuntimeError:
                    # Variable doesn't exist, create new variable
                    env.define(var_name, val)
            
            return value
            
        elif isinstance(expr, MemberExpression):
            # Handle member access like test_module.hello or module.var
            obj_name = expr.object
            member_name = expr.property
            full_name = f"{obj_name}.{member_name}"
            
            print(f"Debug: 处理 MemberExpression: {full_name}")
            
            # First, try to get the full name directly from global environment (for standard imports)
            try:
                return self.global_env.get(full_name)
            except VanctionRuntimeError as e:
                # Only proceed to object access if the error is about undefined variable
                # If the full name was found but not accessible as a property, we should not proceed
                if "property" not in str(e):
                    try:
                        # If not found, check if it's an object access (for alias imports or dictionary objects)
                        obj = self.global_env.get(obj_name)
                        if isinstance(obj, dict) and member_name in obj:
                            return obj[member_name]
                        else:
                            # Try one more time to get the full name directly, in case of a function
                            try:
                                return self.global_env.get(full_name)
                            except:
                                raise VanctionUndefinedError(full_name, "property")
                    except VanctionRuntimeError:
                        # If object not found at all, re-raise the original error
                        raise e
                else:
                    raise e
        
        elif isinstance(expr, CallExpression):
            return self.evaluate_call_expression(expr, env)
        
        elif isinstance(expr, ArrayExpression):
            return [self.evaluate_expression(elem, env) for elem in expr.elements]
        
        elif isinstance(expr, DictExpression):
            result = {}
            for key_expr, value_expr in expr.entries:
                key_val = self.evaluate_expression(key_expr, env)
                value_val = self.evaluate_expression(value_expr, env)
                # Ensure key is hashable type
                if not isinstance(key_val, (int, float, str, bool, type(None))):
                    raise VanctionRuntimeError(f"Dictionary key must be a hashable type, got {type(key_val).__name__}", self.current_file)
                result[key_val] = value_val
            return result
        
        elif isinstance(expr, IndexExpression):
            obj = self.evaluate_expression(expr.object, env)
            index = self.evaluate_expression(expr.index, env)
            
            if isinstance(obj, str):
                # String index access
                if isinstance(index, int):
                    if 0 <= index < len(obj):
                        return obj[index]
                    else:
                        raise VanctionIndexOutOfRangeError(index, len(obj))
                else:
                    raise VanctionTypeError("integer", type(index).__name__)
            
            elif isinstance(obj, list):
                # List index access
                if isinstance(index, int):
                    if 0 <= index < len(obj):
                        return obj[index]
                    else:
                        raise VanctionIndexOutOfRangeError(index, len(obj))
                else:
                    raise VanctionTypeError("integer", type(index).__name__)
            
            elif isinstance(obj, dict):
                # Dictionary index access
                if index in obj:
                    return obj[index]
                else:
                    raise VanctionKeyNotFoundError(str(index))
            
            elif isinstance(obj, tuple):
                # Tuple index access
                if isinstance(index, int):
                    if 0 <= index < len(obj):
                        return obj[index]
                    else:
                        raise VanctionIndexOutOfRangeError(index, len(obj))
                else:
                    raise VanctionTypeError("integer", type(index).__name__)
            
            else:
                raise VanctionRuntimeError(f"Cannot index object of type {type(obj).__name__}", self.current_file)
        
        elif isinstance(expr, TupleExpression):
            return tuple(self.evaluate_expression(elem, env) for elem in expr.elements)
        
        elif isinstance(expr, LambdaExpression):
            # Create anonymous function
            def lambda_func(*args):
                # Create new local environment
                lambda_env = Environment(parent=env)
                
                # Bind parameters
                if len(args) != len(expr.parameters):
                    raise VanctionFunctionCallError(f"Lambda function expects {len(expr.parameters)} arguments, got {len(args)}")
                
                for param, arg in zip(expr.parameters, args):
                    lambda_env.define(param, arg)
                
                # Execute lambda body
                return self.evaluate_expression(expr.body, lambda_env)
            
            return lambda_func
        
        else:
            raise VanctionRuntimeError(f"Unknown expression type: {type(expr)}", self.current_file)
    
    def evaluate_call_expression(self, expression: CallExpression, env: Environment) -> Any:
        function_name = expression.function
        
        # Handle case where LambdaExpression is function
        if isinstance(function_name, LambdaExpression):
            # Get lambda function
            lambda_func = self.evaluate_expression(function_name, env)
            if not callable(lambda_func):
                raise VanctionRuntimeError(f"Lambda expression is not callable", self.current_file)
            
            # Calculate argument values with anytion check
            arguments = []
            for arg in expression.arguments:
                arg_value = self.evaluate_expression(arg, env)
                # Check if argument is AnytionType
                if isinstance(arg_value, AnytionType):
                    raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                arguments.append(arg_value)
            
            # Call lambda function
            return lambda_func(*arguments)
        
        # Handle built-in functions and user-defined functions
        if '.' in function_name:
            # First try to handle object property access (for alias imports like tm.hello)
            try:
                obj_name, prop_name = function_name.split('.', 1)
                obj = self.global_env.get(obj_name) or env.get(obj_name)
                if obj and isinstance(obj, dict) and prop_name in obj:
                    func = obj[prop_name]
                    if isinstance(func, FunctionDef):
                        # Handle user-defined function
                        arguments = []
                        for arg in expression.arguments:
                            arg_value = self.evaluate_expression(arg, env)
                            # Check if argument is AnytionType
                            if isinstance(arg_value, AnytionType):
                                raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                            arguments.append(arg_value)
                        return self.execute_function(func, arguments, env)
                    elif callable(func):
                        # Handle callable object
                        arguments = []
                        for arg in expression.arguments:
                            arg_value = self.evaluate_expression(arg, env)
                            # Check if argument is AnytionType
                            if isinstance(arg_value, AnytionType):
                                raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                            arguments.append(arg_value)
                        keyword_arguments = {}
                        for name, arg in expression.keyword_arguments.items():
                            kw_value = self.evaluate_expression(arg, env)
                            # Check if keyword argument is AnytionType
                            if isinstance(kw_value, AnytionType):
                                raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                            keyword_arguments[name] = kw_value
                        return func(*arguments, **keyword_arguments)
            except VanctionRuntimeError:
                pass
            
            # If not object property access, try as complete function name (like test_module.hello)
            # First check if it's a user-defined function (like math.add)
            if function_name in self.global_env.functions:
                func = self.global_env.get_function(function_name)
                arguments = []
                for arg in expression.arguments:
                    arg_value = self.evaluate_expression(arg, env)
                    # Check if argument is AnytionType
                    if isinstance(arg_value, AnytionType):
                        raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                    arguments.append(arg_value)
                return self.execute_function(func, arguments, env)
            else:
                # Try to get from global environment first, then current environment
                builtin_func = None
                try:
                    # Try to get from global environment first (for built-in functions like System.print)
                    builtin_func = self.global_env.get(function_name)
                except VanctionRuntimeError:
                    # If not in global environment, try to get from current environment
                    try:
                        builtin_func = env.get(function_name)
                    except VanctionRuntimeError:
                        pass
                
                if builtin_func and callable(builtin_func):
                    # Handle positional and keyword arguments
                    arguments = []
                    for arg in expression.arguments:
                        arg_value = self.evaluate_expression(arg, env)
                        # Check if argument is AnytionType
                        if isinstance(arg_value, AnytionType):
                            raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                        arguments.append(arg_value)
                    keyword_arguments = {}
                    for name, arg in expression.keyword_arguments.items():
                        kw_value = self.evaluate_expression(arg, env)
                        # Check if keyword argument is AnytionType
                        if isinstance(kw_value, AnytionType):
                            raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                        keyword_arguments[name] = kw_value
                    return builtin_func(*arguments, **keyword_arguments)
                else:
                    raise VanctionUndefinedError(function_name, "function")
        else:
            # Regular function call - first check user-defined functions, then built-in functions
            if function_name in self.global_env.functions:
                func = self.global_env.get_function(function_name)
                arguments = []
                for arg in expression.arguments:
                    arg_value = self.evaluate_expression(arg, env)
                    # Check if argument is AnytionType
                    if isinstance(arg_value, AnytionType):
                        raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                    arguments.append(arg_value)
                return self.execute_function(func, arguments, env)
            else:
                # Check if it's a built-in function (stored as variables)
                builtin_func = None
                try:
                    # Try to get from global environment first (for built-in functions like System.print)
                    builtin_func = self.global_env.get(function_name)
                except VanctionRuntimeError:
                    # If not in global environment, try to get from current environment
                    try:
                        builtin_func = env.get(function_name)
                    except VanctionRuntimeError:
                        pass
                
                if builtin_func and callable(builtin_func):
                    arguments = []
                    for arg in expression.arguments:
                        arg_value = self.evaluate_expression(arg, env)
                        # Check if argument is AnytionType
                        if isinstance(arg_value, AnytionType):
                            raise VanctionAnytionError(self.current_file, getattr(arg, 'line', 0), getattr(arg, 'column', 0))
                        arguments.append(arg_value)
                    return builtin_func(*arguments)
                else:
                    raise VanctionUndefinedError(function_name, "function")
    
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