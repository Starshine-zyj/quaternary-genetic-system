#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基因组核心数据结构模块
定义基因型、表型和执行结果
"""

from dataclasses import dataclass, field
from typing import List, Optional
import random


@dataclass
class Genome:
    """四进制基因组"""
    sequence: str  # 四进制字符串（只包含0-3）
    fitness: float = 0.0
    generation: int = 0
    parent_ids: List[int] = field(default_factory=list)
    mutations: int = 0
    
    def __post_init__(self):
        """验证基因序列的合法性"""
        if not all(c in '0123' for c in self.sequence):
            raise ValueError(f"基因序列必须只包含0-3字符: {self.sequence}")
    
    def __len__(self) -> int:
        return len(self.sequence)
    
    def copy(self) -> 'Genome':
        """创建基因组副本"""
        return Genome(
            sequence=self.sequence,
            fitness=self.fitness,
            generation=self.generation,
            parent_ids=self.parent_ids.copy(),
            mutations=self.mutations
        )
    
    @staticmethod
    def random(length: int, generation: int = 0) -> 'Genome':
        """生成随机基因组（增强版：更高概率生成有效指令）"""
        sequence = ''
        # 前半部分：生成偏向有效指令的序列
        for _ in range(length // 2):
            # 60%概率生成PUSH指令（0x01）
            if random.random() < 0.6:
                sequence += '01' + random.choice('0123') + random.choice('0123')
            # 20%概率生成算术指令
            elif random.random() < 0.8:
                sequence += '1' + random.choice('0123') + random.choice('0123') + random.choice('0123')
            # 10%概率生成OUTPUT指令（0x31）
            elif random.random() < 0.9:
                sequence += '3100'
            # 10%概率生成其他随机指令
            else:
                sequence += ''.join(random.choice('0123') for _ in range(4))
        
        # 后半部分：完全随机
        remaining = length - len(sequence)
        sequence += ''.join(random.choice('0123') for _ in range(remaining))
        
        return Genome(sequence=sequence[:length], generation=generation)
    
    @staticmethod
    def from_dna(dna_sequence: str, generation: int = 0) -> 'Genome':
        """从真实DNA序列创建基因组
        
        Args:
            dna_sequence: DNA序列（ATCG字符）
            generation: 代数
        
        Returns:
            Genome对象
        """
        # DNA碱基到四进制的映射
        base_map = {'A': '0', 'T': '1', 'C': '2', 'G': '3',
                   'a': '0', 't': '1', 'c': '2', 'g': '3'}
        
        # 转换为四进制序列
        quaternary = ''
        for base in dna_sequence:
            if base in base_map:
                quaternary += base_map[base]
            elif base in '0123':
                quaternary += base  # 已经是四进制
            # 忽略其他字符（空格、换行等）
        
        if not quaternary:
            raise ValueError("无效的DNA序列")
        
        return Genome(sequence=quaternary, generation=generation)
    
    def to_bytes(self) -> bytes:
        """转换为字节序列（每2个四进制数字打包为1字节）"""
        result = []
        for i in range(0, len(self.sequence), 2):
            if i + 1 < len(self.sequence):
                byte = int(self.sequence[i], 4) * 16 + int(self.sequence[i+1], 4)
            else:
                byte = int(self.sequence[i], 4) * 16
            result.append(byte)
        return bytes(result)
    
    @staticmethod
    def from_bytes(data: bytes, generation: int = 0) -> 'Genome':
        """从字节序列创建基因组"""
        sequence = ''
        for byte in data:
            high = (byte >> 4) % 4
            low = byte % 4
            sequence += str(high) + str(low)
        return Genome(sequence=sequence, generation=generation)


@dataclass
class ExecutionResult:
    """虚拟机执行结果"""
    success: bool
    output: List[float]
    steps: int
    error: Optional[str] = None
    stack_trace: Optional[List] = None
    
    def __str__(self) -> str:
        if self.success:
            return f"✓ 成功执行 {self.steps} 步，输出: {self.output}"
        else:
            return f"✗ 执行失败: {self.error}"


@dataclass
class GenerationStats:
    """代际统计信息"""
    generation: int
    population_size: int
    best_fitness: float
    avg_fitness: float
    worst_fitness: float
    diversity: float  # 基因多样性
    elapsed_time: float
    
    def __str__(self) -> str:
        return (f"代 {self.generation:4d} | "
                f"最佳: {self.best_fitness:8.4f} | "
                f"平均: {self.avg_fitness:8.4f} | "
                f"多样性: {self.diversity:6.4f}")
