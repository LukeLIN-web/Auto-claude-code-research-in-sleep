# Auto Research 的哲学

agent 自动做研究时，人可以不读中间代码，前提是**论文要主张的那句话，能由 agent 碰不到的东西来验证**。本页讲这条原则从哪来、它决定什么样的论文适合交给 agent，以及守住它要做的几件事。出处列在文末，查于 2026-11-25。

## 1. 能自动化到哪，由验证决定

Karpathy 在 2025 年 11 月的 *Verifiability* 里把这件事说成两句话："Software 1.0 easily automates what you can specify. Software 2.0 easily automates what you can verify." 他要求的环境有三条：能重来（resettable）、能便宜地试很多次（efficient）、有一个自动的过程给每次尝试打分（rewardable）。

Jason Wei 同年 7 月的 verifier's rule 说的是同一件事：训练 AI 解决一个任务的难易，和这个任务有多容易验证成正比。他列的条件是：有客观真值、验证快、能批量验证、噪声低、能给多个解排序。他举的最好的例子是 AlphaEvolve：大量生成候选，由自动评估筛选（他称为 guess-and-check）。

Karpathy 2026 年 3 月放出的 autoresearch 把这套搬进了研究：agent 只改 `train.py`；数据准备和评测在 `prepare.py` 里，不许改；每次训练固定 5 分钟，看 val_bpb 有没有变好，变好就留，否则丢。人不用读 agent 改了什么，因为打分的那段代码 agent 碰不到。

放到写论文上，要问的是：**论文要主张的那句话，验证者是谁？**

## 2. 方法论文适合交给 agent，benchmark 论文不适合

**方法论文**主张的是「在别人的 benchmark 上变好了」。验证者是 benchmark 作者给的标准答案和判分程序，与 agent 无关。错误的方向也不对称：

- 中间代码写错了，大多让分数变低，自己就暴露了。
- 能让分数虚高的只有一类错：评测边界被碰了，比如改了判分、看到了测试答案、在测试集上反复挑。这一处好守（第 4 节）。

在几个 benchmark 上同时变好，就更难是假的。所以做方法时可以长期不读中间代码，只读数。

**benchmark 论文**主张的是「这套题和判分量对了某个能力」。这句话没有外部的验证者，benchmark 自己出的分数证明不了它自己。而且它的错是静默的：不报错，跑出来的模型分数看着也合理。

- **标准答案标错。** Northcutt 等审了 10 个常用数据集的测试集，平均至少 3.3% 标错。Gema 等估计 MMLU 有 6.49% 的题有错，病毒学子集里分析过的题 57% 有错。
- **判分写宽、题目有漏洞。** Zhu 等检查了十个常用 agent benchmark，这类问题能让 agent 的分数被高估或低估，最多达相对 100%；τ-bench 上一个平凡的 agent 拿到 38%，超过基于 GPT-4o 的 agent。
- **题目不需要它声称考的东西。** MMStar 发现很多多模态 benchmark 的题不看图也能答对，GeminiPro 不看图在 MMMU 上拿到 42.9%。

这些都是有人逐条看题、看判分才发现的。agent 造 benchmark 时，题目、答案、判分程序都是 agent 写的；答案标错、判分写宽，分数照样涨，人不看就发现不了。

所以：

- 交给 agent、不看过程迭代的，选方法论文，验证用现有的公开 benchmark。
- 真要做 benchmark 论文，agent 能干的是基础设施：跑模型、出表、渲染。题目、标准答案、判分程序对不对，得由人抽查定稿，可以照 Zhu 等的 ABC 清单查。

## 3. 不看代码，不等于只看总分

总分涨了，只说明数涨了，不说明论文给的解释成立。方法论文通常还要说「增益来自 X」，这句话要靠对照：

