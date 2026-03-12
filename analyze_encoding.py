#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
计算 16指令VM 的正确编码
"""

def encode_instruction(opcode_class, operand):
    """
    将指令编码为四进制
    opcode_class: 0=数据操作, 1=算术运算, 2=控制流, 3=特殊操作
    operand: 0-3
    """
    decimal = opcode_class * 4 + operand
    high = decimal // 4
    low = decimal % 4
    return f"{high}{low}"

print("=== 16指令VM编码规则 ===")
print("每2位四进制 → 十进制 → opcode (// 4 * 10), operand (% 4)")
print()

# 测试编码
print("PUSH 42:")
print(f"  opcode=0 (PUSH), operand=42")
print(f"  问题: operand只能是0-3！")
print(f"  解决: 用多条PUSH指令或改用栈操作")
print()

print("示例编码:")
instructions = [
    (("PUSH", 2), "00", 2),
    (("OUTPUT", 0), "31", 0),
    (("HALT", 0), "32", 0),
]

for (name, op), code, decimal in instructions:
    val = int(code, 4)
    opcode = val // 4 * 10
    operand = val % 4
    print(f"  {code} (四进制) → {val:2d} (十进制) → opcode={opcode:2d}, operand={operand} ({name})")

print()
print("问题分析: 16指令VM的PUSH只能压入0-3！")
print("要输出42需要:")
print("  1) 多条指令计算: PUSH_3 DUP MUL DUP MUL DUP ADD ...")
print("  2) 或者VM内部有常量池")
