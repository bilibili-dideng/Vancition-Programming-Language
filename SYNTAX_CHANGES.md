# Vanction语言语法变更说明

## 重要更新：else-if语法变更

### 变更时间
2024年版本更新

### 变更内容

#### ✅ 新的推荐语法（使用连字符）
```vanction
func check_score(score) {
    if (score >= 90) {
        return "A";
    } else-if (score >= 80) {
        return "B";
    } else-if (score >= 70) {
        return "C";
    } else-if (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}
```

#### ❌ 已禁用的旧语法（使用空格）
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

### 变更原因

1. **语法一致性**：使用`else-if`连字符形式使语法更加清晰统一
2. **避免歧义**：消除`else`和`if`作为独立标记可能产生的解析歧义
3. **语言特色**：形成Vanction语言独特的语法风格

### 向后兼容性

- **不兼容**：旧的`else if`语法已被完全禁用
- **错误提示**：使用旧语法会收到明确的错误信息：
  ```
  Syntax Error: left brace ({) expected, found 'if'
  ```

### 迁移指南

#### 自动迁移步骤

1. **查找旧语法**：搜索代码中的`else if`（空格分隔）
2. **替换为新语法**：将`else if`替换为`else-if`
3. **测试验证**：运行程序确保逻辑正确

#### 示例迁移

**迁移前（旧语法）：**
```vanction
if (condition1) {
    | 代码块1
} else if (condition2) {
    | 代码块2
} else if (condition3) {
    | 代码块3
} else {
    | 默认代码块
}
```

**迁移后（新语法）：**
```vanction
if (condition1) {
    | 代码块1
} else-if (condition2) {
    | 代码块2
} else-if (condition3) {
    | 代码块3
} else {
    | 默认代码块
}
```

### 新增功能

#### 支持多个连续else-if
新的语法支持任意数量的连续`else-if`语句：

```vanction
func categorize_number(num) {
    if (num < 0) {
        return "负数";
    } else-if (num == 0) {
        return "零";
    } else-if (num <= 10) {
        return "小正数";
    } else-if (num <= 100) {
        return "中等正数";
    } else-if (num <= 1000) {
        return "大正数";
    } else {
        return "巨大正数";
    }
}
```

### 测试验证

#### 测试文件
- `simple_else_if_logic.va` - 基础else-if逻辑测试
- `test_else_if_only.va` - else-if语法验证
- `final_else_if_demo.va` - 完整功能演示

#### 运行测试
```bash
python vanction.py simple_else_if_logic.va
```

### 常见问题

#### Q: 为什么要做这个变更？
A: 为了提高语法的一致性和清晰度，避免解析歧义，形成Vanction语言独特的风格。

#### Q: 旧的代码怎么办？
A: 需要手动将`else if`替换为`else-if`，这是一个简单的查找替换操作。

#### Q: 还会有其他类似的语法变更吗？
A: 未来可能会根据语言发展需要进行调整，但会确保提供清晰的迁移路径。

### 总结

这次语法变更使Vanction语言的条件语句更加清晰和一致。虽然需要修改现有代码，但迁移过程简单直接，新版本提供了更强大的功能和更好的语法体验。