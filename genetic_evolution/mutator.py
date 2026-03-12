#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变异和交叉操作模块
实现基因组的演化操作
"""

import random
from typing import Tuple
from .genome import Genome


class Mutator:
    """基因变异器"""
    
    def __init__(self, base_mutation_rate: float = 0.01, 
                 adaptive: bool = True):
        """
        Args:
            base_mutation_rate: 基础变异率
            adaptive: 是否启用自适应变异率
        """
        self.base_mutation_rate = base_mutation_rate
        self.adaptive = adaptive
        
    def mutate(self, genome: Genome, generation: int) -> Genome:
        """点突变"""
        mutation_rate = self._get_mutation_rate(generation)
        
        sequence = list(genome.sequence)
        mutations = 0
        
        for i in range(len(sequence)):
            if random.random() < mutation_rate:
                # 随机替换为其他碱基
                old_base = sequence[i]
                new_base = random.choice([c for c in '0123' if c != old_base])
                sequence[i] = new_base
                mutations += 1
        
        new_genome = Genome(
            sequence=''.join(sequence),
            generation=generation,
            parent_ids=[id(genome)],
            mutations=mutations
        )
        
        return new_genome
    
    def crossover(self, parent1: Genome, parent2: Genome, 
                  generation: int) -> Tuple[Genome, Genome]:
        """单点交叉"""
        min_len = min(len(parent1), len(parent2))
        if min_len < 2:
            return parent1.copy(), parent2.copy()
        
        # 随机选择交叉点
        crossover_point = random.randint(1, min_len - 1)
        
        # 创建子代
        child1_seq = parent1.sequence[:crossover_point] + parent2.sequence[crossover_point:]
        child2_seq = parent2.sequence[:crossover_point] + parent1.sequence[crossover_point:]
        
        child1 = Genome(
            sequence=child1_seq,
            generation=generation,
            parent_ids=[id(parent1), id(parent2)]
        )
        
        child2 = Genome(
            sequence=child2_seq,
            generation=generation,
            parent_ids=[id(parent2), id(parent1)]
        )
        
        return child1, child2
    
    def two_point_crossover(self, parent1: Genome, parent2: Genome,
                           generation: int) -> Tuple[Genome, Genome]:
        """两点交叉"""
        min_len = min(len(parent1), len(parent2))
        if min_len < 3:
            return self.crossover(parent1, parent2, generation)
        
        # 选择两个交叉点
        point1 = random.randint(1, min_len - 2)
        point2 = random.randint(point1 + 1, min_len - 1)
        
        # 交换中间片段
        child1_seq = (parent1.sequence[:point1] + 
                     parent2.sequence[point1:point2] + 
                     parent1.sequence[point2:])
        
        child2_seq = (parent2.sequence[:point1] + 
                     parent1.sequence[point1:point2] + 
                     parent2.sequence[point2:])
        
        child1 = Genome(
            sequence=child1_seq,
            generation=generation,
            parent_ids=[id(parent1), id(parent2)]
        )
        
        child2 = Genome(
            sequence=child2_seq,
            generation=generation,
            parent_ids=[id(parent2), id(parent1)]
        )
        
        return child1, child2
    
    def insert_mutation(self, genome: Genome, generation: int) -> Genome:
        """插入突变（增加基因长度）"""
        if random.random() < 0.1:  # 10%概率插入
            pos = random.randint(0, len(genome.sequence))
            insert_len = random.randint(1, 4)
            insert_seq = ''.join(random.choice('0123') for _ in range(insert_len))
            
            new_seq = genome.sequence[:pos] + insert_seq + genome.sequence[pos:]
            
            return Genome(
                sequence=new_seq,
                generation=generation,
                parent_ids=[id(genome)],
                mutations=insert_len
            )
        
        return genome.copy()
    
    def delete_mutation(self, genome: Genome, generation: int) -> Genome:
        """删除突变（减少基因长度）"""
        if len(genome.sequence) > 8 and random.random() < 0.1:  # 保持最小长度
            pos = random.randint(0, len(genome.sequence) - 4)
            delete_len = random.randint(1, 4)
            
            new_seq = genome.sequence[:pos] + genome.sequence[pos + delete_len:]
            
            return Genome(
                sequence=new_seq,
                generation=generation,
                parent_ids=[id(genome)],
                mutations=delete_len
            )
        
        return genome.copy()
    
    def _get_mutation_rate(self, generation: int) -> float:
        """计算自适应变异率"""
        if not self.adaptive:
            return self.base_mutation_rate
        
        # 早期高变异率，后期低变异率
        decay = 0.95 ** (generation / 100)
        return self.base_mutation_rate * (0.1 + 0.9 * decay)
