# Vanction语言快速入门教程

本教程将帮助你快速上手Vanction编程语言，涵盖语言的所有关键词和核心功能，并提供可直接运行的代码示例。

## 语言概述

Vanction是一个简单易学的编程语言，专为教育目的和快速原型设计而创建。它具有现代编程语言的语法特性，同时保持简洁明了。

## 环境准备

Vanction是一个基于Python的解释器，只需确保你的系统已安装Python 3.6或更高版本。

## 运行方式

### 1. 运行源文件

```bash
python vanction.py 文件名.va
```

### 2. 交互式REPL模式

```bash
python vanction.py --repl
```

在REPL模式下，可以直接输入代码并执行，输入`exit`或`quit`退出。

## 基础语法

### 注释

**重要提醒：Vanction语言使用 `|` 符号作为注释符号！**

```vanction
| 这是单行注释，以单个竖线开始

|\
  这是多行注释
  以 |\ 开始，以 /| 结束
  可以跨越多行
/|

|*
 * 这是文档注释
 * 以 |* 开始，以 *| 结束
 * 用于函数或类的文档说明
*|
```
### 入口函数
Vanction的入口函数是`main`函数，所有的代码都从`main`函数开始执行。
```vanction
func main() {
    System.print("Hello, Vanction!");
}
```

#### 请注意，下列的代码省略了入口函数main，如果你要实际运行这些代码，请在main函数添加这些代码：
```vanction
func main() {
    # 这里是你的代码
}
```

### 语句结束

Vanction语句以分号`;`结束：

```vanction
x = 5;
System.print(x);
```

## 数据类型

### 数字

支持整数和浮点数：

```vanction
integer_num = 42;
float_num = 3.14;
```

### 字符串

字符串用双引号或单引号包围：

```vanction
greeting = "Hello, Vanction!";
name = 'World';
```

### 布尔值

布尔值通过比较操作获得：

```vanction
true_value = (5 > 3);  | 结果为true
false_value = (1 == 2);  | 结果为false
```

### 数组

数组是有序的数据集合：

```vanction
numbers = [1, 2, 3, 4, 5];
mixed = [1, "two", 3.0, true];
```

### 字典

字典是键值对的集合：

```vanction
person = {"name": "Alice", "age": 25, "city": "New York"};
```

### 元组

元组是不可变的有序数据集合：

```vanction
coordinates = (10, 20);
```

## 变量和常量

### 变量定义

使用赋值符号`=`定义变量：

```vanction
variable_name = value;
count = 0;
message = "Hello";
```

### 常量定义

使用`immut`关键字定义不可变常量：

```vanction
immut PI = 3.14159;
immut MAX_VALUE = 100;
```

## 运算符

### 算术运算符

```vanction
addition = 5 + 3;      | 加法
subtraction = 10 - 4;  | 减法
multiplication = 6 * 7;  | 乘法
division = 20 / 5;     | 除法
modulo = 10 % 3;       | 取模
power = 2 ^ 3;         | 幂运算（2的3次方）
```
需要注意的是，包括但不限于不能：2^3，必须有空格间隔，如：2 ^ 3

### 比较运算符

```vanction
equal = (5 == 5);       | 等于
not_equal = (5 != 3);   | 不等于
less_than = (3 < 5);    | 小于
greater_than = (5 > 3); | 大于
less_equal = (3 <= 5);  | 小于等于
greater_equal = (5 >= 3); | 大于等于
```

### 逻辑运算符

```vanction
logical_and = (true && false);  | 逻辑与
logical_or = (true || false);   | 逻辑或
logical_not = !true;            | 逻辑非
```

### 位运算符

```vanction
bitwise_or = 5 | 3;     | 按位或
bitwise_xor = 5 ^^ 3;   | 按位异或
bitwise_and = 5 & 3;    | 按位与
left_shift = 5 << 1;    | 左移
right_shift = 5 >> 1;   | 右移
```

## 控制流

### if-else语句

```vanction
age = 18;
if age >= 18 {
    System.print("你是成年人");
} else {
    System.print("你是未成年人");
}

| 多条件分支
score = 85;
if score >= 90 {
    System.print("等级: A");
} else-if score >= 80 {
    System.print("等级: B");
} else-if score >= 70 {
    System.print("等级: C");
} else {
    System.print("等级: F");
}
```

### while循环

```vanction
counter = 0;
while counter < 5 {
    System.print("计数器: " + str(counter));
    counter = counter + 1;
}
```

### for循环

Vanction支持两种for循环语法：

#### 传统for循环

```vanction
for i = 0; i < 5; i = i + 1 {
    System.print("i = " + str(i));
}
```

#### for-in循环

```vanction
numbers = [1, 2, 3, 4, 5];
for num in numbers {
    System.print("数字: " + str(num));
}
```

### switch语句

```vanction
day = 3;
switch day {
    case 1 {
        System.print("星期一");
    }
    case 2 {
        System.print("星期二");
    }
    case 3 {
        System.print("星期三");
    }
    default {
        System.print("其他天");
    }
}
```

### 跳转语句

```vanction
| break语句 - 跳出循环
counter = 0;
while true {
    counter = counter + 1;
    if counter > 5 {
        break;
    }
    System.print(counter);
}

| continue语句 - 跳过当前循环的剩余部分
for i = 0; i < 10; i = i + 1 {
    if i % 2 == 0 {
        continue;
    }
    System.print(i);  | 只打印奇数
}
```

