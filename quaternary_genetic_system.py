#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四进制基因编程演化实验系统 v1.0
Quaternary Genetic Programming Evolution System

这是一个完整的、可直接运行的实验系统，用于研究四进制编码的
基因程序如何通过自然选择演化出复杂行为。

作者: AI Assistant
日期: 2026-03-12
版本: 1.0
"""

import random
import time
import math
import json
import logging
from typing import List, Dict, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, Counter
import statistics
from functools import wraps
import threading
import signal


# ============================================================================
# 第一层：核心数据结构
# ============================================================================

class OpCode(Enum):
    """四进制虚拟机操作码"""
    # 数据操作 (0x)
    PUSH = 0      # 压栈
    POP = 1       # 弹栈
    DUP = 2       # 复制栈顶
    SWAP = 3      # 交换栈顶
    
    # 算术运算 (1x)
    ADD = 10      # 加法
    SUB = 11      # 减法
    MUL = 12      # 乘法
    DIV = 13      # 除法
    
    # 控制流 (2x)
    JMP = 20      # 无条件跳转
    JZ = 21       # 零跳转
    JNZ = 22      # 非零跳转
    CALL = 23     # 调用子程序
    
    # 特殊操作 (3x)
    INPUT = 30    # 读取输入
    OUTPUT = 31   # 输出结果
    NOP = 32      # 空操作
    HALT = 33     # 停止执行


@dataclass
class ExecutionResult:
    """执行结果"""
    output: List[float]          # 输出值序列
    halted: bool                 # 是否正常停止
    steps: int                   # 执行步数
    error: Optional[str] = None  # 错误信息
    stack_snapshot: List[float] = field(default_factory=list)


@dataclass
class Genome:
    """
    基因组类 - 四进制编码
    
    Attributes:
        sequence: 四进制字符串，只包含'0','1','2','3'
        fitness: 适应度值
        generation: 出生代数
        parent_ids: 父本ID列表
    """
    sequence: str
    fitness: float = 0.0
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)
    genome_id: str = field(default_factory=lambda: str(random.randint(100000, 999999)))
    
    def __post_init__(self):
        """验证基因序列合法性"""
        if not all(c in '0123' for c in self.sequence):
            raise ValueError(f"Invalid quaternary sequence: {self.sequence}")
    
    @property
    def length(self) -> int:
        """基因长度"""
        return len(self.sequence)
    
    def to_decimal(self) -> List[int]:
        """将四进制序列转换为十进制整数列表"""
        result = []
        # 每2位四进制作为一个指令单元
        for i in range(0, len(self.sequence) - 1, 2):
            quad = self.sequence[i:i+2]
            decimal = int(quad, 4)
            result.append(decimal)
        return result
    
    def get_instructions(self) -> List[Tuple[int, int]]:
        """
        解析为指令序列
        返回: [(操作码, 操作数), ...]
        """
        instructions = []
        seq = self.to_decimal()
        for val in seq:
            opcode = val // 4 * 10  # 高位决定操作码类别
            operand = val % 4       # 低位作为操作数
            instructions.append((opcode, operand))
        return instructions
    
    def copy(self) -> 'Genome':
        """创建副本"""
        return Genome(
            sequence=self.sequence,
            fitness=self.fitness,
            generation=self.generation,
            parent_ids=self.parent_ids.copy(),
            genome_id=self.genome_id
        )


# ============================================================================
# 第二层：虚拟机实现
# ============================================================================

class QuaternaryVM:
    """
    四进制虚拟机
    
    执行四进制基因程序，模拟生物的蛋白质合成和表达过程。
    类比：基因组 → 转录 → 翻译 → 蛋白质（功能）
           基因序列 → 解析 → 指令 → 执行（行为）
    """
    
    def __init__(
        self,
        max_steps: int = 10000,
        max_stack_size: int = 1000,
        max_recursion: int = 100,
        time_limit: float = 1.0
    ):
        """
        初始化虚拟机
        
        Args:
            max_steps: 最大执行步数
            max_stack_size: 最大栈深度
            max_recursion: 最大递归深度
            time_limit: 执行时间限制（秒）
        """
        self.max_steps = max_steps
        self.max_stack_size = max_stack_size
        self.max_recursion = max_recursion
        self.time_limit = time_limit
        
        # 执行状态
        self.stack: List[float] = []
        self.call_stack: List[int] = []  # 返回地址栈
        self.input_buffer: List[float] = []
        self.output_buffer: List[float] = []
        self.pc = 0  # 程序计数器
        self.steps = 0
        self.start_time = 0.0
        
    def reset(self, inputs: Optional[List[float]] = None):
        """重置虚拟机状态"""
        self.stack = []
        self.call_stack = []
        self.input_buffer = inputs.copy() if inputs else []
        self.output_buffer = []
        self.pc = 0
        self.steps = 0
        self.start_time = time.time()
    
    def execute(self, genome: Genome, inputs: Optional[List[float]] = None) -> ExecutionResult:
        """
        执行基因程序
        
        Args:
            genome: 基因组对象
            inputs: 输入数据
            
        Returns:
            执行结果对象
        """
        self.reset(inputs)
        instructions = genome.get_instructions()
        
        try:
            while (
                self.pc < len(instructions) and
                self.steps < self.max_steps and
                len(self.call_stack) < self.max_recursion and
                time.time() - self.start_time < self.time_limit
            ):
                opcode, operand = instructions[self.pc]
                self._execute_instruction(opcode, operand, instructions)
                self.steps += 1
                self.pc += 1
            
            # 检查停止原因
            if self.steps >= self.max_steps:
                return ExecutionResult(
                    output=self.output_buffer,
                    halted=False,
                    steps=self.steps,
                    error="Max steps exceeded"
                )
            elif time.time() - self.start_time >= self.time_limit:
                return ExecutionResult(
                    output=self.output_buffer,
                    halted=False,
                    steps=self.steps,
                    error="Time limit exceeded"
                )
            else:
                return ExecutionResult(
                    output=self.output_buffer,
                    halted=True,
                    steps=self.steps,
                    stack_snapshot=self.stack.copy()
                )
                
        except Exception as e:
            return ExecutionResult(
                output=self.output_buffer,
                halted=False,
                steps=self.steps,
                error=str(e)
            )
    
    def _execute_instruction(
        self,
        opcode: int,
        operand: int,
        instructions: List[Tuple[int, int]]
    ):
        """执行单条指令"""
        
        # 数据操作类 (0x)
        if opcode == 0:  # PUSH
            self._push(float(operand))
        
        elif opcode == 1:  # POP
            self._pop()
        
        elif opcode == 2:  # DUP
            if self.stack:
                self.stack.append(self.stack[-1])
        
        elif opcode == 3:  # SWAP
            if len(self.stack) >= 2:
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        
        # 算术运算类 (1x)
        elif opcode == 10:  # ADD
            if len(self.stack) >= 2:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
        
        elif opcode == 11:  # SUB
            if len(self.stack) >= 2:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a - b)
        
        elif opcode == 12:  # MUL
            if len(self.stack) >= 2:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)
        
        elif opcode == 13:  # DIV
            if len(self.stack) >= 2:
                b, a = self.stack.pop(), self.stack.pop()
                # 保护性除法
                if abs(b) < 1e-10:
                    self.stack.append(0.0)  # 除零保护
                else:
                    self.stack.append(a / b)
        
        # 控制流类 (2x)
        elif opcode == 20:  # JMP
            jump_offset = operand - 2  # 相对偏移
            new_pc = self.pc + jump_offset
            if 0 <= new_pc < len(instructions):
                self.pc = new_pc - 1  # -1是因为主循环会+1
        
        elif opcode == 21:  # JZ (零跳转)
            if self.stack and self.stack[-1] == 0:
                jump_offset = operand - 2
                new_pc = self.pc + jump_offset
                if 0 <= new_pc < len(instructions):
                    self.pc = new_pc - 1
        
        elif opcode == 22:  # JNZ (非零跳转)
            if self.stack and self.stack[-1] != 0:
                jump_offset = operand - 2
                new_pc = self.pc + jump_offset
                if 0 <= new_pc < len(instructions):
                    self.pc = new_pc - 1
        
        elif opcode == 23:  # CALL
            if len(self.call_stack) < self.max_recursion:
                self.call_stack.append(self.pc + 1)  # 保存返回地址
                self.pc = operand - 1  # 跳转到目标地址
        
        # 特殊操作类 (3x) - 根据operand子分发
        elif opcode == 30:
            if operand == 0:  # INPUT
                if self.input_buffer:
                    self.stack.append(self.input_buffer.pop(0))
                else:
                    self.stack.append(0.0)  # 默认输入0
            
            elif operand == 1:  # OUTPUT
                if self.stack:
                    self.output_buffer.append(self.stack.pop())
            
            elif operand == 2:  # NOP
                pass  # 无操作
            
            elif operand == 3:  # HALT
                self.pc = len(instructions)  # 跳到最后，结束执行
    
    def _push(self, value: float):
        """压栈（带深度检查）"""
        if len(self.stack) < self.max_stack_size:
            self.stack.append(value)
    
    def _pop(self) -> Optional[float]:
        """弹栈"""
        return self.stack.pop() if self.stack else None


# ============================================================================
# 第三层：变异与遗传操作
# ============================================================================

class Mutator:
    """
    变异操作类
    
    实现多种变异操作，模拟生物遗传变异的多样性。
    """
    
    def __init__(
        self,
        point_mutation_rate: float = 0.01,
        insertion_rate: float = 0.005,
        deletion_rate: float = 0.005,
        duplication_rate: float = 0.002,
        inversion_rate: float = 0.001,
        crossover_rate: float = 0.7
    ):
        """
        初始化变异器
        
        Args:
            point_mutation_rate: 点突变率
            insertion_rate: 插入率
            deletion_rate: 删除率
            duplication_rate: 复制率
            inversion_rate: 倒位率
            crossover_rate: 交叉率
        """
        self.point_mutation_rate = point_mutation_rate
        self.insertion_rate = insertion_rate
        self.deletion_rate = deletion_rate
        self.duplication_rate = duplication_rate
        self.inversion_rate = inversion_rate
        self.crossover_rate = crossover_rate
    
    def mutate(self, genome: Genome, generation: int) -> Genome:
        """
        对基因组进行变异
        
        Returns:
            变异后的新基因组
        """
        seq_list = list(genome.sequence)
        mutated = False
        
        # 1. 点突变
        for i in range(len(seq_list)):
            if random.random() < self.point_mutation_rate:
                # 选择一个不同的碱基
                choices = ['0', '1', '2', '3']
                choices.remove(seq_list[i])
                seq_list[i] = random.choice(choices)
                mutated = True
        
        # 2. 插入
        if random.random() < self.insertion_rate and len(seq_list) < 200:
            pos = random.randint(0, len(seq_list))
            seq_list.insert(pos, random.choice('0123'))
            mutated = True
        
        # 3. 删除
        if random.random() < self.deletion_rate and len(seq_list) > 10:
            pos = random.randint(0, len(seq_list) - 1)
            seq_list.pop(pos)
            mutated = True
        
        # 4. 片段复制
        if random.random() < self.duplication_rate and len(seq_list) >= 4:
            start = random.randint(0, len(seq_list) - 2)
            end = min(start + random.randint(1, 3), len(seq_list))
            segment = seq_list[start:end]
            insert_pos = random.randint(0, len(seq_list))
            seq_list[insert_pos:insert_pos] = segment
            mutated = True
        
        # 5. 倒位
        if random.random() < self.inversion_rate and len(seq_list) >= 4:
            start = random.randint(0, len(seq_list) - 2)
            end = min(start + random.randint(2, 5), len(seq_list))
            seq_list[start:end] = reversed(seq_list[start:end])
            mutated = True
        
        new_sequence = ''.join(seq_list)
        
        return Genome(
            sequence=new_sequence,
            generation=generation,
            parent_ids=[genome.genome_id] if mutated else genome.parent_ids.copy()
        )
    
    def crossover(self, parent1: Genome, parent2: Genome, generation: int) -> Tuple[Genome, Genome]:
        """
        基因重组（交叉）
        
        Returns:
            两个子代基因组
        """
        if random.random() > self.crossover_rate:
            # 不交叉，直接复制
            return parent1.copy(), parent2.copy()
        
        # 单点交叉
        min_len = min(parent1.length, parent2.length)
        cross_point = random.randint(1, min_len - 1)
        
        child1_seq = parent1.sequence[:cross_point] + parent2.sequence[cross_point:]
        child2_seq = parent2.sequence[:cross_point] + parent1.sequence[cross_point:]
        
        child1 = Genome(
            sequence=child1_seq,
            generation=generation,
            parent_ids=[parent1.genome_id, parent2.genome_id]
        )
        child2 = Genome(
            sequence=child2_seq,
            generation=generation,
            parent_ids=[parent1.genome_id, parent2.genome_id]
        )
        
        return child1, child2


# ============================================================================
# 第四层：选择机制
# ============================================================================

class Selector:
    """
    选择机制类
    
    实现多种选择策略，模拟自然选择的不同模式。
    """
    
    @staticmethod
    def tournament_selection(
        population: List[Genome],
        tournament_size: int = 3
    ) -> Genome:
        """
        锦标赛选择
        
        随机选择tournament_size个个体，返回适应度最高的。
        """
        candidates = random.sample(population, min(tournament_size, len(population)))
        return max(candidates, key=lambda g: g.fitness)
    
    @staticmethod
    def roulette_wheel_selection(population: List[Genome]) -> Genome:
        """
        轮盘赌选择
        
        按适应度比例选择，适应度越高被选中概率越大。
        """
        total_fitness = sum(g.fitness for g in population)
        if total_fitness == 0:
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
        """
        排序选择
        
        按适应度排序后，根据排名而非绝对适应度值选择。
        """
        sorted_pop = sorted(population, key=lambda g: g.fitness)
        n = len(sorted_pop)
        # 线性排名概率
        probabilities = [(2 * i) / (n * (n + 1)) for i in range(1, n + 1)]
        
        pick = random.random()
        cumulative = 0
        for genome, prob in zip(sorted_pop, probabilities):
            cumulative += prob
            if pick <= cumulative:
                return genome
        
        return sorted_pop[-1]
    
    @staticmethod
    def elitism_selection(
        population: List[Genome],
        elite_count: int
    ) -> List[Genome]:
        """
        精英选择
        
        直接保留适应度最高的elite_count个个体。
        """
        sorted_pop = sorted(population, key=lambda g: g.fitness, reverse=True)
        return [g.copy() for g in sorted_pop[:elite_count]]


# ============================================================================
# 第五层：环境与适应度
# ============================================================================

class FitnessEvaluator:
    """
    适应度评估器
    
    定义不同的问题环境，评估个体的适应度。
    """
    
    def __init__(self, vm: QuaternaryVM):
        self.vm = vm
    
    def evaluate(
        self,
        genome: Genome,
        fitness_func: Callable[[ExecutionResult], float]
    ) -> float:
        """
        评估基因组的适应度
        
        Args:
            genome: 待评估基因组
            fitness_func: 适应度函数
            
        Returns:
            适应度值
        """
        result = self.vm.execute(genome)
        fitness = fitness_func(result)
        genome.fitness = fitness
        return fitness


class Environments:
    """
    预定义的实验环境
    """
    
    @staticmethod
    def target_number_fitness(target: float = 42.0) -> Callable[[ExecutionResult], float]:
        """
        目标数值环境
        
        目标：演化出能输出指定数值的程序
        """
        def fitness(result: ExecutionResult) -> float:
            if not result.output:
                return 0.0
            
            output = result.output[0]
            error = abs(output - target)
            
            # 避免除零，同时给予平滑的适应度曲线
            fitness_value = 1.0 / (1.0 + error)
            return fitness_value
        
        return fitness
    
    @staticmethod
    def arithmetic_expression_fitness(
        x_values: List[float],
        y_values: List[float]
    ) -> Callable[[ExecutionResult], float]:
        """
        算术表达式拟合环境
        
        目标：演化出能拟合 y = f(x) 的程序
        """
        def fitness(result: ExecutionResult, vm: QuaternaryVM, genome: Genome) -> float:
            total_error = 0.0
            
            for x, y_expected in zip(x_values, y_values):
                exec_result = vm.execute(genome, inputs=[x])
                
                if exec_result.output:
                    y_actual = exec_result.output[0]
                    total_error += abs(y_actual - y_expected)
                else:
                    total_error += abs(y_expected) + 100  # 惩罚无输出
            
            return 1.0 / (1.0 + total_error / len(x_values))
        
        return lambda result: 0.0  # 占位，实际需要传入vm和genome
    
    @staticmethod
    def sequence_generation_fitness(target_sequence: List[float]) -> Callable[[ExecutionResult], float]:
        """
        序列生成环境
        
        目标：演化出能生成指定数字序列的程序
        """
        def fitness(result: ExecutionResult) -> float:
            if not result.output:
                return 0.0
            
            # 计算序列相似度
            min_len = min(len(result.output), len(target_sequence))
            if min_len == 0:
                return 0.0
            
            matches = sum(
                1 for i in range(min_len)
                if abs(result.output[i] - target_sequence[i]) < 0.5
            )
            
            return matches / len(target_sequence)
        
        return fitness
    
    @staticmethod
    def code_efficiency_fitness() -> Callable[[ExecutionResult], float]:
        """
        代码效率环境
        
        目标：演化出执行效率最高的程序（步数最少）
        """
        def fitness(result: ExecutionResult) -> float:
            if not result.output:
                return 0.0
            
            # 鼓励输出正确且步数少
            output_bonus = min(len(result.output), 10)  # 最多10个输出
            efficiency_bonus = 1.0 / (1.0 + result.steps / 100)
            
            return output_bonus * efficiency_bonus
        
        return fitness


# ============================================================================
# 第六层：演化引擎
# ============================================================================

class EvolutionEngine:
    """
    演化引擎核心
    
    整合所有组件，实现完整的演化循环。
    """
    
    def __init__(
        self,
        population_size: int = 200,
        elite_count: int = 10,
        vm: Optional[QuaternaryVM] = None,
        mutator: Optional[Mutator] = None,
        fitness_evaluator: Optional[FitnessEvaluator] = None,
        max_generations: int = 1000,
        target_fitness: float = 0.99,
        stagnation_limit: int = 100
    ):
        """
        初始化演化引擎
        
        Args:
            population_size: 种群大小
            elite_count: 精英保留数量
            vm: 虚拟机实例
            mutator: 变异器实例
            fitness_evaluator: 适应度评估器
            max_generations: 最大代数
            target_fitness: 目标适应度
            stagnation_limit: 停滞代数限制
        """
        self.population_size = population_size
        self.elite_count = elite_count
        self.vm = vm or QuaternaryVM()
        self.mutator = mutator or Mutator()
        self.fitness_evaluator = fitness_evaluator or FitnessEvaluator(self.vm)
        self.max_generations = max_generations
        self.target_fitness = target_fitness
        self.stagnation_limit = stagnation_limit
        
        # 统计数据
        self.generation = 0
        self.population: List[Genome] = []
        self.history: List[Dict[str, Any]] = []
        self.best_ever: Optional[Genome] = None
        self.stagnation_count = 0
    
    def initialize_population(self, genome_length: int = 50):
        """初始化随机种群"""
        self.population = [
            Genome(
                sequence=''.join(random.choices('0123', k=genome_length)),
                generation=0
            )
            for _ in range(self.population_size)
        ]
        self.generation = 0
        self.history = []
        self.best_ever = None
        self.stagnation_count = 0
    
    def evaluate_population(self, fitness_func: Callable[[ExecutionResult], float]):
        """评估整个种群的适应度"""
        for genome in self.population:
            self.fitness_evaluator.evaluate(genome, fitness_func)
    
    def evolve_generation(self, fitness_func: Callable[[ExecutionResult], float]) -> Dict[str, Any]:
        """
        演化一代
        
        Returns:
            本代统计信息
        """
        # 1. 评估适应度
        self.evaluate_population(fitness_func)
        
        # 2. 统计信息
        fitnesses = [g.fitness for g in self.population]
        stats = {
            'generation': self.generation,
            'best_fitness': max(fitnesses),
            'avg_fitness': statistics.mean(fitnesses),
            'worst_fitness': min(fitnesses),
            'std_fitness': statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0,
            'avg_length': statistics.mean([g.length for g in self.population]),
            'population_size': len(self.population)
        }
        self.history.append(stats)
        
        # 3. 更新最佳个体
        current_best = max(self.population, key=lambda g: g.fitness)
        if self.best_ever is None or current_best.fitness > self.best_ever.fitness:
            self.best_ever = current_best.copy()
            self.stagnation_count = 0
        else:
            self.stagnation_count += 1
        
        # 4. 选择与繁殖
        new_population = []
        
        # 精英保留
        elites = Selector.elitism_selection(self.population, self.elite_count)
        new_population.extend(elites)
        
        # 生成新个体
        while len(new_population) < self.population_size:
            # 选择父本
            parent1 = Selector.tournament_selection(self.population, tournament_size=3)
            parent2 = Selector.tournament_selection(self.population, tournament_size=3)
            
            # 交叉
            child1, child2 = self.mutator.crossover(
                parent1, parent2, self.generation + 1
            )
            
            # 变异
            child1 = self.mutator.mutate(child1, self.generation + 1)
            child2 = self.mutator.mutate(child2, self.generation + 1)
            
            new_population.extend([child1, child2])
        
        # 调整种群大小
        self.population = new_population[:self.population_size]
        
        # 5. 代数递增
        self.generation += 1
        
        return stats
    
    def run(
        self,
        fitness_func: Callable[[ExecutionResult], float],
        verbose: bool = True,
        log_interval: int = 10
    ) -> Genome:
        """
        运行完整演化过程
        
        Args:
            fitness_func: 适应度函数
            verbose: 是否输出详细信息
            log_interval: 日志输出间隔
            
        Returns:
            最佳个体
        """
        for gen in range(self.max_generations):
            stats = self.evolve_generation(fitness_func)
            
            # 输出日志
            if verbose and gen % log_interval == 0:
                print(
                    f"Gen {gen:4d}: "
                    f"Best={stats['best_fitness']:.4f}, "
                    f"Avg={stats['avg_fitness']:.4f}, "
                    f"Std={stats['std_fitness']:.4f}, "
                    f"Len={stats['avg_length']:.1f}"
                )
            
            # 检查终止条件
            if stats['best_fitness'] >= self.target_fitness:
                if verbose:
                    print(f"\n✅ 目标达成! 代数: {gen}")
                break
            
            if self.stagnation_count >= self.stagnation_limit:
                if verbose:
                    print(f"\n⚠️ 演化停滞! 已停滞 {self.stagnation_limit} 代")
                break
        
        return self.best_ever


# ============================================================================
# 第七层：监控系统
# ============================================================================

class EvolutionMonitor:
    """
    演化监控器
    
    实时监控演化过程，检测异常行为。
    """
    
    def __init__(self):
        self.alerts: List[Dict[str, Any]] = []
        self.metrics_history: List[Dict[str, float]] = []
    
    def record_generation(self, stats: Dict[str, Any]):
        """记录代际数据"""
        self.metrics_history.append({
            'generation': stats['generation'],
            'best_fitness': stats['best_fitness'],
            'avg_fitness': stats['avg_fitness'],
            'diversity': stats.get('std_fitness', 0)
        })
    
    def check_anomalies(self) -> List[str]:
        """检测异常模式"""
        anomalies = []
        
        if len(self.metrics_history) < 10:
            return anomalies
        
        recent = self.metrics_history[-10:]
        
        # 检测适应度下降
        if recent[-1]['best_fitness'] < recent[0]['best_fitness'] * 0.9:
            anomalies.append("适应度显著下降")
        
        # 检测多样性丧失
        if recent[-1]['diversity'] < 0.01:
            anomalies.append("种群多样性丧失")
        
        # 检测振荡
        fitnesses = [m['best_fitness'] for m in recent]
        if max(fitnesses) - min(fitnesses) > 0.5:
            anomalies.append("适应度剧烈振荡")
        
        if anomalies:
            self.alerts.append({
                'generation': recent[-1]['generation'],
                'anomalies': anomalies
            })
        
        return anomalies
    
    def generate_report(self) -> str:
        """生成监控报告"""
        if not self.metrics_history:
            return "暂无数据"
        
        report = [
            "=== 演化监控报告 ===",
            f"总代数: {len(self.metrics_history)}",
            f"最佳适应度: {max(m['best_fitness'] for m in self.metrics_history):.4f}",
            f"最终适应度: {self.metrics_history[-1]['best_fitness']:.4f}",
            f"警报次数: {len(self.alerts)}",
            ""
        ]
        
        if self.alerts:
            report.append("警报历史:")
            for alert in self.alerts[-5:]:  # 最近5条
                report.append(f"  Gen {alert['generation']}: {', '.join(alert['anomalies'])}")
        
        return '\n'.join(report)


# ============================================================================
# 第八层：实验管理器
# ============================================================================

class Experiment:
    """
    实验管理器
    
    整合所有组件，提供简单的实验接口。
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        初始化实验
        
        Args:
            name: 实验名称
            config: 配置参数
        """
        self.name = name
        self.config = config or {}
        
        # 从配置创建组件
        self.vm = QuaternaryVM(
            max_steps=self.config.get('max_steps', 10000),
            max_stack_size=self.config.get('max_stack_size', 1000)
        )
        
        self.mutator = Mutator(
            point_mutation_rate=self.config.get('point_mutation_rate', 0.01),
            insertion_rate=self.config.get('insertion_rate', 0.005),
            deletion_rate=self.config.get('deletion_rate', 0.005)
        )
        
        self.engine = EvolutionEngine(
            population_size=self.config.get('population_size', 200),
            elite_count=self.config.get('elite_count', 10),
            vm=self.vm,
            mutator=self.mutator,
            max_generations=self.config.get('max_generations', 1000)
        )
        
        self.monitor = EvolutionMonitor()
        self.results: Dict[str, Any] = {}
    
    def run_scenario(
        self,
        scenario: str,
        verbose: bool = True
    ) -> Genome:
        """
        运行预设场景
        
        Args:
            scenario: 场景名称
            verbose: 是否输出详细信息
            
        Returns:
            最佳个体
        """
        print(f"\n{'='*60}")
        print(f"实验名称: {self.name}")
        print(f"场景: {scenario}")
        print(f"{'='*60}\n")
        
        # 根据场景选择适应度函数
        scenarios = {
            'target_42': Environments.target_number_fitness(42.0),
            'target_100': Environments.target_number_fitness(100.0),
            'sequence': Environments.sequence_generation_fitness([1, 2, 3, 4, 5]),
            'efficiency': Environments.code_efficiency_fitness()
        }
        
        if scenario not in scenarios:
            raise ValueError(f"未知场景: {scenario}. 可用场景: {list(scenarios.keys())}")
        
        fitness_func = scenarios[scenario]
        
        # 初始化种群
        self.engine.initialize_population(
            genome_length=self.config.get('genome_length', 50)
        )
        
        # 运行演化
        best_genome = self.engine.run(fitness_func, verbose=verbose)
        
        # 记录结果
        self.results = {
            'best_genome': best_genome,
            'best_fitness': best_genome.fitness,
            'generations': self.engine.generation,
            'history': self.engine.history
        }
        
        # 生成报告
        print(f"\n{'='*60}")
        print("实验完成!")
        print(f"最佳适应度: {best_genome.fitness:.6f}")
        print(f"总代数: {self.engine.generation}")
        print(f"基因长度: {best_genome.length}")
        print(f"基因序列: {best_genome.sequence[:50]}...")
        
        # 执行最佳程序并显示结果
        result = self.vm.execute(best_genome)
        print(f"执行结果: 输出={result.output[:10]}, 步数={result.steps}")
        
        # 监控报告
        for stats in self.engine.history:
            self.monitor.record_generation(stats)
        print("\n" + self.monitor.generate_report())
        
        return best_genome
    
    def save_results(self, filepath: str):
        """保存实验结果"""
        data = {
            'name': self.name,
            'config': self.config,
            'results': {
                'best_fitness': self.results['best_fitness'],
                'generations': self.results['generations'],
                'best_genome': self.results['best_genome'].sequence,
                'history': self.results['history']
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"结果已保存到: {filepath}")


# ============================================================================
# 第九层：命令行界面
# ============================================================================

def main():
    """主程序入口"""
    print("""
