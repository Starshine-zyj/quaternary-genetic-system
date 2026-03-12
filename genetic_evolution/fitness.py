#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
适应度评估模块
定义多种实验环境和评估函数
"""

from typing import Callable, List
from .genome import Genome
from .vm import QuaternaryVM


class FitnessEvaluator:
    """适应度评估器"""
    
    def __init__(self, vm: QuaternaryVM):
        self.vm = vm
    
    def evaluate(self, genome: Genome, fitness_func: Callable) -> float:
        """评估单个基因组的适应度"""
        try:
            fitness = fitness_func(genome, self.vm)
            genome.fitness = fitness
            return fitness
        except Exception as e:
            genome.fitness = 0.0
            return 0.0


class Environments:
    """预定义实验环境"""
    
    @staticmethod
    def target_number_fitness(target: float) -> Callable:
        """
        目标数值环境：程序输出尽可能接近目标值
        
        适应度范围：0.0 - 1.0
        - 输出完全匹配目标 → 1.0
        - 没有输出 → 0.0
        """
        def fitness(genome: Genome, vm: QuaternaryVM) -> float:
            result = vm.execute(genome, inputs=[])
            
            # 没有输出或执行失败
            if not result.success or not result.output:
                return 0.0
            
            # 计算与目标的距离
            output_value = result.output[-1] if result.output else 0.0
            distance = abs(target - output_value)
            
            # 适应度：距离越小越好，理论上限 = 1.0
            fitness_value = 1.0 / (1.0 + distance)
            
            return fitness_value
        
        return fitness
    
    @staticmethod
    def sequence_generation_fitness(target_sequence: List[float]) -> Callable:
        """序列生成环境：输出指定序列"""
        def fitness(genome: Genome, vm: QuaternaryVM) -> float:
            result = vm.execute(genome, inputs=[])
            if not result.success:
                return 0.0
            
            # 计算序列相似度
            score = 0.0
            for i, target_val in enumerate(target_sequence):
                if i < len(result.output):
                    distance = abs(target_val - result.output[i])
                    score += 100.0 / (1.0 + distance)
            
            # 惩罚长度不匹配
            length_penalty = abs(len(target_sequence) - len(result.output)) * 10
            
            return max(0, score - length_penalty)
        
        return fitness
    
    @staticmethod
    def code_efficiency_fitness() -> Callable:
        """代码效率环境：用最少步数完成计算"""
        def fitness(genome: Genome, vm: QuaternaryVM) -> float:
            result = vm.execute(genome, inputs=[1.0, 2.0, 3.0])
            if not result.success or not result.output:
                return 0.0
            
            # 奖励产生输出
            output_score = len(result.output) * 50
            
            # 奖励步数少
            efficiency_score = max(0, (5000 - result.steps) / 10)
            
            return output_score + efficiency_score
        
        return fitness
    
    @staticmethod
    def arithmetic_fitness() -> Callable:
        """算术环境：计算输入数字的和"""
        def fitness(genome: Genome, vm: QuaternaryVM) -> float:
            test_cases = [
                ([1.0, 2.0], 3.0),
                ([5.0, 7.0], 12.0),
                ([10.0, 20.0], 30.0),
                ([3.0, 4.0], 7.0),
            ]
            
            total_score = 0.0
            for inputs, expected in test_cases:
                result = vm.execute(genome, inputs=inputs)
                if result.success and result.output:
                    output = result.output[-1]
                    distance = abs(expected - output)
                    total_score += 100.0 / (1.0 + distance)
            
            return total_score
        
        return fitness
    
    @staticmethod
    def pattern_recognition_fitness() -> Callable:
        """模式识别环境：识别输入序列的规律"""
        def fitness(genome: Genome, vm: QuaternaryVM) -> float:
            # 测试识别等差数列
            test_cases = [
                ([1.0, 2.0, 3.0], 4.0),  # 下一个是4
                ([2.0, 4.0, 6.0], 8.0),  # 下一个是8
                ([5.0, 10.0, 15.0], 20.0),  # 下一个是20
            ]
            
            total_score = 0.0
            for inputs, expected in test_cases:
                result = vm.execute(genome, inputs=inputs)
                if result.success and result.output:
                    output = result.output[-1]
                    distance = abs(expected - output)
                    total_score += 150.0 / (1.0 + distance)
            
            return total_score
        
        return fitness
