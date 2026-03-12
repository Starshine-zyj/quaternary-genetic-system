#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析演化实验的最佳DNA，看它如何达到1039.97适应度
"""

from quaternary_genetic_system import Genome, QuaternaryVM, Environments

# 从演化日志获取原始DNA
original_dna = "01332221313301323221221322221321332321321332221213333022130222032232032211131300"
print(f"原始DNA长度: {len(original_dna)} 碱基")

# 截取前120个（演化日志显示基因长度120）
# 实际基因程序= 60条指令（120碱基 / 2）
dna = original_dna[:120]
print(f"使用DNA: {dna}")
print(f"指令数量: {len(dna) // 2} 条")
print()

# 创建基因组和虚拟机
genome = Genome(dna)
vm = QuaternaryVM()

# 执行程序
result = vm.execute(genome)

print("=" * 70)
print("执行结果:")
print("=" * 70)
print(f"输出: {result.output}")
print(f"停机: {result.halted}")
print(f"步数: {result.steps}")
print(f"栈快照: {result.stack_snapshot}")
if result.error:
    print(f"错误: {result.error}")
print()

# 计算适应度（目标=42）
fitness_func = Environments.target_number_fitness(target=42.0)
fitness = fitness_func(result)

print("=" * 70)
print("适应度分析:")
print("=" * 70)
print(f"目标值: 42.0")
print(f"实际输出: {result.output[0] if result.output else 'None'}")
if result.output:
    error = abs(result.output[0] - 42.0)
    print(f"误差: {error}")
    print(f"理论适应度: {1.0 / (1.0 + error):.6f}")
print(f"实际适应度: {fitness:.6f}")
print()

# 检查是否有多输出
if len(result.output) > 1:
    print(f"[!] 多个输出: {result.output}")
    print("可能每个输出都计算了适应度并累加！")
    total = sum(1.0 / (1.0 + abs(val - 42.0)) for val in result.output)
    print(f"累加适应度: {total:.6f}")
print()

print("=" * 70)
print("结论:")
print("=" * 70)
if fitness < 1.0:
    print(f"[OK] 适应度 {fitness:.4f} < 1.0，符合单次评估")
    print(f"[?] 但演化日志显示 1039.97，说明有缩放因子或多次评估")
    print()
    print("可能的缩放机制:")
    print(f"  1. 适应度 x 1000 缩放因子 = {fitness * 1000:.4f}")
    print(f"  2. 多个测试用例累加")
    print(f"  3. 代数奖励: fitness + generation")
    print(f"  4. 效率奖励: fitness + 1000/steps")
else:
    print(f"[!] 适应度 {fitness:.4f} >= 1.0，说明有特殊机制")
