# Vanction语言零基础教程

## 概述
Vanction是一门简单易学的编程语言，专为初学者设计。本教程基于实际测试通过的功能，确保所有示例都能正常运行。

## 基本语法

### 1. Hello World
```vanction
func main() {
    System.print("Hello World!");
}
```

### 2. 注释
使用 `|` 符号进行单行注释：
```vanction
| 这是一个注释
func main() {
    | 打印欢迎信息
    System.print("欢迎使用Vanction!");
}
```

### 3. 变量和赋值
```vanction
func main() {
    | 变量赋值
    name = "Vanction";
    version = 1.0;
    count = 10;
    
    System.print("语言:", name);
    System.print("版本:", version);
    System.print("数量:", count);
}
```

### 4. 基本运算
支持加(+)、减(-)、乘(*)、除(/)运算：
```vanction
func main() {
    a = 15;
    b = 4;
    
    System.print("a =", a, "b =", b);
    System.print("a + b =", a + b);  | 19
    System.print("a - b =", a - b);  | 11
    System.print("a * b =", a * b);  | 60
    System.print("a / b =", a / b);  | 3.75
}
```

### 5. 字符串连接
```vanction
func main() {
    first_name = "张";
    last_name = "三";
    full_name = first_name + last_name;
    
    greeting = "欢迎, " + full_name + "!";
    System.print(greeting);
}
```

## 控制流

### 6. 条件语句 (if/else/else-if)
```vanction
func main() {
    age = 18;
    
    if (age >= 18) {
        System.print("你是成年人");
    } else {
        System.print("你是未成年人");
    }
    
    | 比较运算符: >, <, >=, <=, ==, !=
    score = 85;
    if (score >= 90) {
        System.print("优秀");
    } else-if (score >= 80) {
        System.print("良好");
    } else-if (score >= 70) {
        System.print("中等");
    } else-if (score >= 60) {
        System.print("及格");
    } else {
        System.print("不及格");
    }
}
```

### 7. 循环语句 (while)
```vanction
func main() {
    | 计算1到5的和
    sum = 0;
    i = 1;
    
    while (i <= 5) {
        sum = sum + i;
        System.print("当前数字:", i, "当前和:", sum);
        i = i + 1;
    }
    
    System.print("最终和:", sum);
}
```

## 函数

### 8. 函数定义和调用
```vanction
func add(a, b) {
    return a + b;
}

func multiply(x, y) {
    result = x * y;
    return result;
}

func main() {
    | 调用函数
    sum = add(5, 3);
    product = multiply(4, 7);
    
    System.print("5 + 3 =", sum);
    System.print("4 * 7 =", product);
    
    | 嵌套函数调用
    complex = add(multiply(2, 3), multiply(4, 5));
    System.print("2*3 + 4*5 =", complex);
}
```

### 9. 递归函数
```vanction
func factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func main() {
    result = factorial(5);
    System.print("5的阶乘 =", result);  | 120
}
```

## 语法更新说明

### 10. 新的else-if语法
从版本更新开始，Vanction语言采用了新的条件语句语法：

**✅ 推荐的语法（使用连字符）:**
```vanction
func check_score(score) {
    if (score >= 90) {
        return "A";
    } else-if (score >= 80) {
        return "B";
    } else-if (score >= 70) {
        return "C";
    } else {
        return "F";
    }
}
```

**❌ 已禁用的语法（使用空格）:**
```vanction
| 这种语法不再支持，会报语法错误
func check_score(score) {
    if (score >= 90) {
        return "A";
    } else if (score >= 80) {  | 错误：left brace ({) expected, found 'if'
        return "B";
    }
}
```

这种改变使得语法更加清晰和一致，避免了歧义。

## 布尔值

### 11. 布尔常量
Vanction支持 `true` 和 `false` 布尔值：
```vanction
func is_adult(age) {
    if (age >= 18) {
        return true;
    } else {
        return false;
    }
}

func main() {
    result1 = is_adult(20);
    result2 = is_adult(15);
    
    System.print("20岁是成年人:", result1);  | true
    System.print("15岁是成年人:", result2);  | false
}
```

## 综合示例

### 12. 完整程序示例
```vanction
| 学生成绩管理系统

func calculate_average(score1, score2, score3) {
    total = score1 + score2 + score3;
    return total / 3;
}

func get_grade(average) {
    if (average >= 90) {
        return "A";
    }
    if (average >= 80) {
        return "B";
    }
    if (average >= 70) {
        return "C";
    }
    if (average >= 60) {
        return "D";
    }
    return "F";
}

func main() {
    System.print("=== 学生成绩管理系统 ===");
    
    | 学生信息
    student_name = "李小明";
    math = 95;
    english = 88;
    science = 92;
    
    | 计算平均分
    average = calculate_average(math, english, science);
    
    | 获取等级
    grade = get_grade(average);
    
    | 输出结果
    System.print("学生姓名:", student_name);
    System.print("数学成绩:", math);
    System.print("英语成绩:", english);
    System.print("科学成绩:", science);
    System.print("平均分:", average);
    System.print("等级:", grade);
    
    | 判断是否优秀
    if (grade == "A") {
        System.print("恭喜！成绩优秀！");
    } else {
        System.print("继续努力！");
    }
}
```

## 运行程序

### 12. 如何运行Vanction程序
1. 将代码保存为 `.va` 文件（如：hello.va）
2. 在命令行中运行：
   ```bash
   python vanction.py hello.va
   ```

## 语言特性总结

### ✅ 支持的功能：
- ✅ 变量赋值和基本运算
- ✅ 函数定义和调用
- ✅ 条件语句 (if/else)
- ✅ 循环语句 (while)
- ✅ 比较运算符
- ✅ 字符串操作
- ✅ 递归函数
- ✅ 布尔值常量 (true/false)
- ✅ 多参数函数
- ✅ 嵌套函数调用

## 学习建议

1. **从简单开始**：先编写Hello World程序，逐步添加功能
2. **多用注释**：用注释解释代码逻辑
3. **测试每步**：每添加新功能就运行测试
4. **函数分解**：将复杂问题分解成小函数
5. **调试工具**：遇到问题时使用调试器

## 故障排除

### 常见问题：
1. **语法错误**：检查是否缺少分号 `;`
2. **变量未定义**：确保变量在使用前已赋值
3. **函数未找到**：检查函数名拼写和参数数量
4. **注释错误**：使用 `//` 而不是 `|`

### 错误示例：
```vanction
| 错误示例
func main() {
    | 错误：缺少分号
    System.print("Hello")
    
    | 错误：变量未定义
    System.print(undefined_var);
}
```

### 正确示例：
```vanction
| 正确示例
func main() {
    | 正确：有分号
    System.print("Hello");
    
    | 正确：先定义变量
    message = "Hello Vanction!";
    System.print(message);
}
```

本教程基于实际测试验证，所有示例代码都能正常运行。继续学习Vanction，享受编程的乐趣吧！