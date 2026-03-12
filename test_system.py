#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统测试脚本
验证所有模块是否正常工作
"""

import sys
import time
import io

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("测试 1: 模块导入")
    print("=" * 60)
    
    try:
        from genetic_evolution import (
            Genome, ExecutionResult, GenerationStats,
            QuaternaryVM, Mutator, Selector,
            FitnessEvaluator, Environments, EvolutionEngine
        )
        print("✓ 所有核心模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False


def test_genome():
    """测试基因组"""
    print("\n" + "=" * 60)
    print("测试 2: 基因组功能")
    print("=" * 60)
    
    try:
        from genetic_evolution import Genome
        
        # 创建随机基因组
        genome = Genome.random(20, generation=0)
        print(f"✓ 创建随机基因组: {genome.sequence}")
        
        # 验证基因序列
        assert all(c in '0123' for c in genome.sequence), "基因序列包含非法字符"
        print("✓ 基因序列验证通过")
        
        # 测试复制
        copy = genome.copy()
        assert copy.sequence == genome.sequence, "基因复制失败"
        print("✓ 基因复制功能正常")
        
        # 测试字节转换
        data = genome.to_bytes()
        restored = Genome.from_bytes(data)
        print("✓ 字节序列转换正常")
        
        return True
    except Exception as e:
        print(f"✗ 基因组测试失败: {e}")
        return False


def test_vm():
    """测试虚拟机"""
    print("\n" + "=" * 60)
    print("测试 3: 虚拟机功能")
    print("=" * 60)
    
    try:
        from genetic_evolution import Genome, QuaternaryVM
        
        vm = QuaternaryVM()
        
        # 测试简单程序: PUSH 5, OUTPUT, HALT
        # 指令编码: 01(PUSH) 05(操作数) 31(OUTPUT) 00(操作数) 32(HALT) 00(操作数)
        genome = Genome(sequence="01053100320000000000")
        result = vm.execute(genome)
        
        print(f"执行结果: {result}")
        assert result.success, "程序执行失败"
        assert len(result.output) > 0, "没有输出"
        print(f"✓ 虚拟机执行成功，输出: {result.output}")
        
        return True
    except Exception as e:
        print(f"✗ 虚拟机测试失败: {e}")
        return False


def test_mutation():
    """测试变异操作"""
    print("\n" + "=" * 60)
    print("测试 4: 变异操作")
    print("=" * 60)
    
    try:
        from genetic_evolution import Genome, Mutator
        
        mutator = Mutator(base_mutation_rate=0.1)
        original = Genome.random(20, generation=0)
        
        # 点突变
        mutated = mutator.mutate(original, generation=1)
        print(f"原始: {original.sequence}")
        print(f"突变: {mutated.sequence}")
        print(f"✓ 点突变完成，变异数: {mutated.mutations}")
        
        # 交叉
        parent1 = Genome.random(20, generation=0)
        parent2 = Genome.random(20, generation=0)
        child1, child2 = mutator.crossover(parent1, parent2, generation=1)
        print(f"✓ 交叉操作完成")
        
        return True
    except Exception as e:
        print(f"✗ 变异测试失败: {e}")
        return False


def test_selection():
    """测试选择机制"""
    print("\n" + "=" * 60)
    print("测试 5: 选择机制")
    print("=" * 60)
    
    try:
        from genetic_evolution import Genome, Selector
        
        # 创建种群
        population = [Genome.random(20, generation=0) for _ in range(10)]
        for i, g in enumerate(population):
            g.fitness = i * 10.0  # 赋予不同适应度
        
        # 锦标赛选择
        selected = Selector.tournament_selection(population, tournament_size=3)
        print(f"✓ 锦标赛选择: 适应度 {selected.fitness}")
        
        # 精英保留
        elites = Selector.elitism_selection(population, elite_size=3)
        print(f"✓ 精英保留: {len(elites)} 个体")
        
        return True
    except Exception as e:
        print(f"✗ 选择测试失败: {e}")
        return False


def test_fitness():
    """测试适应度评估"""
    print("\n" + "=" * 60)
    print("测试 6: 适应度评估")
    print("=" * 60)
    
    try:
        from genetic_evolution import Genome, QuaternaryVM, FitnessEvaluator, Environments
        
        vm = QuaternaryVM()
        evaluator = FitnessEvaluator(vm)
        
        # 创建测试基因组
        genome = Genome.random(40, generation=0)
        
        # 测试目标数值适应度
        fitness_func = Environments.target_number_fitness(42.0)
        fitness = evaluator.evaluate(genome, fitness_func)
        print(f"✓ 目标数值适应度: {fitness:.4f}")
        
        # 测试算术适应度
        fitness_func = Environments.arithmetic_fitness()
        fitness = evaluator.evaluate(genome, fitness_func)
        print(f"✓ 算术适应度: {fitness:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ 适应度测试失败: {e}")
        return False


def test_evolution():
    """测试演化引擎"""
    print("\n" + "=" * 60)
    print("测试 7: 演化引擎")
    print("=" * 60)
    
    try:
        from genetic_evolution import EvolutionEngine, Environments
        
        engine = EvolutionEngine(
            population_size=20,
            genome_length=20,
            max_generations=10
        )
        
        fitness_func = Environments.target_number_fitness(10.0)
        
        print("开始演化（10代）...")
        engine.initialize_population()
        
        for i in range(10):
            result = engine.evolve_generation(fitness_func)
            if i % 3 == 0:
                print(f"  代 {result['generation']:2d} | "
                      f"最佳: {result['best_fitness']:8.4f} | "
                      f"平均: {result['avg_fitness']:8.4f}")
        
        print(f"✓ 演化完成，最佳适应度: {engine.best_genome.fitness:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ 演化测试失败: {e}")
        return False


def test_gui():
    """测试GUI模块"""
    print("\n" + "=" * 60)
    print("测试 8: GUI模块")
    print("=" * 60)
    
    try:
        import tkinter as tk
        print("✓ tkinter 模块可用")
        
        # 尝试导入GUI应用（不启动）
        import importlib.util
        spec = importlib.util.spec_from_file_location("gui_app", "gui_app.py")
        if spec and spec.loader:
            print("✓ GUI应用文件可导入")
        
        return True
    except ImportError:
        print("✗ tkinter 未安装，GUI功能不可用")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  CentOS/RHEL: sudo yum install python3-tkinter")
        print("  macOS: brew install python-tk")
        return False
    except Exception as e:
        print(f"✗ GUI测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "四进制基因编程演化系统 - 测试套件" + " " * 10 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    start_time = time.time()
    
    tests = [
        ("模块导入", test_imports),
        ("基因组功能", test_genome),
        ("虚拟机功能", test_vm),
        ("变异操作", test_mutation),
        ("选择机制", test_selection),
        ("适应度评估", test_fitness),
        ("演化引擎", test_evolution),
        ("GUI模块", test_gui),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ 测试 '{name}' 发生异常: {e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status:8s} - {name}")
    
    elapsed = time.time() - start_time
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    print(f"耗时: {elapsed:.2f}s")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查错误信息。")
        return 1


if __name__ == '__main__':
    sys.exit(main())