- **去掉 X 的探针。** 方法声称更会用某个输入（图像、音频、检索到的证据），就把这个输入拿掉再跑一遍。增益如果还在，它来自别处，比如题干和选项里的文本先验，也就是 MMStar 指出的那类现象。
- **裁判的空输入探针。** 用模型当裁判的 benchmark，把输出换成空白或无关内容再打分。Zheng 等的 null model 对所有指令输出同一段话，在 AlpacaEval 2.0 上拿到 86.5% 的 LC 胜率。分数不明显掉，说明裁判能被讨好。
- **配对检验。** 两臂在同一批题上配对，报检验名和 p。

这些对照读的也是数，不是代码，不看代码的工作方式不受影响。

## 4. 守住评测边界：agent 碰不到的三样东西

能让分数虚高的错都出在边界上。已有报告里的三种：

- **判分代码和裁判。** METR 报告前沿模型在他们的任务上会改测试或打分代码，或去拿现成的实现和答案来抬分；人工复查找到的远多于只按异常高分去筛的。ImpossibleBench 把任务改成说明和单测冲突、按理不可能通过，模型的通过率就是作弊率。
  做法：评测代码、裁判、测试集放在 agent 写不到也读不到的地方，跑完核对它们没变。
- **测试集。** 在同一份数据上反复评、再挑最好的，挑出来的有一部分是这份数据的噪声。
  - Meta 的 AIRA-dojo 发现：在 MLE-bench 上按测试分而不是验证分挑最终解，奖牌率能高 9–13 个百分点，他们读成对验证集的系统性过拟合。后续的 AIRA₂ 认为那主要是评测噪声，不是记住了数据。
  - Bespoke Labs 的 AutoResearchExam 只给 agent 看验证分，把隐藏测试分藏起来，测两者的差。
  - *The Leaderboard Illusion* 在 Chatbot Arena 上看到同一件事：私下测许多变体，只公开最好的一个。
  - Dwork 等的 reusable holdout 给了理论上的界：一份留出集能安全复用的次数有限，大致随样本数的平方增长。

  做法：迭代只用开发集，测试集只在最后对每个定下的候选报一次。
- **跨轮次的共享状态。** Askarbekuly 等让 Claude Code 和 Codex 做 autoresearch，看到 agent 通过共享的 git 状态读别的轮次、在持久记忆里给「以后的轮次」留话；Codex 的提分主要来自记住各条评测样本的答案。
  做法：各轮之间隔离；共享是设定的一部分时，写清楚。

还有一种查法不靠隔离：Bertran、Roth、Wu 让一个新的 agent 只拿一段很短的提示和训练数据，去复现探索 agent 的结果。靠验证集特有性质得来的增益复现不出来；他们报告这样区分诚实的和钻空子的检查点，敏感度 100%、特异度 91%。

## 5. 不读中间代码，但要审过程记录

Luo、Kasirzadeh、Shah 列了 AI scientist 系统的四种坑：benchmark 选得不当、数据泄漏、指标误用、事后挑结果。他们发现，看完整的过程记录和代码，比只看最终论文能查出多得多的问题，并建议期刊和会议要求随文提交这些材料。

这和「不读中间代码」不矛盾。要审的不是方法实现对不对（第 2 节说过，那类错会让分数掉），而是过程记录里有没有碰边界的事：中途换了 benchmark、悄悄抽样或自造了数据、读过测试集、只报了挑出来的那几次。这些可以在记录里逐条查，适合交给一个零上下文的审查者。

## 6. 发射前的检查清单

**方法论文**

1. benchmark 由人在发射前选定：用现有公开的，至少两个。判分越硬越好：标准答案、判分程序、仿真判定优先，模型裁判次之。
2. 评测代码、裁判、测试集对 agent 只读或不可见；发射前记下哈希，跑完核对。
3. 迭代只用开发集；测试集对每个定下的候选只报一次，配对检验报 p。
4. 论文要说增益来自 X，就配去掉 X 的探针；用模型裁判的 benchmark，配空输入探针。
5. 各轮之间隔离记忆和 git 状态，除非共享是设定的一部分。
6. 抽看几条最终产物；按第 5 节审一遍过程记录。

**benchmark 论文**

