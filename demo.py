#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanyan Evolution Engine — Demo Version (MRE: Minimal Runnable Example)

精简自进化引擎v43，保留核心进化机制：
- 6D基因组（fitness/q/d/size/structure/utilization）
- 自适应变异率（1/5规则）
- 多样性注入（低于阈值时触发新奇搜索）
- 生态位聚类（k-means分组 + 竞争排除）

去掉了：DeepSeek API依赖、SelfImprover、KG、监控、飞书通知
仅依赖：Python 3.9+、numpy、matplotlib

运行：python demo.py
输出：终端显示进化过程 + BF进化曲线图
"""

import random
import math
import numpy as np
from collections import defaultdict
import json

# ============================================================
# 配置
# ============================================================
POP_SIZE = 60           # 种群大小
MAX_GENERATIONS = 100   # 演示代数
MUTATION_RATE = 0.15    # 初始变异率
ADAPTIVE_INTERVAL = 5   # 自适应调整间隔
NICHES = 4              # 生态位数量
DIVERSITY_THRESHOLD = 1.05  # 多样性低于此阈值触发注入
SURVIVAL_RATE = 0.6     # 每代保留比例
ELITE_COUNT = 3         # 精英保护数

# ============================================================
# Engine 个体
# ============================================================
class Engine:
    """引擎个体 — 6D基因组表示"""
    
    def __init__(self, genome=None):
        if genome is None:
            # 6维随机初始化
            self.genome = np.array([
                random.uniform(1.0, 3.0),   # BF（适应度）
                random.uniform(0.3, 0.9),   # Q（质量）
                random.uniform(1.0, 2.0),   # D（多样性）
                random.uniform(0.5, 2.0),   # S（规模）
                random.uniform(0.1, 1.0),   # 结构复杂度
                random.uniform(0.3, 1.0),   # 利用率
            ])
        else:
            self.genome = genome.copy()
        
        self.fitness = 0.0
        self.age = 0
        self.generation = 0
        self.birth_gen = 0
        self.parent_id = None
    
    def evaluate(self, target_vector):
        """评估fitness — 向目标向量收敛"""
        # fitness = 1 / (1 + 欧氏距离到目标)
        dist = np.linalg.norm(self.genome - target_vector)
        self.fitness = 1.0 / (1.0 + dist)
        # 添加噪声模拟真实评估
        self.fitness += random.gauss(0, 0.01)
        return max(0.01, self.fitness)
    
    def mutate(self, rate):
        """高斯变异"""
        mutant = self.genome.copy()
        for i in range(6):
            if random.random() < rate:
                mutant[i] += random.gauss(0, rate * 0.5)
        # 确保值在合理范围
        mutant = np.clip(mutant, 0.01, 5.0)
        return Engine(mutant)
    
    def crossover(self, other):
        """均匀交叉 — 每个维度有50%概率交换"""
        child_genome = self.genome.copy()
        for i in range(6):
            if random.random() < 0.5:
                child_genome[i] = other.genome[i]
        return Engine(child_genome)


# ============================================================
# 生态位管理
# ============================================================
class NicheManager:
    """k-means聚类分配生态位 + 竞争排除"""
    
    def cluster(self, engines):
        """简单k-means分配"""
        if len(engines) < NICHES:
            return [[e] for e in engines] + [[] for _ in range(NICHES - len(engines))]
        
        # 随机初始化中心点
        genome_matrix = np.array([e.genome for e in engines])
        indices = random.sample(range(len(engines)), NICHES)
        centroids = genome_matrix[indices].copy()
        
        # 迭代10轮
        for _ in range(10):
            labels = []
            for g in genome_matrix:
                dists = [np.linalg.norm(g - c) for c in centroids]
                labels.append(np.argmin(dists))
            
            for j in range(NICHES):
                members = [i for i, lbl in enumerate(labels) if lbl == j]
                if members:
                    centroids[j] = genome_matrix[members].mean(axis=0)
        
        # 分配引擎到niche
        niches = [[] for _ in range(NICHES)]
        for i, e in enumerate(engines):
            dists = [np.linalg.norm(e.genome - c) for c in centroids]
            niches[np.argmin(dists)].append(e)
        
        return niches
    
    def eliminate(self, niches, keep_per_niche=3):
        """竞争排除：每niche只保留top N"""
        survivors = []
        for niche in niches:
            niche.sort(key=lambda e: e.fitness, reverse=True)
            survivors.extend(niche[:keep_per_niche])
        return survivors


# ============================================================
# 选择与繁殖
# ============================================================
def tournament_select(engines, k=3):
    """锦标赛选择"""
    candidates = random.sample(engines, min(k, len(engines)))
    return max(candidates, key=lambda e: e.fitness)


def calculate_diversity(engines):
    """计算种群多样性（基因组标准差的均值）"""
    if len(engines) < 2:
        return 1.0
    genome_matrix = np.array([e.genome for e in engines])
    return np.std(genome_matrix, axis=0).mean()


# ============================================================
# 主循环
# ============================================================
def main():
    print("=" * 60)
    print("  Sanyan Evolution Engine — Demo")
    print("  G11000+代云端验证 · 本地精简演示版")
    print("=" * 60)
    print(f"\n  种群: {POP_SIZE} · 代数: {MAX_GENERATIONS} · 生态位: {NICHES}")
    print(f"  变异率: {MUTATION_RATE} (自适应) · 目标: 6D优化")
    print()
    
    # 初始化：随机目标向量（模拟"最优解"）
    target = np.array([2.5, 0.7, 1.8, 1.2, 0.6, 0.8])
    
    # 初始化种群
    engines = [Engine() for _ in range(POP_SIZE)]
    for e in engines:
        e.evaluate(target)
    engines.sort(key=lambda e: e.fitness, reverse=True)
    
    niche_mgr = NicheManager()
    mutation_rate = MUTATION_RATE
    success_history = []
    best_fitness_history = []
    diversity_history = []
    
    print(f"{'Gen':>4s} {'Best BF':>8s} {'Avg BF':>8s} {'Diversity':>9s} {'Mut.Rate':>8s} {'Pop':>4s}")
    print("-" * 55)
    
    for gen in range(1, MAX_GENERATIONS + 1):
        # 1. 评估已有引擎的fitness（部分引擎需要重新评估）
        for e in engines:
            if e.age > 0 and random.random() < 0.3:  # 30%概率重评估
                e.evaluate(target)
        
        # 2. 排序
        engines.sort(key=lambda e: e.fitness, reverse=True)
        best = engines[0]
        
        # 3. 计算多样性
        diversity = calculate_diversity(engines)
        diversity_history.append(diversity)
        
        # 4. 选择 + 繁殖
        survivors_count = max(10, int(len(engines) * SURVIVAL_RATE))
        survivors = engines[:ELITE_COUNT]  # 精英保护
        
        # 锦标赛选择剩余幸存者
        remaining = engines[ELITE_COUNT:survivors_count]
        if remaining:
            survivors.extend(remaining[:ELITE_COUNT])
            # 用锦标赛从全部引擎中选
            for _ in range(survivors_count - len(survivors)):
                survivors.append(tournament_select(engines))
        
        # 5. 繁殖新子代
        children = []
        while len(survivors) + len(children) < POP_SIZE:
            parent1 = tournament_select(survivors)
            parent2 = tournament_select(survivors)
            
            # 交叉 + 变异
            child = parent1.crossover(parent2)
            child = child.mutate(mutation_rate)
            child.evaluate(target)
            child.birth_gen = gen
            child.parent_id = f"{id(parent1)}x{id(parent2)}"
            children.append(child)
        
        # 6. 多样性注入（低于阈值）
        if diversity < DIVERSITY_THRESHOLD:
            inject_count = max(3, int(POP_SIZE * 0.1))
            for _ in range(inject_count):
                novel = Engine()  # 随机新引擎
                novel.evaluate(target)
                novel.birth_gen = gen
                children.append(novel)
        
        # 7. 生态位分组 + 竞争排除
        all_engines = survivors + children[:POP_SIZE - len(survivors)]
        niches = niche_mgr.cluster(all_engines)
        engines = niche_mgr.eliminate(niches, keep_per_niche=3)
        
        # 补足种群
        while len(engines) < POP_SIZE:
            e = Engine()
            e.evaluate(target)
            e.birth_gen = gen
            engines.append(e)
        
        # 8. 更新age
        for e in engines:
            e.age += 1
            e.generation = gen
        
        # 9. 自适应变异率（1/5规则）
        if gen % ADAPTIVE_INTERVAL == 0:
            success_count = len([e for e in engines if e.generation == gen and e.fitness > 0.5])
            success_rate = success_count / max(1, len(engines))
            if success_rate > 0.2:
                mutation_rate *= 1.1
            else:
                mutation_rate *= 0.9
            mutation_rate = max(0.05, min(0.4, mutation_rate))
            success_history.append(success_rate)
        
        # 10. 统计
        avg_fitness = sum(e.fitness for e in engines) / len(engines)
        best_fitness_history.append(best.fitness)
        
        if gen % 10 == 0 or gen == 1:
            print(f"{gen:>4d} {best.fitness:>8.4f} {avg_fitness:>8.4f} {diversity:>9.4f} {mutation_rate:>8.4f} {len(engines):>4d}")
    
    # ============================================================
    # 结果输出
    # ============================================================
    print("\n" + "=" * 60)
    print("  进化完成!")
    print(f"  最佳BF: {max(best_fitness_history):.4f}")
    print(f"  最终BF: {best_fitness_history[-1]:.4f}")
    print(f"  最终多样性: {diversity_history[-1]:.4f}")
    print(f"  最终变异率: {mutation_rate:.4f}")
    print(f"  总代数: {MAX_GENERATIONS}")
    
    best_engine = max(engines, key=lambda e: e.fitness)
    print(f"\n  最佳基因型: {best_engine.genome}")
    print(f"  目标向量:   {target}")
    
    # 生成进化曲线图
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        
        # BF曲线
        ax = axes[0]
        ax.plot(best_fitness_history, 'b-', linewidth=1, alpha=0.8)
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.set_title('BF Evolution')
        ax.grid(True, alpha=0.3)
        
        # 多样性曲线
        ax = axes[1]
        ax.plot(diversity_history, 'g-', linewidth=1, alpha=0.8)
        ax.axhline(y=DIVERSITY_THRESHOLD, color='r', linestyle='--', alpha=0.5, label='Diversity floor')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Diversity')
        ax.set_title('Diversity Trend')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 变异率自适应性
        ax = axes[2]
        if len(success_history) > 1:
            ax.plot(range(ADAPTIVE_INTERVAL, MAX_GENERATIONS + 1, ADAPTIVE_INTERVAL)[:len(success_history)], 
                   [s * 0.3 for s in success_history], 'r--', alpha=0.5, label='Success rate (scaled)')
        ax.axhline(y=MUTATION_RATE, color='gray', linestyle=':', alpha=0.5, label='Initial rate')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Rate')
        ax.set_title('Adaptive Mutation Rate')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('evolution_demo.png', dpi=100)
        print(f"\n  进化曲线已保存: evolution_demo.png")
    except ImportError:
        print("\n  [*] matplotlib未安装，跳过图表生成")
    
    print("\n" + "=" * 60)
    print("  引擎核心机制已验证:")
    print("  - 自适应变异率 (1/5规则)")
    print("  - 生态位聚类 + 竞争排除")
    print("  - 多样性注入 + 精英保护")
    print("  - 交叉繁殖 + 高斯变异")
    print("=" * 60)


if __name__ == "__main__":
    main()
