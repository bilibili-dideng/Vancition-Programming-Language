# Vanction 编程语言

Vanction 是一个简单易学的编程语言，专为教育和快速原型设计而开发。

## 特性

- **简洁的语法**: 类似现代编程语言的语法，易于阅读和编写
- **函数支持**: 支持自定义函数定义和调用
- **变量系统**: 支持变量定义和赋值
- **控制流**: 支持 if-else 条件语句和 while 循环
- **内置函数**: 提供 System.print 等内置函数
- **交互式解释器**: 支持 REPL 模式进行交互式编程

## 快速开始

### 安装

Vanction 是基于 Python 的解释器，无需额外安装。只需确保系统安装了 Python 3.6+。

### 运行程序

```bash
| 运行 Vanction 源文件
python vanction.py examples/hello.va

| 启动交互式解释器
python vanction.py --repl
```

## 语法示例

### Hello World

```vanction
func main() {
    System.print("Hello World!")
}
```

### 变量和函数

```vanction
func greet(name) {
    System.print("Hello, " + name + "!")
}

func main() {
    message = "Vanction Language"
    version = 1.0
    
    System.print(message)
    System.print("Version:", version)
    
    greet("World")
}
```

### 控制流

```Vanction
func main() {
    | if-else 条件语句
    age = 18
    if age >= 18 {
        System.print("You are an adult")
    } else {
        System.print("You are a minor")
    }
    
    score = 85
    if (score >= 90) {
        System.print("Grade: A")
    } else-if (score >= 80) {
        System.print("Grade: B")
    } else-if (score >= 70) {
        System.print("Grade: C")
    } else {
        System.print("Grade: F")
    }
    
    | while 循环
    counter = 0
    while counter < 5 {
        System.print("Counter:", counter)
        counter = counter + 1
    }
}
```

### 函数返回值

```Vanction
func add(a, b) {
    return a + b
}

func main() {
    result = add(5, 3)
    System.print("5 + 3 =", result)
}
```

## 语言特性

### 数据类型

- **数字**: 整数和浮点数 (1, 3.14)
- **字符串**: 双引号包围的文本 ("Hello")
- **布尔值**: 通过比较运算得到 (true/false)

### 运算符

- **算术运算符**: +, -, *, /
- **比较运算符**: ==, !=, <, >, <=, >=
- **逻辑运算符**: and, or
- **赋值运算符**: =

### 内置函数

- `System.print(...)`: 打印输出，支持多个参数 "message","end"
- `len(string)`: 获取字符串长度
- `str(value)`: 转换为字符串
- `int(value)`: 转换为整数
- `float(value)`: 转换为浮点数
- ‘System.input(...)’

## 扩展功能

Vanction 语言设计为易于扩展，可以通过以下方式添加新功能：

1. **添加新的内置函数**: 在 `interpreter.py` 的 `setup_builtin_functions` 方法中添加
2. **添加新的语法**: 扩展 `lexer.py` 和 `parser.py` 来支持新的语法结构
3. **添加新的运算符**: 在 `parser.py` 和 `interpreter.py` 中实现新的运算符

## 贡献

欢迎提交 Issue 和 Pull Request 来改进 Vanction 语言！

## 许可证

MIT License - 详见 LICENSE 文件