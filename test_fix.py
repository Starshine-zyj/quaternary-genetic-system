#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修复后的指令解码"""

import sys
sys.path.insert(0, 'd:/工作日志/杂项/胡思乱想')
from genetic_evolution.vm import QuaternaryVM
from genetic_evolution.genome import Genome

print("=== 测试3位操作码解码 ===\n")

# 测试案例
tests = [
    ("0010", "PUSH(0)"),
    ("0011", "PUSH(1)"),
    ("0012", "PUSH(2)"),
    ("0013", "PUSH(3)"),
    ("3010", "OUTPUT(0)"),
    ("3011", "OUTPUT(1)"),
    ("3020", "HALT(0)"),
]

vm = QuaternaryVM()

for dna, expected in tests:
    # 解码
    opcode = int(dna[0:3], 4)
    operand = int(dna[3:4], 4)
    instruction = vm.INSTRUCTIONS.get(opcode, 'UNKNOWN')
    
    result = f"{instruction}({operand})"
    status = "[OK]" if result == expected else "[FAIL]"
    
    print(f"{status} DNA '{dna}' -> opcode={opcode:2d} -> {result} (expected: {expected})")

print("\n=== 测试完整程序执行 ===\n")

# 测试程序：PUSH(2) → OUTPUT → HALT
test_program = "0012" + "3010" + "3020"
print(f"程序DNA: {test_program}")
print(f"指令: PUSH(2) → OUTPUT → HALT")
print()

genome = Genome(sequence=test_program, generation=0)
result = vm.execute(genome)

print(f"执行结果:")
print(f"  成功: {result.success}")
print(f"  输出: {result.output}")
print(f"  步数: {result.steps}")
