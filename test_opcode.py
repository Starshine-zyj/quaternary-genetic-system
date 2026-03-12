#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试指令编码"""

print("=== 指令编码测试 ===")
print(f"0x31 (Python十六进制) = {0x31}")
print(f"int('31', 4) (四进制) = {int('31', 4)}")
print()

# 测试指令表
INSTRUCTIONS = {
    0x00: 'NOP',
    0x01: 'PUSH',
    0x31: 'OUTPUT',
    0x32: 'HALT',
}

print("=== 指令表内容 ===")
for key, value in sorted(INSTRUCTIONS.items()):
    print(f"{key:3d} (0x{key:02x}) -> {value}")
print()

# 测试四进制解码
test_seq = "0131"
opcode = int(test_seq[0:2], 4)
operand = int(test_seq[2:4], 4)
print(f"=== 解码 '{test_seq}' ===")
print(f"opcode = int('{test_seq[0:2]}', 4) = {opcode}")
print(f"operand = int('{test_seq[2:4]}', 4) = {operand}")
print(f"指令 = {INSTRUCTIONS.get(opcode, 'UNKNOWN')}")
