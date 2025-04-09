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

パラコンパクトというのは聞いたことがあるが、セミコンパクトとは。

* Unix システムコール API は半コンパクトだ。Unix プログラマーはアプリケーション
  の大半の実装に十分なシステムコール（ファイルシステム、シグナル、プロセス）の部
  分集合がその脳裡にある。
* C 言語ライブラリーはコンパクトでない。数学関数だけでもそのすべてがプログラマー
  一人の頭蓋に収まることはない。

認知心理学の基礎的な知見を援用し、魔法の数字とされる 7 を閾値とする：

> This gives us a good rule of thumb for evaluating the compactness of APIs:
> Does a programmer have to remember more than seven entry points? Anything
> larger than this is unlikely to be strictly compact.

コンパクトなものの例をさらに挙げる：

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

<!-- fudge: ごまかす -->

次の記述にある薄いラッパーというのは何か筋が良さそうだ：

> Many of its most effective tools are thin wrappers around a direct translation
> of some single powerful algorithm.

しばらく diff の議論が続く。

例えば diff を使う人が中心的なアルゴリズムを完璧に理解しなくても何をするのかを
直感的に理解することができるのは、次の理由による：

> First, the central engine is solid, small, and has never needed one line of
> maintenance. Second, the results are clear and consistent, unmarred by
> surprises where heuristics fail. (Doug McIlroy)

<!-- unmarred: having no injury, defacement, or imperfection -->

> The opposite of a formal approach is using *heuristics*—rules of thumb leading
> toward a solution that is probabilistically, but not certainly, correct.

発見的手法を採用する状況は例えば：

* 決定論的に正しい解答が不可能である場合（例：スパムフィルター）
* 形式的に正しい方法が知られているが、実行不能なほど高く付く場合（例：仮想メモ
  リー管理）

発見的手法の厄介事とは：

> The trouble with heuristics is that they proliferate special cases and edge
> cases. If nothing else, you usually have to backstop a heuristic with some
> sort of recovery mechanism when it fails.

特別な場合や極端な場合がべらぼうに増える。

<!-- proliferate: to increase a lot and suddenly in number -->

### The Value of Detachment

制約は、経済性だけでなく、ある種のエレガントな設計を促した。

> To design for compactness and orthogonality, start from zero. Zen teaches that
> attachment leads to suffering; experience with software design teaches that
> attachment to unnoticed assumptions leads to non-orthogonality, noncompact
> designs, and projects that fail or become maintenance nightmares.

ゼロから始めるというのは、要らない仮定や先入観に執着するなという心得と捉えればい
い。

> Abstract. Simplify. Generalize.

単純な文章でこの節の本質を表し切った。

> Jokes about the relationship between Unix and Zen are a live part of the Unix
> tradition as well.

そういえば Python も禅がどうのとか言っていた記憶がある。

## Software Is a Many-Layered Thing

関数やオブジェクトの階層を設計する方向は大まかに二つある。どちらの方向をいつ選ぶ
コードの階層化に大きな影響を与える。

### Top-Down versus Bottom-Up

オブジェクト指向プログラミング言語のクラス階層と同様に、上下関係は抽象度の高いほ
うが上とする。

> One direction is bottom-up, from concrete to abstract — working up from the
> specific operations in the problem domain that you know you will need to
> perform. （中略） The other direction is top-down, abstract to concrete — from
> the highest-level specification describing the project as a whole, or the
> application logic, downwards to individual operations.

トップダウンとボトムアップの違いを具体的に考えるには、設計が次のどちらを中心に構
成されているのかを求めろ：

* メインループ
* メインループが呼び出すことが可能な操作全てのライブラリー

この方向選択は重大事だと述べる。

> Purely top-down programming often has the effect of overinvesting effort in
> code that has to be scrapped and rebuilt because the interface doesn't pass a
> reality check.
>
> In self-defense against this, programmers try to do both things — express the
> abstract specification as top-down application logic, and capture a lot of
> low-level domain primitives in functions or libraries, so they can be reused
> when the high-level design changes.

Unix プログラマーはシステムプログラミングを中心とした伝統を受け継いでいる。そこ
では、低水準要素がハードウェア階層の操作であり重要だ。そのため、学習本能によりボ
トムアップ方式に傾倒する。

