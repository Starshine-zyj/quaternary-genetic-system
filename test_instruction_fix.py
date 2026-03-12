#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试指令解码修复
验证 OUTPUT 和 HALT 指令是否能正常工作
"""

import sys
from quaternary_genetic_system import QuaternaryVM, Genome

def test_output_instruction():
    """测试OUTPUT指令"""
    print("=" * 60)
    print("测试 OUTPUT 指令")
    print("=" * 60)
    
    # 创建VM
    vm = QuaternaryVM()
    
    # 测试DNA: PUSH 2, PUSH 1, OUTPUT, OUTPUT, HALT
    # 02 = PUSH 2
    # 01 = PUSH 1
    # 31 = OUTPUT (opcode=30, operand=1)
    # 31 = OUTPUT
    # 33 = HALT (opcode=30, operand=3)
    dna = "0201313133"
    
    print(f"DNA: {dna}")
    print("指令序列:")
    print("  02 -> PUSH 2")
    print("  01 -> PUSH 1")
    print("  31 -> OUTPUT (opcode=30, operand=1)")
    print("  31 -> OUTPUT (opcode=30, operand=1)")
    print("  33 -> HALT (opcode=30, operand=3)")
    print()
    
    genome = Genome(dna)
    result = vm.execute(genome)
    
    print(f"执行结果:")
    print(f"  输出: {result.output}")
    print(f"  步数: {result.steps}")
    print(f"  停止: {result.halted}")
    print()
    
    # 预期输出: [1, 2] (后进先出)
    expected = [1, 2]
    if result.output == expected:
        print("[OK] OUTPUT 指令工作正常!")
        return True
    else:
        print(f"[FAIL] OUTPUT 指令失败! 预期 {expected}, 实际 {result.output}")
        return False


def test_halt_instruction():
    """测试HALT指令"""
    print("=" * 60)
    print("测试 HALT 指令")
    print("=" * 60)
    
    vm = QuaternaryVM()
    
    # 测试DNA: PUSH 1, OUTPUT, HALT, PUSH 2, OUTPUT
    # 01 = PUSH 1
    # 31 = OUTPUT
    # 33 = HALT (应该在这里停止)
    # 02 = PUSH 2 (不应该执行)
    # 31 = OUTPUT (不应该执行)
    dna = "0131330231"
    
    print(f"DNA: {dna}")
    print("指令序列:")
    print("  01 -> PUSH 1")
    print("  31 -> OUTPUT")
    print("  33 -> HALT (应该停止)")
    print("  02 -> PUSH 2 (不应执行)")
    print("  31 -> OUTPUT (不应执行)")
    print()
    
    genome = Genome(dna)
    result = vm.execute(genome)
    
    print(f"执行结果:")
    print(f"  输出: {result.output}")
    print(f"  步数: {result.steps}")
    print(f"  停止: {result.halted}")
    print()
    
    # 预期输出: [1] (HALT后的指令不应执行)
    expected = [1]
    if result.output == expected:
        print("[OK] HALT 指令工作正常!")
        return True
    else:
        print(f"[FAIL] HALT 指令失败! 预期 {expected}, 实际 {result.output}")
        return False


def test_target_number_fitness():
    """测试目标数值适应度计算"""
    print("=" * 60)
    print("测试目标数值适应度计算")
    print("=" * 60)
    
    from quaternary_genetic_system import Environments
    
    # 创建适应度函数 (目标值 = 42)
    fitness_func = Environments.target_number_fitness(target=42.0)
    
    # 测试不同输出的适应度
    test_cases = [
        ("输出 42", "02", [2.0], None),  # PUSH 2 (接近42的替代)
        ("输出 3", "03", [3.0], None),   # PUSH 3
        ("输出 0", "00", [0.0], None),   # PUSH 0
    ]
    
    print(f"目标值: 42.0")
    print()
    
    vm = QuaternaryVM()
    all_pass = True
    
    for name, push_code, expected_stack, _ in test_cases:
        # DNA: PUSH X, OUTPUT, HALT
        # 0X = PUSH X
        # 31 = OUTPUT
        # 33 = HALT
        dna = f"{push_code}3133"
        
        genome = Genome(dna)
        result = vm.execute(genome)
        
        # 计算适应度
        fitness = fitness_func(result)
        
        # 计算理论适应度
        if result.output:
            error = abs(result.output[0] - 42.0)
            theory_fitness = 1.0 / (1.0 + error)
        else:
            theory_fitness = 0.0
        
        print(f"{name}:")
        print(f"  DNA: {dna}")
        print(f"  输出: {result.output}")
        print(f"  适应度: {fitness:.6f} (理论: {theory_fitness:.6f})")
        
        # 验证适应度是否在合理范围
        if result.output and abs(fitness - theory_fitness) < 0.001:
            print(f"  [OK] 适应度正确")
        elif not result.output:
            print(f"  [OK] 无输出，适应度为0")
        else:
            print(f"  [FAIL] 适应度错误!")
            all_pass = False
        print()
    
    return all_pass


def test_fitness_upper_bound():
    """验证适应度上限"""
    print("=" * 60)
    print("验证适应度上限")
    print("=" * 60)
    
    from quaternary_genetic_system import Environments
    
    # 创建适应度函数 (目标值 = 2.0)
    fitness_func = Environments.target_number_fitness(target=2.0)
    
    # DNA: PUSH 2, OUTPUT, HALT
    # 02 = PUSH 2
    # 31 = OUTPUT
    # 33 = HALT
    dna = "023133"
    
    print(f"目标值: 2.0")
    print(f"DNA: {dna} (PUSH 2, OUTPUT, HALT)")
    print()
    
    genome = Genome(dna)
    vm = QuaternaryVM()
    result = vm.execute(genome)
    fitness = fitness_func(result)
    
    print(f"输出: {result.output}")
    print(f"适应度: {fitness:.10f}")
    print()
    
    # 验证是否达到理论上限 1.0
    if result.output and abs(fitness - 1.0) < 1e-9:
        print("[OK] 完美输出时适应度 = 1.0 (理论上限)")
        return True
    elif not result.output:
        print("[FAIL] 没有输出！OUTPUT指令可能失效")
        return False
    else:
        print(f"[FAIL] 适应度应该是 1.0, 实际是 {fitness:.10f}")
        return False


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "指令解码修复验证测试" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    results = []
    
    # 测试1: OUTPUT指令
    results.append(("OUTPUT指令", test_output_instruction()))
    print()
    
    # 测试2: HALT指令
    results.append(("HALT指令", test_halt_instruction()))
    print()
    
    # 测试3: 适应度计算
    results.append(("适应度计算", test_target_number_fitness()))
    print()
    
    # 测试4: 适应度上限
    results.append(("适应度上限", test_fitness_upper_bound()))
    print()
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print()
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] 所有测试通过! 指令解码BUG已修复!")
        sys.exit(0)
    else:
        print(f"\n[WARNING] {total - passed} 个测试失败")
        sys.exit(1)
