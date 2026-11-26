---
name: paper-jargon-pass
description: "Use when a paper reads fine to the author but a reviewer would stall on it — 论文术语审查/没定义就用的词和数字/审稿人读不懂/统一术语/undefined notation/jargon audit for papers. Catches terms and notation used before they are defined (figure canvases included), lab-internal vocabulary leaked into English, config numbers that arrive before the thing they configure is named, one word with several meanings, artifact-lineage phrases only the outputs/ tree can translate, and 废话/无中生有. Voice, cohesion and clarity rewriting is /paper-polish, which calls this skill. Three passes — assembly check, blind read of the compiled PDF, verify against code/data and rewrite."
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
| 图表读者 | **只有这张图/表和它的 caption**,以及它落页之前的正文 | caption 里的词、**画布上画着的每个标签与符号**,若只在后文定义,对它的读者就是没定义 |

caption 不要求自足(user 裁定 2026-08-26,正本在 `paper-table-craft`「It becomes a glossary」):正文在这张图表落页之前定义过的词,caption 里用了不记;只在后文定义的照页序记,修法不是在 caption 里补定义。

**图的画布也是阅读单元,而且是最早被撞见的那个**:审稿人先翻图再读正文。方法图/架构图上的符号徽章、边标、轴名
与 caption 同待遇——`s_m`、`q_{m,k}`、`φ_bc`、`ω`、`K` 画在 §1 的 Fig 1 上而 §3 才定义,就是未定义记号
(user 裁定 2026-09-21,「⟨symbol⟩, ⟨symbol⟩ 啥意思」)。修法在图不在文:换成 caption 或前文已经在用的词
(`member ranking`、`candidate members`、`bias-correction head`),**不是**在画布上补 gloss,也不是在 caption 里补定义
(`paper-figure-craft` 同日裁定)。图落在哪一节,画布上就只能用到那一节为止的词。

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

> 引用完整性不归这个技能管:`references.bib` 只 pull 不写,缺条目、`[?]`、key 对不上一律不修不报(见论文目录的 `CLAUDE.md`)。第 4 条只用来发现**丢节**,不用来发现缺文献。

## 第一趟:盲读

```bash
pdftotext -layout main.pdf - | sed -n '1,240p'   # 正文,按页序,一次一段
for f in figures/*.pdf; do echo "== $f"; pdftotext "$f" -; done   # 每张图画布上的全部文字,按图的落页并入
```

手绘 SVG 图的画布文字就是 `scripts/fig_*_blueprint.json` 里锁住的字符串,matplotlib 图的在 `scripts/fig_*.py`
的硬编码字符串里;`pdftotext` 抓的是排版结果,以它为准。

装成**这个领域的审稿人**:懂 LoRA、bootstrap、greedy decoding、MCQ,但没读过这个仓库、没读过前几轮结果页、不知道这个组内部管什么叫什么。读到第 N 页时**不许**往后翻找定义、不许 grep 代码、不许打开 `scripts/`、不许读 appendix 去救正文。

> 隔离提醒:如果本次会话已经读过这份稿子的实现或前几轮审查记录,你已经污染了。此时把盲读派给独立 subagent(只给 pdftotext 页序文本和图的画布文字、禁止读任何别的文件),你只汇总不补充。

**待审文字多就拆给几个并行读者**(user 2026-11-16「paper polish skill 实在太慢了」)。一个读者会在一轮里把整份 ledger 想完再写:12–13 KB 的待审句子要 17–30 分钟,有一次还撞上输出上限,整轮作废;3–4 KB 只要 4–8 分钟。所以每 4 KB 左右的待审文字派一个读者,最多 4 个,在同一条消息里一起派。每个读者都拿**整份**页序文本和画布文字,所以跨节的「先用后定义」照样查得出;但它只给分到自己的那几句记条目,写自己的 `ledger-<k>.md`。汇总的一方按 id 合并,两个读者记了同一处就算一条。`/paper-polish` 的 `scripts/blind_pack.py` 就是按这个规则切分的。

### 记什么:两种信号

