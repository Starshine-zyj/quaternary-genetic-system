#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四进制基因编程演化系统 v2.1 - 图形化界面
增强版：支持自定义DNA输入、修复适应度显示、优化初始化
v2.1 新增：导出最佳基因、分析指令序列（3个分析标签页）
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
    """演化系统图形化界面 v2.0"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("四进制基因编程演化系统 v2.1 - by yingjiezhu")
        self.root.geometry("1400x900")
        
        self.engine: Optional[EvolutionEngine] = None
        self.is_running = False
        self.update_queue = queue.Queue()
        self.best_genome: Optional[Genome] = None  # 保存最佳基因组
        
        self._create_widgets()
        self._schedule_update()
        
    def _create_widgets(self):
        """创建界面组件"""
        # 创建notebook用于分页
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 配置页
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="🎛️ 参数配置")
        self._create_config_page(config_frame)
        
        # DNA输入页
        dna_frame = ttk.Frame(notebook)
        notebook.add(dna_frame, text="🧬 DNA输入")
        self._create_dna_page(dna_frame)
        
        # 演化监控页
        monitor_frame = ttk.Frame(notebook)
        notebook.add(monitor_frame, text="📊 演化监控")
        self._create_monitor_page(monitor_frame)
        
        # 底部控制栏
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.start_btn = ttk.Button(control_frame, text="▶ 开始演化", 
                                    command=self._start_evolution, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="⏸ 暂停", 
                                   command=self._stop_evolution, 
                                   width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(control_frame, text="🔄 重置", 
                                    command=self._reset, width=15)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="✓ 就绪")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                font=("Arial", 10, "bold"))
        status_label.pack(side=tk.RIGHT, padx=10)
        
    def _create_config_page(self, parent):
        """创建配置页面"""
        # 左侧：基本参数
        left_frame = ttk.LabelFrame(parent, text="基本参数", padding="15")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        params = [
            ("种群大小:", "pop_size", "100", "个体数量，建议50-500"),
            ("基因长度:", "genome_len", "120", "四进制长度，建议80-200"),
            ("最大代数:", "max_gen", "1000", "演化代数，建议500-5000"),
            ("变异率:", "mutation_rate", "0.01", "基因突变概率，建议0.001-0.1"),
            ("交叉率:", "crossover_rate", "0.7", "基因重组概率，建议0.6-0.9"),
            ("精英数量:", "elite_size", "5", "保留最优个体数，建议3-10"),
        ]
        
        self.param_vars = {}
        for i, (label, key, default, hint) in enumerate(params):
            ttk.Label(left_frame, text=label, font=("Arial", 10)).grid(
                row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            var = tk.StringVar(value=default)
            self.param_vars[key] = var
            entry = ttk.Entry(left_frame, textvariable=var, width=20, font=("Arial", 11))
            entry.grid(row=i, column=1, sticky=tk.W, pady=8)
            
            ttk.Label(left_frame, text=hint, foreground="gray", 
                     font=("Arial", 8)).grid(row=i, column=2, sticky=tk.W, 
                                            padx=(10, 0), pady=8)
        
        # 右侧：实验环境
        right_frame = ttk.LabelFrame(parent, text="实验环境", padding="15")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.env_var = tk.StringVar(value="target_number")
        environments = [
            ("🎯 目标数值演化", "target_number", "让程序输出特定数值"),
            ("📝 序列生成", "sequence_generation", "生成特定数字序列"),
            ("⚡ 代码效率优化", "code_efficiency", "用最少步数完成计算"),
            ("➕ 算术运算学习", "arithmetic", "学习加法运算"),
            ("🔍 模式识别", "pattern_recognition", "识别等差数列规律"),
        ]
        
        for i, (text, value, desc) in enumerate(environments):
            frame = ttk.Frame(right_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Radiobutton(frame, text=text, variable=self.env_var, 
                          value=value).pack(side=tk.LEFT)
            ttk.Label(frame, text=f"  ({desc})", foreground="gray",
                     font=("Arial", 8)).pack(side=tk.LEFT)
        
        # 环境参数
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        param_frame = ttk.Frame(right_frame)
        param_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(param_frame, text="目标值:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.target_var = tk.StringVar(value="42.0")
        ttk.Entry(param_frame, textvariable=self.target_var, width=15, 
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        ttk.Label(param_frame, text="(仅用于目标数值环境)", 
                 foreground="gray", font=("Arial", 8)).pack(side=tk.LEFT)
        
    def _create_dna_page(self, parent):
        """创建DNA输入页面"""
        # 说明区域
        info_frame = ttk.LabelFrame(parent, text="ℹ️ 使用说明", padding="15")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = """
        🧬 自定义DNA功能说明：
        
        1. 您可以输入真实物种的DNA序列（ATCG格式）或四进制序列（0123格式）
        2. 系统会将DNA序列映射为四进制编码：A→0, T→1, C→2, G→3
        3. 导入的DNA将作为种群的种子基因，其他个体通过变异生成
        4. 支持多行输入，系统会自动忽略空格、换行和注释行
        5. 建议长度：80-500个碱基
        
        💡 应用场景：
        - 研究真实基因序列的计算潜力
        - 测试生物信息学假设
        - 探索DNA编码的数学性质
        """
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT,
                 font=("Arial", 9)).pack(anchor=tk.W)
        
        # DNA输入区域
        input_frame = ttk.LabelFrame(parent, text="🧬 DNA序列输入", padding="15")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 开关
        self.use_custom_dna = tk.BooleanVar(value=False)
        ttk.Checkbutton(input_frame, text="✅ 使用自定义DNA初始化种群", 
                       variable=self.use_custom_dna,
                       style="Switch.TCheckbutton").pack(anchor=tk.W, pady=5)
        
        # 文本输入
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.dna_text = scrolledtext.ScrolledText(text_frame, width=80, height=15,
                                                  font=("Consolas", 10), wrap=tk.WORD)
        self.dna_text.pack(fill=tk.BOTH, expand=True)
        
        # 示例按钮
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="📘 人类胰岛素基因", 
                  command=lambda: self._load_example("insulin")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🦠 大肠杆菌lacZ基因", 
                  command=lambda: self._load_example("lacz")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🧪 随机四进制序列", 
                  command=lambda: self._load_example("random")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ 清除", 
                  command=lambda: self.dna_text.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=5)
        
        # 统计信息
        self.dna_stats_var = tk.StringVar(value="")
        ttk.Label(input_frame, textvariable=self.dna_stats_var, 
                 foreground="blue", font=("Arial", 9)).pack(anchor=tk.W)
        
        # 实时统计
        def update_stats(*args):
            content = self.dna_text.get('1.0', tk.END).strip()
            if content:
                clean = ''.join(c for c in content.upper() if c in 'ATCG0123')
                atcg = sum(1 for c in clean if c in 'ATCG')
                quat = sum(1 for c in clean if c in '0123')
                self.dna_stats_var.set(
                    f"📊 统计：总长度 {len(clean)} 个碱基 "
                    f"(DNA: {atcg}, 四进制: {quat})"
                )
            else:
                self.dna_stats_var.set("")
        
        self.dna_text.bind('<KeyRelease>', update_stats)
        
    def _create_monitor_page(self, parent):
        """创建监控页面"""
        # 左侧：日志和统计
        left_panel = ttk.Frame(parent)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,5), pady=10)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(left_panel, text="📊 实时统计", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0,10))
        
        stats_labels = [
            ("当前代数", "generation", "0"),
            ("最佳适应度", "best_fitness", "0.0000"),
            ("平均适应度", "avg_fitness", "0.0000"),
            ("种群多样性", "diversity", "0.0000"),
            ("运行时间", "elapsed", "0.00s"),
        ]
        
        self.stat_vars = {}
        for i, (label, key, default) in enumerate(stats_labels):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=10, pady=8)
            
            ttk.Label(frame, text=f"{label}:", font=("Arial", 9)).pack(side=tk.LEFT)
            var = tk.StringVar(value=default)
            self.stat_vars[key] = var
            ttk.Label(frame, textvariable=var, font=("Arial", 12, "bold"),
                     foreground="blue").pack(side=tk.LEFT, padx=(10, 0))
        
        # ✅ 添加进度条
        progress_frame = ttk.Frame(stats_frame)
        progress_frame.grid(row=3, column=0, columnspan=4, sticky=tk.EW, padx=10, pady=10)
        
        ttk.Label(progress_frame, text="进度:", font=("Arial", 9)).pack(side=tk.LEFT)
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.progress_label = tk.StringVar(value="0%")
        ttk.Label(progress_frame, textvariable=self.progress_label,
                 font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        # 演化日志
        log_frame = ttk.LabelFrame(left_panel, text="📜 演化日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # 日志工具栏
        log_toolbar = ttk.Frame(log_frame)
        log_toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(log_toolbar, text="📥 导出日志", 
                  command=self._export_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(log_toolbar, text="🗑️ 清空日志", 
                  command=self._clear_log).pack(side=tk.LEFT, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=60, height=25,
                                                  font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 右侧：最佳个体
        right_panel = ttk.Frame(parent)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5,10), pady=10)
        
        # 最佳基因组
        best_frame = ttk.LabelFrame(right_panel, text="🏆 最佳基因组", padding="10")
        best_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        # 添加工具栏
        best_toolbar = ttk.Frame(best_frame)
        best_toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(best_toolbar, text="📥 导出基因", 
                  command=self._export_best_genome).pack(side=tk.LEFT, padx=5)
        ttk.Button(best_toolbar, text="🔍 分析指令", 
                  command=self._analyze_instructions).pack(side=tk.LEFT, padx=5)
        
        self.best_text = scrolledtext.ScrolledText(best_frame, width=50, height=15,
                                                   font=("Consolas", 9))
        self.best_text.pack(fill=tk.BOTH, expand=True)
        
        # 执行结果
        result_frame = ttk.LabelFrame(right_panel, text="⚙️ 虚拟机执行结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=50, height=10,
                                                     font=("Consolas", 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def _load_example(self, example_name):
        """加载示例DNA"""
        examples = {
            "insulin": (
                "# 人类胰岛素基因（INS）部分序列\n"
                "# 来源：人类11号染色体，编码胰岛素激素\n"
                "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCT\n"
                "GACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCT\n"
                "CTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAG\n"
                "GCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGC\n"
                "CTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGC"
            ),
            "lacz": (
                "# 大肠杆菌lacZ基因部分序列\n"
                "# 编码β-半乳糖苷酶，用于乳糖代谢\n"
                "ATGACCATGATTACGAATTCGAGCTCGGTACCCGGGGATCCTCTAGAGTCGACCTGC\n"
                "AGGCATGCAAGCTTGGCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCT\n"
                "GGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAAT\n"
                "AGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAA"
            ),
            "random": (
                "# 随机四进制序列（修正版 - 3位操作码格式）\n"
                "# 格式：3位操作码 + 1位操作数\n"
                "# PUSH(2) → OUTPUT → HALT 循环\n"
                "0012"  # PUSH(2) - opcode=001(4)=1, operand=2
                "3010"  # OUTPUT - opcode=301(4)=49
                "3020"  # HALT - opcode=302(4)=50
                "0000"  # NOP
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010" "3020" "0000"
                "0012" "3010"  # 最后2条指令（总共168个数字/42条指令）
            )
        }
        
        if example_name in examples:
            self.dna_text.delete('1.0', tk.END)
            self.dna_text.insert('1.0', examples[example_name])
            self.use_custom_dna.set(True)
            self._log(f"✓ 已加载示例：{example_name}")
            
    def _start_evolution(self):
        """开始演化"""
        try:
            # ✅ 立即更新UI状态，给用户反馈
            self.start_btn.config(state=tk.DISABLED)
            self.status_var.set("⏳ 正在初始化...")
            self._log("⏳ 正在读取参数和初始化引擎...")
            
            # 强制更新UI
            self.root.update_idletasks()
            
            # 获取参数
            pop_size = int(self.param_vars['pop_size'].get())
            genome_len = int(self.param_vars['genome_len'].get())
            max_gen = int(self.param_vars['max_gen'].get())
            mutation_rate = float(self.param_vars['mutation_rate'].get())
            crossover_rate = float(self.param_vars['crossover_rate'].get())
            elite_size = int(self.param_vars['elite_size'].get())
            
            # 参数验证
            if not (10 <= pop_size <= 10000):
                raise ValueError("种群大小应在10-10000之间")
            if not (20 <= genome_len <= 10000):
                raise ValueError("基因长度应在20-10000之间")
            
            # 准备种子基因组
            seed_genomes = None
            if self.use_custom_dna.get():
                self.status_var.set("⏳ 正在解析DNA序列...")
                self.root.update_idletasks()
                
                dna_input = self.dna_text.get('1.0', tk.END)
                clean_dna = self._parse_dna(dna_input)
                
                if clean_dna:
                    self._log(f"✓ 解析DNA序列：{len(clean_dna)} 个碱基")
                    seed_genome = Genome.from_dna(clean_dna, generation=0)
                    seed_genomes = [seed_genome]
                    self._log(f"✓ 转换为四进制：{seed_genome.sequence[:80]}...")
                else:
                    self._log("⚠ 未检测到有效DNA，使用随机初始化")
            
            # 创建引擎
            self.status_var.set("⏳ 正在创建演化引擎...")
            self.root.update_idletasks()
            
            self.engine = EvolutionEngine(
                population_size=pop_size,
                genome_length=genome_len,
                mutation_rate=mutation_rate,
                crossover_rate=crossover_rate,
                elite_size=elite_size,
                max_generations=max_gen
            )
            
            # 初始化种群
            self.status_var.set(f"⏳ 正在初始化种群({pop_size}个个体)...")
            self.root.update_idletasks()
            
            self.engine.initialize_population(seed_genomes=seed_genomes)
            
            # 选择适应度函数
            fitness_func = self._get_fitness_function()
            
            # 开始演化
            self.is_running = True
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("🏃 演化运行中...")
            
            self._log("="*60)
            self._log(f"🚀 演化实验启动")
            self._log(f"📊 种群大小: {pop_size}, 基因长度: {genome_len}")
            self._log(f"🎯 环境: {self.env_var.get()}")
            if seed_genomes:
                self._log(f"🧬 使用自定义DNA初始化")
            self._log("="*60)
            
            # 启动线程
            thread = threading.Thread(target=self._run_evolution,
                                     args=(fitness_func,), daemon=True)
            thread.start()
            
        except Exception as e:
            self.start_btn.config(state=tk.NORMAL)
            self.status_var.set("❌ 启动失败")
            messagebox.showerror("错误", f"启动失败：{str(e)}")
            
    def _parse_dna(self, text):
        """解析DNA序列"""
        clean = []
        for line in text.split('\n'):
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            # 提取ATCG和0123
            for c in line.upper():
                if c in 'ATCG0123':
                    clean.append(c)
        return ''.join(clean)
    
    def _get_fitness_function(self):
        """获取适应度函数"""
        env = self.env_var.get()
        
        if env == "target_number":
            target = float(self.target_var.get())
            return Environments.target_number_fitness(target)
        elif env == "sequence_generation":
            return Environments.sequence_generation_fitness([1, 2, 3, 4, 5])
        elif env == "code_efficiency":
            return Environments.code_efficiency_fitness()
        elif env == "arithmetic":
            return Environments.arithmetic_fitness()
        elif env == "pattern_recognition":
            return Environments.pattern_recognition_fitness()
        else:
            return Environments.target_number_fitness(42.0)
    
    def _run_evolution(self, fitness_func):
        """运行演化（后台线程）"""
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
        self.status_var.set("⏸ 已暂停")
        self._log("⏸ 演化已暂停")
        
    def _reset(self):
        """重置"""
        self._stop_evolution()
        self.log_text.delete('1.0', tk.END)
        self.best_text.delete('1.0', tk.END)
        self.result_text.delete('1.0', tk.END)
        
        for var in self.stat_vars.values():
            var.set("--")
        
        # ✅ 重置进度条
        self.progress_var.set(0)
        self.progress_label.set("0%")
        
        self.status_var.set("✓ 就绪")
        self._log("🔄 系统已重置\n")
        
    def _schedule_update(self):
        """定时更新UI（优化版：批量处理消息）"""
        try:
            # ✅ 批量处理队列中的消息，避免逐个处理导致的延迟
            processed = 0
            max_batch = 10  # 每次最多处理10条消息
            
            while processed < max_batch:
                msg_type, data = self.update_queue.get_nowait()
                
                if msg_type == 'update':
                    self._update_display(data)
                elif msg_type == 'finished':
                    self._on_finished()
                elif msg_type == 'error':
                    self._on_error(data)
                
                processed += 1
                    
        except queue.Empty:
            pass
        
        # ✅ 增加UI更新频率（100ms → 50ms），提高响应速度
        self.root.after(50, self._schedule_update)
        
    def _update_display(self, result):
        """更新显示（优化版：减少UI操作）"""
        generation = result['generation']
        
        # ✅ 始终更新统计数字（轻量级操作）
        self.stat_vars['generation'].set(str(generation))
        self.stat_vars['best_fitness'].set(f"{result['best_fitness']:.4f}")
        self.stat_vars['avg_fitness'].set(f"{result['avg_fitness']:.4f}")
        self.stat_vars['diversity'].set(f"{result['diversity']:.4f}")
        self.stat_vars['elapsed'].set(f"{result['elapsed']:.2f}s")
        
        # ✅ 更新进度条
        if self.engine and self.engine.max_generations > 0:
            progress = int((generation / self.engine.max_generations) * 100)
            self.progress_var.set(progress)
            self.progress_label.set(f"{progress}%")
        
        # ✅ 降低日志更新频率（从每10代改为每20代）
        if generation % 20 == 0 or generation == 1:
            self._log(str(result['stats']))
        
        # ✅ 降低最佳个体更新频率（从每代更新改为每10代）
        if generation % 10 == 0 or generation == 1:
            best = result['best_genome']
            self.best_genome = best  # 保存最佳基因组引用
            self.best_text.delete('1.0', tk.END)
            
            # 使用单次insert减少操作次数
            info = (
                f"🏆 代数: {best.generation}\n"
                f"💯 适应度: {best.fitness:.6f}\n"
                f"📏 长度: {len(best.sequence)}\n"
                f"🧬 变异数: {best.mutations}\n\n"
                f"基因序列:\n{best.sequence}\n"
            )
            self.best_text.insert(tk.END, info)
        
        # ✅ 降低执行结果更新频率（从每代更新改为每10代）
        if generation % 10 == 0 or generation == 1:
            best = result['best_genome']
            vm = QuaternaryVM()
            exec_result = vm.execute(best)
            
            self.result_text.delete('1.0', tk.END)
            
            # 使用单次insert减少操作次数
            output_info = ""
            if exec_result.output:
                output_info = (
                    f"输出值: {exec_result.output[-1]:.6f}\n"
                    f"所有输出: {exec_result.output}\n"
                )
            
            error_info = f"\n错误: {exec_result.error}\n" if exec_result.error else ""
            
            result_info = (
                f"执行状态: {'✓ 成功' if exec_result.success else '✗ 失败'}\n"
                f"执行步数: {exec_result.steps}\n"
                f"{output_info}"
                f"{error_info}"
            )
            self.result_text.insert(tk.END, result_info)
    
    def _on_finished(self):
        """演化完成"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("✅ 演化完成")
        self._log("\n" + "="*60)
        self._log("✅ 演化实验完成！")
        self._log("="*60)
        messagebox.showinfo("完成", "演化实验已完成！")
        
    def _on_error(self, error_msg):
        """发生错误"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("❌ 错误")
        self._log(f"❌ 错误: {error_msg}")
        messagebox.showerror("错误", f"演化过程出错：{error_msg}")
    
    def _log(self, message):
        """写入日志"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def _export_log(self):
        """导出日志到文件"""
        try:
            from datetime import datetime
            from tkinter import filedialog
            
            # 获取日志内容
            log_content = self.log_text.get('1.0', tk.END).strip()
            
            if not log_content:
                messagebox.showwarning("警告", "日志为空，无法导出")
                return
            
            # 生成默认文件名（包含时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"evolution_log_{timestamp}.txt"
            
            # 打开保存对话框
            filepath = filedialog.asksaveasfilename(
                title="导出日志",
                defaultextension=".txt",
                initialfile=default_filename,
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("日志文件", "*.log"),
                    ("所有文件", "*.*")
                ]
            )
            
            if filepath:
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    # 添加元数据头部
                    f.write("=" * 80 + "\n")
                    f.write("四进制基因编程演化系统 v2.0 - 演化日志\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"当前代数: {self.stat_vars['generation'].get()}\n")
                    f.write(f"最佳适应度: {self.stat_vars['best_fitness'].get()}\n")
                    f.write(f"平均适应度: {self.stat_vars['avg_fitness'].get()}\n")
                    f.write(f"种群多样性: {self.stat_vars['diversity'].get()}\n")
                    f.write(f"运行时间: {self.stat_vars['elapsed'].get()}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    # 写入日志内容
                    f.write(log_content)
                    f.write("\n\n" + "=" * 80 + "\n")
                    f.write("日志导出完成\n")
                
                messagebox.showinfo("成功", f"日志已导出至:\n{filepath}")
                self._log(f"✓ 日志已导出: {filepath}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出日志失败:\n{str(e)}")
            self._log(f"❌ 导出失败: {str(e)}")
    
    def _clear_log(self):
        """清空日志"""
        if messagebox.askyesno("确认", "确定要清空所有日志吗？\n此操作不可撤销！"):
            self.log_text.delete('1.0', tk.END)
            self._log("🗑️ 日志已清空")
    
    def _export_best_genome(self):
        """导出最佳基因组的详细信息"""
        try:
            if not self.best_genome:
                messagebox.showwarning("警告", "还没有最佳基因组数据")
                return
            
            from datetime import datetime
            from tkinter import filedialog
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"best_genome_{timestamp}.txt"
            
            # 打开保存对话框
            filepath = filedialog.asksaveasfilename(
                title="导出最佳基因",
                defaultextension=".txt",
                initialfile=default_filename,
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("Markdown文件", "*.md"),
                    ("所有文件", "*.*")
                ]
            )
            
            if not filepath:
                return
            
            # 执行基因组获取详细信息
            vm = QuaternaryVM()
            result = vm.execute(self.best_genome)
            
            # 四进制序列转DNA映射
            dna_map = {'0': 'A', '1': 'T', '2': 'C', '3': 'G'}
            dna_sequence = ''.join(dna_map[c] for c in self.best_genome.sequence)
            
            # 解码指令序列
            instructions = []
            seq = self.best_genome.sequence
            for i in range(0, len(seq), 4):
                if i + 3 < len(seq):
                    opcode = int(seq[i:i+3], 4)
                    operand = int(seq[i+3:i+4], 4)
                    
                    # 获取指令名称
                    instr_map = {
                        0x00: 'NOP', 0x01: 'PUSH', 0x02: 'POP', 0x03: 'DUP',
                        0x10: 'ADD', 0x11: 'SUB', 0x12: 'MUL', 0x13: 'DIV',
                        0x20: 'JMP', 0x21: 'JZ', 0x22: 'JNZ', 0x23: 'CALL',
                        0x30: 'INPUT', 0x31: 'OUTPUT', 0x32: 'HALT', 0x33: 'SWAP',
                    }
                    instr_name = instr_map.get(opcode, f'UNKNOWN({opcode:02x})')
                    
                    instructions.append({
                        'index': len(instructions),
                        'quaternary': seq[i:i+4],
                        'dna': dna_sequence[i:i+4],
                        'opcode': opcode,
                        'operand': operand,
                        'instruction': instr_name
                    })
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("四进制基因编程 - 最佳基因组详细报告\n")
                f.write("=" * 80 + "\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"代数: {self.best_genome.generation}\n")
                f.write(f"适应度: {self.best_genome.fitness:.6f}\n")
                f.write(f"变异数: {self.best_genome.mutations}\n")
                f.write(f"序列长度: {len(self.best_genome.sequence)}\n")
                f.write("=" * 80 + "\n\n")
                
                # 基因序列
                f.write("## 1. 基因序列\n\n")
                f.write("### 四进制编码:\n")
                f.write(self._format_sequence(self.best_genome.sequence, 60) + "\n\n")
                
                f.write("### DNA序列映射 (A=0, T=1, C=2, G=3):\n")
                f.write(self._format_sequence(dna_sequence, 60) + "\n\n")
                
                # 执行结果
                f.write("## 2. 虚拟机执行结果\n\n")
                f.write(f"执行状态: {'✓ 成功' if result.success else '✗ 失败'}\n")
                f.write(f"执行步数: {result.steps}\n")
                if result.output:
                    f.write(f"输出值: {result.output[-1]:.6f}\n")
                    f.write(f"所有输出: {result.output}\n")
                if result.error:
                    f.write(f"错误信息: {result.error}\n")
                f.write("\n")
                
                # 指令序列详细列表
                f.write("## 3. 指令序列详细列表\n\n")
                f.write(f"指令数量: {len(instructions)}\n\n")
                f.write("| 序号 | 四进制 | DNA  | 操作码 | 操作数 | 指令      |\n")
                f.write("|------|--------|------|--------|--------|----------|\n")
                
                for instr in instructions:
                    f.write(f"| {instr['index']:4d} | "
                           f"{instr['quaternary']:6s} | "
                           f"{instr['dna']:4s} | "
                           f"0x{instr['opcode']:02x}   | "
                           f"{instr['operand']:6d} | "
                           f"{instr['instruction']:8s} |\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("导出完成\n")
            
            messagebox.showinfo("成功", f"基因组已导出至:\n{filepath}")
            self._log(f"✓ 基因组已导出: {filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出基因组失败:\n{str(e)}")
            self._log(f"❌ 导出失败: {str(e)}")
    
    def _format_sequence(self, seq: str, width: int) -> str:
        """格式化序列为多行"""
        lines = []
        for i in range(0, len(seq), width):
            lines.append(seq[i:i+width])
        return '\n'.join(lines)
    
    def _analyze_instructions(self):
        """分析指令序列 - 打开新窗口显示详细分析"""
        try:
            if not self.best_genome:
                messagebox.showwarning("警告", "还没有最佳基因组数据")
                return
            
            # 创建分析窗口
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("🔍 指令序列分析")
            analysis_window.geometry("1200x800")
            
            # 创建notebook
            notebook = ttk.Notebook(analysis_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 页面1：指令列表
            instr_frame = ttk.Frame(notebook)
            notebook.add(instr_frame, text="📋 指令列表")
            self._create_instruction_list_tab(instr_frame)
            
            # 页面2：执行追踪
            trace_frame = ttk.Frame(notebook)
            notebook.add(trace_frame, text="🔬 执行追踪")
            self._create_execution_trace_tab(trace_frame)
            
            # 页面3：统计分析
            stats_frame = ttk.Frame(notebook)
            notebook.add(stats_frame, text="📊 统计分析")
            self._create_statistics_tab(stats_frame)
            
        except Exception as e:
            messagebox.showerror("错误", f"分析失败:\n{str(e)}")
            self._log(f"❌ 分析失败: {str(e)}")
    
    def _create_instruction_list_tab(self, parent):
        """创建指令列表标签页"""
        # 解码指令
        instructions = self._decode_instructions(self.best_genome.sequence)
        
        # 创建文本框
        text = scrolledtext.ScrolledText(parent, font=("Consolas", 10), wrap=tk.NONE)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加内容
        text.insert(tk.END, "=" * 100 + "\n")
        text.insert(tk.END, f"指令序列详细列表 (共 {len(instructions)} 条指令)\n")
        text.insert(tk.END, "=" * 100 + "\n\n")
        
        text.insert(tk.END, f"{'序号':<6} {'四进制':<8} {'DNA':<6} {'操作码':<8} "
                           f"{'操作数':<8} {'指令':<10} {'说明':<40}\n")
        text.insert(tk.END, "-" * 100 + "\n")
        
        instr_descriptions = {
            'NOP': '空操作',
            'PUSH': '压栈操作数',
            'POP': '弹出栈顶',
            'DUP': '复制栈顶',
            'ADD': '加法: a + b',
            'SUB': '减法: a - b',
            'MUL': '乘法: a * b',
            'DIV': '除法: a / b (安全)',
            'JMP': '无条件跳转',
            'JZ': '零跳转',
            'JNZ': '非零跳转',
            'CALL': '函数调用',
            'INPUT': '读取输入',
            'OUTPUT': '输出栈顶',
            'HALT': '停机',
            'SWAP': '交换栈顶两元素',
        }
        
        for instr in instructions:
            desc = instr_descriptions.get(instr['instruction'], '未知指令')
            text.insert(tk.END, 
                       f"{instr['index']:<6} "
                       f"{instr['quaternary']:<8} "
                       f"{instr['dna']:<6} "
                       f"0x{instr['opcode']:02x}     "
                       f"{instr['operand']:<8} "
                       f"{instr['instruction']:<10} "
                       f"{desc:<40}\n")
        
        text.config(state=tk.DISABLED)
    
    def _create_execution_trace_tab(self, parent):
        """创建执行追踪标签页"""
        text = scrolledtext.ScrolledText(parent, font=("Consolas", 9), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 执行程序并记录每一步
        text.insert(tk.END, "=" * 100 + "\n")
        text.insert(tk.END, "虚拟机执行追踪 (逐步执行记录)\n")
        text.insert(tk.END, "=" * 100 + "\n\n")
        
        # 简化的追踪执行
        stack = []
        output = []
        instructions = self._decode_instructions(self.best_genome.sequence)
        
        text.insert(tk.END, f"{'步骤':<6} {'指令':<10} {'操作数':<8} {'栈':<40} {'输出':<20}\n")
        text.insert(tk.END, "-" * 100 + "\n")
        
        step = 0
        for i, instr in enumerate(instructions[:100]):  # 限制100步
            step += 1
            instr_name = instr['instruction']
            operand = instr['operand']
            
            # 执行指令
            if instr_name == 'PUSH':
                stack.append(float(operand))
            elif instr_name == 'POP' and stack:
                stack.pop()
            elif instr_name == 'DUP' and stack:
                stack.append(stack[-1])
            elif instr_name == 'ADD' and len(stack) >= 2:
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif instr_name == 'SUB' and len(stack) >= 2:
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif instr_name == 'MUL' and len(stack) >= 2:
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif instr_name == 'DIV' and len(stack) >= 2:
                b, a = stack.pop(), stack.pop()
                stack.append(a / b if b != 0 else 0)
            elif instr_name == 'OUTPUT' and stack:
                output.append(stack[-1])
            elif instr_name == 'HALT':
                text.insert(tk.END, f"{step:<6} {'HALT':<10} {'':<8} "
                           f"{'程序停止':<40} {str(output):<20}\n")
                break
            
            # 显示状态
            stack_str = str([f"{x:.2f}" for x in stack[-5:]])  # 只显示栈顶5个
            output_str = str([f"{x:.2f}" for x in output[-3:]])  # 只显示最近3个输出
            text.insert(tk.END, f"{step:<6} {instr_name:<10} {operand:<8} "
                       f"{stack_str:<40} {output_str:<20}\n")
        
        text.insert(tk.END, "\n" + "=" * 100 + "\n")
        text.insert(tk.END, f"执行完成 - 总步数: {step}\n")
        text.insert(tk.END, f"最终栈: {stack}\n")
        text.insert(tk.END, f"所有输出: {output}\n")
        if output:
            text.insert(tk.END, f"最终输出值: {output[-1]:.6f}\n")
        
        text.config(state=tk.DISABLED)
    
    def _create_statistics_tab(self, parent):
        """创建统计分析标签页"""
        text = scrolledtext.ScrolledText(parent, font=("Consolas", 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        instructions = self._decode_instructions(self.best_genome.sequence)
        
        # 统计指令类型
        instr_count = {}
        for instr in instructions:
            name = instr['instruction']
            instr_count[name] = instr_count.get(name, 0) + 1
        
        # 分类统计
        categories = {
            '数据操作': ['NOP', 'PUSH', 'POP', 'DUP'],
            '算术运算': ['ADD', 'SUB', 'MUL', 'DIV'],
            '控制流': ['JMP', 'JZ', 'JNZ', 'CALL'],
            '特殊操作': ['INPUT', 'OUTPUT', 'HALT', 'SWAP'],
        }
        
        text.insert(tk.END, "=" * 80 + "\n")
        text.insert(tk.END, "指令序列统计分析\n")
        text.insert(tk.END, "=" * 80 + "\n\n")
        
        text.insert(tk.END, f"总指令数: {len(instructions)}\n")
        text.insert(tk.END, f"基因长度: {len(self.best_genome.sequence)} (四进制)\n")
        text.insert(tk.END, f"编码效率: {len(instructions) / len(self.best_genome.sequence) * 100:.1f}%\n\n")
        
        # 按类别统计
        text.insert(tk.END, "## 指令类别分布\n\n")
        for category, instrs in categories.items():
            count = sum(instr_count.get(i, 0) for i in instrs)
            percentage = count / len(instructions) * 100 if instructions else 0
            text.insert(tk.END, f"{category:12s}: {count:4d} 条 ({percentage:5.1f}%)\n")
        
        text.insert(tk.END, "\n## 各指令使用频率\n\n")
        text.insert(tk.END, f"{'指令':<12} {'数量':<8} {'占比':<10} {'条形图':<40}\n")
        text.insert(tk.END, "-" * 80 + "\n")
        
        sorted_instrs = sorted(instr_count.items(), key=lambda x: x[1], reverse=True)
        for instr, count in sorted_instrs:
            percentage = count / len(instructions) * 100
            bar = '█' * int(percentage / 2)  # 每2%显示一个方块
            text.insert(tk.END, f"{instr:<12} {count:<8} {percentage:>5.1f}%     {bar:<40}\n")
        
        text.insert(tk.END, "\n## 程序特征分析\n\n")
        
        # 分析程序特征
        has_output = any(i['instruction'] == 'OUTPUT' for i in instructions)
        has_halt = any(i['instruction'] == 'HALT' for i in instructions)
        has_arithmetic = any(i['instruction'] in ['ADD', 'SUB', 'MUL', 'DIV'] for i in instructions)
        has_control = any(i['instruction'] in ['JMP', 'JZ', 'JNZ', 'CALL'] for i in instructions)
        
        text.insert(tk.END, f"✓ 包含输出操作: {'是' if has_output else '否'}\n")
        text.insert(tk.END, f"✓ 包含停机指令: {'是' if has_halt else '否'}\n")
        text.insert(tk.END, f"✓ 包含算术运算: {'是' if has_arithmetic else '否'}\n")
        text.insert(tk.END, f"✓ 包含控制流: {'是' if has_control else '否'}\n")
        
        # 执行结果
        vm = QuaternaryVM()
        result = vm.execute(self.best_genome)
        
        text.insert(tk.END, f"\n执行成功: {'是' if result.success else '否'}\n")
        text.insert(tk.END, f"执行步数: {result.steps}\n")
        if result.output:
            text.insert(tk.END, f"输出数量: {len(result.output)}\n")
            text.insert(tk.END, f"最终输出: {result.output[-1]:.6f}\n")
        if result.error:
            text.insert(tk.END, f"错误信息: {result.error}\n")
        
        text.config(state=tk.DISABLED)
    
    def _decode_instructions(self, sequence: str) -> list:
        """解码四进制序列为指令列表"""
        instructions = []
        dna_map = {'0': 'A', '1': 'T', '2': 'C', '3': 'G'}
        
        for i in range(0, len(sequence), 4):
            if i + 3 < len(sequence):
                quaternary = sequence[i:i+4]
                dna = ''.join(dna_map[c] for c in quaternary)
                opcode = int(sequence[i:i+3], 4)
                operand = int(sequence[i+3:i+4], 4)
                
                instr_map = {
                    0x00: 'NOP', 0x01: 'PUSH', 0x02: 'POP', 0x03: 'DUP',
                    0x10: 'ADD', 0x11: 'SUB', 0x12: 'MUL', 0x13: 'DIV',
                    0x20: 'JMP', 0x21: 'JZ', 0x22: 'JNZ', 0x23: 'CALL',
                    0x30: 'INPUT', 0x31: 'OUTPUT', 0x32: 'HALT', 0x33: 'SWAP',
                }
                instr_name = instr_map.get(opcode, f'UNKNOWN')
                
                instructions.append({
                    'index': len(instructions),
                    'quaternary': quaternary,
                    'dna': dna,
                    'opcode': opcode,
                    'operand': operand,
                    'instruction': instr_name
                })
        
        return instructions


def main():
    """主函数"""
    root = tk.Tk()
    app = EvolutionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
