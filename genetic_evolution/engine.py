#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演化引擎核心模块
管理种群演化过程
"""

import time
from typing import List, Callable, Dict, Any
from .genome import Genome, GenerationStats
from .vm import QuaternaryVM
from .mutator import Mutator
from .selector import Selector
from .fitness import FitnessEvaluator


class EvolutionEngine:
    """演化引擎"""
    
    def __init__(self, 
                 population_size: int = 100,
                 genome_length: int = 40,
                 mutation_rate: float = 0.01,
                 crossover_rate: float = 0.7,
                 elite_size: int = 5,
                 max_generations: int = 1000):
        """
        Args:
            population_size: 种群大小
            genome_length: 基因组长度
            mutation_rate: 变异率
            crossover_rate: 交叉率
            elite_size: 精英个体数量
            max_generations: 最大代数
        """
        self.population_size = population_size
        self.genome_length = genome_length
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.max_generations = max_generations
        
        self.vm = QuaternaryVM()
        self.mutator = Mutator(base_mutation_rate=mutation_rate, adaptive=True)
        self.evaluator = FitnessEvaluator(self.vm)
        
        self.population: List[Genome] = []
        self.generation = 0
        self.best_genome: Genome = None
        self.history: List[GenerationStats] = []
        
    def initialize_population(self, seed_genomes: List[Genome] = None):
        """初始化种群
        
        Args:
            seed_genomes: 可选的种子基因组列表（可用于导入真实基因）
        """
        if seed_genomes:
            # 使用提供的种子基因组
            self.population = []
            for genome in seed_genomes:
                # 调整长度
                if len(genome.sequence) < self.genome_length:
                    # 太短则重复
                    repeat_times = (self.genome_length // len(genome.sequence)) + 1
                    adjusted_seq = (genome.sequence * repeat_times)[:self.genome_length]
                else:
                    # 太长则截断
                    adjusted_seq = genome.sequence[:self.genome_length]
                
                self.population.append(Genome(
                    sequence=adjusted_seq,
                    generation=0
                ))
            
            # 填充剩余个体
            while len(self.population) < self.population_size:
                self.population.append(Genome.random(self.genome_length, generation=0))
        else:
            # 随机初始化
            self.population = [
                Genome.random(self.genome_length, generation=0)
                for _ in range(self.population_size)
            ]
        
        self.generation = 0
        
    def evolve_generation(self, fitness_func: Callable) -> Dict[str, Any]:
        """演化一代"""
        start_time = time.time()
        
        # 1. 评估适应度
        for genome in self.population:
            self.evaluator.evaluate(genome, fitness_func)
        
        # 2. 统计信息
        fitnesses = [g.fitness for g in self.population]
        best_fitness = max(fitnesses)
        avg_fitness = sum(fitnesses) / len(fitnesses)
        worst_fitness = min(fitnesses)
        
        # 计算多样性
        diversity = self._calculate_diversity()
        
        # 3. 选择最佳个体
        self.best_genome = max(self.population, key=lambda g: g.fitness)
        
        # 4. 精英保留
        elites = Selector.elitism_selection(self.population, self.elite_size)
        
        # 5. 生成新种群
        new_population = elites.copy()
        
        while len(new_population) < self.population_size:
            # 选择父代
            parent1 = Selector.tournament_selection(self.population, tournament_size=3)
            parent2 = Selector.tournament_selection(self.population, tournament_size=3)
            
            # 交叉
            if len(new_population) < self.population_size - 1:
                import random
                if random.random() < self.crossover_rate:
                    child1, child2 = self.mutator.crossover(parent1, parent2, self.generation + 1)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
                    child1.generation = self.generation + 1
                    child2.generation = self.generation + 1
                
                # 变异
                child1 = self.mutator.mutate(child1, self.generation + 1)
                child2 = self.mutator.mutate(child2, self.generation + 1)
                
                new_population.extend([child1, child2])
            else:
                # 只需要一个子代
                child = parent1.copy()
                child.generation = self.generation + 1
                child = self.mutator.mutate(child, self.generation + 1)
                new_population.append(child)
        
        # 6. 更新种群
        self.population = new_population[:self.population_size]
        self.generation += 1
        
        # 7. 记录统计
        elapsed = time.time() - start_time
        stats = GenerationStats(
            generation=self.generation,
            population_size=len(self.population),
            best_fitness=best_fitness,
            avg_fitness=avg_fitness,
            worst_fitness=worst_fitness,
            diversity=diversity,
            elapsed_time=elapsed
        )
        self.history.append(stats)
        
        return {
            'generation': self.generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'diversity': diversity,
            'best_genome': self.best_genome,
            'stats': stats
        }
    
    def run(self, fitness_func: Callable, 
            verbose: bool = True,
            callback: Callable = None) -> Genome:
        """运行演化实验"""
        self.initialize_population()
        
        for gen in range(self.max_generations):
            result = self.evolve_generation(fitness_func)
            
            if verbose and gen % 10 == 0:
                print(result['stats'])
            
            if callback:
                should_continue = callback(result)
                if not should_continue:
                    break
        
        return self.best_genome
    
    def _calculate_diversity(self) -> float:
        """计算种群多样性（基于汉明距离）"""
        if len(self.population) < 2:
            return 0.0
        
        total_distance = 0
        count = 0
        
        for i in range(len(self.population)):
            for j in range(i + 1, min(i + 10, len(self.population))):
                seq1 = self.population[i].sequence
                seq2 = self.population[j].sequence
                min_len = min(len(seq1), len(seq2))
                distance = sum(c1 != c2 for c1, c2 in zip(seq1[:min_len], seq2[:min_len]))
                total_distance += distance
                count += 1
        
        if count == 0:
            return 0.0
        
        avg_distance = total_distance / count
        max_possible = self.genome_length
        
        return avg_distance / max_possible if max_possible > 0 else 0.0
