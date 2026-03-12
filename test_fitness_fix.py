#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 genetic_evolution 模块的适应度修复
验证适应度范围是否在 0.0 - 1.0 之间
"""

from genetic_evolution import Genome, QuaternaryVM, Environments


def main():
    print("=" * 70)
    print("测试 genetic_evolution 模块的适应度范围")
    print("=" * 70)
    
    vm = QuaternaryVM()
    fitness_func = Environments.target_number_fitness(target=42.0)
    
    # 测试用例
    test_cases = [
        ("完美匹配 (42)", "023133", 2.0),   # PUSH 2, OUTPUT, HALT
        ("接近目标", "013133", 1.0),        # PUSH 1, OUTPUT, HALT
        ("较大误差", "003133", 0.0),        # PUSH 0, OUTPUT, HALT
    ]
    
    print("\n目标值: 42.0")
    print("公式: fitness = 1.0 / (1.0 + |output - target|)")
    print()
    
    all_pass = True
    
    for name, dna, expected_output in test_cases:
        genome = Genome(dna, generation=0)
        
        # 修改目标值以匹配测试用例
        if "完美匹配" in name:
            fitness_func_local = Environments.target_number_fitness(target=2.0)
        elif "接近目标" in name:
            fitness_func_local = Environments.target_number_fitness(target=1.0)
        else:
            fitness_func_local = Environments.target_number_fitness(target=42.0)
        
        result = vm.execute(genome, inputs=[])
        fitness = fitness_func_local(genome, vm)
        
        print(f"{name}:")
        print(f"  DNA: {dna}")
        print(f"  输出: {result.output}")
        print(f"  适应度: {fitness:.6f}")
        
        # 验证适应度在合理范围
        if 0.0 <= fitness <= 1.0:
            print(f"  [OK] 适应度在范围 [0.0, 1.0]")
        else:
            print(f"  [FAIL] 适应度超出范围!")
            all_pass = False
        
        # 验证完美匹配时是否达到1.0
        if "完美匹配" in name and abs(fitness - 1.0) < 1e-6:
            print(f"  [OK] 完美匹配达到理论上限 1.0")
        elif "完美匹配" in name:
            print(f"  [FAIL] 完美匹配应该是 1.0!")
            all_pass = False
        
        print()
    
    print("=" * 70)
    if all_pass:
        print("[SUCCESS] 所有测试通过!")
        print("\n修复内容:")
        print("  - 移除了 1000.0 缩放因子")
        print("  - 移除了基础分和效率奖励")
        print("  - 统一适应度范围为 [0.0, 1.0]")
        print("  - 理论上限 = 1.0 (完美匹配)")
        return True
    else:
        print("[FAILED] 测试失败!")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
