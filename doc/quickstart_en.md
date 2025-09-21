# Vanction Language Quick Start Guide

This tutorial will help you quickly get started with the Vanction programming language, covering all keywords and core features with ready-to-run code examples.

## Language Overview

Vanction is a simple, easy-to-learn programming language designed for educational purposes and rapid prototyping. It features modern programming language syntax while maintaining simplicity and clarity.

## Environment Setup

Vanction is a Python-based interpreter, so just ensure your system has Python 3.6 or higher installed.

## Running Vanction

### 1. Running Source Files

```bash
python vanction.py filename.va
```

### 2. Interactive REPL Mode

```bash
python vanction.py --repl
```

In REPL mode, you can directly input and execute code. Type `exit` or `quit` to exit.

## Basic Syntax

### Comments

**Important Note: Vanction uses the `|` symbol for comments!**

```vanction
| This is a single-line comment, starting with a single vertical bar

|\
  This is a multi-line comment
  Starting with |\ and ending with /|
  It can span multiple lines
/|

|*
 * This is a documentation comment
 * Starting with |* and ending with *|
 * Used for documenting functions or classes
*|
```

### Entry Function

Vanction's entry function is `main`; all code starts executing from the `main` function.

```vanction
func main() {
    System.print("Hello, Vanction!");
}
```

#### Please note that the following code examples omit the main function. If you want to run them, add the code to the main function:

```vanction
func main() {
    # Your code here
}
```

### Statement Termination

Vanction statements end with a semicolon `;`:

```vanction
x = 5;
System.print(x);
```

## Data Types

### Numbers

Supports integers and floating-point numbers:

```vanction
integer_num = 42;
float_num = 3.14;
```

### Strings

Strings are enclosed in double or single quotes:

```vanction
greeting = "Hello, Vanction!";
name = 'World';
```

### Booleans

Boolean values are obtained through comparison operations:

```vanction
true_value = (5 > 3);  | Result is true
false_value = (1 == 2);  | Result is false
```

### Arrays

Arrays are ordered collections of data:

```vanction
numbers = [1, 2, 3, 4, 5];
mixed = [1, "two", 3.0, true];
```

### Dictionaries

Dictionaries are collections of key-value pairs:

```vanction
person = {"name": "Alice", "age": 25, "city": "New York"};
```

### Tuples

Tuples are immutable ordered collections of data:

```vanction
coordinates = (10, 20);
```

## Variables and Constants

### Variable Definition

Use the assignment symbol `=` to define variables:

```vanction
variable_name = value;
count = 0;
message = "Hello";
```

### Constant Definition

Use the `immut` keyword to define immutable constants:

```vanction
immut PI = 3.14159;
immut MAX_VALUE = 100;
```

## Operators

### Arithmetic Operators

```vanction
addition = 5 + 3;      | Addition
subtraction = 10 - 4;  | Subtraction
multiplication = 6 * 7;  | Multiplication
division = 20 / 5;     | Division
modulo = 10 % 3;       | Modulo
power = 2 ^ 3;         | Exponentiation (2 to the power of 3)
```
Note that operators like `^` must have spaces around them, e.g., `2 ^ 3` not `2^3`.

### Comparison Operators

```vanction
equal = (5 == 5);       | Equal
not_equal = (5 != 3);   | Not equal
less_than = (3 < 5);    | Less than
greater_than = (5 > 3); | Greater than
less_equal = (3 <= 5);  | Less than or equal
greater_equal = (5 >= 3); | Greater than or equal
```

### Logical Operators

```vanction
logical_and = (true && false);  | Logical AND
logical_or = (true || false);   | Logical OR
logical_not = !true;            | Logical NOT
```

### Bitwise Operators

```vanction
bitwise_or = 5 | 3;     | Bitwise OR
bitwise_xor = 5 ^^ 3;   | Bitwise XOR
bitwise_and = 5 & 3;    | Bitwise AND
left_shift = 5 << 1;    | Left shift
right_shift = 5 >> 1;   | Right shift
```

## Control Flow

### if-else Statements

```vanction
age = 18;
if age >= 18 {
    System.print("You are an adult");
} else {
    System.print("You are a minor");
}

| Multiple condition branches
score = 85;
if score >= 90 {
    System.print("Grade: A");
} else-if score >= 80 {
    System.print("Grade: B");
} else-if score >= 70 {
    System.print("Grade: C");
} else {
    System.print("Grade: F");
}
```

### while Loops

```vanction
counter = 0;
while counter < 5 {
    System.print("Counter: " + str(counter));
    counter = counter + 1;
}
```

### for Loops

Vanction supports two for loop syntaxes:

#### Traditional for Loop

```vanction
for i = 0; i < 5; i = i + 1 {
    System.print("i = " + str(i));
}
```

#### for-in Loop

```vanction
numbers = [1, 2, 3, 4, 5];
for num in numbers {
    System.print("Number: " + str(num));
}
```

### switch Statements

```vanction
day = 3;
switch day {
    case 1 {
        System.print("Monday");
    }
    case 2 {
        System.print("Tuesday");
    }
    case 3 {
        System.print("Wednesday");
    }
    default {
        System.print("Other day");
    }
}
```

### Jump Statements

