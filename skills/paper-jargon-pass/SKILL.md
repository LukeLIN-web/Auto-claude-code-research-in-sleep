---
name: paper-jargon-pass
description: "Use when a paper reads fine to the author but a reviewer would stall on it — 论文术语审查/没定义就用的词和数字/审稿人读不懂/统一术语/undefined notation/jargon audit for papers. Catches terms used before they are defined, lab-internal working vocabulary that leaked into English (考场→\"court\", 口径→\"caliber\"), config numbers that arrive before the thing they configure is named (\"600-second blocks\", \"the top B=3 blocks\"), one word carrying three meanings, and 废话/无中生有 — prose narrating things that do not exist (\"Video-Odyssey publishes no row for this backbone and has no column\"), flagged by the delete-test and deleted or demoted to a table footnote. Three passes: assembly check → blind read of the compiled PDF → verify against code/data and rewrite."
argument-hint: "[paper 目录或 clone 目录,默认自动发现]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# 论文术语盲读审查(装配检查 → 盲读 PDF → 查证改写)

审查对象:**$ARGUMENTS**

## 核心原则

**顺序不可颠倒。** 先盲读、后看代码和实验产物。你(或作者)一旦读过 pipeline 的实现,就再也看不见术语了——每个自造词都会自动被脑补成"显然的意思",这正是它当初被写出来的原因。第一趟的唯一目的是保留"看不懂"这个信号,它一次性、不可再生。

**读 PDF,不读 .tex。** 论文的阅读顺序不是文件顺序:`\input` 的次序、浮动体的落页、caption 与正文的先后,决定了读者**实际**在第几页第一次撞见某个词。在 `.tex` 里"定义在 §3.1、使用在 §4"看着没问题,排版后 §4 的表可能落在第 4 页而 §3.1 在第 6 页。盲读的输入是 `pdftotext -layout main.pdf -` 的页序文本。

**审稿人不是一个读者,是三个。**

| 读者 | 读到时手里有什么 | 判定 |
|---|---|---|
| 摘要读者 | 标题和摘要,别的什么都没有 | 摘要里的每个符号、每个数字、每个自造名词,要么当场定义,要么删掉 |
| 正文读者 | 读到这一页为止的所有正文 | 定义必须先于首次使用(按页序) |
| 图表读者 | **只有这张图/表和它的 caption** | caption 里的词若只在正文定义,对它的读者就是没定义 |

caption 和表注是**独立阅读单元**——审稿人翻表格的次数远多于逐行读正文。用了正文才定义的词,算未定义,不算"前文有"。

## 第 0 趟:装配检查(先跑,零阅读)

论文源码是多文件拼装的,拼装本身会坏,而坏掉的方式肉眼读单个文件看不出来。**在读任何内容之前**先跑完这一组;命中任何一条,先报给用户,不要继续往下审——审一份装配错的稿子是白干。

```bash
cd <clone 目录>
# 1) 两个 section 文件内容相同 = 某一节被覆盖丢失(Overleaf 端复制粘贴事故的典型签名)
md5sum sections/*.tex | awk '{print $1}' | sort | uniq -d
# 2) main.tex \input 的目标都存在
grep -o '\\input{[^}]*}' main.tex
# 3) \label 重名(丢节的第二签名:同一个 \label{sec:intro} 出现两次)
grep -rho '\\label{[^}]*}' sections/ tables/ | sort | uniq -d
# 4) 编译期未定义引用 / 重复标签
grep -n "There were undefined references\|multiply defined\|Citation .* undefined" main.log | head
# 5) 章节清单与 aux 对账:该有的节都在吗
grep -o '\\newlabel{sec:[^}]*}' main.aux
```

丢节要从 git 里捞回来,不要重写:`git log --oneline -- sections/03_method.tex`,再逐个 commit 比对
`git show <c>:sections/03_method.tex | head -1`,找到最后一个正常版本恢复。**恢复到 clone 里可以,推 Overleaf 必须先问用户**——clone 是用户共享仓的镜像。

> 引用完整性不归这个技能管:`references.bib` 只 pull 不写,缺条目、`[?]`、key 对不上一律不修不报(见 `paper/CLAUDE.md`)。第 4 条只用来发现**丢节**,不用来发现缺文献。

