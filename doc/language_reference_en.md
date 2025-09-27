# Vanction Language Complete Reference Manual

## Introduction
Vanction is a modern scripting language that supports functional programming, object-oriented, and procedural programming paradigms. This manual covers all language features and keywords.

## Table of Contents
1. [Basic Syntax](#basic-syntax)
2. [Data Types](#data-types)
3. [Variables and Constants](#variables-and-constants)
4. [Operators](#operators)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [String Processing](#string-processing)
8. [Comment System](#comment-system)
9. [Exception Handling](#exception-handling)
10. [Built-in Functions](#built-in-functions)
11. [Complete Keywords](#complete-keywords)

## Basic Syntax

### Program Structure
Each Vanction program must contain a `main` function as the entry point:
```vanction
func main() {
    System.print("Hello, Vanction!");
}
```

### Statement Termination
Vanction uses semicolon (`;`) as the statement terminator:
```vanction
x = 10;
y = x + 5;
```

## Data Types

### Basic Types
- **Numbers**: `123`, `3.14`, `-42`
- **Strings**: `"hello"`, `'world'`
- **Boolean**: `true`, `false`
- **Null**: `null`

### Composite Types
- **Array**: `[1, 2, 3, "hello"]`
- **Dictionary**: `{"name": "Vanction", "version": 2.0}`

### Special Types
- **Unassigned**: `unassigned` - used to define uninitialized variables
- **Any Type**: `anytion` - special placeholder type

## Variables and Constants

### Variable Definition
```vanction
| Regular variables
age = 25;
name = "Vanction";

| Arrays and dictionaries
numbers = [1, 2, 3, 4, 5];
person = {"name": "Alice", "age": 30};
```

### Immutable Variables (immut)
Use the `immut` keyword to define unmodifiable variables:
```vanction
immut pi = 3.14159;
immut version = "2.0";

| Attempting to modify will throw an error
| pi = 3.14;  | Error: Cannot modify immutable variable 'pi'
```

### Constant Definition (define)
Use the `define` keyword to define compile-time constants:
```vanction
define MAX_SIZE 100;
define APP_NAME "Vanction";

define SPECIAL_VALUE;  | Uses anytion as placeholder
```

## Operators

### Arithmetic Operators
```vanction
a = 10;
b = 3;

add = a + b;      | 13
sub = a - b;      | 7  
mul = a * b;      | 30
div = a / b;      | 3.333...
mod = a % b;      | 1
pow = a ^ b;      | 1000
```

### Comparison Operators
```vanction
eq = a == b;      | false
ne = a != b;      | true
lt = a < b;       | false
gt = a > b;       | true
le = a <= b;      | false
ge = a >= b;      | true
```

### Logical Operators
```vanction
and_result = true and false;   | false
or_result = true or false;    | true
not_result = !true;           | false
```

### Bitwise Operators
```vanction
bitwise_and = 5 & 3;      | 1
bitwise_or = 5 | 3;       | 7
bitwise_xor = 5 ^^ 3;     | 6
left_shift = 5 << 1;      | 10
right_shift = 5 >> 1;     | 2
```

## Control Flow

### Conditional Statements (if-else-if-else)
```vanction
age = 18;

if (age < 18) {
    System.print("Underage");
} else-if (age == 18) {
    System.print("Just became adult");
} else {
    System.print("Adult");
}
```

### Switch Statement
```vanction
func main() {
    day = "Monday";
    
    switch day {
        case "Monday" {
            System.print("Monday");
        }
        case "Friday" {
            System.print("Friday");
        }
        case "Saturday", "Sunday" {
            System.print("Weekend");
        }
        default {
            System.print("Weekday");
        }
    }
}
```

### For Loop
Vanction supports three forms of for loops:

#### 1. Traditional for loop
```vanction
for (i = 0; i < 5; i = i + 1) {
    System.print(i);
}
```

#### 2. For-in loop (array)
```vanction
fruits = ["apple", "banana", "orange"];

for (fruit in fruits) {
    System.print(fruit);
}
```

#### 3. For-in loop (dictionary)
```vanction
person = {"name": "Bob", "age": 25};

for (key, value in person) {
    System.print(key + ": " + value);
}
```

### While Loop
```vanction
count = 0;

while (count < 3) {
    System.print(count);
    count = count + 1;
}
```

## Functions

### Function Definition
```vanction
func greet(name) {
    return "Hello, " + name;
}

func add(a, b) {
    return a + b;
}
```

### Lambda Expressions
```vanction
func main() {
    | Define lambda functions
    square = (x) -> x * x;
    double = (x) -> x * 2;
    
    | Use lambda functions
    result1 = square(5);      | 25
    result2 = double(10);     | 20
    
    | Higher-order functions
    func apply_operation(numbers, operation) {
        result = [];
        for (n in numbers) {
            result.append(operation(n));
        }
        return result;
    }
    
    numbers = [1, 2, 3, 4, 5];
    squared = apply_operation(numbers, (x) -> x * x);
}
```

### Multiple Return Values
```vanction
func calculate(a, b) {
    sum = a + b;
    diff = a - b;
    product = a * b;
    return sum, diff, product;
}
func main() {
    s, d, p = calculate(10, 3);
}
```

## String Processing

### Formatted Strings (f"...")
```vanction
name = "Vanction";
version = 2.0;
message = f"Welcome to {name} version {version}";

| Complex expressions
pi = 3.14159;
info = f"The value of pi is {pi}, twice is {pi * 2}";
```

### Raw Strings ($"...")
```vanction
| Raw strings do not process escape characters
path = $"C:\\Users\\Name\\Documents";
regex = $"\d+\.\d+";

| Compare with normal strings (will escape)
normal = "First line\nSecond line";
raw = $"First line\nSecond line";    | \n will be output as-is
```

### String Operations
```vanction
text = "Hello, Vanction!";

| String methods
length = str.length(text);           | 16
contains = str.contains(text, "Vanction");  | true
replaced = str.replace(text, "Vanction", "World");  | "Hello, World!"
upper = str.upper(text);             | "HELLO, VANCTION!"
lower = str.lower(text);             | "hello, vanction!"
parts = str.split(text, ",");        | ["Hello", " Vanction!"]
stripped = str.strip("  hello  ");    | "hello"
```

## Comment System

### Single-line Comments
```vanction
| This is a single-line comment
x = 10;  | End-of-line comment
```

### Multi-line Comments
```vanction
|\
This is a multi-line comment
Can write multiple lines
Comment ends
/|

y = 20;
```

### Documentation Comments
```vanction
|*This is a documentation comment
 * Used for function or module description
 * Supports special format
*|

func important_function() {
    | Function implementation
}
```

## Exception Handling

### Try-Catch-Finally
```vanction
try {
    result = 10 / 0;    | Will throw an exception
} catch (error) {
    System.print("Caught error: " + error);
} finally {
    System.print("Cleanup work");
}
```

### Throwing Exceptions (throw)
```vanction
func validate_age(age) {
    if age < 0 {
        throw "Age cannot be negative";
    }
    if age > 150 {
        throw "Age cannot exceed 150";
    }
    return true;
}

try {
    validate_age(-5);
} catch (e) {
    System.print("Validation failed: " + e);
}
```

## Built-in Functions

### System Functions
```vanction
| Output functions
System.print("Hello World");
System.print(123);
System.print([1, 2, 3]);

| Input functions
name = System.input("Please enter your name: ");
```

### Range Function (range)
```vanction
| Generate number ranges
r1 = range(5);        | [0, 1, 2, 3, 4]
r2 = range(2, 6);     | [2, 3, 4, 5]

| Use in for loops
for (i in range(3)) {
    System.print(i);
}
```

### Array Operations
```vanction
arr = [1, 2, 3];

| Add elements
arr.append(4);
arr.insert(0, 0);

| Remove elements
arr.remove(2);    | Remove element with value 2
arr.pop();        | Remove last element

| Query
index = arr.index(3);
contains = arr.contains(3);

| Other operations
arr.reverse();
arr.sort();
length = arr.length();
```

### Type Conversion
```vanction
| Convert to string
str_int = str(123);
str_float = str(3.14);
str_bool = str(true);

| Convert to number
num_from_str = int("42");
float_from_str = float("3.14");

| Type checking
is_string = type("hello") == "string";
is_number = type(123) == "number";
is_array = type([1, 2, 3]) == "array";
```

### File Operations
```vanction
| File read/write
File.write("test.txt", "Hello Vanction!");
content = File.read("test.txt");

| File check
exists = File.exists("test.txt");
File.delete("test.txt");
```

## Complete Keywords

| Keyword       | Description        | Example                                 |
|-----------|------------------|------------------------------------|
| `func`    | Function definition    | `func add(a, b) { return a + b; }` |
| `return`  | Function return      | `return x * 2;`                    |
| `if`      | Conditional judgment   | `if x > 0 { ... }`                 |
| `else-if` | Multi-condition branch | `else-if x == 0 { ... }`           |
| `else`    | Default branch      | `else { ... }`                     |
| `switch`  | Multi-way branch    | `switch value { ... }`             |
| `case`    | Branch condition    | `case "value" { ... }`             |
| `default` | Default branch      | `default { ... }`                  |
| `for`     | Loop control        | `for (i = 0; i < 10; i++) { ... }` |
| `while`   | Conditional loop    | `while condition { ... }`          |
| `in`      | Iterator keyword    | `for (item in array) { ... }`      |
| `try`     | Exception handling  | `try { ... } catch (e) { ... }`    |
| `catch`   | Exception capture   | `catch (error) { ... }`            |
| `finally` | Final processing    | `finally { ... }`                  |
| `throw`   | Throw exception     | `throw "error message";`           |
| `immut`   | Immutable variable  | `immut pi = 3.14;`                 |
| `define`  | Constant definition | `define MAX_SIZE 100;`             |
| `true`    | Boolean true        | `flag = true;`                     |
| `false`   | Boolean false       | `flag = false;`                    |
| `null`    | Null value          | `value = null;`                    |
| `lambda`  | Lambda expression   | `lambda x -> x * x`                |
| `System`  | System object       | `System.print("hello");`           |
| `File`    | File object         | `File.read("file.txt");`          |
| `str`     | String object       | `str.length("hello");`             |
| `type`    | Type checking       | `type(value);`                     |
| `range`   | Range generation    | `range(5);`                        |

## Complete Example Program

```vanction
func main() {
    System.print("=== Vanction Language Feature Test ===");

    | 1. Test data types
    System.print("\n1. Data Type Test;");
    num = 42;
    str = "Hello";
    arr = [1, 2, 3];
    dict = {"key": "value"};
    System.print(f"Number: {num}, String: {str}");
    System.print(f"Array: {arr}, Dictionary: {dict}");

    | 2. Test immutable variables
    System.print("\n2. Immutable Variable Test;");
    immut constant = "Cannot be modified";
    System.print(f"Constant value: {constant}");

    | 3. Test string formatting
    System.print("\n3. String Formatting Test;");
    name = "Vanction";
    version = 2.0;
    formatted = f"Language: {name}, Version: {version}";
    System.print(formatted);

    | 4. Test raw strings
    System.print("\n4. Raw String Test;");
    raw = $"Path: C:\\Users\\Test\\nNo escape";
    System.print(raw);

    | 5. Test control flow
    System.print("\n5. Control Flow Test;");
    for (i in range(3)) {
        System.print(f"Loop count: {i}");
    }

    | 6. Test lambda expressions
    System.print("\n6. Lambda Expression Test;");
    square = lambda x -> x * x;
    result = square(5);
    System.print(f"Square of 5: {result}");

    | 7. Test exception handling
    System.print("\n7. Exception Handling Test;");
    try {
        throw "Test exception";
    } catch (e) {
        System.print(f"Caught exception: {e}");
    }

    System.print("\n=== All Tests Completed ===");
}
```

---

*This manual covers all major features of the Vanction language*