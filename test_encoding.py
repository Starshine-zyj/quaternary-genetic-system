#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试编码/解码
opcode = 49

# 按代码的方式"编码"
q1 = opcode // 4
q0 = opcode % 4
encoded = f"{q1}{q0}"
print(f"编码 49 → '{encoded}'")

# 按代码的方式"解码"
decoded = int(encoded, 4)
print(f"解码 '{encoded}' (四进制) → {decoded}")

# 正确的四进制
real_q = []
n = opcode
while n > 0:
    real_q.insert(0, str(n % 4))
    n //= 4
real_quaternary = ''.join(real_q)
print(f"\n正确的四进制：49 = {real_quaternary}")
print(f"解码回来：int('{real_quaternary}', 4) = {int(real_quaternary, 4)}")