## 第一趟:盲读

```bash
pdftotext -layout main.pdf - | sed -n '1,240p'   # 正文,按页序,一次一段
```

装成**这个领域的审稿人**:懂 LoRA、bootstrap、greedy decoding、MCQ,但没读过这个仓库、没读过前几轮结果页、不知道这个组内部管什么叫什么。读到第 N 页时**不许**往后翻找定义、不许 grep 代码、不许打开 `scripts/`、不许读 appendix 去救正文。

> 隔离提醒:如果本次会话已经读过这份稿子的实现或前几轮审查记录,你已经污染了。此时把每一节派给一个独立 subagent 盲读(每个只给一段 pdftotext 文本、禁止读任何文件),你只汇总不补充。

### 记什么:两种信号

- **卡住**(A/B 组)——必须停下重读,或必须往回/往后翻页才能继续。能带着一个临时含义按正常速度读下去、且后文没有推翻它的,不记。
- **空转**(C 组·废话)——读得毫不费力,但读完说不出这句在这干什么:它不定义、不主张、不配置。判据是**删句测试**:把这句删掉重读前后段,若没有任何主张、定义或配置常数失去支撑,记。

卡住的承重条目通常 5–15 条。**超过 20 条就停止逐词记录,直接写文档级判定**——那已经不是措辞问题,而是这篇稿子缺一个记号约定小节或缺一张符号表。空转条目超过 ~15 条同理:那不是几句废话,是整篇在写审计日志,文档级判定里直接建议跑 `/paper-prose-tighten` 做全文清理,本技能只处置盲读撞见的这几条。

### 类型

**A 组 · 换词/补定义能修的**

- **名字晚于数字**——`600-second blocks` / `eight candidate windows` / `the top $B{=}3$ blocks` / `keep-cap 12` / `max-pos 36{,}864`:配置常数照写没问题(数字是允许的),但**它配置的那个东西必须已经被命名过**。"block""window""readout budget"没定义之前,`B{=}3` 只是一个不知道在数什么的数。修法是在名词首次出现处给一句话定义,不是把数字删掉。
- **内部工作语 / 翻译残留**——组里中文黑话被直译进英文,读起来像正经术语,作者永远看不见:`考场→court`、`口径→caliber`、`臂→arm`、`剂量→dose`、`打底→ground`。检验法只有一条:**这个词在本领域公开文献里,是这个意思吗?** 不是就换。`arm` 有(临床试验),`court` 没有。
- **一词多义 / 含义漂移**——同一个词在三处指三样东西(`caliber` 一会儿指窗口枚举、一会儿指权重配置、一会儿指 prompt 版本)。同一个词第三次出现时你又得重猜 = 记。
- **同物异名**——`regime` 与 `régime`、`region` 与 `window`、`benchmark` 与 `court`、`localization-training system` 与 `retrieval-trained system` 与 `localization-only row` 指同一条臂。读者会以为是三个东西。
- **宏与上标无图例**——`\newcommand` 定义的东西对读者不存在:`\method`、`$\Tans$`、`\starred`、`\textsuperscript{\ddag}`、`$\circ$`。查的是每个宏**排版后首次出现**的位置,以及图例是否在那之前。
- **悬空指代**——"the anchor""that régime""both enumerations""the deep benchmark":哪个?哪两个?什么叫 deep?
- **名不副实**——`coverage` 在三处分别是"证据命中率""音频保留比例""块覆盖",名字一样含义不同。

**B 组 · 换词修不了的**(盲读者最容易发现,因为你没有先验去替它圆场)

- **隐含前提**——句子通顺,但要先知道某个没写出来的设定才成立。
- **数值互斥**——同一篇里 `65{,}536-token position limit` 与 `max-pos 36{,}864` 并存:可能是两个不同的量(模型位置上限 vs 读出截断),也可能是错。**盲读者分不出来,正是问题所在**——记下来,第二趟对账。
- **自相矛盾**——摘要断言 A,正文撤回 A;两表同一格给不同数。**这是 bug,单独报,不许靠改措辞抹平。**
- **数目不自洽**——号称"五个 benchmark"实际列了四个加一个附录的;"all eight"与表里行数对不上。
- **一句话塞太多**——单个术语都没问题,但一句里堆了十几个专名(用户举的那句就是:分块 + 定位 pass + 候选窗 + top-B + 读出预算 + 答题前向,全在一个分号句里)。处置是**拆句**,不是换词。

