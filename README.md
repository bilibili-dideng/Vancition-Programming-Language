# Vanction Programming Language

![Vanction Language](icon/Vanction.ico)

Vanction is a modern, versatile scripting language that seamlessly blends functional programming, object-oriented, and procedural paradigms. Designed with simplicity and power in mind, Vanction offers an intuitive syntax while maintaining the capability to handle complex programming tasks.

## 🌟 Key Features

- **Multi-Paradigm Support**: Functional, Object-Oriented, and Procedural programming
- **Intuitive Syntax**: Clean and readable code structure
- **Powerful String Processing**: Built-in formatted strings and raw string literals
- **Comprehensive Control Flow**: if-else-if-else, switch, for, while loops
- **Exception Handling**: Robust try-catch-finally mechanism
- **Immutable Variables**: Support for constants and immutable data
- **Lambda Expressions**: First-class functions and higher-order programming
- **Rich Built-in Functions**: Extensive standard library

## 🚀 Quick Start

### main
```vanction
func main() {
    System.print("Hello, World!");
}
```

### you can...
```bash
pyinstaller --onefile --icon=icon/Vanction.ico vanction.py 
```

### Your First Vanction Program
Create a file called `hello.va`:
```vanction
func main() {
    System.print("Hello, Vanction World!");
    
    | Calculate factorial
    func factorial(n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    result = factorial(5);
    System.print(f"5! = {result}");
}
```

Run it:
```bash
python vanction.py hello.va
```

## 📖 Language Highlights

### Variables and Constants
```vanction
| Regular variables
name = "Vanction";
version = 2.0;

| Immutable variables
immut pi = 3.14159;

| Compile-time constants
define MAX_SIZE 100;
```

### String Magic
```vanction
| Formatted strings
name = "Vanction";
greeting = f"Welcome to {name} version {version}!";

| Raw strings (no escape processing)
path = $"C:\\Users\\Developer\\Project";
```

### Control Flow
```vanction
| For loops
for (i in range(5)) {
    System.print(f"Count: {i}");
}

| Switch statements
switch day {
    case "Monday" {
        System.print("Start of work week");
    }
    case "Friday" {
        System.print("Almost weekend!");
    }
    default {
        System.print("Regular day");
    }
}
```

### Functions and Lambdas
```vanction
| Regular functions
func add(a, b) {
    return a + b;
}

| Lambda expressions
square = (x) -> x * x;
double = (x) -> x * 2;

| Higher-order functions
func apply_operation(numbers, operation) {
    result = [];
    for (n in numbers) {
        result.append(operation(n));
    }
    return result;
}
```

### Exception Handling
```vanction
try {
    result = 10 / 0;
} catch (error) {
    System.print(f"Error caught: {error}");
} finally {
    System.print("Cleanup complete");
}
```

## 📚 Documentation

- **[Complete Language Reference](doc/language_reference_en.md)** - Comprehensive guide to all Vanction features
- **[语言参考手册 (中文)](doc/language_reference_zh.md)** - 中文完整语言参考

## 🛠️ Project Structure

```
Vanction-Language/
├── vanction.py          # Main interpreter entry point
├── lexer.py            # Lexical analyzer
├── parser.py           # Syntax parser
├── interpreter.py      # Runtime interpreter
├── doc/                # Documentation
│   ├── language_reference_en.md
│   └── language_reference_zh.md
├── icon/               # Project icons
└── README.md           # This file

```
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Happy Coding with Vanction!** 🎉