- **卡住**(A/B 组)——必须停下重读,或必须往回/往后翻页才能继续。能带着一个临时含义按正常速度读下去、且后文没有推翻它的,不记。
- **空转**(C 组·废话)——读得毫不费力,但读完说不出这句在这干什么:它不定义、不主张、不配置。判据是**删句测试**:把这句删掉重读前后段,若没有任何主张、定义或配置常数失去支撑,记。
- **血统**(A 组·产物血统词)——**上面两个信号都抓不到它**:它读得顺(不卡),所在的句子又承重(删句测试过不了)。
  它藏在一个修饰语里:`drawn from a re-calibrated copy of the deployed ensemble`、`on an earlier station-grid interpolation`、
  `the 6 h-step hindcast`、`under that same earlier normalization`、`a third hindcast`。盲读时对每个 *re-* / *earlier* / *stored* /
  *copy* / *third* 修饰语多问一句:「它告诉我送进前向的输入有什么不同?」答不出就记,置信度写 `no idea`——
  这一组不靠读感,第二趟还要按信号词 grep 补扫(见 A 组条目)。

卡住的承重条目通常 5–15 条。**超过 20 条就停止逐词记录,直接写文档级判定**——那已经不是措辞问题,而是这篇稿子缺一个记号约定小节或缺一张符号表。空转条目超过 ~15 条同理:那不是几句废话,是整篇在写审计日志,文档级判定里直接建议跑 `/paper-prose-tighten` 做全文清理,本技能只处置盲读撞见的这几条。

### 类型

**A 组 · 换词/补定义能修的**

- **名字晚于数字**——`6-hour lead steps` / `eight candidate members` / `the top $K{=}3$ members` / `spread-cap 12` / `max-lead 168`:配置常数照写没问题(数字是允许的),但**它配置的那个东西必须已经被命名过**。"lead step""member""spread cap"没定义之前,`K{=}3` 只是一个不知道在数什么的数。修法是在名词首次出现处给一句话定义,不是把数字删掉。
- **内部工作语 / 翻译残留**——组里中文黑话被直译进英文,读起来像正经术语,作者永远看不见:`擂台→ring`、`口径→caliber`、`臂→arm`、`剂量→dose`、`打底→ground`。检验法只有一条:**这个词在本领域公开文献里,是这个意思吗?** 不是就换。`ring` 没有 ⇒ 换。本仓库另有 user 裁定:`臂→arm` 也整稿禁用,按语境换 variant / configuration / condition / setting / 对照自己的名字,不一键替换(2026-09-22)。
- **一词多义 / 含义漂移**——同一个词在三处指三样东西(`caliber` 一会儿指站点网格、一会儿指权重配置、一会儿指归一化版本)。同一个词第三次出现时你又得重猜 = 记。
- **同物异名**——`regime` 与 `régime`、`tile` 与 `patch`、`benchmark` 与 `ring`、`bias-correction system` 与 `post-processed system` 与 `correction-only row` 指同一条臂。读者会以为是三个东西。**为避免重复而换的同义词也算**:`the held-out forecaster` 下一句成了 `this model`、再下一句成了 `the new predictor`——英文写作课教的「换词避免重复」在论文里是错的,同一个东西全稿只用一个名词(user 2026-11-12「加强下表达和衔接」;衔接的其余部分见 [`/paper-polish` 的 references/rewrite.md](../paper-polish/references/rewrite.md) § 2)。
- **画布上的记号早于定义**——方法图/架构图上的 `s_m`、`q_{m,k}`、`φ_bc`、`ω`、`1…K`,图落在 p.2 而定义在 p.4。
  修法只有一个:换成 caption 或图之前的正文已经在用的词(`member ranking`、`candidate members`、`retained members`、
  `bias-correction head`);画布上补 gloss 与 caption 里补定义都不算修(user 裁定 2026-09-21)。