**C 组 · 废话**(不是看不懂,是没内容;处置只有删或降级,没有"改写"选项。判死生需要全稿语境——套件枚举了哪些考场、别的表有哪些行——所以 C 组**不吃盲读隔离**:盲读只标记空转句,判定放第二趟,也可以在第二趟直接用 grep 候选清单补扫)

- **无中生有**——句子的主语是一个不存在的东西:`Video-Odyssey publishes no row for this backbone and has no column for it`、`X does not report Y for this setting`、`no official number exists for…`。为一个空格子、一个别人没做的实验、一条没有的基线写整句正文。它最隐蔽,因为读起来像尽职的披露——这正是它能活过历版草稿的原因。判死生只看一条:**读者在这个图表里看得见这个空缺吗?** 看得见(某格是 `—`、某行比套件枚举少一行、n 比全量小)→ 缺席承重,落法是图例里的一短句(`a dash = none published` 就是范本),不是叙事句;看不见(那个实体从头就不在这张表里)→ 删。同一句法两种命运:`Video-Odyssey has no whole-clip arm.`(解释表里可见的空格)留;`Video-Odyssey publishes no row for this backbone and has no column.`(表里根本没有这一列,而真正被省掉的候选它反而只字未提)删。
- 其余子类照 `/paper-prose-tighten` 的切除分类认:记账计数、自辩元叙述、否弃方案的游记、复述与叠 hedge。盲读时不用背分类,过删句测试就记;完整判据与保留红线(显著性限定词、划范围的分母、协议差异不许删)以那份技能为准。

写到 `paper/review-stage/jargon/<UTC时间戳>/ledger-<节名>.md`(**不要写进 Overleaf clone**)。一节一份。用分块不用表格。

```
### N. <一句话标题>
- 首次出现:PDF p3 / sections/04_results.tex:60      ← 两个都要:页序定"晚于使用",行号定"改哪里"
- 其它出现::64 :127 / tables/08_minicpm_avoc.tex:9  ← 只列让理解更糟的那几处
- 原句:<逐字抄,别转述>
- 类型:内部工作语
- 卡点:<为什么读不下去,一句话>
- 我猜是:<你的猜测>  置信度:sure | guess | no idea
- 严重度:承重 | 局部 | 表面
- 读者:摘要 | 正文 | 图表        ← caption-only 的词单列,它的修法不一样(改 caption 自足,不是改正文)
```

- **置信度**衡量*你*有多确定;**严重度**衡量*读者*被伤得多重:`承重`=主张挂在它上面,不懂它这一节就白读。二者独立。

C 组条目字段更少(没有"我猜是"——废话不需要猜,只需要删句测试):

```
### C-N. <一句话标题>
- 位置:PDF p4 / sections/05_results.tex:88
- 原句:<逐字抄,别转述>
- 删句测试:删掉后受损的主张 = 无      ← 写得出受损者就不是废话,改判 keep,不进 ledger
- 处置:删 | 降级表注
```

ledger 末尾另开两节:

- **文档级判定**——不锚在任何行号上的整篇问题。论文里最常见的三条:①**缺记号约定**(应该在 §3.1 开头用一段把 block / window / readout budget / $B$ / $M$ 一次性定义,而不是散在六处);②**这一节是对另一节的 diff**(症状:一半悬空指代都"翻到 §3 十秒就能答"——如果 §3 存在的话);③**术语在正文与 caption 之间不同步**。这类问题的正解是加一段/改结构,不是逐词改写。
- **良品名单**——你专门判定过"这是真术语,别动"的词:`LoRA`、`prefill`、`greedy decoding`、`bootstrap`、`oracle`、`intention-to-treat`、`pp`。不写下来,第二趟会重新纠结,甚至把它们改成大白话。

## 第二趟:查证 + 改写

现在才允许读实现、跑脚本、翻实验产物。

