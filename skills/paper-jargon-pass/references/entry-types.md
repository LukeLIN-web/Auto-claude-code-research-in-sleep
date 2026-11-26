# 读者与条目类型(第一趟记、第二趟改都用)

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

## 类型

**A 组 · 换词/补定义能修的**

- **名字晚于数字**——`6-hour lead steps` / `eight candidate members` / `the top $K{=}3$ members` / `spread-cap 12` / `max-lead 168`:配置常数照写没问题(数字是允许的),但**它配置的那个东西必须已经被命名过**。"lead step""member""spread cap"没定义之前,`K{=}3` 只是一个不知道在数什么的数。修法是在名词首次出现处给一句话定义,不是把数字删掉。
- **内部工作语 / 翻译残留**——组里中文黑话被直译进英文,读起来像正经术语,作者永远看不见:`擂台→ring`、`口径→caliber`、`臂→arm`、`剂量→dose`、`打底→ground`。检验法只有一条:**这个词在本领域公开文献里,是这个意思吗?** 不是就换。`ring` 没有 ⇒ 换。本仓库另有 user 裁定:`臂→arm` 也整稿禁用,按语境换 variant / configuration / condition / setting / 对照自己的名字,不一键替换(2026-09-22)。
- **一词多义 / 含义漂移**——同一个词在三处指三样东西(`caliber` 一会儿指站点网格、一会儿指权重配置、一会儿指归一化版本)。同一个词第三次出现时你又得重猜 = 记。
- **同物异名**——`regime` 与 `régime`、`tile` 与 `patch`、`benchmark` 与 `ring`、`bias-correction system` 与 `post-processed system` 与 `correction-only row` 指同一条臂。读者会以为是三个东西。**为避免重复而换的同义词也算**:`the held-out forecaster` 下一句成了 `this model`、再下一句成了 `the new predictor`——英文写作课教的「换词避免重复」在论文里是错的,同一个东西全稿只用一个名词(user 2026-11-12「加强下表达和衔接」;衔接的其余部分见 [`/paper-polish` 的 references/rewrite.md](../../paper-polish/references/rewrite.md) § 2)。
- **画布上的记号早于定义**——方法图/架构图上的 `s_m`、`q_{m,k}`、`φ_bc`、`ω`、`1…K`,图落在 p.2 而定义在 p.4。
  修法只有一个:换成 caption 或图之前的正文已经在用的词(`member ranking`、`candidate members`、`retained members`、
  `bias-correction head`);画布上补 gloss 与 caption 里补定义都不算修(user 裁定 2026-09-21)。
- **宏与上标无图例**——`\newcommand` 定义的东西对读者不存在:`\method`、`$\Tlead$`、`\starred`、`\textsuperscript{\ddag}`、`$\circ$`。查的是每个宏**排版后首次出现**的位置,以及图例是否在那之前。
- **悬空指代**——"the anchor""that régime""both grids""the deep benchmark":哪个?哪两个?什么叫 deep?**代词同理**:句首 `This` / `It` / `They` 前面有两个可能的先行词,读者要回头猜 = 记;修法是补上名词(`This shows` → `This gap shows`),名词取稿子已有的那个。
- **名不副实**——`coverage` 在三处分别是"区间命中率""站点保留比例""网格覆盖",名字一样含义不同。
- **产物血统词**——`a re-calibrated copy of the deployed ensemble`、`an earlier station-grid interpolation`、
  `the 6 h-step hindcast`、`under that same earlier normalization`、`a third hindcast`、`the stored bias-correction passes`。
  每个词都是普通英文,读者带着临时含义就能按正常速度读过去,所以**「卡住」门槛永远抓不到它**。
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
