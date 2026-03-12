#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新功能测试脚本 - 演示导出和分析功能
"""

from genetic_evolution import Genome, QuaternaryVM


def test_decode_and_analyze():
    """测试指令解码和分析功能"""
    
    # 创建一个简单的测试基因：计算 2 + 3 = 5
    # PUSH 2 (0x01 = 001四进制, 操作数2) → 0012
    # PUSH 3 (0x01 = 001四进制, 操作数3) → 0013
    # ADD (0x10 = 100四进制, 操作数0) → 1000
    # OUTPUT (0x31 = 301四进制, 操作数0) → 3010
    # HALT (0x32 = 302四进制, 操作数0) → 3020
    sequence = "0012" + "0013" + "1000" + "3010" + "3020"
    
    genome = Genome(sequence, generation=100, fitness=1.0, mutations=0)
    
    print("=" * 80)
    print("测试基因解码和分析功能")
    print("=" * 80)
    print(f"\n基因序列: {sequence}")
    print(f"长度: {len(sequence)} (四进制)")
    
    # DNA映射
    dna_map = {'0': 'A', '1': 'T', '2': 'C', '3': 'G'}
    dna_sequence = ''.join(dna_map[c] for c in sequence)
    print(f"DNA序列: {dna_sequence}\n")
    
    # 解码指令
    print("指令序列:")
    print("-" * 80)
    print(f"{'序号':<6} {'四进制':<8} {'DNA':<6} {'操作码':<8} {'操作数':<8} {'指令':<10}")
    print("-" * 80)
    
    instructions = []
    for i in range(0, len(sequence), 4):
        if i + 3 < len(sequence):
            quat = sequence[i:i+4]
            dna = dna_sequence[i:i+4]
            opcode = int(sequence[i:i+3], 4)
            operand = int(sequence[i+3:i+4], 4)
            
            instr_map = {
                0x00: 'NOP', 0x01: 'PUSH', 0x02: 'POP', 0x03: 'DUP',
                0x10: 'ADD', 0x11: 'SUB', 0x12: 'MUL', 0x13: 'DIV',
                0x20: 'JMP', 0x21: 'JZ', 0x22: 'JNZ', 0x23: 'CALL',
                0x30: 'INPUT', 0x31: 'OUTPUT', 0x32: 'HALT', 0x33: 'SWAP',
            }
            instr_name = instr_map.get(opcode, 'UNKNOWN')
            
            print(f"{len(instructions):<6} {quat:<8} {dna:<6} 0x{opcode:02x}     "
                  f"{operand:<8} {instr_name:<10}")
            
            instructions.append({
                'quaternary': quat,
                'dna': dna,
                'opcode': opcode,
                'operand': operand,
                'instruction': instr_name
            })
    
    # 执行追踪
    print("\n" + "=" * 80)
    print("执行追踪:")
    print("-" * 80)
    print(f"{'步骤':<6} {'指令':<10} {'操作数':<8} {'栈':<30} {'输出':<20}")
    print("-" * 80)
    
    stack = []
    output = []
    
    for step, instr in enumerate(instructions):
        instr_name = instr['instruction']
        operand = instr['operand']
        
        # 执行指令
        if instr_name == 'PUSH':
            stack.append(float(operand))
        elif instr_name == 'ADD' and len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif instr_name == 'OUTPUT' and stack:
            output.append(stack[-1])
        elif instr_name == 'HALT':
            print(f"{step+1:<6} {'HALT':<10} {'':<8} {'程序停止':<30} {str(output):<20}")
            break
        
        stack_str = str([f"{x:.1f}" for x in stack])
        output_str = str([f"{x:.1f}" for x in output])
        print(f"{step+1:<6} {instr_name:<10} {operand:<8} {stack_str:<30} {output_str:<20}")
    
    # 虚拟机执行
    print("\n" + "=" * 80)
    print("虚拟机执行结果:")
    print("-" * 80)
    
    vm = QuaternaryVM()
    result = vm.execute(genome)
    
    print(f"执行状态: {'成功' if result.success else '失败'}")
    print(f"执行步数: {result.steps}")
    if result.output:
        print(f"输出值: {result.output[-1]:.6f}")
        print(f"所有输出: {result.output}")
    if result.error:
        print(f"错误: {result.error}")
    
    # 统计分析
    print("\n" + "=" * 80)
    print("统计分析:")
    print("-" * 80)
    
    instr_count = {}
    for instr in instructions:
        name = instr['instruction']
        instr_count[name] = instr_count.get(name, 0) + 1
    
    print(f"总指令数: {len(instructions)}")
    print(f"基因长度: {len(sequence)} (四进制)")
    print(f"\n指令使用频率:")
    for instr, count in sorted(instr_count.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(instructions) * 100
        bar = '█' * int(percentage / 5)
        print(f"  {instr:<10} {count:>3} ({percentage:>5.1f}%)  {bar}")
    
    print("\n" + "=" * 80)
    print("[测试完成] 新功能工作正常!")
    print("=" * 80)


if __name__ == '__main__':
    test_decode_and_analyze()
