# Vanction 编程语言快速入门

## 什么是 Vanction

Vanction 是一个简单易学的编程语言，专为教育和快速原型设计而开发。它拥有简洁的语法，支持基本的编程概念，非常适合编程初学者或需要快速实现想法的开发者。

## 安装要求

Vanction 是基于 Python 的解释器，因此您需要在系统上安装 Python 3.6 或更高版本。

- Windows: 访问 [Python 官网](https://www.python.org/downloads/) 下载并安装
- macOS: 使用 Homebrew 安装 `brew install python`
- Linux: 使用包管理器安装，如 `sudo apt install python3`

## 获取 Vanction

直接从代码仓库获取 Vanction 解释器的源代码。

暂无发布

## 基本语法

### 1. Hello World 程序

创建一个简单的 Vanction 程序：

```vanction
func main() {
    System.print("Hello World!");
}

main();
```

将上面的代码保存为 `hello.va` 文件。

### 2. 变量和赋值

在 Vanction 中，您可以直接创建变量，不需要声明类型：

```vanction
name = "Vanction";
version = 1.0;
count = 5;
```

### 3. 函数定义和调用

定义自己的函数：

```vanction
func greet(person) {
    System.print("你好，" + person + "!");
}

func add(a, b) {
    return a + b;
}

// 调用函数
greet("世界");
result = add(3, 5);
System.print("结果是：", result);
```

### 4. 控制流

#### 条件语句

```vanction
age = 18;
if age >= 18 {
    System.print("你是成年人");
} else {
    System.print("你是未成年人");
}

score = 85;
if (score >= 90) {
    System.print("等级：A");
} else-if (score >= 80) {
    System.print("等级：B");
} else {
    System.print("等级：C");
}
```

#### 循环语句

```vanction
counter = 0;
while counter < 5 {
    System.print("计数：", counter);
    counter = counter + 1;
}
```

## 运行 Vanction 程序

### 方法 1: 运行源文件

```bash
python vanction.py hello.va
```

### 方法 2: 使用交互式解释器

```bash
python vanction.py --repl
```

在交互式模式下，您可以直接输入 Vanction 代码并立即看到结果。

## 内置函数

Vanction 提供了一些常用的内置函数：

- `System.print(...)`: 打印输出，支持多个参数
- `System.input(...)`: 获取用户输入
- `len(string)`: 获取字符串长度
- `str(value)`: 转换为字符串
- `int(value)`: 转换为整数
- `float(value)`: 转换为浮点数

## 示例程序

### 简单计算器

```vanction
func calculator() {
    System.print("简单计算器");
    a = float(System.input("输入第一个数字："));
    b = float(System.input("输入第二个数字："));
    
    System.print("加法结果：", a + b);
    System.print("减法结果：", a - b);
    System.print("乘法结果：", a * b);
    if b != 0 {
        System.print("除法结果：", a / b);
    } else {
        System.print("错误：除数不能为零");
    }
}

calculator();
```

## 学习资源

- 查看项目根目录的 [README.md](../README.md) 获取更多详细信息
- 尝试修改示例代码，探索 Vanction 的更多功能

## 常见问题

**问：程序运行报错 "Expected semicolon after expression" 是什么意思？**
**答：** 这表示您的代码缺少分号。在 Vanction 中，每个语句结束时需要使用分号。

**问：如何退出交互式解释器？**
**答：** 输入 `exit` 或 `quit` 命令即可退出。

**问：可以在 Vanction 中定义复杂的数据结构吗？**
**答：** 目前 Vanction 支持基本的数据类型，如数字、字符串和布尔值。