- **宏与上标无图例**——`\newcommand` 定义的东西对读者不存在:`\method`、`$\Tlead$`、`\starred`、`\textsuperscript{\ddag}`、`$\circ$`。查的是每个宏**排版后首次出现**的位置,以及图例是否在那之前。
- **悬空指代**——"the anchor""that régime""both grids""the deep benchmark":哪个?哪两个?什么叫 deep?**代词同理**:句首 `This` / `It` / `They` 前面有两个可能的先行词,读者要回头猜 = 记;修法是补上名词(`This shows` → `This gap shows`),名词取稿子已有的那个。
- **名不副实**——`coverage` 在三处分别是"区间命中率""站点保留比例""网格覆盖",名字一样含义不同。
- **产物血统词**——`a re-calibrated copy of the deployed ensemble`、`an earlier station-grid interpolation`、
  `the 6 h-step hindcast`、`under that same earlier normalization`、`a third hindcast`、`the stored bias-correction passes`。
  每个词都是普通英文,读者带着临时含义就能按正常速度读过去,所以**「卡住」门槛永远抓不到它**——
  2026-09-25 `re-calibrated copy` 出现在附录正文和一张生成表的 caption 里,活过了两轮盲读,正因为它不卡。
  它是 `outputs/` 目录树的血统(哪一代回算、哪次重校、哪个网格)漏进散文:只有手里有产物树的人知道
  *re-calibrated* 指的是对保留成员重跑的偏差校正 pass。判法不是「卡不卡」,是**换一个问题**:
  「这个修饰语告诉读者送进前向的输入有什么不同?」稿子里没写出那个不同,就是血统词。
  处置两选一,**按序试**:①删掉修饰语,主句保留(`drawn as in Appendix X` 已经把随机控制说完了);
  ②它指的输入差别确实改变读数(换了站点网格 / 换了归一化 / 换了校正头),就把**那个差别**写出来,
  一个从句,用稿子已有的词(`on a station grid that predates the deployed one`)。
  **绝不补定义**——给 `re-calibrated copy` 下定义等于把产物目录名搬进论文。
  另外每条都要**同时报 user**:血统词常常是嫁接件的自白(一条臂混两代产物,根 CLAUDE.md §5),
  「重跑到部署网格上」还是「删这条消融」是 user 的裁定,改词只是遮住它。

**B 组 · 换词修不了的**(盲读者最容易发现,因为你没有先验去替它圆场)

- **隐含前提**——句子通顺,但要先知道某个没写出来的设定才成立。
- **数值互斥**——同一篇里 `240-hour forecast horizon` 与 `max-lead 168` 并存:可能是两个不同的量(模型最长预报时效 vs 评测截断),也可能是错。**盲读者分不出来,正是问题所在**——记下来,第二趟对账。
- **自相矛盾**——摘要断言 A,正文撤回 A;两表同一格给不同数。**这是 bug,单独报,不许靠改措辞抹平。**
- **数目不自洽**——号称"五个 benchmark"实际列了四个加一个附录的;"all eight"与表里行数对不上。
- **一句话塞太多**——单个术语都没问题,但一句里堆了十几个专名(用户举的那句就是:切网格 + 校正 pass + 候选成员 + top-K + 离散度上限 + 集成前向,全在一个分号句里)。处置是**拆句**,不是换词。

**C 组 · 废话**(不是看不懂,是没内容;处置只有删或降级,没有"改写"选项。判死生需要全稿语境——套件枚举了哪些 benchmark、别的表有哪些行——所以 C 组**不吃盲读隔离**:盲读只标记空转句,判定放第二趟,也可以在第二趟直接用 grep 候选清单补扫)

- **无中生有**——句子的主语是一个不存在的东西(`X does not report Y for this setting`)。判死生看读者在这张图表里看不看得见这个空缺,判据和落法见 `/paper-prose-tighten` 第 5 类。
- 其余子类照 `/paper-prose-tighten` 的切除分类认:记账计数、自辩元叙述、否弃方案的游记、复述与叠 hedge。盲读时不用背分类,过删句测试就记;完整判据与保留红线(显著性限定词、划范围的分母、协议差异不许删)以那份技能为准。

写到论文目录(放论文 `CLAUDE.md` 的那个目录)下的 `review-stage/jargon/<UTC时间戳>/ledger-<节名>.md`(**不要写进 Overleaf clone**)。一节一份,拆给几个读者时一个读者一份(`ledger-<k>.md`)。用分块不用表格。

