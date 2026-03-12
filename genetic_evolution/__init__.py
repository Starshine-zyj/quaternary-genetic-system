#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四进制基因编程演化系统
"""

from .genome import Genome, ExecutionResult, GenerationStats
from .vm import QuaternaryVM
from .mutator import Mutator
from .selector import Selector
from .fitness import FitnessEvaluator, Environments
from .engine import EvolutionEngine

__version__ = '1.0.0'
__all__ = [
    'Genome',
    'ExecutionResult',
    'GenerationStats',
    'QuaternaryVM',
    'Mutator',
    'Selector',
    'FitnessEvaluator',
    'Environments',
    'EvolutionEngine',
]
