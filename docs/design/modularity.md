# Chapter 4. Modularity

[TOC]

> The Rule of Modularity bears amplification here: The only way to write complex
> software that won't fall on its face is to build it out of simple modules
> connected by well-defined interfaces, so that most problems are local and you
> can have some hope of fixing or optimizing a part without breaking the whole.

本章冒頭部分には Unix プログラマーがモジュール化を得意とするという記述が複数現れ
る。

昔は関数呼び出しのオーバーヘッドが無視できぬほどだったらしく、大きな関数を書く傾
向があったという。

## Encapsulation and Optimal Module Size

モジュール性の規則。性質の良いモジュールは次の規則に従う：

* お互いの内部を公開しない。
* お互いの実装の途中を呼び出さない。
* 大域データを乱雑に共有しない。
* API を使って通信する。

> On the design level, it is the APIs (not the bits of implementation between
> them) that really define your architecture.

<!-- choke point: 渋滞点 -->

有能な開発者には、インターフェースを定義し、それを説明する簡単なコメントを書き、
それからコードを書くことから始める者がいるという。

1970 年代以来、計算機科学では次のことが常識となっている：ソフトウェアシステムは
入れ子構造のモジュールの階層として設計し、各階層のモジュールの粒度は最小限に抑え
る。

本書の [Figure 4.1] はモジュールの欠陥密度とモジュール規模のプロットだ。これによ
ると：

[Figure 4.1]: <http://www.catb.org/esr/writings/taoup/html/graphics/hatton.png>

> Very small and very large modules are associated with more bugs than those of
> intermediate size.

以降、このバグ密度曲線を Hatton 曲線と呼ぶことにする。

プロットが線形にならない理由は色々と考えられるが、モジュールの規模が小さいからと
いって、インターフェイスも単純になるとは限らないからなどが挙げられる？

脚注の Brooks の法則を引用しておく：

> Brooks's Law predicts that adding programmers to a late project makes it
> later. More generally, it predicts that costs and error rates rise as the
> square of the number of programmers on a project.

何かのときに出典と要旨を口述できるようにしておきたい。

## Compactness and Orthogonality

> Unix programmers have learned to think very hard about two other properties
> when designing APIs, command sets, protocols, and other ways to make computers
> do tricks: *compactness* and *orthogonality*.

計算機に数学の解析論のような芸をさせるということか？

### Compactness

本書のコンパクト性の定義はこうだ：

> Compactness is the property that a design can fit inside a human being's head.

具体的には、経験豊富な使用者が手引書を普通必要とするかどうかだ。そうでなければそ
の設計はコンパクトだと言える。

> Very few software designs are compact in an absolute sense, but many are
> compact in a slightly looser sense of the term. （中略） Practically speaking,
> such designs normally need a reference card or cheat sheet but not a manual.
> We'll call such designs *semi-compact*, as opposed to *strictly compact*.

例: TBW

TBD: 豆知識

> Among Unix tools, make(1) is compact; autoconf(1) and automake(1) are not.
> Among markup languages, HTML is semi-compact, but DocBook （中略） is not. The
> man(7) macros are compact, but troff(1) markup is not.
>
> Among general-purpose programming languages, C and Python are semi-compact;
> Perl, Java, Emacs Lisp, and shell are not (especially since serious shell
> programming requires you to know half-a-dozen other tools like sed(1) and
> awk(1)). C++ is anti-compact — the language's designer has admitted that he
> doesn't expect any one programmer to ever understand it all.

知っている HTML と DocBook の対比については納得する。シェルが半コンパクトでない
というのは意外だが、それは他の CLI を使いこなすことを前提としているためか。
Python が半コンパクトとみなすことを許しても、C++ はさすがにコンパクトであるとみ
なすわけにはいかない。この仕様が私の頭蓋に収まるわけがない。

> The purpose of emphasizing compactness as a virtue is not to condition you to
> treat compactness as an absolute requirement, but to teach you to do what Unix
> programmers do: value compactness properly, design for it whenever possible,
> and not throw it away casually.

コンパクト性がどのモジュールにも必要だと主張しているわけでは全然ないが、可能な限
りコンパクトに設計するのは価値がある。

### Orthogonality

> Orthogonality is one of the most important properties that can help make even
> complex designs compact. In a purely orthogonal design, operations do not have
> side effects;

直交性というか、ベクトルの線形独立性のような概念だと解釈できる。画像編集ソフトの
Brightness/Contrast コントロールは直交性がある：

> Imagine how much more difficult it would be to adjust a monitor on which the
> brightness knob affected the color balance: you'd have to compensate by
> tweaking the color balance every time after you changed the brightness. Worse,
> imagine if the contrast control also affected the color balance; then, you'd
> have to adjust both knobs simultaneously in exactly the right way to change
> either contrast or color balance alone while holding the other constant.

単純性は直交性を含意する：

> Doug McIlroy's advice to “Do one thing well” is usually interpreted as being
> about simplicity. But it's also, implicitly and at least as importantly, about
> orthogonality.

直交性はテストと開発の時間を短縮する。

直交コードは文書化しやすく、再利用しやすい。

リファクタリング：

> The concept of *refactoring*, which first emerged as an explicit idea from the
> ‘Extreme Programming’ school, is closely related to orthogonality. To refactor
> code is to change its structure and organization without changing its
> observable behavior.

Unix API は直交性の良い例なので、非 Unix プログラマーであっても研究する価値はあ
る：

> But on the whole the Unix API is a good example: Otherwise it not only would
> not but *could* not be so widely imitated by C libraries on other operating
> systems. This is also a reason that the Unix API repays study even if you are
> not a Unix programmer; it has lessons about orthogonality to teach.

### The SPOT Rule

DRY 原則および SPOT 規則という術語を導入する最初のパラグラフがきわめて重要だ：

> *The Pragmatic Programmer* articulates a rule for one particular kind of
> orthogonality that is especially important. Their “Don't Repeat Yourself” rule
> is: every piece of knowledge must have a single, unambiguous, authoritative
> representation within a system. In this book we prefer, following a suggestion
> by Brian Kernighan, to call this the Single Point Of Truth or SPOT rule.

反復は一貫性を欠き、コードが微妙に壊れてしまう。

* 全ての反復を変更する必要があるのに、一部だけを変更してしまう。
* コードの構成をきちんと考えていない。

> Complexity is a cost; don't pay it twice.

これは標語として開発室の壁にでも掲示しておくといい。

リファクタリング：

> Often it's possible to remove code duplication by refactoring; that is,
> changing the organization of your code without changing the core algorithms.

反復や重複を発見したら、そこから DRY, SPOT に近づける方向に変更することを真剣に
考えろ、と読んだ。

### Compactness and the Strong Single Center

一行目から難しいのには参った：

> One subtle but powerful way to promote compactness in a design is to organize
> it around a strong core algorithm addressing a clear formal definition of the
> problem, avoiding heuristics and fudging.

次の記述にある薄いラッパーというのは何か筋が良さそうだ：

> Many of its most effective tools are thin wrappers around a direct translation
> of some single powerful algorithm.

TBD: しばらく diff の議論が続く。



### The Value of Detachment

## Software Is a Many-Layered Thing

### Top-Down versus Bottom-Up

### Glue Layers

### Case Study: C Considered as Thin Glue

## Libraries

### Case Study: GIMP Plugins

## Unix and Object-Oriented Languages

## Coding for Modularity
