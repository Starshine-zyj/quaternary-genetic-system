#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四进制基因编程演化系统 - 图形化界面
基于Tkinter的可视化实验平台
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from typing import Optional

from genetic_evolution import (
    EvolutionEngine, Environments, Genome, QuaternaryVM
)


class EvolutionGUI:
    """演化系统图形化界面"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("四进制基因编程演化系统")
        self.root.geometry("1200x800")
        
        self.engine: Optional[EvolutionEngine] = None
        self.is_running = False
        self.update_queue = queue.Queue()
        
        self._create_widgets()
        self._schedule_update()
        
    def _create_widgets(self):
        """创建界面组件"""
        # 顶部控制面板
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # 参数配置
        params_frame = ttk.LabelFrame(control_frame, text="演化参数", padding="10")
        params_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 种群大小
        ttk.Label(params_frame, text="种群大小:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pop_size_var = tk.StringVar(value="100")
        ttk.Entry(params_frame, textvariable=self.pop_size_var, width=10).grid(row=0, column=1, padx=5)
        
        # 基因长度
        ttk.Label(params_frame, text="基因长度:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.genome_len_var = tk.StringVar(value="40")
        ttk.Entry(params_frame, textvariable=self.genome_len_var, width=10).grid(row=1, column=1, padx=5)
        
        # 最大代数
        ttk.Label(params_frame, text="最大代数:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.max_gen_var = tk.StringVar(value="1000")
        ttk.Entry(params_frame, textvariable=self.max_gen_var, width=10).grid(row=2, column=1, padx=5)
        
        # 变异率
        ttk.Label(params_frame, text="变异率:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20,0))
        self.mutation_rate_var = tk.StringVar(value="0.01")
        ttk.Entry(params_frame, textvariable=self.mutation_rate_var, width=10).grid(row=0, column=3, padx=5)
        
        # 交叉率
        ttk.Label(params_frame, text="交叉率:").grid(row=1, column=2, sticky=tk.W, pady=2, padx=(20,0))
        self.crossover_rate_var = tk.StringVar(value="0.7")
        ttk.Entry(params_frame, textvariable=self.crossover_rate_var, width=10).grid(row=1, column=3, padx=5)
        
        # 精英数量
        ttk.Label(params_frame, text="精英数量:").grid(row=2, column=2, sticky=tk.W, pady=2, padx=(20,0))
        self.elite_size_var = tk.StringVar(value="5")
        ttk.Entry(params_frame, textvariable=self.elite_size_var, width=10).grid(row=2, column=3, padx=5)
        
        # 实验环境选择
        env_frame = ttk.LabelFrame(control_frame, text="实验环境", padding="10")
        env_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        self.env_var = tk.StringVar(value="target_number")
        environments = [
            ("目标数值", "target_number"),
            ("序列生成", "sequence_generation"),
            ("代码效率", "code_efficiency"),
            ("算术运算", "arithmetic"),
            ("模式识别", "pattern_recognition"),
        ]
        
        for i, (text, value) in enumerate(environments):
            ttk.Radiobutton(env_frame, text=text, variable=self.env_var, 
                          value=value).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # 环境参数
        ttk.Label(env_frame, text="目标值:").grid(row=5, column=0, sticky=tk.W, pady=(10,2))
        self.target_var = tk.StringVar(value="42.0")
        ttk.Entry(env_frame, textvariable=self.target_var, width=15).grid(row=6, column=0, pady=2)
        
        # 控制按钮
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        self.start_btn = ttk.Button(btn_frame, text="开始演化", command=self._start_evolution, width=12)
        self.start_btn.pack(pady=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self._stop_evolution, 
                                   width=12, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)
        
        self.reset_btn = ttk.Button(btn_frame, text="重置", command=self._reset, width=12)
        self.reset_btn.pack(pady=5)
        
        # 主显示区域
        main_frame = ttk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：实时日志
        log_frame = ttk.LabelFrame(main_frame, text="演化日志", padding="5")
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=60, height=30, 
                                                  font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 右侧：统计信息和最佳个体
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(right_frame, text="实时统计", padding="10")
        stats_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0,5))
        
        stats_labels = [
            ("当前代数:", "generation"),
            ("最佳适应度:", "best_fitness"),
            ("平均适应度:", "avg_fitness"),
            ("种群多样性:", "diversity"),
            ("运行时间:", "elapsed"),
        ]
        
        self.stat_vars = {}
        for i, (label, key) in enumerate(stats_labels):
            ttk.Label(stats_frame, text=label, font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky=tk.W, pady=5)
            var = tk.StringVar(value="--")
            self.stat_vars[key] = var
            ttk.Label(stats_frame, textvariable=var, font=("Arial", 12)).grid(
                row=i, column=1, sticky=tk.E, pady=5, padx=(20,0))
        
        # 最佳个体
        best_frame = ttk.LabelFrame(right_frame, text="最佳基因组", padding="10")
        best_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.best_text = scrolledtext.ScrolledText(best_frame, width=50, height=15,
                                                   font=("Consolas", 9))
        self.best_text.pack(fill=tk.BOTH, expand=True)
        
        # 执行结果
        result_frame = ttk.LabelFrame(right_frame, text="执行结果", padding="10")
        result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5,0))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=50, height=8,
                                                     font=("Consolas", 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def _start_evolution(self):
        """开始演化"""
        try:
            # 获取参数
            pop_size = int(self.pop_size_var.get())
            genome_len = int(self.genome_len_var.get())
            max_gen = int(self.max_gen_var.get())
            mutation_rate = float(self.mutation_rate_var.get())
            crossover_rate = float(self.crossover_rate_var.get())
            elite_size = int(self.elite_size_var.get())
            
            # 创建演化引擎
            self.engine = EvolutionEngine(
                population_size=pop_size,
                genome_length=genome_len,
                mutation_rate=mutation_rate,
                crossover_rate=crossover_rate,
                elite_size=elite_size,
                max_generations=max_gen
            )
            
            # 选择适应度函数
            env = self.env_var.get()
            if env == "target_number":
                target = float(self.target_var.get())
                fitness_func = Environments.target_number_fitness(target)
            elif env == "sequence_generation":
                fitness_func = Environments.sequence_generation_fitness([1, 2, 3, 4, 5])
            elif env == "code_efficiency":
                fitness_func = Environments.code_efficiency_fitness()
            elif env == "arithmetic":
                fitness_func = Environments.arithmetic_fitness()
            elif env == "pattern_recognition":
                fitness_func = Environments.pattern_recognition_fitness()
            else:
                fitness_func = Environments.target_number_fitness(42.0)
            
            # 更新UI状态
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("演化运行中...")
            
            # 清空日志
            self.log_text.delete(1.0, tk.END)
            
            # 在新线程中运行演化
            thread = threading.Thread(target=self._run_evolution, 
                                     args=(fitness_func,), daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动演化失败: {str(e)}")
            
    def _run_evolution(self, fitness_func):
        """在后台线程运行演化"""
        start_time = time.time()
        
        def callback(result):
            elapsed = time.time() - start_time
            result['elapsed'] = elapsed
            self.update_queue.put(('update', result))
            return self.is_running
        
        try:
            self.engine.run(fitness_func, verbose=False, callback=callback)
            self.update_queue.put(('finished', None))
        except Exception as e:
            self.update_queue.put(('error', str(e)))
            
    def _stop_evolution(self):
        """停止演化"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("已停止")
        
    def _reset(self):
        """重置"""
        self._stop_evolution()
        self.log_text.delete(1.0, tk.END)
        self.best_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        for var in self.stat_vars.values():
            var.set("--")
        self.status_var.set("就绪")
        
    def _schedule_update(self):
        """定时更新UI"""
        try:
            while True:
                msg_type, data = self.update_queue.get_nowait()
                
                if msg_type == 'update':
                    self._update_display(data)
                elif msg_type == 'finished':
                    self._on_finished()
                elif msg_type == 'error':
                    self._on_error(data)
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self._schedule_update)
        
    def _update_display(self, result):
        """更新显示"""
        # 更新统计信息
        self.stat_vars['generation'].set(str(result['generation']))
        self.stat_vars['best_fitness'].set(f"{result['best_fitness']:.4f}")
        self.stat_vars['avg_fitness'].set(f"{result['avg_fitness']:.4f}")
        self.stat_vars['diversity'].set(f"{result['diversity']:.4f}")
        self.stat_vars['elapsed'].set(f"{result['elapsed']:.2f}s")
        
        # 更新日志
        if result['generation'] % 10 == 0:
            log_msg = f"{result['stats']}\n"
            self.log_text.insert(tk.END, log_msg)
            self.log_text.see(tk.END)
        
        # 更新最佳个体
        best = result['best_genome']
        self.best_text.delete(1.0, tk.END)
        self.best_text.insert(tk.END, f"代数: {best.generation}\n")
        self.best_text.insert(tk.END, f"适应度: {best.fitness:.6f}\n")
        self.best_text.insert(tk.END, f"长度: {len(best.sequence)}\n")
        self.best_text.insert(tk.END, f"变异数: {best.mutations}\n\n")
        self.best_text.insert(tk.END, f"基因序列:\n{best.sequence}\n\n")
        
        # 显示执行结果
        vm = QuaternaryVM()
        exec_result = vm.execute(best)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{exec_result}\n\n")
        if exec_result.output:
            self.result_text.insert(tk.END, f"输出值: {exec_result.output}\n")
        
    def _on_finished(self):
        """演化完成"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("演化完成")
        messagebox.showinfo("完成", "演化实验已完成!")
        
    def _on_error(self, error_msg):
        """发生错误"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("错误")
        messagebox.showerror("错误", f"演化过程出错: {error_msg}")


def main():
    """主函数"""
    root = tk.Tk()
    app = EvolutionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
