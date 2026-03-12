#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试：输出42的DNA
"""

from quaternary_genetic_system import Genome, QuaternaryVM, Environments

# 构造一个输出42的简单程序
# 16指令VM: PUSH只能压0-3，需要计算
# 42 = 3 * 14 = 3 * (3 * 4 + 2) = 3 * 3 * 4 + 3 * 2
# 42 = 3 * 3 * 3 + 3 * 3 * 3 + 3 * 3

# 简化: 先试试能输出什么
dna_tests = [
    ("PUSH 3", "0003" + "3100" + "3200"),  # PUSH 3, OUTPUT, HALT
    ("PUSH 2", "0002" + "3100" + "3200"),  # PUSH 2, OUTPUT, HALT
    ("3*3=9", "0003" + "0200" + "1200" + "3100" + "3200"),  # PUSH 3, DUP, MUL, OUTPUT, HALT
]

print("=" * 70)
print("测试不同DNA的输出")
print("=" * 70)

fitness_func = Environments.target_number_fitness(target=42.0)

for name, dna in dna_tests:
    genome = Genome(dna)
    vm = QuaternaryVM()
    result = vm.execute(genome)
    
    if result.output:
        output = result.output[0]
        error = abs(output - 42.0)
        fitness = fitness_func(result)
        
        print(f"\n{name}:")
        print(f"  DNA: {dna}")
        print(f"  输出: {output}")
        print(f"  误差: {error}")
        print(f"  适应度: {fitness:.6f}")
    else:
        print(f"\n{name}: 无输出")
        print(f"  DNA: {dna}")
        print(f"  错误: {result.error}")

print("\n" + "=" * 70)
print("分析: 如果适应度公式真的是 1/(1+error)")
print("  那么适应度永远 < 1.0")
print("  实验中的 1039.97 无法用这个公式解释！")
print("=" * 70)
