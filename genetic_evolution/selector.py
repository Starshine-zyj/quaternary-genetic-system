#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选择机制模块
实现种群的选择策略
"""

import random
from typing import List
from .genome import Genome


class Selector:
    """选择器"""
    
    @staticmethod
    def tournament_selection(population: List[Genome], 
                           tournament_size: int = 3) -> Genome:
        """锦标赛选择"""
        candidates = random.sample(population, min(tournament_size, len(population)))
        return max(candidates, key=lambda g: g.fitness)
    
    @staticmethod
    def roulette_selection(population: List[Genome]) -> Genome:
        """轮盘赌选择"""
        total_fitness = sum(g.fitness for g in population)
        if total_fitness <= 0:
            return random.choice(population)
        
        pick = random.uniform(0, total_fitness)
        current = 0
        for genome in population:
            current += genome.fitness
            if current >= pick:
                return genome
        
        return population[-1]
    
    @staticmethod
    def rank_selection(population: List[Genome]) -> Genome:
        """排名选择"""
        sorted_pop = sorted(population, key=lambda g: g.fitness)
        ranks = list(range(1, len(sorted_pop) + 1))
        total_rank = sum(ranks)
        
        pick = random.uniform(0, total_rank)
        current = 0
        for i, genome in enumerate(sorted_pop):
            current += ranks[i]
            if current >= pick:
                return genome
        
        return sorted_pop[-1]
    
    @staticmethod
    def elitism_selection(population: List[Genome], 
                         elite_size: int) -> List[Genome]:
        """精英保留"""
        sorted_pop = sorted(population, key=lambda g: g.fitness, reverse=True)
        return sorted_pop[:elite_size]
    
    @staticmethod
    def diversity_selection(population: List[Genome], 
                          select_size: int) -> List[Genome]:
        """多样性选择（基于基因序列差异）"""
        if len(population) <= select_size:
            return population.copy()
        
        selected = [max(population, key=lambda g: g.fitness)]
        remaining = [g for g in population if g not in selected]
        
        while len(selected) < select_size and remaining:
            # 选择与已选个体差异最大的
            best_candidate = None
            max_diversity = -1
            
            for candidate in remaining:
                diversity = sum(
                    Selector._hamming_distance(candidate.sequence, s.sequence)
                    for s in selected
                )
                if diversity > max_diversity:
                    max_diversity = diversity
                    best_candidate = candidate
            
            if best_candidate:
                selected.append(best_candidate)
                remaining.remove(best_candidate)
        
        return selected
    
    @staticmethod
    def _hamming_distance(seq1: str, seq2: str) -> int:
        """计算汉明距离"""
        min_len = min(len(seq1), len(seq2))
        distance = abs(len(seq1) - len(seq2))
        distance += sum(c1 != c2 for c1, c2 in zip(seq1[:min_len], seq2[:min_len]))
        return distance
