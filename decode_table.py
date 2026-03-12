#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整解码测试：验证opcode计算
"""

print("=" * 70)
print("16指令VM完整解码表")
print("=" * 70)
print(f"{'四进制':<8} {'十进制':<6} {'opcode':<8} {'operand':<8} {'指令'}")
print("=" * 70)

# 所有可能的2位四进制组合 (00-33)
for high in range(4):
    for low in range(4):
        quad = f"{high}{low}"
        val = int(quad, 4)  # 转十进制
        opcode = val // 4 * 10
        operand = val % 4
        
        # 指令名称
        if opcode == 0:
            if operand == 0: name = "PUSH"
            elif operand == 1: name = "POP"
            elif operand == 2: name = "DUP"
            elif operand == 3: name = "SWAP"
            else: name = f"DATA_{operand}"
        elif opcode == 10:
            names = ["ADD", "SUB", "MUL", "DIV"]
            name = names[operand] if operand < len(names) else f"ARITH_{operand}"
        elif opcode == 20:
            names = ["JMP", "JZ", "JNZ", "CALL"]
            name = names[operand] if operand < len(names) else f"CTRL_{operand}"
        elif opcode == 30:
            names = ["INPUT", "OUTPUT", "NOP", "HALT"]
            name = names[operand] if operand < len(names) else f"SPEC_{operand}"
        else:
            name = "???"
        
        print(f"{quad:<8} {val:<6} {opcode:<8} {operand:<8} {name}")

print("=" * 70)
print("关键发现:")
print("  1. opcode = val // 4 * 10 只能生成: 0, 10, 20, 30")
print("  2. OUTPUT 应该是 opcode=30, operand=1 → 四进制 '31'")
print("  3. HALT 应该是 opcode=30, operand=3 → 四进制 '33'")
print("  4. 代码中 elif opcode == 31/32/33 永远不会触发！")
print("=" * 70)