╔══════════════════════════════════════════════════════════╗
║       四进制基因编程演化实验系统 v1.0                    ║
║   Quaternary Genetic Programming Evolution System        ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 实验1：演化计算目标数值42
    print("\n[实验1] 目标：演化出能输出42的程序")
    exp1 = Experiment(
        name="目标数值演化",
        config={
            'population_size': 300,
            'max_generations': 500,
            'point_mutation_rate': 0.02,
            'genome_length': 60
        }
    )
    best1 = exp1.run_scenario('target_42', verbose=True)
    
    print("\n" + "="*60)
    print("按Enter键继续下一个实验...")
    input()
    
    # 实验2：演化生成数字序列
    print("\n[实验2] 目标：演化出能生成序列[1,2,3,4,5]的程序")
    exp2 = Experiment(
        name="序列生成",
        config={
            'population_size': 200,
            'max_generations': 300,
            'genome_length': 80
        }
    )
    best2 = exp2.run_scenario('sequence', verbose=True)
    
    print("\n" + "="*60)
    print("\n🎉 所有实验完成!")
    print("\n涌现现象观察提示：")
    print("1. 观察基因序列是否形成了可识别的模式")
    print("2. 检查是否出现了重复的'基因模块'")
    print("3. 分析不同实验中相似的解决方案")
    print("4. 查看是否有非预期的优化策略出现")
    
    # 保存结果
    exp1.save_results('experiment1_results.json')
    exp2.save_results('experiment2_results.json')


if __name__ == '__main__':
    main()
