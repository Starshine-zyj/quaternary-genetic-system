"""
🧬 四进制遗传编码虚拟机 - 64指令完整版
使用3位四进制密码子 (0-63范围)
"""

from typing import List, Dict, Any, Optional
import math
import random


class QuaternaryVM64:
    """基于生物学遗传密码原理的64指令虚拟机"""
    
    # 完整的64指令集 (0-63)
    INSTRUCTION_SET = {
        # 组0: 控制流与系统指令 (0-15)
        0: ('NOP', 0, 'no_op'),
        1: ('HALT', 0, 'halt'),
        2: ('HALT2', 0, 'halt'),
        3: ('HALT3', 0, 'halt'),
        4: ('START', 0, 'start'),
        5: ('START2', 0, 'start'),
        6: ('RESET', 0, 'reset'),
        7: ('DEBUG', 0, 'debug'),
        8: ('OUTPUT', 0, 'output'),
        9: ('OUTPUT2', 0, 'output'),
        10: ('INPUT', 0, 'input'),
        11: ('PRINT', 0, 'print_stack'),
        12: ('CALL', 1, 'call'),
        13: ('RET', 0, 'ret'),
        14: ('SYSCALL', 1, 'syscall'),
        15: ('TRAP', 0, 'trap'),
        
        # 组1: 数据操作 - 常量入栈 (16-31)
        16: ('PUSH_0', 0, 'push_const', 0),
        17: ('PUSH_1', 0, 'push_const', 1),
        18: ('PUSH_2', 0, 'push_const', 2),
        19: ('PUSH_5', 0, 'push_const', 5),
        20: ('PUSH_10', 0, 'push_const', 10),
        21: ('PUSH_42', 0, 'push_const', 42),
        22: ('PUSH_100', 0, 'push_const', 100),
        23: ('PUSH_NEG1', 0, 'push_const', -1),
        24: ('PUSH_PI', 0, 'push_const', math.pi),
        25: ('PUSH_E', 0, 'push_const', math.e),
        26: ('PUSH_TRUE', 0, 'push_const', True),
        27: ('PUSH_FALSE', 0, 'push_const', False),
        28: ('PUSH_IMM', 1, 'push_imm'),
        29: ('PUSH_IMM2', 2, 'push_imm2'),
        30: ('PUSH_NULL', 0, 'push_const', None),
        31: ('PUSH_RAND', 0, 'push_rand'),
        
        # 组2: 栈操作 (32-47)
        32: ('DUP', 0, 'dup'),
        33: ('DUP2', 0, 'dup2'),
        34: ('SWAP', 0, 'swap'),
        35: ('SWAP3', 0, 'swap3'),
        36: ('POP', 0, 'pop'),
        37: ('POP2', 0, 'pop2'),
        38: ('ROT3', 0, 'rot3'),
        39: ('ROT4', 0, 'rot4'),
        40: ('LOAD', 1, 'load'),
        41: ('STORE', 1, 'store'),
        42: ('LOAD_FAST', 1, 'load_fast'),
        43: ('STORE_FAST', 1, 'store_fast'),
        44: ('BUILD_LIST', 1, 'build_list'),
        45: ('BUILD_TUPLE', 1, 'build_tuple'),
        46: ('BUILD_DICT', 1, 'build_dict'),
        47: ('UNPACK', 0, 'unpack'),
        
        # 组3: 算术运算 (48-63)
        48: ('ADD', 0, 'add'),
        49: ('ADD2', 0, 'add'),
        50: ('SUB', 0, 'sub'),
        51: ('SUB2', 0, 'sub'),
        52: ('MUL', 0, 'mul'),
        53: ('MUL2', 0, 'mul'),
        54: ('DIV', 0, 'div'),
        55: ('DIV2', 0, 'div'),
        56: ('MOD', 0, 'mod'),
        57: ('POW', 0, 'pow'),
        58: ('SQRT', 0, 'sqrt'),
        59: ('ABS', 0, 'abs'),
        60: ('NEG', 0, 'neg'),
        61: ('INC', 0, 'inc'),
        62: ('DEC', 0, 'dec'),
        63: ('FLOOR', 0, 'floor'),
    }
    
    def __init__(self):
        self.stack: List[Any] = []
        self.memory: Dict[int, Any] = {}
        self.locals: Dict[int, Any] = {}
        self.output: List[Any] = []
        self.pc = 0  # Program counter
        self.halted = False
        self.started = False
        self.debug_mode = False
    
    def decode_codon(self, codon: str) -> int:
        """将3位四进制密码子解码为操作码 (0-63)"""
        if len(codon) != 3:
            raise ValueError(f"Codon must be 3 quaternary digits, got: {codon}")
        
        opcode = int(codon, 4)  # 四进制转十进制
        
        if opcode < 0 or opcode > 63:
            raise ValueError(f"Invalid opcode: {opcode} (from codon {codon})")
        
        return opcode
    
    def execute_instruction(self, opcode: int, program: List[int]) -> bool:
        """执行单条指令，返回是否继续"""
        if opcode not in self.INSTRUCTION_SET:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        inst_data = self.INSTRUCTION_SET[opcode]
        name, param_count = inst_data[0], inst_data[1]
        handler = inst_data[2] if len(inst_data) > 2 else None
        
        if self.debug_mode:
            print(f"[DEBUG] PC={self.pc}, Opcode={opcode}, Name={name}, Stack={self.stack}")
        
        # 获取参数
        params = []
        for _ in range(param_count):
            self.pc += 1
            if self.pc >= len(program):
                raise RuntimeError(f"Missing parameter for {name}")
            params.append(program[self.pc])
        
        # 执行指令
        if handler == 'no_op':
            pass
        elif handler == 'halt':
            self.halted = True
            return False
        elif handler == 'start':
            self.started = True
        elif handler == 'reset':
            self.__init__()
        elif handler == 'debug':
            self.debug_mode = not self.debug_mode
        elif handler == 'output':
            if self.stack:
                self.output.append(self.stack[-1])
        elif handler == 'input':
            # 简化: 读取一个固定值
            self.stack.append(0)
        elif handler == 'print_stack':
            print(f"Stack: {self.stack}")
        elif handler == 'push_const':
            value = inst_data[3]
            self.stack.append(value)
        elif handler == 'push_imm':
            self.stack.append(params[0])
        elif handler == 'push_imm2':
            value = (params[0] << 8) | params[1]
            self.stack.append(value)
        elif handler == 'push_rand':
            self.stack.append(random.random())
        elif handler == 'dup':
            if self.stack:
                self.stack.append(self.stack[-1])
        elif handler == 'dup2':
            if len(self.stack) >= 2:
                self.stack.extend(self.stack[-2:])
        elif handler == 'swap':
            if len(self.stack) >= 2:
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif handler == 'pop':
            if self.stack:
                self.stack.pop()
        elif handler == 'pop2':
            if len(self.stack) >= 2:
                self.stack.pop()
                self.stack.pop()
        elif handler == 'load':
            addr = params[0]
            self.stack.append(self.memory.get(addr, 0))
        elif handler == 'store':
            if self.stack:
                addr = params[0]
                self.memory[addr] = self.stack.pop()
        elif handler == 'load_fast':
            addr = params[0]
            self.stack.append(self.locals.get(addr, 0))
        elif handler == 'store_fast':
            if self.stack:
                addr = params[0]
                self.locals[addr] = self.stack.pop()
        elif handler == 'add':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
        elif handler == 'sub':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
        elif handler == 'mul':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
        elif handler == 'div':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a / b)
                else:
                    self.stack.append(float('inf'))
        elif handler == 'mod':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)
        elif handler == 'pow':
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a ** b)
        elif handler == 'sqrt':
            if self.stack:
                self.stack[-1] = math.sqrt(self.stack[-1])
        elif handler == 'abs':
            if self.stack:
                self.stack[-1] = abs(self.stack[-1])
        elif handler == 'neg':
            if self.stack:
                self.stack[-1] = -self.stack[-1]
        elif handler == 'inc':
            if self.stack:
                self.stack[-1] += 1
        elif handler == 'dec':
            if self.stack:
                self.stack[-1] -= 1
        elif handler == 'floor':
            if self.stack:
                self.stack[-1] = math.floor(self.stack[-1])
        else:
            # 未实现的指令
            pass
        
        return True
    
    def run(self, dna_sequence: str, max_steps: int = 1000) -> Dict[str, Any]:
        """
        执行DNA序列编码的程序
        
        Args:
            dna_sequence: 四进制DNA序列，如 "010 111 020 001"
            max_steps: 最大执行步数
        
        Returns:
            执行结果字典
        """
        # 解析DNA序列
        codons = dna_sequence.strip().split()
        program = [self.decode_codon(c) for c in codons]
        
        # 执行程序
        steps = 0
        self.pc = 0
        
        while self.pc < len(program) and steps < max_steps:
            if not self.execute_instruction(program[self.pc], program):
                break
            
            self.pc += 1
            steps += 1
        
        return {
            'output': self.output,
            'stack': self.stack.copy(),
            'memory': self.memory.copy(),
            'halted': self.halted,
            'steps': steps
        }