ボトムアップの利点をいくつか述べている：

> Bottom-up programming gives you time and room to refine a vague specification.
> Bottom-up also appeals to programmers' natural human laziness — when you have
> to scrap and rebuild code, you tend to have to throw away larger pieces if
> you're working top-down than you do if you're working bottom-up.

実際のコードはこの二つの方式のどちらも用いてプログラムされる傾向がある。そこで
「接着剤」が登場する。

### Glue Layers

> When the top-down and bottom-up drives collide, the result is often a mess.
> The top layer of application logic and the bottom layer of domain primitives
> have to be impedance-matched by a layer of glue logic.

このパラグラフの英文和訳はすごく難しい。

> One of the lessons Unix programmers have learned over decades is that glue is
> nasty stuff and that it is vitally important to keep glue layers as thin as
> possible.

接着のための層を可能な限り薄く保つことが死活的に重要だそうだ。

Web ブラウザーの例では、DOM と画面の間に位置するはずの描画コードが接着層の一部だ
と述べている。このコードはブラウザーの中でバグが最も発生しやすいことが知られてい
る。なので、これを一般化すると？

> A Web browser's glue layer has to mediate not merely between specification and
> domain primitives, but between several different external specifications:

いろいろなものを仲介する必要があるので、不具合が発生しやすいという理解でいいか。

接着層は縦方向に分裂しやすい。

> The thin-glue principle can be viewed as a refinement of the Rule of
> Separation.

最後の一文も和訳しにくい：

> Policy (the application logic) should be cleanly separated from mechanism (the
> domain primitives), but if there is a lot of code that is neither policy nor
> mechanism, chances are that it is accomplishing very little besides adding
> global complexity to the system.

### Case Study: C Considered as Thin Glue

> The C language itself is a good example of the effectiveness of thin glue.

なんてことを言うのだ。

> the architectures in every generation of computers, from early mainframes
> through minicomputers through workstations through PCs, had tended to
> converge.

この極限を classical architecture と呼んでいるのも含めて、この指摘は面白い。

C 言語設計の狙いを一言で表すと「構造化アセンブラー」だ：

> Thompson and Ritchie designed C to be a sort of structured assembler for an
> idealized processor and memory architecture that they expected could be
> efficiently modeled on most conventional computers.

言わんとすることがなんとなく理解できる。スーファミゲームプログラムのアセンブル
コードを解読しているときに、メモ代わりに C 言語のコードを添える者としては。

> C started out as a good fit for microprocessors and, rather than becoming
> irrelevant as its assumptions fell out of date, actually became a better fit
> as hardware converged more closely on the classical architecture.

ハードウェアが極限値 classical architecture にどんどん収束していった。そういうわ
けで、C 言語は汎用プログラミング言語としてすべてを席巻した。

> C, designed as a thin but flexible layer over the classical architecture,
> looks with two decades' additional perspective like almost the best possible
> design for the structured-assembler niche it was intended to fill.

何か具体的な例を挙げられるようにしたい。

> This history is worth recalling and understanding because C shows us how
> powerful a clean, minimalist design can be.

かのサンテグジュペリはかつて飛行機の設計についてこう述べた：完璧に到達するのは、
これ以上加えるものがないときではなく、これ以上取り除くものがないときだ。作家とい
うか、フランス料理の巨匠のような感性だと思う。

> The history of C is also a lesson in the value of having a working reference
> implementation *before* you standardize.

## Libraries

> One consequence of the emphasis that the Unix programming style put on
> modularity and well-defined APIs is a strong tendency to factor programs into
> bits of glue connecting collections of libraries, especially shared libraries
> (the equivalents of what are called dynamically-linked libraries or DLLs under
> Windows and other operating systems).

共有ライブラリーというもの関する詳細な記述などはない。読者は Windows でいうとこ
ろの DLL と同等の意味を持つファイルだという一言で理解できぬようではまずい。

> Under Unix, it is normal practice to make this layering explicit, with the
> service routines collected in a library that is separately documented.

文書がライブラリー単位で分離して整っているというのが要点。

> There is a flip side to this. In the Unix world, libraries which are delivered
> *as libraries* should come with exerciser programs.

オープンであるということでしかなく、文書化された形がプログラムだけしかなく、C プ
ログラムから簡単に呼び出すことができないインターフェイスを持つのは、苛つくという
意見の人がいる。