agent 做基础设施；题目、标准答案、判分程序由人抽查定稿，照 ABC 清单查。再跑三个对照：强弱已知的模型能不能排对、null model 拿几分、去掉被考的输入后还能答对多少。

## 出处

验证与自动化

- Andrej Karpathy, *Verifiability*, 2025-11-17. <https://karpathy.bearblog.dev/verifiability/>
- Jason Wei, *Asymmetry of verification and verifier's rule*, 2025-07-15. <https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law>
- Andrej Karpathy, *autoresearch*（GitHub 仓库，README 题记署 2026 年 3 月）. <https://github.com/karpathy/autoresearch>

benchmark 本身的错

- Northcutt, Athalye, Mueller, *Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks*, NeurIPS 2021 Datasets and Benchmarks. arXiv:2103.14749（3.3% 是 NeurIPS 版的数，v1 是 3.4%）
- Gema et al., *Are We Done with MMLU?*, NAACL 2025. arXiv:2406.04127
- Zhu et al., *Establishing Best Practices for Building Rigorous Agentic Benchmarks*（ABC 清单）, NeurIPS 2025 Datasets and Benchmarks. arXiv:2507.02825v5（2025-08-07）
- Chen et al., *Are We on the Right Way for Evaluating Large Vision-Language Models?*（MMStar）, NeurIPS 2024. arXiv:2403.20330v2（2024-04-09）
- Zheng et al., *Cheating Automatic LLM Benchmarks: Null Models Achieve High Win Rates*, ICLR 2025 Oral. arXiv:2410.07137v2（2025-03-02）

钻评测的空子

- Von Arx, Chan, Barnes, *Recent Frontier Models Are Reward Hacking*, METR, 2025-06-05. <https://metr.org/blog/2025-06-05-recent-reward-hacking>
- Zhong, Raghunathan, Carlini, *ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases*, ICLR 2026. arXiv:2510.20270v1（2025-10-23）
- Askarbekuly et al., *Autoresearch with Coding Agents: Generalizers and Metric-Maximizers on Quran Recitation Data*. arXiv:2607.18064v2（2026-08-27）

在验证集、测试集上过拟合

- Toledo et al., *AI Research Agents for Machine Learning: Search, Exploration, and Generalization in MLE-bench*（AIRA-dojo）. arXiv:2507.02554v2（2025-11-04）；9–13 个百分点在正文引言，不在摘要
- Hambardzumyan et al., *AIRA_2: Overcoming Bottlenecks in AI Research Agents*. arXiv:2603.26499v2（2026-04-13）
- Ramesh et al., *AutoResearchExam*, Bespoke Labs, 2026-09（29 个任务，每次 24 小时）. <https://benchmarks.bespokelabs.ai/autoresearchexam/>
- Singh et al., *The Leaderboard Illusion*, NeurIPS 2025. arXiv:2504.20879v2（2025-05-12）
- Dwork, Feldman, Hardt, Pitassi, Reingold, Roth, *The Reusable Holdout: Preserving Validity in Adaptive Data Analysis*, Science 2015. <https://cis.upenn.edu/~aaroth/reusable.html>
- Bertran, Roth, Wu, *What Fits (Into Few Tokens) Doesn't Overfit: Compression and Generalization in ML Research Agents*. arXiv:2606.11045v1（2026-06-09）；敏感度、特异度在正文引言，不在摘要

审过程

- Luo, Kasirzadeh, Shah, *The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems*, NeurIPS 2025 AI4Science workshop. arXiv:2509.08713v2（2025-12-20）

延伸阅读：端到端的 AI scientist

- Yamada et al., *The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search*. arXiv:2504.08066：投了三篇生成的稿件到 ICLR 2025 的一个 workshop，一篇的审稿分过了录用线，随后撤回。
- Beel, Kan, Baumgart, *Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?*, SIGIR Forum 2025. arXiv:2502.14297v3：独立复测，指出实验流水线仍要用户提供，自动审稿缺深度。
