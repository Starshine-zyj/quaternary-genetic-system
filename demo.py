#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本：展示系统的各种功能
"""

import sys
import io

# 修复Windows控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from genetic_evolution import (
    EvolutionEngine, Environments, Genome, QuaternaryVM
)


def demo1_simple_evolution():
    """演示1：简单的数值演化"""
    print("\n" + "=" * 60)
    print("演示 1: 演化出能输出数值 42 的程序")
    print("=" * 60)
    
    engine = EvolutionEngine(
        population_size=50,
        genome_length=20,
        max_generations=100
    )
    
    fitness_func = Environments.target_number_fitness(42.0)
    
    print("\n开始演化...\n")
    best = engine.run(fitness_func, verbose=True)
    
    print("\n结果:")
    print(f"  最佳适应度: {best.fitness:.4f}")
    print(f"  基因序列: {best.sequence}")
    
    # 执行最佳程序
    vm = QuaternaryVM()
    result = vm.execute(best)
    print(f"  执行结果: {result}")
    
    return best


def demo2_sequence_generation():
    """演示2：序列生成"""
    print("\n" + "=" * 60)
    print("演示 2: 演化出能输出序列 [1,2,3,4,5] 的程序")
    print("=" * 60)
    
    engine = EvolutionEngine(
        population_size=100,
        genome_length=40,
        max_generations=200
    )
    
    target_seq = [1.0, 2.0, 3.0, 4.0, 5.0]
    fitness_func = Environments.sequence_generation_fitness(target_seq)
    
    print("\n开始演化...\n")
    
    gen_count = 0
    def callback(result):
        nonlocal gen_count
        gen_count = result['generation']
        if gen_count % 20 == 0:
            print(result['stats'])
        return True
    
    best = engine.run(fitness_func, verbose=False, callback=callback)
    
    print(f"\n经过 {gen_count} 代演化")
    print(f"  最佳适应度: {best.fitness:.4f}")
    
    # 执行并查看输出
    vm = QuaternaryVM()
    result = vm.execute(best)
    print(f"  程序输出: {result.output}")
    print(f"  目标序列: {target_seq}")
    
    return best


def demo3_arithmetic():
    """演示3：算术运算学习"""
    print("\n" + "=" * 60)
    print("演示 3: 学习计算两数之和")
    print("=" * 60)
    
    engine = EvolutionEngine(
        population_size=100,
        genome_length=40,
        max_generations=300
    )
    
    fitness_func = Environments.arithmetic_fitness()
    
    print("\n开始演化...\n")
    print("测试用例:")
    print("  1 + 2 = 3")
    print("  5 + 7 = 12")
    print("  10 + 20 = 30")
    print("  3 + 4 = 7")
    print()
    
    best = engine.run(fitness_func, verbose=True)
    
    print("\n验证最佳程序:")
    vm = QuaternaryVM()
    
    test_cases = [
        ([1.0, 2.0], 3.0),
        ([5.0, 7.0], 12.0),
        ([10.0, 20.0], 30.0),
    ]
    
    for inputs, expected in test_cases:
        result = vm.execute(best, inputs=inputs)
        if result.success and result.output:
            output = result.output[-1]
            error = abs(expected - output)
            status = "✓" if error < 0.1 else "✗"
            print(f"  {status} {inputs[0]} + {inputs[1]} = {output:.2f} (期望: {expected})")
        else:
            print(f"  ✗ {inputs[0]} + {inputs[1]} = 执行失败")
    
    return best


def demo4_custom_fitness():
    """演示4：自定义适应度函数"""
    print("\n" + "=" * 60)
    print("演示 4: 自定义适应度函数 - 演化出高效程序")
    print("=" * 60)
    
    def custom_fitness(genome, vm):
        """自定义：奖励能产生多个输出且执行效率高的程序"""
        result = vm.execute(genome, inputs=[1.0, 2.0, 3.0])
        
        if not result.success:
            return 0.0
        
        score = 0.0
        
        # 奖励输出数量
        score += len(result.output) * 50
        
        # 奖励执行效率（步数少）
        if result.steps < 5000:
            score += (5000 - result.steps) / 10
        
        # 奖励输出值多样性
        if len(result.output) > 1:
            diversity = len(set(result.output))
            score += diversity * 20
        
        return score
    
    engine = EvolutionEngine(
        population_size=80,
        genome_length=30,
        max_generations=150
    )
    
    print("\n适应度评分标准:")
    print("  - 每个输出: +50分")
    print("  - 执行效率: 最高+500分")
    print("  - 输出多样性: 每个不同值+20分")
    print()
    
    best = engine.run(custom_fitness, verbose=True)
    
    print("\n最佳程序分析:")
    vm = QuaternaryVM()
    result = vm.execute(best, inputs=[1.0, 2.0, 3.0])
    
    print(f"  输出数量: {len(result.output)}")
    print(f"  输出值: {result.output}")
    print(f"  执行步数: {result.steps}")
    print(f"  输出多样性: {len(set(result.output))} 种不同值")
    
    return best


def demo5_genome_analysis():
    """演示5：基因组分析"""
    print("\n" + "=" * 60)
    print("演示 5: 基因组详细分析")
    print("=" * 60)
    
    # 创建一个简单的基因组
    genome = Genome(sequence="0105310032000000")
    
    print(f"\n基因序列: {genome.sequence}")
    print(f"长度: {len(genome.sequence)} 个碱基")
    
    # 解析指令
    print("\n指令解析:")
    seq = genome.sequence
    instruction_count = 0
    
    for i in range(0, len(seq), 4):
        if i + 3 < len(seq):
            opcode = int(seq[i:i+2], 4)
            operand = int(seq[i+2:i+4], 4)
            
            instruction_name = QuaternaryVM.INSTRUCTIONS.get(opcode, "UNKNOWN")
            print(f"  指令 {instruction_count}: {seq[i:i+4]} -> "
                  f"{instruction_name}(操作码:{opcode}, 操作数:{operand})")
            instruction_count += 1
    
    # 执行程序
    print("\n执行结果:")
    vm = QuaternaryVM()
    result = vm.execute(genome)
    print(f"  {result}")
    
    # 字节转换
    print("\n字节表示:")
    byte_data = genome.to_bytes()
    print(f"  {' '.join(f'{b:02X}' for b in byte_data)}")
    
    # 恢复测试
    restored = Genome.from_bytes(byte_data)
    print(f"  恢复后: {restored.sequence}")
    print(f"  一致性: {'✓' if restored.sequence == genome.sequence else '✗'}")


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "四进制基因编程演化系统 - 功能演示" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝")
    
    demos = [
        ("简单数值演化", demo1_simple_evolution),
        ("序列生成演化", demo2_sequence_generation),
        ("算术运算学习", demo3_arithmetic),
        ("自定义适应度", demo4_custom_fitness),
        ("基因组分析", demo5_genome_analysis),
    ]
    
    print("\n可用演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. 全部运行")
    print()
    
    try:
        choice = input("请选择演示 (0-5): ").strip()
        
        if choice == '0':
            # 运行所有演示
            for name, demo_func in demos:
                try:
                    demo_func()
                    input("\n按回车继续...")
                except KeyboardInterrupt:
                    print("\n\n演示中断")
                    break
        elif choice in ['1', '2', '3', '4', '5']:
            idx = int(choice) - 1
            name, demo_func = demos[idx]
            demo_func()
        else:
            print("无效选择")
            return
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n演示中断")
    except Exception as e:
        print(f"\n错误: {e}")


if __name__ == '__main__':
    main()
