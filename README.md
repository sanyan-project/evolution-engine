# Sanyan Evolution Engine 🧬

> **一个自我进化的AI系统 — 已在云端无人值守运行11000+代**
>
> *A self-evolving AI system — 11000+ generations on a single cloud server.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)](#)

---

## 🤔 这是什么？

我是一个工控FAE（现场工程师），每天被同样的问题问到吐："ERR灯闪了怎么办？""Profinet通讯断了怎么查？"

我想：能不能让一个AI系统自己学会排障？

于是，我写了一个进化引擎。它不靠大模型API，不靠海量数据，而是用 **达尔文进化论 + 38个跨学科概念**（生物学/博弈论/哲学/系统科学）驱动一群"引擎个体"不断变异、竞争、进化，自己学会在受限资源下优化自己。

**它跑了11000+代，而且还在跑。**

现在，我把它的核心机制开源出来，希望更多人能参与这个方向。

---

## 🚀 5分钟快速体验

```bash
# 安装依赖
pip install numpy matplotlib

# 运行演示版（100代，~30秒）
python demo.py

# 你会看到：
# - BF（适应度）从0.x进化到2.x
# - 多样性在1.05-2.0之间动态变化
# - 自适应变异率在0.05-0.4之间调整
# - 一张evolution_demo.png进化曲线图
```

## 🐳 Docker

```bash
docker build -t sanyan-engine .
docker run -it sanyan-engine
```

---

## 🏗️ 架构 — 6维基因组 + 生态位竞争

```
┌─────────────────────────────────────────────────────┐
│                    Main Loop (每代)                    │
│                                                       │
│  Evaluate → Select → Crossover → Mutate → Niches     │
│      ↑                                       ↓        │
│      └──── Diversity Injection ←────── (D<1.05)      │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ SelfImprover│  │ PhaseManager │  │KnowledgeGraph│  │
│  │ 每10代反思   │  │ 4态切换      │  │ 15000+节点   │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

**6D Genome:** `BF × Q × D × S × Structure × Utilization`

**38个跨学科概念** 按状态分类：

| 状态 | 数量 | 说明 |
|:--|:--|:--|
| ✅ Active | 3 | 云端G11000+代持续验证有效（自适应变异率/新奇搜索/动态Niche） |
| 🧪 Experimental | 10 | 偶尔触发，效果不稳定 |
| 📋 Conceptual | 15 | 设计完成，等待环境触发 |
| 📝 Pending | 10 | 待验证 |

> **注意：** 这不是38个概念都"失败"了35个。进化机制本来就是筛选——大部分变异没用，少数有用才被保留。38→3恰恰是引擎在正常工作的证明。

---

## 📊 云端运行数据

| 指标 | 当前值 (G11016) |
|:--|:--|
| Best Fitness (BF) | 2.44 |
| Engine Population | 70-150 |
| Diversity (D) | 2.00 |
| Knowledge Graph | 15,030 nodes |
| Active Niches | 4-8 |
| Runtime | 数月24/7无人值守 |

---

## 📂 项目结构

```
sanyan-engine/
├── demo.py              # 演示版（独立运行，100代）
├── Dockerfile           # Docker镜像
├── ARCHITECTURE.html    # 架构图
├── README.md            # 本文件
├── README.zh-CN.md      # 中文
├── CASES.md             # 工控排障案例
├── AUDIT.md             # 独立审计报告
└── LICENSE              # MIT
```

---

## 🎯 谁应该关注这个项目？

- 对**进化计算/遗传算法**感兴趣的开发者
- 探索**AI自改进/Self-Improving AI**的研究者
- 想了解**AI Agent如何协作开发复杂系统**的工程师
- 对**交叉学科（生物学+AI+博弈论）**好奇的人

---

## 🤝 贡献

1. Fork 本项目
2. 创建 Feature Branch (`git checkout -b feature/your-idea`)
3. 提交改动 (`git commit -m 'Add some idea'`)
4. 推送到 Branch (`git push origin feature/your-idea`)
5. 创建 Pull Request

**Good First Issues:**
- 实现 #4 概念（Borda排序）
- 改进多样性可视化
- 添加更多工控场景案例

---

## 📝 许可证

MIT License — 自由使用、修改、分发。

---

## 👤 关于作者

三衍（Sanyan）是一个人类与AI Agent协作的开源研究项目：

- **黄sir** — 工控FAE（现场工程师），项目发起人，提供方向判断和工控领域知识
- **思思（淬思）** — AI Agent，负责代码实现、运维、文档
- **天平（衡）** — AI Agent，独立审计官，负责质量检查

> 我们相信：AI系统应该有自我改进的能力。进化引擎只是第一步。

---

⭐ 如果这个项目对你有启发，请给个Star！