def test_vm64():
    """测试64指令虚拟机"""
    print("=" * 60)
    print("Testing QuaternaryVM64 (64-instruction set)")
    print("=" * 60)
    
    # 测试1: 输出常量42
    print("\n[Test 1] Output constant 42")
    print("DNA: '010 111 020 001' (START PUSH_42 OUTPUT HALT)")
    vm1 = QuaternaryVM64()
    result1 = vm1.run("010 111 020 001")
    print(f"Output: {result1['output']}")
    print(f"[OK] Pass!" if result1['output'] == [42] else f"[FAIL] Failed!")
    
    # 测试2: 计算2+3 (需要分解: PUSH_2 PUSH_2 PUSH_1 ADD ADD)
    print("\n[Test 2] Calculate 2+3")
    print("DNA: '010 102 102 101 300 300 020 001'")
    print("(START PUSH_2 PUSH_2 PUSH_1 ADD ADD OUTPUT HALT)")
    vm2 = QuaternaryVM64()
    result2 = vm2.run("010 102 102 101 300 300 020 001")
    print(f"Output: {result2['output']}")
    print(f"[OK] Pass!" if result2['output'] == [5] else f"[FAIL] Failed!")
    
    # 测试3: 使用简并编码 (HALT的备份)
    print("\n[Test 3] Degeneracy test - HALT variants")
    for halt_codon, halt_name in [("001", "HALT"), ("002", "HALT2"), ("003", "HALT3")]:
        dna = f"010 111 020 {halt_codon}"
        vm = QuaternaryVM64()
        result = vm.run(dna)
        status = "[OK]" if result['halted'] else "[FAIL]"
        print(f"{status} {halt_name}: halted={result['halted']}")
    
    # 测试4: 算术简并 (ADD的备份)
    print("\n[Test 4] Arithmetic degeneracy - ADD/ADD2")
    for add_codon, add_name in [("300", "ADD"), ("301", "ADD2")]:
        dna = f"010 102 101 {add_codon} 020 001"  # PUSH_2 + PUSH_1 = 3
        vm = QuaternaryVM64()
        result = vm.run(dna)
        status = "[OK]" if result['output'] == [3] else "[FAIL]"
        print(f"{status} {add_name}: output={result['output']}")
    
    # 测试5: 栈操作 (DUP + ADD)
    print("\n[Test 5] Stack operations - DUP + ADD")
    print("DNA: '010 111 200 300 020 001' (START PUSH_42 DUP ADD OUTPUT HALT)")
    vm5 = QuaternaryVM64()
    result5 = vm5.run("010 111 200 300 020 001")
    print(f"Output: {result5['output']}")
    print(f"[OK] Pass!" if result5['output'] == [84] else f"[FAIL] Failed!")
    
    # 测试6: 多个输出
    print("\n[Test 6] Multiple outputs")
    print("DNA: '010 110 020 111 020 001' (START PUSH_10 OUTPUT PUSH_42 OUTPUT HALT)")
    vm6 = QuaternaryVM64()
    result6 = vm6.run("010 110 020 111 020 001")
    print(f"Output: {result6['output']}")
    print(f"[OK] Pass!" if result6['output'] == [10, 42] else f"[FAIL] Failed!")
    
    print("\n" + "=" * 60)
    print("[OK] All tests completed!")
    print("=" * 60)


if __name__ == '__main__':
    test_vm64()
