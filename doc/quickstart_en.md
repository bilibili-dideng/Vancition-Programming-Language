# Vanction Programming Language Quick Start Guide

## What is Vanction?

Vanction is a simple, easy-to-learn programming language designed for education and rapid prototyping. It features a clean syntax and supports basic programming concepts, making it ideal for beginners or developers who need to quickly implement ideas.

## Installation Requirements

Vanction is a Python-based interpreter, so you need to have Python 3.6 or higher installed on your system.

- Windows: Visit the [Python website](https://www.python.org/downloads/) to download and install
- macOS: Use Homebrew to install with `brew install python`
- Linux: Use your package manager, such as `sudo apt install python3`

## Getting Vanction

No release available yet.

## Basic Syntax

### 1. Hello World Program

Create a simple Vanction program:

```vanction
func main() {
    System.print("Hello World!");
}

main();
```

Save the above code as a file named `hello.va`.

### 2. Variables and Assignment

In Vanction, you can create variables directly without declaring types:

```vanction
name = "Vanction";
version = 1.0;
count = 5;
```

### 3. Function Definition and Calls

Define your own functions:

```vanction
func greet(person) {
    System.print("Hello, " + person + "!");
}

func add(a, b) {
    return a + b;
}

// Call functions
greet("World");
result = add(3, 5);
System.print("Result is:", result);
```

### 4. Control Flow

#### Conditional Statements

```vanction
age = 18;
if age >= 18 {
    System.print("You are an adult");
} else {
    System.print("You are a minor");
}

score = 85;
if (score >= 90) {
    System.print("Grade: A");
} else-if (score >= 80) {
    System.print("Grade: B");
} else {
    System.print("Grade: C");
}
```

#### Loop Statements

```vanction
counter = 0;
while counter < 5 {
    System.print("Counter:", counter);
    counter = counter + 1;
}
```

## Running Vanction Programs

### Method 1: Run Source Files

```bash
python vanction.py hello.va
```

### Method 2: Use the Interactive Interpreter

```bash
python vanction.py --repl
```

In interactive mode, you can enter Vanction code directly and see results immediately.

## Built-in Functions

Vanction provides several commonly used built-in functions:

- `System.print(...)`: Print output, supports multiple parameters
- `System.input(...)`: Get user input
- `len(string)`: Get string length
- `str(value)`: Convert to string
- `int(value)`: Convert to integer
- `float(value)`: Convert to floating-point number

## Example Programs

### Simple Calculator

```vanction
func calculator() {
    System.print("Simple Calculator");
    a = float(System.input("Enter first number: "));
    b = float(System.input("Enter second number: "));
    
    System.print("Addition result:", a + b);
    System.print("Subtraction result:", a - b);
    System.print("Multiplication result:", a * b);
    if b != 0 {
        System.print("Division result:", a / b);
    } else {
        System.print("Error: Division by zero");
    }
}

calculator();
```

## Learning Resources

- Check the [README.md](../README.md) in the project root directory for more detailed information
- Try modifying example code to explore more features of Vanction

## Frequently Asked Questions

**Q: What does the error "Expected semicolon after expression" mean?**
**A:** This means your code is missing a semicolon. In Vanction, each statement needs to end with a semicolon.

**Q: How do I exit the interactive interpreter?**
**A:** Type `exit` or `quit` to exit the interpreter.

**Q: Can I define complex data structures in Vanction?**
**A:** Currently, Vanction supports basic data types such as numbers, strings, and booleans.