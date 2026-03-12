#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析指令差异"""

# 分析 0012
print("=== 分析 0012 ===")
opcode1 = int("001", 4)
operand1 = int("2", 4)
print(f"操作码: int('001', 4) = {opcode1}")
print(f"操作数: int('2', 4) = {operand1}")
print(f"指令: PUSH({operand1})")
print()

# 分析 0333
print("=== 分析 0333 ===")
opcode2 = int("033", 4)
operand2 = int("3", 4)
print(f"操作码: int('033', 4) = {opcode2}")
print(f"操作数: int('3', 4) = {operand2}")
print(f"指令: ???({operand2})")
print()

# 检查操作码15
import sys
sys.path.insert(0, 'd:/工作日志/杂项/胡思乱想')
from genetic_evolution.vm import QuaternaryVM

vm = QuaternaryVM()
print(f"操作码 {opcode2} 对应指令: {vm.INSTRUCTIONS.get(opcode2, 'UNKNOWN')}")
