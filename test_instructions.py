#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试所有可能的操作码"""

# 导入VM
import sys
sys.path.insert(0, 'd:/工作日志/杂项/胡思乱想')
from genetic_evolution.vm import QuaternaryVM
from genetic_evolution.genome import Genome

vm = QuaternaryVM()

print("=== 指令表完整内容 ===")
for opcode in range(64):  # 四进制2位最大是 33(四进制) = 15(十进制)，但测试到64
    instruction = vm.INSTRUCTIONS.get(opcode, None)
    if instruction:
        # 计算对应的四进制
        q1 = opcode // 4
        q0 = opcode % 4
        print(f"{opcode:3d} (四进制{q1}{q0}) -> {instruction}")

print("\n=== 查找 OUTPUT 指令 ===")
for opcode, name in vm.INSTRUCTIONS.items():
    if name == 'OUTPUT':
        q1 = opcode // 4
        q0 = opcode % 4
        print(f"OUTPUT 的操作码 = {opcode} (十进制) = {q1}{q0} (四进制)")
