#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试新的random DNA"""

import sys
sys.path.insert(0, 'd:/工作日志/杂项/胡思乱想')
from genetic_evolution.vm import QuaternaryVM
from genetic_evolution.genome import Genome
from genetic_evolution.fitness import Environments

# 新的 DNA
dna = "0333301030200000" * 10 + "03333010"  # 168个数字

print(f"DNA长度: {len(dna)}")
print(f"DNA前40个: {dna[:40]}")
print()

# 创建基因组
genome = Genome(sequence=dna, generation=0)

# 执行
vm = QuaternaryVM()
result = vm.execute(genome)

print(f"执行结果:")
print(f"  成功: {result.success}")
print(f"  输出: {result.output}")
print(f"  步数: {result.steps}")
print()

# 计算适应度（目标值42）
fitness_func = Environments.target_number_fitness(target=42.0)
fitness = fitness_func(genome, vm)
print(f"适应度（目标42）: {fitness:.4f}")

# 分析
if result.output:
    output_val = result.output[-1]
    print(f"  输出值: {output_val}")
    print(f"  距离目标: {abs(42 - output_val)}")
