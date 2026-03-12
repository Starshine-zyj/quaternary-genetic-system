#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试OUTPUT指令"""

import sys
sys.path.insert(0, 'd:/工作日志/杂项/胡思乱想')
from genetic_evolution.vm import QuaternaryVM
from genetic_evolution.genome import Genome

# 简单测试
dna = "0012" + "3010" + "3020"  # PUSH(2) → OUTPUT → HALT
print(f"测试DNA: {dna}")
print(f"指令: PUSH(2) -> OUTPUT -> HALT")
print()

genome = Genome(sequence=dna, generation=0)
vm = QuaternaryVM()
result = vm.execute(genome)

print(f"结果:")
print(f"  成功: {result.success}")
print(f"  输出: {result.output}")
print(f"  步数: {result.steps}")
print(f"  错误: {result.error}")
print()

# 测试random DNA的第一个循环
dna2 = "0333" + "3010" + "3020"  # PUSH(3) → OUTPUT → HALT
print(f"Random DNA第1个循环: {dna2}")
print(f"指令: PUSH(3) -> OUTPUT -> HALT")
print()

genome2 = Genome(sequence=dna2, generation=0)
result2 = vm.execute(genome2)

print(f"结果:")
print(f"  成功: {result2.success}")
print(f"  输出: {result2.output}")
print(f"  步数: {result2.steps}")
print(f"  错误: {result2.error}")
