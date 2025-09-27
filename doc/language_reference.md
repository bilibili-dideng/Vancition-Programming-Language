# Vanction语言完整参考手册

## 简介
Vanction是一门现代化的脚本语言，支持函数式编程、面向对象和过程式编程范式。本手册涵盖所有语言特性和关键字。

## 目录
1. [基础语法](#基础语法)
2. [数据类型](#数据类型)
3. [变量和常量](#变量和常量)
4. [运算符](#运算符)
5. [控制流](#控制流)
6. [函数](#函数)
7. [字符串处理](#字符串处理)
8. [注释系统](#注释系统)
9. [异常处理](#异常处理)
10. [内置函数](#内置函数)
11. [关键字大全](#关键字大全)

## 基础语法

### 程序结构
每个Vanction程序必须包含`main`函数作为入口点：
```vanction
func main() {
    System.print("Hello, Vanction!");
}
```

### 语句结束
Vanction使用分号(`;`)作为语句结束符：
```vanction
x = 10;
y = x + 5;
```

## 数据类型

### 基本类型
- **数字**: `123`, `3.14`, `-42`
- **字符串**: `"hello"`, `'world'`
- **布尔值**: `true`, `false`
- **空值**: `null`

### 复合类型
- **数组**: `[1, 2, 3, "hello"]`
- **字典**: `{"name": "Vanction", "version": 2.0}`

### 特殊类型
- **未赋值**: `unassigned` - 用于定义未初始化的变量
- **任意类型**: `anytion` - 特殊的占位符类型

## 变量和常量

### 变量定义
```vanction
| 普通变量
age = 25;
name = "Vanction";

| 数组和字典
numbers = [1, 2, 3, 4, 5];
person = {"name": "Alice", "age": 30};
```

### 不可变变量 (immut)
使用`immut`关键字定义不可修改的变量：
```vanction
immut pi = 3.14159;
immut version = "2.0";

| 尝试修改会抛出错误
| pi = 3.14;  | 错误：Cannot modify immutable variable 'pi'
```

### 常量定义 (define)
使用`define`关键字定义编译期常量：
```vanction
define MAX_SIZE 100;
define APP_NAME "Vanction";

define SPECIAL_VALUE;  | 使用anytion作为占位符
```

## 运算符

### 算术运算符
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

### 比较运算符
```vanction
eq = a == b;      | false
ne = a != b;      | true
lt = a < b;       | false
gt = a > b;       | true
le = a <= b;      | false
ge = a >= b;      | true
```

### 逻辑运算符
```vanction
and_result = true and false;   | false
or_result = true or false;    | true
not_result = !true;           | false
```

### 位运算符
```vanction
bitwise_and = 5 & 3;      | 1
bitwise_or = 5 | 3;       | 7
bitwise_xor = 5 ^^ 3;     | 6
left_shift = 5 << 1;      | 10
right_shift = 5 >> 1;     | 2
```

## 控制流

### 条件语句 (if-else-if-else)
```vanction
age = 18;

if (age < 18) {
    System.print("未成年");
} else-if (age == 18) {
    System.print("刚成年");
} else {
    System.print("已成年");
}
```

### Switch语句
```vanction
func main() {
    day = "Monday";
    
    switch day {
        case "Monday" {
            System.print("星期一");
        }
        case "Friday" {
            System.print("星期五");
        }
        case "Saturday", "Sunday" {
            System.print("周末");
        }
        default {
            System.print("工作日");
        }
    }
}
```

### For循环
Vanction支持三种for循环形式：

#### 1. 传统for循环
```vanction
for (i = 0; i < 5; i = i + 1) {
    System.print(i);
}
```

#### 2. For-in循环（数组）
```vanction
fruits = ["apple", "banana", "orange"];

for (fruit in fruits) {
    System.print(fruit);
}
```

#### 3. For-in循环（字典）
```vanction
person = {"name": "Bob", "age": 25};

for (key, value in person) {
    System.print(key + "; " + value);
}
```

### While循环
```vanction
count = 0;

while (count < 3) {
    System.print(count);
    count = count + 1;
}
```

## 函数

### 函数定义
```vanction
func greet(name) {
    return "Hello, " + name;
}

func add(a, b) {
    return a + b;
}
```

### Lambda表达式
```vanction
func main() {
    | 定义lambda函数
    square = (x) -> x * x;
    double = (x) -> x * 2;
    
    | 使用lambda函数
    result1 = square(5);      | 25
    result2 = double(10);     | 20
    
    | 高阶函数
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

### 多返回值
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

## 字符串处理

### 格式化字符串 (f"...")
```vanction
name = "Vanction";
version = 2.0;
message = f"欢迎使用 {name} 版本 {version}";

| 复杂表达式
pi = 3.14159;
info = f"圆周率的值是 {pi}, 两倍是 {pi * 2}";
```

### 原始字符串 ($"...")
```vanction
| 原始字符串不处理转义字符
path = $"C;\Users\Name\Documents";
regex = $"\d+\.\d+";

| 对比普通字符串（会转义）
normal = "第一行\n第二行";
raw = $"第一行\n第二行";    | \n会原样输出
```

### 字符串操作
```vanction
text = "Hello, Vanction!";

| 字符串方法
length = str.length(text);           | 16
contains = str.contains(text, "Vanction");  | true
replaced = str.replace(text, "Vanction", "World");  | "Hello, World!"
upper = str.upper(text);             | "HELLO, VANCTION!"
lower = str.lower(text);             | "hello, vanction!"
parts = str.split(text, ",");        | ["Hello", " Vanction!"]
stripped = str.strip("  hello  ");    | "hello"
```

## 注释系统

### 单行注释
```vanction
| 这是一个单行注释
x = 10;  | 行尾注释
```

### 多行注释
```vanction
|\
这是一个多行注释
可以写多行内容
注释结束
/|

y = 20;
```

### 文档注释
```vanction
|*这是一个文档注释
 * 用于函数或模块说明
 * 支持特殊格式
*|

func important_function() {
    | 函数实现
}
```

## 异常处理

### Try-Catch-Finally
```vanction
try {
    result = 10 / 0;    | 会抛出异常
} catch (error) {
    System.print("捕获到错误; " + error);
} finally {
    System.print("清理工作");
}
```

### 抛出异常 (throw)
```vanction
func validate_age(age) {
    if age < 0 {
        throw "年龄不能为负数";
    }
    if age > 150 {
        throw "年龄不能超过150";
    }
    return true;
}

try {
    validate_age(-5);
} catch (e) {
    System.print("验证失败; " + e);
}
```

## 内置函数

### 系统函数
```vanction
| 输出函数
System.print("Hello World");
System.print(123);
System.print([1, 2, 3]);

| 输入函数
name = System.input("请输入姓名; ");
```

### 范围函数 (range)
```vanction
| 生成数字范围
r1 = range(5);        | [0, 1, 2, 3, 4]
r2 = range(2, 6);     | [2, 3, 4, 5]

| 在for循环中使用
for (i in range(3)) {
    System.print(i);
}
```

### 数组操作
```vanction
arr = [1, 2, 3];

| 添加元素
arr.append(4);
arr.insert(0, 0);

| 删除元素
arr.remove(2);    | 删除值为2的元素
arr.pop();        | 删除最后一个元素

| 查询
index = arr.index(3);
contains = arr.contains(3);

| 其他操作
arr.reverse();
arr.sort();
length = arr.length();
```

### 类型转换
```vanction
| 转换为字符串
str_int = str(123);
str_float = str(3.14);
str_bool = str(true);

| 转换为数字
num_from_str = int("42");
float_from_str = float("3.14");

| 类型检查
is_string = type("hello") == "string";
is_number = type(123) == "number";
is_array = type([1, 2, 3]) == "array";
```

### 文件操作
```vanction
| 文件读写
File.write("test.txt", "Hello Vanction!");
content = File.read("test.txt");

| 文件检查
exists = File.exists("test.txt");
File.delete("test.txt");
```

## 关键字大全

| 关键字       | 说明        | 示例                                 |
|-----------|-----------|------------------------------------|
| `func`    | 函数定义      | `func add(a, b) { return a + b; }` |
| `return`  | 函数返回      | `return x * 2;`                    |
| `if`      | 条件判断      | `if x > 0 { ... }`                 |
| `else-if` | 多条件分支     | `else-if x == 0 { ... }`           |
| `else`    | 默认分支      | `else { ... }`                     |
| `switch`  | 多路分支      | `switch value { ... }`             |
| `case`    | 分支条件      | `case "value" { ... }`             |
| `default` | 默认分支      | `default { ... }`                  |
| `for`     | 循环控制      | `for (i = 0; i < 10; i++) { ... }` |
| `while`   | 条件循环      | `while condition { ... }`          |
| `in`      | 迭代关键字     | `for (item in array) { ... }`      |
| `try`     | 异常处理      | `try { ... } catch (e) { ... }`    |
| `catch`   | 异常捕获      | `catch (error) { ... }`            |
| `finally` | 最终处理      | `finally { ... }`                  |
| `throw`   | 抛出异常      | `throw "错误信息";`                    |
| `immut`   | 不可变变量     | `immut pi = 3.14;`                 |
| `define`  | 常量定义      | `define MAX_SIZE 100;`             |
| `true`    | 布尔真       | `flag = true;`                     |
| `false`   | 布尔假       | `flag = false;`                    |
| `null`    | 空值        | `value = null;`                    |
| `lambda`  | Lambda表达式 | `lambda x -> x * x`                |
| `System`  | 系统对象      | `System.print("hello");`           |
| `File`    | 文件对象      | `File.read("file.txt");`           |
| `str`     | 字符串对象     | `str.length("hello");`             |
| `type`    | 类型检查      | `type(value);`                     |
| `range`   | 范围生成      | `range(5);`                        |

## 完整示例程序

```vanction
func main() {
    System.print("=== Vanction语言功能测试 ===");

    | 1. 测试数据类型
    System.print("\n1. 数据类型测试;");
    num = 42;
    str = "Hello";
    arr = [1, 2, 3];
    dict = {"key": "value"};
    System.print(f"数字: {num}, 字符串: {str}");
    System.print(f"数组: {arr}, 字典: {dict}");

    | 2. 测试不可变变量
    System.print("\n2. 不可变变量测试;");
    immut constant = "不可修改";
    System.print(f"常量值: {constant}");

    | 3. 测试字符串格式化
    System.print("\n3. 字符串格式化测试;");
    name = "Vanction";
    version = 2.0;
    formatted = f"语言; {name}, 版本; {version}";
    System.print(formatted);

    | 4. 测试原始字符串
    System.print("\n4. 原始字符串测试;");
    raw = $"路径: C:\\Users\\Test\\n不转义";
    System.print(raw);

    | 5. 测试控制流
    System.print("\n5. 控制流测试;");
    for (i in range(3)) {
        System.print(f"循环次数; {i}");
    }

    | 6. 测试lambda表达式
    System.print("\n6. Lambda表达式测试;");
    square = lambda x -> x * x;
    result = square(5);
    System.print(f"5的平方; {result}");

    | 7. 测试异常处理
    System.print("\n7. 异常处理测试;");
    try {
        throw "测试异常";
    } catch (e) {
        System.print(f"捕获异常; {e}");
    }

    System.print("\n=== 所有测试完成 ===");
}
```

---

*本手册涵盖了Vanction语言的所有主要特性*