共有ライブラリーの一形態として、プラグインというものがある：

> An important form of library layering is the *plugin*, a library with a set of
> known entry points that is dynamically loaded after startup time to perform a
> specialized task.

### Case Study: GIMP Plugins

ここで GIMP の話題になる。著者は GIMP のアプリケーション設計を次のように分析して
いる。アプリケーション自体が一つのライブラリーであるとみなしている：

> But GIMP is built as a library of image-manipulation and housekeeping routines
> called by a relatively thin layer of control code. The driver code knows about
> the GUI, but not directly about image formats; the library routines reverse
> this by knowing about image formats and operations but not about the GUI.

GIMP の主要部分は libgimp と呼ばれる文書化されたライブラリー層であり、他のプログ
ラムは libgimp を使うことがある。実際、Windows 版だが GIMP2 のインストールフォル
ダーを調べると、実行ファイルのあるフォルダーにファイル `libgimp-2.0-0.dll` が存
在する。さらに多数の DLL ファイルが配置されていて、これらにプラグインファイルが
紛れているのだろう。

> A registry of GIMP plugins is available on the World Wide Web.

プラグインを任意に選択してアプリケーションとしての GIMP に組み込むという設計。

> Though most GIMP plugins are small, simple C programs, it is also possible to
> write a plugin that exposes the library API to a scripting language;

GIMP プラグインも公開インターフェイスを開陳して、他のプログラムが使えるようにす
ることが可能と読める。

## Unix and Object-Oriented Languages

私は Unix とオブジェクト指向プログラミングのどちらにも助けられたと感じている者な
ので、次の見解は意外：

> There is some tension and conflict between the Unix tradition of modularity
> and the usage patterns that have developed around OO languages. Unix
> programmers have always tended to be a bit more skeptical about OO than their
> counterparts elsewhere.

> Even when Unix programmers use other languages, they tend to want to carry
> over the thin-glue/shallow-layering style that Unix models have taught them.

オブジェクト指向言語は抽象化を容易にすることは、コードで単純な仕事を複雑な方法で
やってしまうような場合に逆効果になり得る。

いくら層の一枚一枚は薄くても、重ね過ぎると透明性を損なう：

> It becomes too difficult to see down through them and mentally model what the
> code is actually doing. The Rules of Simplicity, Clarity, and Transparency get
> violated wholesale, and the result is code full of obscure bugs and continuing
> maintenance problems.

<!-- exacerbate: to make something that is already bad even worse -->

> Another side effect of OO abstraction is that opportunities for optimization
> tend to disappear.

確かに。可換則などの代数的な性質が成り立つかどうかが示されないとも述べている。

> Unix programmers tend to share an instinctive sense of these problems. ...

* Unix 界では正統派オブジェクト指向プログラミングに対する批判が、よそでは許され
  ていないほど声高に叫ばれている。
* Unix プログラマーはオブジェクト指向プログラミングを使わない状況を知っている。

オブジェクト指向プログラミングは GUI では上手くいく。クラスと概念の対応関係が間
違いにくいからではないかとある。

まとめ：

> One of the central challenges of design in the Unix style is how to combine
> the virtue of detachment (simplifying and generalizing problems from their
> original context) with the virtue of thin glue and shallow, flat, transparent
> hierarchies of code and design.

## Coding for Modularity

モジュール性を向上させるのに役立つかもしれないチェックリスト。

* 大域変数の個数
* モジュール個別の規模が [Hatton の急所][Hatton] の急所に収まる
* 関数の呼び出し側との契約を（形式的にでなくてよいので）一行で記述できる
* 内部 API がある
* API, クラス、データ構造などの入口の数が七で収まる
* モジュールあたりの入口の数はどう分布しているか

一行コメントの思想は Python の docstring が受け継いでいる。

ここでの内部 API とは、関数呼び出しやデータ構造の集合体であって、それを単位とし
て他の人に陳述可能であるものを指す。優れた API はその背後にある実装を見ずとも、
筋が通っていて無理がないものだという：

> Try to describe it to another programmer over the phone. If you fail, it is
> very probably too complex, and poorly designed.

[Hatton]: <http://www.catb.org/esr/writings/taoup/html/graphics/hatton.png>