## 函数

### 函数定义

使用`func`关键字定义函数：

```vanction
func greet(name) {
    System.print("Hello, " + name + "!");
}

| 带返回值的函数
func add(a, b) {
    return a + b;
}
```

### 函数调用

```vanction
greet("World");
result = add(5, 3);
System.print("5 + 3 = " + str(result));
```

### Lambda表达式

Lambda表达式提供了创建匿名函数的简洁方式：

```vanction
square = (x) -> x * x;
System.print(square(5));  | 输出: 25

| Lambda作为参数
numbers = [1, 2, 3, 4, 5];
doubled = map(numbers, (x) -> x * 2);
```

## 异常处理

### try-catch-finally语句

```vanction
try {
    | 可能抛出异常的代码
    result = 10 / 0;
} catch (error) {
    | 处理异常
    System.print("发生错误: " + error.message);
} finally {
    | 无论是否发生异常都会执行的代码
    System.print("清理资源");
}
```

### 抛出异常

使用`throw`关键字抛出异常：

```vanction
func divide(a, b) {
    if b == 0 {
        throw "除数不能为零";
    }
    return a / b;
}
```

## 模块系统

### 导入模块

```vanction
| 标准导入
import math;

| 使用导入的模块
result = math.add(5, 3);

| 使用别名导入
import math using m;
result = m.add(5, 3);
```

## 内置函数

### 输出函数

```vanction
System.print("Hello World");
System.print("多个参数", 1, 2, 3);
```

### 输入函数

```vanction
name = System.input("请输入你的名字: ");
System.print("你好, " + name);
```

### 类型转换函数

```vanction
| 转换为整数
int_value = int("123");

| 转换为浮点数
float_value = float("3.14");

| 转换为字符串
string_value = str(42);
```

### 字符串处理函数

```vanction
| 获取字符串长度
length = len("Hello");  | 返回: 5

| 检查字符串包含
contains = contains("Hello World", "World");  | 返回: true

| 替换字符串
replaced = replace("Hello World", "World", "Vanction");  | 返回: "Hello Vanction"

| 分割字符串
parts = split("a,b,c", ",");  | 返回: ["a", "b", "c"]
```

### 数组操作函数

```vanction
arr = [1, 2, 3];

| 添加元素
append(arr, 4);  | arr变为: [1, 2, 3, 4]

| 移除元素
remove(arr, 2);  | arr变为: [1, 3, 4]

| 弹出元素
popped = pop(arr);  | popped为: 4, arr变为: [1, 3]

| 获取元素索引
index = index(arr, 3);  | 返回: 1
```

### 字典操作函数

```vanction
dict = {"name": "Alice", "age": 25};

| 获取所有键
keys = keys(dict);  | 返回: ["name", "age"]

| 获取所有值
values = values(dict);  | 返回: ["Alice", 25]

| 获取所有键值对
items = items(dict);  | 返回: [("name", "Alice"), ("age", 25)]

| 检查键是否存在
has_key = has_key(dict, "name");  | 返回: true
```

## 完整示例程序

下面是一个完整的Vanction程序示例，展示了语言的各种特性：

```vanction
| 这是一个Vanction语言的完整示例程序

| 定义常量
immut PI = 3.14159;

| 定义函数 - 计算圆的面积
func calculate_area(radius) {
    return PI * radius ^ 2;
}

| 主函数
func main() {
    System.print("==== Vanction语言示例程序 ====");
    
    | 变量定义
    name = System.input("请输入你的名字: ");
    System.print("你好, " + name + "!");
    
    | 输入半径并计算面积
    radius_str = System.input("请输入圆的半径: ");
    radius = float(radius_str);
    area = calculate_area(radius);
    System.print("圆的面积: " + str(area));
    fib_list = [];
    for (i in range(10)) {
        array.append(fib_list,i);
    }
    | 使用字典
    person = {"name": name, "favorite_number": fib_list[9]};
    System.print("\n个人信息:");
    System.print("姓名: " + person["name"]);
    System.print("最喜欢的数字: " + str(person["favorite_number"]));
    
    | 异常处理示例
    try {
        System.print("\n请输入一个除数: ");
        divisor_str = System.input();
        divisor = int(divisor_str);
        result = 100 / divisor;
        System.print("100 / " + divisor_str + " = " + str(result));
    } catch (error) {
        System.print("发生错误: " + error.message);
    } finally {
        System.print("异常处理结束");
    }
    
    System.print("\n程序执行完毕！");
}
```

将上面的代码保存为`example.va`文件，然后使用`python vanction.py example.va`命令运行它。

## 扩展Vanction

Vanction语言设计为易于扩展，你可以通过以下方式添加新功能：

1. **添加新的内置函数**：在`interpreter.py`中的`setup_builtin_functions`方法中添加
2. **添加新的语法**：扩展`lexer.py`和`parser.py`以支持新的语法结构
3. **添加新的运算符**：在`parser.py`和`interpreter.py`中实现新的运算符

## 总结

通过本教程，你已经了解了Vanction语言的所有核心特性，包括数据类型、变量、运算符、控制流、函数、异常处理和模块系统等。现在你可以开始编写自己的Vanction程序了！