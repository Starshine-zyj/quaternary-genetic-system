#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试改进的虚拟机 - 查看指令解码"""

import sys
sys.path.insert(0, '.')

from genetic_evolution.improved_vm import ImprovedQuaternaryVM
from genetic_evolution.genome import Genome

vm = ImprovedQuaternaryVM()

# 测试DNA: 110002310001101
dna = "110002310001101"
print(f"DNA: {dna}")
print(f"Length: {len(dna)}")

genome = Genome.from_dna(dna, generation=0)
print(f"Genome sequence: {genome.sequence}")
print(f"Sequence length: {len(genome.sequence)}")

instructions = vm.decode_instructions(genome)
print(f"\nDecoded instructions ({len(instructions)} total):")
for i, opcode in enumerate(instructions):
    instr_name = vm.INSTRUCTIONS.get(opcode, 'UNKNOWN')
    # 转换为八进制显示（便于对照）
    oct_str = oct(opcode)
    print(f"  [{i}] {genome.sequence[i*3:(i+1)*3]} -> opcode={opcode:3d} ({oct_str}) -> {instr_name}")

print("\n" + "="*60)
print("Executing...")
result = vm.execute(genome)
print(f"Output: {result['output']}")
print(f"Stack: {result['stack']}")
print(f"Steps: {result['steps']}")
print(f"Halted: {result['halted']}")
print(f"Error: {result['error']}")
