#!/usr/bin/env python3
"""
Vanction 编程语言解释器

一个简单的编程语言，支持函数定义、变量、控制流和内置函数。

示例代码:
```vanction
func main() {
    System.print("Hello World!")
}
```
"""

import sys
import os
import argparse
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_file(filename: str):
    """Run Vanction source file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Lexical analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpret and execute
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)

def run_repl():
    """运行交互式解释器"""
    print("Vanction 编程语言 REPL v1.0")
    print("输入 'exit' 或 'quit' 退出")
    print("-" * 30)
    
    current_input = []
    brace_count = 0
    
    while True:
        try:
            # 确定提示符
            prompt = "vanction> " if brace_count == 0 else "...> "
            
            # 读取输入
            line = input(prompt).strip()
            
            if line.lower() in ['exit', 'quit']:
                print("再见!")
                break
            
            if not line and brace_count == 0:
                continue
            
            # 计算大括号数量
            brace_count += line.count('{') - line.count('}')
            current_input.append(line)
            
            # 如果还有未闭合的大括号，继续读取
            if brace_count > 0:
                continue
            
            # 合并所有输入
            full_code = '\n'.join(current_input)
            current_input = []
            
            # 为每次输入创建新的解释器实例
            interpreter = Interpreter()
            
            # 词法分析
            lexer = Lexer(full_code)
            tokens = lexer.tokenize()
            
            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            
            # 解释执行
            interpreter.interpret(ast)
            
        except KeyboardInterrupt:
            print("\n使用 'exit' 或 'quit' 退出")
            current_input = []
            brace_count = 0
        except EOFError:
            print("\n再见!")
            break
        except SyntaxError as e:
            print(f"语法错误: {e}")
            current_input = []
            brace_count = 0
        except Exception as e:
            print(f"运行时错误: {e}")
            current_input = []
            brace_count = 0

def main():
    parser = argparse.ArgumentParser(description='Vanction 编程语言解释器')
    parser.add_argument('file', nargs='?', help='Vanction源文件')
    parser.add_argument('--repl', action='store_true', help='运行交互式解释器')
    
    args = parser.parse_args()
    
    if args.repl or not args.file:
        run_repl()
    else:
        # 检测args.file是否为绝对路径
        if not os.path.isabs(args.file):
            # 如果是相对路径，转换为相对于当前工作目录的绝对路径
            file = os.path.abspath(args.file)
        else:
            # 如果是绝对路径，直接使用
            file = args.file
        run_file(file)

if __name__ == "__main__":
    main()