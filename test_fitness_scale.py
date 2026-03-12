#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试适应度缩放机制
验证为什么适应度能达到1039.97
"""

from quaternary_genetic_system import Environments, QuaternaryVM, Genome

# 创建虚拟机
vm = QuaternaryVM()

# 创建适应度函数
fitness_func = Environments.target_number_fitness(target=42.0)

# 测试不同输出值的适应度
# 16指令VM编码: 每个指令 = opcode(1位) + operand(1位)
# PUSH=0, OUTPUT=31, HALT=32
test_cases = [
    ("完美输出42", "0052" + "3100" + "3200", 42.0),      # PUSH 42, OUTPUT, HALT
    ("输出43", "0053" + "3100" + "3200", 43.0),          # PUSH 43, OUTPUT, HALT
    ("输出10", "0016" + "3100" + "3200", 10.0),          # PUSH 10 (0x0A), OUTPUT, HALT
    ("输出1", "0001" + "3100" + "3200", 1.0),            # PUSH 1, OUTPUT, HALT
    ("输出0", "0000" + "3100" + "3200", 0.0),            # PUSH 0, OUTPUT, HALT
    ("无输出", "3200", None),                            # HALT
]

print("=" * 70)
print("适应度缩放机制测试")
print("=" * 70)
print(f"目标值: 42.0")
print(f"适应度公式: fitness = 1.0 / (1.0 + |output - target|)")
print("=" * 70)

for name, dna, expected_output in test_cases:
    genome = Genome(dna)
    result = vm.execute(genome)
    
    # 计算适应度
    fitness = fitness_func(result)
    
    # 显示结果
    actual_output = result.output[0] if result.output else None
    error = abs(actual_output - 42.0) if actual_output is not None else float('inf')
    
    print(f"\n{name}:")
    print(f"  DNA: {dna}")
    print(f"  输出: {actual_output}")
    print(f"  误差: {error}")
    print(f"  适应度: {fitness:.6f}")
    print(f"  验证: {1.0 / (1.0 + error) if actual_output is not None else 0.0:.6f}")

print("\n" + "=" * 70)
print("结论:")
print("  如果适应度 > 1.0，可能的原因:")
print("  1. 多次测试用例累加")
print("  2. 多输出奖励")
print("  3. 效率/长度奖励")
print("  4. 自定义缩放因子")
print("=" * 70)
