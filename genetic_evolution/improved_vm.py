#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的四进制虚拟机 - 基于遗传密码原理设计

核心特性：
1. 3位四进制密码子 (4³ = 64 种指令)
2. 简并性编码（关键指令有多个备份）
3. 功能分组（按类别组织操作码）
4. 内置起始/终止标记（类似AUG/UAA）
"""

from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ImprovedQuaternaryVM:
    """
    改进的四进制虚拟机
    
    指令格式：每3个四进制数字 = 1条指令
    操作码范围：0-63 (4³ = 64)
    """
    
    # 完整的64指令集（基于遗传密码原理）
    INSTRUCTIONS = {
        # 第一组：数据操作 (000-033)
        0o000: 'NOP',           # 空操作
        0o001: 'PUSH_0',        # 压入0
        0o002: 'PUSH_1',        # 压入1
        0o003: 'PUSH_2',        # 压入2
        0o010: 'PUSH_3',        # 压入3
        0o011: 'POP',           # 弹出栈顶
        0o012: 'DUP',           # 复制栈顶
        0o013: 'SWAP',          # 交换栈顶两元素
        0o020: 'PUSH_10',       # 压入10
        0o021: 'PUSH_20',       # 压入20
        0o022: 'PUSH_30',       # 压入30
        0o023: 'PUSH_42',       # 压入42（常用目标值）
        0o030: 'LOAD_MEM',      # 从内存加载
        0o031: 'STORE_MEM',     # 存储到内存
        0o032: 'CLEAR_STACK',   # 清空栈
        0o033: 'RESERVED_033',  # 保留
        
        # 第二组：算术运算 (100-133)
        0o100: 'ADD',           # 加法
        0o101: 'SUB',           # 减法
        0o102: 'MUL',           # 乘法
        0o103: 'DIV',           # 除法
        0o110: 'MOD',           # 取模
        0o111: 'INC',           # 自增1
        0o112: 'DEC',           # 自减1
        0o113: 'NEG',           # 取负
        0o120: 'ADD',           # ADD简并编码1（容错）
        0o121: 'SUB',           # SUB简并编码1
        0o122: 'MUL',           # MUL简并编码1
        0o123: 'DIV',           # DIV简并编码1
        
        # 第三组：比较与逻辑 (200-233)
        0o200: 'CMP_EQ',        # 相等比较
        0o201: 'CMP_LT',        # 小于比较
        0o202: 'CMP_GT',        # 大于比较
        0o203: 'CMP_LE',        # 小于等于
        0o210: 'AND',           # 逻辑与
        0o211: 'OR',            # 逻辑或
        0o212: 'NOT',           # 逻辑非
        0o213: 'XOR',           # 异或
        
        # 第四组：控制流 (300-333)
        0o300: 'JMP',           # 无条件跳转
        0o301: 'JZ',            # 为零跳转
        0o302: 'JNZ',           # 非零跳转
        0o303: 'CALL',          # 函数调用
        0o310: 'RET',           # 函数返回
        0o311: 'LOOP_START',    # 循环开始标记
        0o312: 'LOOP_END',      # 循环结束
        0o313: 'BREAK',         # 跳出循环
        
        # 第五组：输入输出 (1000-1033)
        0o1000: 'OUTPUT',       # 输出栈顶
        0o1001: 'INPUT',        # 读取输入
        0o1002: 'PRINT_STACK',  # 打印整个栈
        0o1003: 'DEBUG',        # 调试信息
        0o1010: 'OUTPUT',       # OUTPUT简并1（容错）
        0o1011: 'OUTPUT',       # OUTPUT简并2
        0o1012: 'OUTPUT',       # OUTPUT简并3
        
        # 第六组：程序控制 (1100-1133)
        0o1100: 'START',        # 程序起始标记（类似AUG起始密码子）
        0o1101: 'HALT',         # 停机（终止密码子1，类似UAA）
        0o1102: 'HALT',         # 停机简并1（终止密码子2，类似UAG）
        0o1103: 'HALT',         # 停机简并2（终止密码子3，类似UGA）
        0o1110: 'CHECKPOINT',   # 检查点
        0o1111: 'RESET',        # 重置虚拟机状态
        
        # 第七组：特殊操作 (1200-1233)
        0o1200: 'RANDOM',       # 生成随机数
        0o1201: 'TIME',         # 获取时间戳
        0o1202: 'GENE_MARKER',  # 基因标记（用于分析）
        0o1203: 'MUTATE_FLAG',  # 变异标志
    }
    
    def __init__(self, max_steps: int = 10000, stack_limit: int = 1000):
        """初始化虚拟机"""
        self.max_steps = max_steps
        self.stack_limit = stack_limit
        self.reset()
    
    def reset(self):
        """重置虚拟机状态"""
        self.stack: List[float] = []
        self.memory: Dict[int, float] = {}
        self.output: List[float] = []
        self.pc = 0  # 程序计数器
        self.steps = 0
        self.halted = False
        self.error = None
    
    def decode_instructions(self, genome) -> List[int]:
        """
        解码基因序列为指令列表
        
        格式：每3个四进制数字 = 1条指令
        范围：0-63 (4³ = 64种指令)
        
        Args:
            genome: 基因组对象，包含四进制序列
        
        Returns:
            指令操作码列表
        """
        instructions = []
        seq = genome.sequence
        
        for i in range(0, len(seq), 3):
            if i + 2 < len(seq):
                # 3位四进制数字转为操作码（0-63）
                opcode_str = seq[i:i+3]
                opcode = int(opcode_str, 4)
                instructions.append(opcode)
            
        return instructions
    
    def execute(self, genome, max_steps: Optional[int] = None) -> Dict:
        """
        执行基因程序
        
        Args:
            genome: 基因组对象
            max_steps: 最大执行步数
        
        Returns:
            执行结果字典
        """
        self.reset()
        max_steps = max_steps or self.max_steps
        
        try:
            instructions = self.decode_instructions(genome)
            
            if not instructions:
                return self._get_result()
            
            # 执行指令循环
            while self.pc < len(instructions) and self.steps < max_steps and not self.halted:
                opcode = instructions[self.pc]
                instruction_name = self.INSTRUCTIONS.get(opcode, 'UNKNOWN')
                
                # 执行指令
                self._execute_instruction(opcode, instruction_name, instructions)
                
                self.pc += 1
                self.steps += 1
                
                # 栈溢出保护
                if len(self.stack) > self.stack_limit:
                    self.error = "Stack overflow"
                    break
            
        except Exception as e:
            self.error = str(e)
            logger.warning(f"Execution error: {e}")
        
        return self._get_result()
    
    def _execute_instruction(self, opcode: int, instruction: str, instructions: List[int]):
        """执行单条指令"""
        
        # 数据操作
        if instruction == 'NOP':
            pass
        elif instruction == 'PUSH_0':
            self.stack.append(0.0)
        elif instruction == 'PUSH_1':
            self.stack.append(1.0)
        elif instruction == 'PUSH_2':
            self.stack.append(2.0)
        elif instruction == 'PUSH_3':
            self.stack.append(3.0)
        elif instruction == 'PUSH_10':
            self.stack.append(10.0)
        elif instruction == 'PUSH_20':
            self.stack.append(20.0)
        elif instruction == 'PUSH_30':
            self.stack.append(30.0)
        elif instruction == 'PUSH_42':
            self.stack.append(42.0)
        elif instruction == 'POP':
            if self.stack:
                self.stack.pop()
        elif instruction == 'DUP':
            if self.stack:
                self.stack.append(self.stack[-1])
        elif instruction == 'SWAP':
            if len(self.stack) >= 2:
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif instruction == 'CLEAR_STACK':
            self.stack.clear()
        
        # 算术运算
        elif instruction == 'ADD':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
        elif instruction == 'SUB':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
        elif instruction == 'MUL':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
        elif instruction == 'DIV':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a / b)
        elif instruction == 'MOD':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a % b)
        elif instruction == 'INC':
            if self.stack:
                self.stack[-1] += 1
        elif instruction == 'DEC':
            if self.stack:
                self.stack[-1] -= 1
        elif instruction == 'NEG':
            if self.stack:
                self.stack[-1] = -self.stack[-1]
        
        # 比较与逻辑
        elif instruction == 'CMP_EQ':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1.0 if a == b else 0.0)
        elif instruction == 'CMP_LT':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1.0 if a < b else 0.0)
        elif instruction == 'CMP_GT':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1.0 if a > b else 0.0)
        
        # 输入输出（包括简并编码）
        elif instruction == 'OUTPUT':
            if self.stack:
                self.output.append(self.stack[-1])
        elif instruction == 'PRINT_STACK':
            if self.stack:
                self.output.extend(self.stack)
        
        # 程序控制（包括简并编码）
        elif instruction == 'START':
            pass  # 标记指令，不执行操作
        elif instruction == 'HALT':
            self.halted = True
        elif instruction == 'RESET':
            self.reset()
        
        # 未知指令
        elif instruction == 'UNKNOWN':
            pass  # 静默忽略（容错性）
    
    def _get_result(self) -> Dict:
        """获取执行结果"""
        return {
            'output': self.output,
            'stack': self.stack.copy(),
            'steps': self.steps,
            'halted': self.halted,
            'error': self.error
        }


def test_improved_vm():
    """测试改进的虚拟机"""
    from genetic_evolution.genome import Genome
    
    print("=" * 60)
    print("测试改进的四进制虚拟机（基于遗传密码原理）")
    print("=" * 60)
    
    vm = ImprovedQuaternaryVM()
    
    # 测试1：计算 2+3 并输出
    print("\n[测试1] 计算 2+3 并输出")
    dna1 = "110000200310010001101"  # START, PUSH_2, PUSH_3, ADD, OUTPUT, HALT
    genome1 = Genome.from_dna(dna1, generation=0)
    result1 = vm.execute(genome1)
    print(f"DNA: {dna1}")
    print(f"输出: {result1['output']}")
    print(f"预期: [5.0]")
    print(f"[OK] Pass!" if result1['output'] == [5.0] else "[FAIL] Failed!")
    
    # 测试2：直接输出42（使用专用指令）
    print("\n[测试2] 直接输出42（使用PUSH_42专用指令）")
    dna2 = "110002310001101"  # START, PUSH_42, OUTPUT, HALT
    genome2 = Genome.from_dna(dna2, generation=0)
    result2 = vm.execute(genome2)
    print(f"DNA: {dna2}")
    print(f"输出: {result2['output']}")
    print(f"预期: [42.0]")
    print(f"[OK] Pass!" if result2['output'] == [42.0] else "[FAIL] Failed!")
    
    # 测试3：测试简并编码（OUTPUT的备份编码）
    print("\n[测试3] 测试简并编码（OUTPUT有4种编码）")
    dna3_variants = [
        ("110002310001101", "标准OUTPUT (1000)"),
        ("110002310101101", "简并OUTPUT1 (1010)"),
        ("110002310111101", "简并OUTPUT2 (1011)"),
        ("110002310121101", "简并OUTPUT3 (1012)"),
    ]
    for dna, desc in dna3_variants:
        genome = Genome.from_dna(dna, generation=0)
        result = vm.execute(genome)
        status = "[OK]" if result['output'] == [42.0] else "[FAIL]"
        print(f"{status} {desc}: output {result['output']}")
    
    # 测试4：测试HALT简并编码（3种终止密码子）
    print("\n[测试4] 测试HALT简并编码（3种终止密码子）")
    halt_variants = [
        ("110002310001101", "标准HALT (1101, 类似UAA)"),
        ("110002310001102", "简并HALT1 (1102, 类似UAG)"),
        ("110002310001103", "简并HALT2 (1103, 类似UGA)"),
    ]
    for dna, desc in halt_variants:
        genome = Genome.from_dna(dna, generation=0)
        result = vm.execute(genome)
        status = "[OK]" if result['halted'] else "[FAIL]"
        print(f"{status} {desc}: halted={result['halted']}")
    
    # 测试5：复杂程序（多次输出）
    print("\n[测试5] 复杂程序：输出10, 20, 30")
    dna5 = "1100" "020" "1000" "021" "1010" "022" "1011" "1101"
    # START, PUSH_10, OUTPUT, PUSH_20, OUTPUT简并1, PUSH_30, OUTPUT简并2, HALT
    genome5 = Genome.from_dna(dna5, generation=0)
    result5 = vm.execute(genome5)
    print(f"DNA: {dna5}")
    print(f"输出: {result5['output']}")
    print(f"预期: [10.0, 20.0, 30.0]")
    print(f"[OK] Pass!" if result5['output'] == [10.0, 20.0, 30.0] else "[FAIL] Failed!")
    
    print("\n" + "=" * 60)
    print("[OK] All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_improved_vm()
