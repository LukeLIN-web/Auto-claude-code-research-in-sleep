# 第 0 趟:装配检查(先跑,零阅读)

论文源码是多文件拼装的,拼装本身会坏,而坏掉的方式肉眼读单个文件看不出来。**在读任何内容之前**先跑完这一组;命中任何一条,先报给用户,不要继续往下审——审一份装配错的稿子是白干。

`sections/`、`tables/` 代表这篇稿子自己的章节目录和表目录,按 `main.tex` 的 `\input` 行换成实际目录(有的模板是 `sec/`)再跑,否则通配符什么也匹配不到。

```bash
cd <clone 目录>
# 1) 两个 section 文件内容相同 = 某一节被覆盖丢失(Overleaf 端复制粘贴事故的典型签名)
md5sum sections/*.tex | awk '{print $1}' | sort | uniq -d
# 2) main.tex \input 的目标都存在
grep -o '\\input{[^}]*}' main.tex | sed 's/\\input{\(.*\)}/\1/' | while read f; do [ -e "$f" ] || [ -e "$f.tex" ] || echo "缺 $f"; done
# 3) \label 重名(丢节的第二签名:同一个 \label{sec:intro} 出现两次)
command grep -rho '\\label{[^}]*}' sections/ tables/ | sort | uniq -d
# 4) 编译期未定义引用 / 重复标签
grep -n "There were undefined references\|multiply defined\|Citation .* undefined" main.log | head
# 5) 章节清单与 aux 对账:该有的节都在吗
grep -o '\\newlabel{sec:[^}]*}' main.aux
```

丢节要从 git 里捞回来,不要重写:`git log --oneline -- sections/03_method.tex`,再逐个 commit 比对
`git show <c>:sections/03_method.tex | head -1`,找到最后一个正常版本恢复。**恢复到 clone 里可以,推 Overleaf 必须先问用户**——clone 是用户共享仓的镜像。

> 引用完整性不归这个技能管:`references.bib` 只 pull 不写,缺条目、`[?]`、key 对不上一律不修不报(见论文目录的 `CLAUDE.md`)。第 4 条只用来发现**丢节**,不用来发现缺文献。
