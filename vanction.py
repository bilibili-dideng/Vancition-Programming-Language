#!/usr/bin/env python3
"""
Vanction Programming Language Interpreter

A simple programming language that supports function definitions, variables, control flow, and built-in functions.

Example code:
```vanction
func main() {
    System.print("Hello World!")
}
```
"""

import sys
import os
import argparse

# Increase integer string conversion limit to handle very large numbers
sys.set_int_max_str_digits(0)  # 0 means unlimited

from lexer import Lexer
from parser import Parser, ExpressionStatement
from interpreter import Interpreter, VanctionException, VanctionRuntimeError

def run_file(filename: str):
    """Run Vanction source file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Lexical analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Syntax analysis
        parser = Parser(tokens, filename)
        ast = parser.parse()
        
        # Interpret and execute
        interpreter = Interpreter()
        interpreter.interpret(ast, filename)  # Pass filename parameter
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except SyntaxError as e:
        print(f"{e}")
        sys.exit(1)
    except VanctionException as e:
        # VanctionException already contains complete formatted information, output directly
        print(str(e))
        sys.exit(1)
    except VanctionRuntimeError as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)

def run_repl():
    """Run interactive interpreter"""
    print("Vanction Programming Language REPL v1.0")
    print("Enter 'exit' or 'quit' to exit")
    print("-" * 30)
    
    # Create a persistent interpreter instance to maintain function and variable definitions
    interpreter = Interpreter()
    
    while True:
        try:
            # Check for input from pipe
            import sys
            if not sys.stdin.isatty():
                # If there's pipe input, read all content at once
                try:
                    full_code = sys.stdin.read().strip()
                    if not full_code:
                        break
                    
                    # Lexical analysis
                    lexer = Lexer(full_code)
                    tokens = lexer.tokenize()
                    
                    # Syntax analysis
                    parser = Parser(tokens, "<stdin>")
                    ast = parser.parse()
                    
                    # Use REPL mode to interpret and execute
                    interpreter.interpret_repl(ast)
                    break
                    
                except SyntaxError as e:
                    print(f"Syntax error: {e}")
                    break
                except Exception as e:
                    print(f"Runtime error: {e}")
                    break
            
            # Normal interactive input
            line = input("vanction> ").strip()
            
            if line.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not line:
                continue
            
            try:
                # Ensure statement ends with semicolon
                if not line.endswith(';'):
                    line = line + ';'
                
                # Lexical analysis
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                
                # Syntax analysis
                parser = Parser(tokens, "<repl>")
                ast = parser.parse()
                
                # Use custom approach for REPL to handle and display expression results
                if hasattr(ast, 'top_level_statements') and ast.top_level_statements:
                    # Process top-level statements specially for REPL
                    for stmt in ast.top_level_statements:
                        if isinstance(stmt, ExpressionStatement):
                            expr = stmt.expression
                            # Evaluate expression directly and print result
                            result = interpreter.evaluate_expression(expr, interpreter.global_env)
                            if result is not None:
                                print(result)
                        else:
                            # Execute other types of statements normally
                            interpreter.execute_statement(stmt, interpreter.global_env)
                else:
                    # Fallback to original interpret_repl method
                    interpreter.interpret_repl(ast)
                
            except SyntaxError as e:
                print(f"Syntax error: {e}")
            except Exception as e:
                print(f"Runtime error: {e}")
            
        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
        except EOFError:
            print("\nGoodbye!")
            break

def main():
    parser = argparse.ArgumentParser(description='Vanction Programming Language Interpreter')
    parser.add_argument('file', nargs='?', help='Vanction source file')
    parser.add_argument('--repl', action='store_true', help='Run interactive interpreter')
    
    args = parser.parse_args()
    
    if args.repl or not args.file:
        run_repl()
    else:
        # Check if args.file is absolute path
        if not os.path.isabs(args.file):
            # If relative path, convert to absolute path relative to current working directory
            file = os.path.abspath(args.file)
        else:
            # If absolute path, use directly
            file = args.file
        run_file(file)

if __name__ == "__main__":
    main()