```
### N. <一句话标题>
- 首次出现:PDF p3 / sections/04_results.tex:60      ← 两个都要:页序定"晚于使用",行号定"改哪里"
- 其它出现::64 :127 / tables/08_ablation.tex:9  ← 只列让理解更糟的那几处
- 原句:<逐字抄,别转述>
- 类型:内部工作语
- 卡点:<为什么读不下去,一句话>
- 我猜是:<你的猜测>  置信度:sure | guess | no idea
- 严重度:承重 | 局部 | 表面
- 读者:摘要 | 正文 | 图表
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

- **文档级判定**——不锚在任何行号上的整篇问题。论文里最常见的三条:①**缺记号约定**(应该在 §3.1 开头用一段把 lead step / member / spread cap / $K$ / $M$ 一次性定义,而不是散在六处);②**这一节是对另一节的 diff**(症状:一半悬空指代都"翻到 §3 十秒就能答"——如果 §3 存在的话);③**术语在正文与 caption 之间不同步**。这类问题的正解是加一段/改结构,不是逐词改写。
- **良品名单**——你专门判定过"这是真术语,别动"的词:`LoRA`、`prefill`、`greedy decoding`、`bootstrap`、`oracle`、`intention-to-treat`、`pp`。不写下来,第二趟会重新纠结,甚至把它们改成大白话。

## 第二趟:查证 + 改写

现在才允许读实现、跑脚本、翻实验产物。

**先找承重条目之间的共同根因。** 它们往往有一半出自同一个病(最常见:整篇缺一段记号约定)。一段小节能一次干掉六条,逐条处置是最浪费的做法。

**改之前先对账。** `grep` 原词的命中率比想象中低:论文里的词在代码里往往叫别的名字(`member` = `ens_slot`、`lead step` = `t_out`)。有效顺序是**先把数字对一遍**:B 组记下的"数值互斥"条目,拿表和图读数的数据文件、逐题的评测产物、出图脚本逐个核。数字错只能这样找出来,读措辞永远发现不了。

**B 组不进改写流程**:自相矛盾、数目不自洽、数值互斥 → 直接列给用户(信哪个由用户定);断句歧义、一句话塞太多 → 改结构(拆句/拆列表),不换词;隐含前提 → 补一句口径**并同时报**(作者脑子里有一套没写下来的约定,补完得让他确认补对了)。

**C 组在改写前处置,只有两个动作**:①默认**整句删**。删完重读该段:一查悬空指代(被删句喂养的 "this comparison""that row" 会跟着悬空),二反跑删句测试——若某个主张真的少了支撑,恢复原句、改判 keep 并记一笔为什么。②缺席确实需要交代的(表里有 `—`/`*` 等着解释),先**降级成表注一条**,再删正文句。删句持 `/paper-prose-tighten` 的红线:显著性限定词、划范围的分母、让对比不公平的协议差异,不许跟着整句陪葬——它们缩成主张上的一个形容词或一条表注活下来。

两个实战陷阱:

- **废话的主产地是 caption,而表 caption 多为脚本生成**(文件头有 AUTO-GENERATED 标记)。删句必须落在生成器(`tab_*.py` / caption SSOT)并重跑构建——直接改 `.tex` 会被下一次 build 原样复活;降级出的表注同样写进生成器。顺手核对生成器注释:它可能声称"caption 里解释了"而 caption 里其实没有。
- **上一版分析的披露句不许删**:`An earlier pre-specified analysis had shown little effect; the full read supersedes it` 形似流水账,但删掉=隐藏一次结果不一致的前置分析,变相把主张洗得更稳。这类句子连同你的判断上报 user,与 B 组同待遇。

A 组逐条处置。**四个动作是有序的,不是并列的**——从上往下试,能停在第 1 条就别走到第 4 条
(user 裁定 2026-08-26,由本技能第一次实战而来):

> **奥卡姆剃刀:没有必要不要新增名词。**
> 一个词读者看不懂,默认答案是**删掉它**或**换成稿子里已经在用的词**,
> **不是给它补一句定义**。补定义是最后手段——它把一个词从"读者的困惑"
> 升级成"读者必须记住的负担",名词表越长,稿子越难读。

1. **删掉这个词**(不是删整句)——句子改用已有的词把同一件事说出来。
   **范例(即本条由来)**:`the gate` 全稿出现 29 次,指的是"按 $s_m$ 给集成成员排序、留 top-$K$"。
   §3.2 本来就把 $s_m$ 叫作 *a ranking score*,于是全稿 `gate` → `ranking`,一个新名词不留。
   当时的错误做法是在 Fig 1 caption 里补一句 "that gate being the ranking step that…"——
   **那是给一个不该存在的名词发身份证。**
2. **换成稿子里已经在用的词 / 领域通行叫法**——按序找:自己稿子里的同义词(零新增名词),再是公开文献或教材的叫法,再是依赖库或上游 benchmark 的官方命名;不自己发明新词。
   `ring` → `benchmark`、`tier` → `channel`(稿子本来就有 channel)、`level`(打平义)→ `tie`。
3. **删掉整句**——这个术语全篇只用一次、删了不损失任何主张。**这一条比想象中常用**。
4. **首次出现处补一句定义**(≤1 个从句)——**只有前三条都不成立时才用**:
   概念真实存在、稿子里没有同义词、领域也确实没有现成词,且它承重到不能删。
   `member (one perturbed run; eight of them form each ensemble)`。

**只出现一次的词一律先假定要删。** 一个名词全稿只用一次,几乎不可能是承重概念——
它是作者写那一句时顺手造的。删它,用已有的词重写那半句。
`the live target` / `amortization floor` / `recency slot` / `seed budget` / `the churn` /
`Room to spread` 都是这么删掉的,每一条的替换都来自稿子已有的词(`the verifying analysis` /
`cannot be reused` / `reserved for the most recent analysis cycle` / `the eight perturbed members` /
`the change` / `More than one member`)。

**自查(第二趟收尾跑一次)**:把候选词按全稿出现次数排序。`n == 1` 的逐个问"删得掉吗";
`n` 很大但读者仍看不懂的,问"稿子里有没有同义词"——`gate` 就是后者,**频次不是保留理由**。

```bash
c=<clone 目录>
for w in "the gate" "the ladder" "the map" "regime"; do
  printf '%3d  %s\n' "$(grep -roiF "$w" $c/sections/*.tex | wc -l)" "$w"
