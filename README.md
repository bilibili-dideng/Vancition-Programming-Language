# Vanction Programming Language

Vanction is a simple and easy-to-learn programming language designed for education and rapid prototyping.

## Features

- **Clean Syntax**: Modern programming language-like syntax, easy to read and write
- **Function Support**: Support for custom function definitions and calls
- **Variable System**: Support for variable definition and assignment
- **Control Flow**: Support for if-else conditional statements and while loops
- **Built-in Functions**: Provides built-in functions like System.print
- **Interactive Interpreter**: Supports REPL mode for interactive programming

## Quick Start

### Installation

Vanction is a Python-based interpreter that requires no additional installation. Just ensure Python 3.6+ is installed on your system.

### Running Programs

```bash
# Run Vanction source file
python vanction.py examples/hello.va

# Start interactive interpreter
python vanction.py --repl
```

## Syntax Examples

### Hello World

```vanction
func main() {
    System.print("Hello World!")
}
```

### Variables and Functions

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

### Control Flow

```vanction
func main() {
    # if-else conditional statements
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
    
    # while loop
    counter = 0
    while counter < 5 {
        System.print("Counter:", counter)
        counter = counter + 1
    }
}
```

### Function Return Values

```vanction
func add(a, b) {
    return a + b
}

func main() {
    result = add(5, 3)
    System.print("5 + 3 =", result)
}
```

## Language Features

### Data Types

- **Numbers**: Integers and floating-point numbers (1, 3.14)
- **Strings**: Text enclosed in double quotes ("Hello")
- **Booleans**: Obtained through comparison operations (true/false)

### Operators

- **Arithmetic Operators**: +, -, *, /
- **Comparison Operators**: ==, !=, <, >, <=, >=
- **Logical Operators**: and, or
- **Assignment Operators**: =

### Built-in Functions

- `System.print(...)`: Print output, supports multiple parameters
- `len(string)`: Get string length
- `str(value)`: Convert to string
- `int(value)`: Convert to integer
- `float(value)`: Convert to float
- `System.input(...)`: Get user input

## Extension Features

Vanction language is designed to be easily extensible. New features can be added through:

1. **Adding New Built-in Functions**: Add in the `setup_builtin_functions` method in `interpreter.py`
2. **Adding New Syntax**: Extend `lexer.py` and `parser.py` to support new syntax structures
3. **Adding New Operators**: Implement new operators in `parser.py` and `interpreter.py`

## Contributing

Issues and Pull Requests are welcome to improve the Vanction language!

## License

MIT License - See LICENSE file for details