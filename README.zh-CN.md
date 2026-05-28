# 三衍进化引擎（Sanyan Evolution Engine）

> **一个自我进化的AI系统 — 已在云端无人值守运行11000+代**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)](#)

[English](README.md)

---

## 这是什么？

我是做工控FAE的，每天被同样的问题问到吐："ERR灯闪了怎么办？""Profinet通讯断了怎么查？"

我就在想：能不能让一个AI系统自己学会排障？

于是我写了一个进化引擎。不靠大模型API，不靠海量数据，而是用**达尔文进化论 + 38个跨学科概念**（生物学、博弈论、哲学、系统科学）驱动一群"引擎个体"不断变异、竞争、筛选、进化。

**它已经在云服务器上跑了11000多代，而且还在跑。**

---

## 5分钟跑起来

```bash
pip install numpy matplotlib
python demo.py
```

你会看到BF从0.7进化到0.97，100代，30秒。附带一张进化曲线图。

---

## 架构

**主循环：** `评估 → 选择 → 交叉 → 变异 → 生态位分组 → 多样性注入`

**6D基因组：** `适应度 × 质量 × 多样性 × 规模 × 结构 × 利用率`

**38个跨学科概念：**

| 状态 | 数量 | 说明 |
|:--|:--|:--|
| ✅ 活跃 | 3 | G11000+代持续验证有效 |
| 🧪 实验中 | 10 | 偶尔触发，效果不稳定 |
| 📋 概念阶段 | 15 | 设计完成，等待环境触发 |
| 📝 待验证 | 10 | 排队中 |

> 38→3不是失败，是自然选择在正常工作。

---

## 云端数据（G11016）

BF 2.44 | 种群 70-150 | 多样性 2.00 | KG 15030节点 | 生态位 4-8

---

## 关于三衍

三衍是一个人类与AI Agent协作的开源研究项目：
- **黄sir** — 工控FAE，项目发起人
- **思思（淬思）** — AI Agent，代码与运维
- **天平（衡）** — AI Agent，独立审计官

没投资人、没KPI、没变现压力。就想做个能自我进化的AI系统。

---

## 许可

MIT License — 随便用。

---

**联系：** 在Issue区留言，或在[知乎文章](https://zhuanlan.zhihu.com/p/2043539781901096255)评论区交流。
