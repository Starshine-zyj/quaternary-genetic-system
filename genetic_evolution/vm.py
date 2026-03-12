#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四进制虚拟机模块
执行基因组编码的程序
"""

import time
from typing import List, Optional
from .genome import Genome, ExecutionResult


class QuaternaryVM:
    """四进制虚拟机"""
    
    # 指令集定义（三碱基密码子：操作码2位 + 操作数2位）
    INSTRUCTIONS = {
        # 数据操作 (0x)
        0x00: 'NOP',      # 空操作
        0x01: 'PUSH',     # 将操作数压栈
        0x02: 'POP',      # 弹出栈顶
        0x03: 'DUP',      # 复制栈顶
        
        # 算术运算 (1x)
        0x10: 'ADD',      # 加法
        0x11: 'SUB',      # 减法
        0x12: 'MUL',      # 乘法
        0x13: 'DIV',      # 除法（安全除法，除0返回0）
        
        # 控制流 (2x)
        0x20: 'JMP',      # 无条件跳转
        0x21: 'JZ',       # 零跳转
        0x22: 'JNZ',      # 非零跳转
        0x23: 'CALL',     # 函数调用
        
        # 特殊操作 (3x)
        0x30: 'INPUT',    # 读取输入
        0x31: 'OUTPUT',   # 输出栈顶值
        0x32: 'HALT',     # 停机
        0x33: 'SWAP',     # 交换栈顶两个元素
    }
    
    def __init__(self, max_steps: int = 10000, max_stack_depth: int = 1000, 
                 timeout: float = 1.0):
        self.max_steps = max_steps
        self.max_stack_depth = max_stack_depth
        self.timeout = timeout
        
    def execute(self, genome: Genome, inputs: Optional[List[float]] = None) -> ExecutionResult:
        """执行基因组程序"""
        stack = []
        output = []
        input_ptr = 0
        pc = 0  # 程序计数器
        steps = 0
        start_time = time.time()
        
        if inputs is None:
            inputs = []
        
        # 解码指令序列（每4个四进制数字为一条指令：3位操作码 + 1位操作数）
        instructions = []
        seq = genome.sequence
        for i in range(0, len(seq), 4):
            if i + 3 < len(seq):
                # 3位操作码 (支持0-63的指令) + 1位操作数 (0-3)
                opcode = int(seq[i:i+3], 4)
                operand = int(seq[i+3:i+4], 4)
                instructions.append((opcode, operand))
        
        if not instructions:
            return ExecutionResult(success=False, output=[], steps=0, 
                                 error="空指令序列")
        
        try:
            while pc < len(instructions):
                # 检查执行限制
                if steps >= self.max_steps:
                    return ExecutionResult(success=False, output=output, steps=steps,
                                         error=f"超过最大执行步数 {self.max_steps}")
                
                if time.time() - start_time > self.timeout:
                    return ExecutionResult(success=False, output=output, steps=steps,
                                         error=f"执行超时 {self.timeout}s")
                
                if len(stack) > self.max_stack_depth:
                    return ExecutionResult(success=False, output=output, steps=steps,
                                         error=f"栈溢出 {self.max_stack_depth}")
                
                opcode, operand = instructions[pc]
                instruction = self.INSTRUCTIONS.get(opcode, 'UNKNOWN')
                
                # 执行指令
                if instruction == 'NOP':
                    pass
                
                elif instruction == 'PUSH':
                    stack.append(float(operand))
                
                elif instruction == 'POP':
                    if stack:
                        stack.pop()
                
                elif instruction == 'DUP':
                    if stack:
                        stack.append(stack[-1])
                
                elif instruction == 'ADD':
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()
                        stack.append(a + b)
                
                elif instruction == 'SUB':
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()
                        stack.append(a - b)
                
                elif instruction == 'MUL':
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()
                        stack.append(a * b)
                
                elif instruction == 'DIV':
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()
                        if b != 0:
                            stack.append(a / b)
                        else:
                            stack.append(0.0)  # 安全除法
                
                elif instruction == 'JMP':
                    pc = operand % len(instructions)
                    steps += 1
                    continue
                
                elif instruction == 'JZ':
                    if stack and stack[-1] == 0:
                        pc = operand % len(instructions)
                        steps += 1
                        continue
                
                elif instruction == 'JNZ':
                    if stack and stack[-1] != 0:
                        pc = operand % len(instructions)
                        steps += 1
                        continue
                
                elif instruction == 'INPUT':
                    if input_ptr < len(inputs):
                        stack.append(inputs[input_ptr])
                        input_ptr += 1
                
                elif instruction == 'OUTPUT':
                    if stack:
                        output.append(stack[-1])
                
                elif instruction == 'HALT':
                    return ExecutionResult(success=True, output=output, steps=steps)
                
                elif instruction == 'SWAP':
                    if len(stack) >= 2:
                        stack[-1], stack[-2] = stack[-2], stack[-1]
                
                pc += 1
                steps += 1
            
            # 程序正常结束
            return ExecutionResult(success=True, output=output, steps=steps)
        
        except Exception as e:
            return ExecutionResult(success=False, output=output, steps=steps,
                                 error=f"运行时错误: {str(e)}")