**先找承重条目之间的共同根因。** 它们往往有一半出自同一个病(最常见:整篇缺一段记号约定)。一段小节能一次干掉六条,逐条处置是最浪费的做法。

**改之前先对账。** `grep` 原词的命中率比想象中低:论文里的词在代码里往往叫别的名字(`window` = `region`、`readout` = `answer_forward`)。有效顺序是**先把数字对一遍**:B 组记下的"数值互斥"条目,拿 `paper/data/*.json`、`outputs/eval/` 逐题产物、`scripts/fig_*.py` 逐个核。数字错只能这样找出来,读措辞永远发现不了。

**B 组不进改写流程**:自相矛盾、数目不自洽、数值互斥 → 直接列给用户(信哪个由用户定);断句歧义、一句话塞太多 → 改结构(拆句/拆列表),不换词;隐含前提 → 补一句口径**并同时报**(作者脑子里有一套没写下来的约定,补完得让他确认补对了)。

**C 组在改写前处置,只有两个动作**:①默认**整句删**。删完重读该段:一查悬空指代(被删句喂养的 "this comparison""that row" 会跟着悬空),二反跑删句测试——若某个主张真的少了支撑,恢复原句、改判 keep 并记一笔为什么。②缺席确实需要交代的(表里有 `—`/`*` 等着解释),先**降级成表注一条**,再删正文句。删句持 `/paper-prose-tighten` 的红线:显著性限定词、划范围的分母、让对比不公平的协议差异,不许跟着整句陪葬——它们缩成主张上的一个形容词或一条表注活下来。

两个实战陷阱:

- **废话的主产地是 caption,而表 caption 多为脚本生成**(文件头有 AUTO-GENERATED 标记)。删句必须落在生成器(`tab_*.py` / caption SSOT)并重跑构建——直接改 `.tex` 会被下一次 build 原样复活;降级出的表注同样写进生成器。顺手核对生成器注释:它可能声称"caption 里解释了"而 caption 里其实没有。
- **上一版分析的披露句不许删**:`An earlier pre-specified analysis had shown little effect; the full read supersedes it` 形似流水账,但删掉=隐藏一次结果不一致的前置分析,变相把主张洗得更稳。这类句子连同你的判断上报 user,与 B 组同待遇。

A 组逐条处置,四选一:

1. **首次出现处补一句定义**(≤1 个从句)——概念真实存在、领域确实没有现成词时用。`window (a 75 s span; eight of them tile each block)`。
2. **换成领域通行叫法**——领域已有标准说法时用。首次出现处可保留一次原词:`benchmark (referred to as "court" in our logs)` 只在必须让老读者对上时才留,**通常直接换干净**。
3. **降级**——这个词只在附录/表注里需要 → 从正文删掉,定义落在表注里。
4. **删掉整句**——这个术语全篇只用一次、删了不损失任何主张。**这一条比想象中常用**:一个没定义又只用一次的自造词,通常是稿子不需要的词。

**"领域通用词"从哪来**(按优先级):公开文献/教材的叫法 → 依赖库或上游 benchmark 的官方命名 → 稿子里已经在用的更通用的同义词。**不要自己发明新词**——发明就是又造了一个只有作者懂的词。

### 改写纪律(论文特有,比文档严)

- **只动措辞,不动事实、不动数字、不动结论。** 界线:从方法节/代码/产物**搬运**一条已存在的事实过来当定义 = 允许;**推断、补全缺失项、扩大结论范围** = 动事实,禁止。表里少两行 → 只报不补。
- **删词不许顺手升级主张**:原文只指了表就别改写成"最强/领先"。
- **补定义不许变成补 caveat**。这份稿子的规矩是 caveat 越少越好(`paper/CLAUDE.md`);"X 只在 Y 条件下成立"这种句子不是定义,是 caveat,该进 todo 不进正文。定义是**说 X 是什么**,一句话,陈述句。
- **正文不写结果数字**:如果某条的修法是"把数值搬进正文解释",停——数字的家是表和图,正文只说方向和判没判住。配置常数(块长、$B$、窗宽、token 上限、帧预算)不算结果数字,照写。
- **换词是全仓操作,且必须扫到图**:`.tex` 正文 + table caption + 表头 + `paper/scripts/fig_*.py` 里的硬编码字符串 + 手工 PNG。只改 `.tex` 的结果是旧词留在 arch 图里,审稿人一眼抓到。改完跑 `cd paper/scripts && ./build_figs.sh` 重出图。
- **两个 clone 都要改**(TMLR / ICLR 各一份 `sections/`),别只改当前打开的那个。
- 每处改动可回溯到 ledger 的某一条;ledger 上没有的地方不顺手改。
- `sure` + `表面` 的可以只记不改。**预期 50%+ 条目最终判为无需改,这是正常的**,不是第一趟记多了。