done | sort -n
# 血统词候选(读感抓不到,只能 grep):每条命中问「它说的输入差别写出来了吗」;表 caption 改生成器
grep -rnoiE '\b(re-?calibrated|re-?scaled|re-?struck|re-?run|rerun|re-?fit|earlier|a third|stored|cached|booked|copy of the)\b[^.]{0,70}' \
  $c/sections/*.tex $c/tables/*.tex
```

### 改写纪律(论文特有,比文档严)

- **只动措辞,不动事实、不动数字、不动结论。** 界线:从方法节/代码/产物**搬运**一条已存在的事实过来当定义 = 允许;**推断、补全缺失项、扩大结论范围** = 动事实,禁止。表里少两行 → 只报不补。
- **删词不许顺手升级主张**:原文只指了表就别改写成"最强/领先"。
- **补定义不许变成补 caveat**。这份稿子的规矩是 caveat 越少越好(论文目录的 `CLAUDE.md`);"X 只在 Y 条件下成立"这种句子不是定义,是 caveat,该进 todo 不进正文。定义是**说 X 是什么**,一句话,陈述句。
- **正文不写结果数字**:如果某条的修法是"把数值搬进正文解释",停——数字的家是表和图,正文只说方向和判没判住。配置常数(时间步长、$K$、网格分辨率、时效上限、成员数)不算结果数字,照写。
- **换词是全仓操作,且必须扫到图**:`.tex` 正文 + table caption + 表头 + 出图脚本里的硬编码字符串 + 手工 PNG。只改 `.tex` 的结果是旧词留在 arch 图里,审稿人一眼抓到。改完照论文目录 `CLAUDE.md` 的命令重出图。
- 每处改动可回溯到 ledger 的某一条;ledger 上没有的地方不顺手改。
- `sure` + `表面` 的可以只记不改。**预期 50%+ 条目最终判为无需改,这是正常的**,不是第一趟记多了。

## 验收

1. **重编译**(用论文目录 `CLAUDE.md` 写的命令),rc=0,新的 `undefined reference` 数不增加(既有的 undefined citation 不管)。
2. **摘要自足**:摘要里每个符号/自造名词都在摘要内定义或已删。
3. **页序检查**(可脚本化):对每个被改的术语,`pdftotext` 后定义出现的页 ≤ 首次使用的页。**含图**:每张图画布上的
   每个符号(`pdftotext figures/<图>.pdf -`),定义页 ≤ 图的落页;Fig 1 落在 §1 ⇒ 画布上一个 §3 记号都不许有。
4. **验收盲读是强制步骤,且必须派给独立 subagent**——你在第二趟里已经被实现污染第二次了,自己重读绝对发现不了残留。给它新编的 PDF 前两页 + 一张随机 caption,不给任何上下文;待审文字多就照第一趟的规则拆给几个并行读者。被 `/paper-polish` 调用时不做(见它的 § 6)。新一轮不再产生 `承重` 条目才算过；同一批改动最多验收两轮（只核修改的重读也算一轮）。第二轮之后只改真错（数错、说过头、前后矛盾），其余列给 user，不派第三轮——零上下文的读者每轮总能找出新东西，「读到干净为止」不会停。
5. 全篇没有新增只有本组懂的词;换掉的词全仓无残留(`grep -rn` 旧词,含 `fig_*.py`)。
6. 汇报分三块,**顺序不能反**:①装配问题与结构改动(丢节、缺记号小节)②发现的 bug(自相矛盾、数值互斥、数目不自洽)③已删的废话(每条附一行删句测试)与已改的措辞。措辞列表最长但最不重要,放最后。