```vanction
| break statement - Exit the loop
counter = 0;
while true {
    counter = counter + 1;
    if counter > 5 {
        break;
    }
    System.print(counter);
}

| continue statement - Skip the rest of the current loop iteration
for i = 0; i < 10; i = i + 1 {
    if i % 2 == 0 {
        continue;
    }
    System.print(i);  | Only prints odd numbers
}
```

## Functions

### Function Definition

Use the `func` keyword to define functions:

```vanction
func greet(name) {
    System.print("Hello, " + name + "!");
}

| Function with return value
func add(a, b) {
    return a + b;
}
```

### Function Call

```vanction
greet("World");
result = add(5, 3);
System.print("5 + 3 = " + str(result));
```

### Lambda Expressions

Lambda expressions provide a concise way to create anonymous functions:

```vanction
square = (x) -> x * x;
System.print(square(5));  | Output: 25

| Lambda as parameter
numbers = [1, 2, 3, 4, 5];
doubled = map(numbers, (x) -> x * 2);
```

## Exception Handling

### try-catch-finally Statements

```vanction
try {
    | Code that might throw an exception
    result = 10 / 0;
} catch (error) {
    | Handle the exception
    System.print("Error occurred: " + error.message);
} finally {
    | Code that runs regardless of whether an exception occurred
    System.print("Cleaning up resources");
}
```

### Throwing Exceptions

Use the `throw` keyword to throw exceptions:

```vanction
func divide(a, b) {
    if b == 0 {
        throw "Division by zero is not allowed";
    }
    return a / b;
}
```

## Module System

### Importing Modules

```vanction
| Standard import
import math;

| Using imported module
result = math.add(5, 3);

| Import with alias
import math using m;
result = m.add(5, 3);
```

## Built-in Functions

### Output Functions

```vanction
System.print("Hello World");
System.print("Multiple arguments", 1, 2, 3);
```

### Input Functions

```vanction
name = System.input("Please enter your name: ");
System.print("Hello, " + name);
```

### Type Conversion Functions

```vanction
| Convert to integer
int_value = int("123");

| Convert to float
float_value = float("3.14");

| Convert to string
string_value = str(42);
```

### String Processing Functions

```vanction
| Get string length
length = len("Hello");  | Returns: 5

| Check string contains
contains = contains("Hello World", "World");  | Returns: true

| Replace string
replaced = replace("Hello World", "World", "Vanction");  | Returns: "Hello Vanction"

| Split string
parts = split("a,b,c", ",");  | Returns: ["a", "b", "c"]
```

### Array Operation Functions

```vanction
arr = [1, 2, 3];

| Add element
append(arr, 4);  | arr becomes: [1, 2, 3, 4]

| Remove element
remove(arr, 2);  | arr becomes: [1, 3, 4]

| Pop element
popped = pop(arr);  | popped is: 4, arr becomes: [1, 3]

| Get element index
index = index(arr, 3);  | Returns: 1
```

### Dictionary Operation Functions

```vanction
dict = {"name": "Alice", "age": 25};

| Get all keys
keys = keys(dict);  | Returns: ["name", "age"]

| Get all values
values = values(dict);  | Returns: ["Alice", 25]

| Get all key-value pairs
items = items(dict);  | Returns: [("name", "Alice"), ("age", 25)]

| Check if key exists
has_key = has_key(dict, "name");  | Returns: true
```

## Complete Example Program

Here is a complete Vanction program example that demonstrates various features of the language:

```vanction
| This is a complete Vanction language example program

| Define constant
immut PI = 3.14159;

| Define function - Calculate circle area
func calculate_area(radius) {
    return PI * radius ^ 2;
}

| Main function
func main() {
    System.print("==== Vanction Language Example Program ====");
    
    | Variable definition
    name = System.input("Please enter your name: ");
    System.print("Hello, " + name + "!");
    
    | Input radius and calculate area
    radius_str = System.input("Please enter the radius of the circle: ");
    radius = float(radius_str);
    area = calculate_area(radius);
    System.print("Area of the circle: " + str(area));
    fib_list = [];
    for (i in range(10)) {
        array.append(fib_list,i);
    }
    | Using dictionary
    person = {"name": name, "favorite_number": fib_list[9]};
    System.print("\nPersonal Information:");
    System.print("Name: " + person["name"]);
    System.print("Favorite number: " + str(person["favorite_number"]));
    
    | Exception handling example
    try {
        System.print("\nPlease enter a divisor: ");
        divisor_str = System.input();
        divisor = int(divisor_str);
        result = 100 / divisor;
        System.print("100 / " + divisor_str + " = " + str(result));
    } catch (error) {
        System.print("Error occurred: " + error.message);
    } finally {
        System.print("Exception handling completed");
    }
    
    System.print("\nProgram execution completed!");
}
```

Save the above code as `example.va` and run it using the command `python vanction.py example.va`.

## Extending Vanction

Vanction is designed to be easy to extend. You can add new features in the following ways:

1. **Add new built-in functions**: Add them in the `setup_builtin_functions` method in `interpreter.py`
2. **Add new syntax**: Extend `lexer.py` and `parser.py` to support new syntax structures
3. **Add new operators**: Implement them in `parser.py` and `interpreter.py`

## Summary

Through this tutorial, you have learned all the core features of the Vanction language, including data types, variables, operators, control flow, functions, exception handling, and the module system. Now you can start writing your own Vanction programs!