## 验收

1. **重编译**:`cd paper/scripts && ./compile.sh`,rc=0,新的 `undefined reference` 数不增加(既有的 undefined citation 不管)。
2. **摘要自足**:摘要里每个符号/自造名词都在摘要内定义或已删。
3. **页序检查**(可脚本化):对每个被改的术语,`pdftotext` 后定义出现的页 ≤ 首次使用的页。
4. **验收盲读是强制步骤,且必须派给独立 subagent**——你在第二趟里已经被实现污染第二次了,自己重读绝对发现不了残留。给它新编的 PDF 前两页 + 一张随机 caption,不给任何上下文。新一轮不再产生 `承重` 条目才算过。
5. 全篇没有新增只有本组懂的词;换掉的词全仓无残留(`grep -rn` 旧词,含 `fig_*.py`)。
6. 汇报分三块,**顺序不能反**:①装配问题与结构改动(丢节、缺记号小节)②发现的 bug(自相矛盾、数值互斥、数目不自洽)③已删的废话(每条附一行删句测试)与已改的措辞。措辞列表最长但最不重要,放最后。

## 常见错判

| 症状 | 纠正 |
|---|---|
| 直接读 `.tex` 盲读 | 读者读的是排版后的页序;读 `.tex` 会漏掉"定义落在使用之后一页"这整类问题 |
| 边读边 grep 实现"确认一下" | 盲读就作废了;确认放第二趟 |
| 后文/附录有定义就放过 | 定义晚于使用照记,把定义搬到首次出现处 |
| caption 里的词"正文定义过了" | caption 是独立阅读单元,算未定义 |
| 每个没见过的名词都记 → 上百条 | 门槛是"必须重读或翻页",不是"不眼熟" |
| 承重 20+ 还在逐词记 | 那是结构问题,转去写文档级判定(缺记号约定小节) |
| 把 `LoRA`/`bootstrap`/`prefill` 改成大白话 | 领域读者认得的原样留,进良品名单 |
| 中文黑话直译当术语放过(`court`/`caliber`) | 最隐蔽的一类:它读起来像术语。按"领域文献里是这个意思吗"判 |
| 发明一个"更清楚"的新词 | 只能用领域已有的词,否则是新黑话 |
| 补定义时顺手补一句"但这只在…成立" | 那是 caveat,不是定义;caveat 进 todo 不进正文 |
| 两处数字打架,顺手改一处对齐 | 这是 bug,先报;信哪个由用户定 |
| 只改了 `.tex`,图里旧词还在 | 换词要扫 `scripts/fig_*.py` 并重出图 |
| 只改了一个 Overleaf clone | 两个 clone 的 `sections/` 都要改 |
| 顺手修了 `references.bib` / undefined citation | bib 只 pull 不写,一律不碰不报 |
| 把"X 没有 Y / X 不报 Z"当成严谨的披露留着 | 主语是不存在之物的句子先过删句测试;真承重的缺席降级成表注,不留正文 |
| grep 命中一堆 absence 句就开删 | 命中清单是候选不是死刑名单:实测 ~8 成是承重的协议/范围声明;唯一判据是删句测试 + 可见空缺规则,别为交差硬删 |
| 把废话改写得更通顺 | C 组没有改写选项:改写废话得到的是更顺的废话;只删或降级 |
| 删句后不查前后指代 | 被删句喂养的 "this comparison""that row" 会悬空;删一句要重读整段 |
| 盲读记出几十条废话还在逐句处置 | 那是整篇的病,写进文档级判定,转 `/paper-prose-tighten` 做全文清理 |
