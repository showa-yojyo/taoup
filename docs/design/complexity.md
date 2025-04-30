# Chapter 13. Complexity

[TOC]

> But what *is* “as simple as possible”? How do you tell?

## Speaking of Complexity

1. ソフトウェアの複雑性とは何かを定義する。
2. 複雑さの種類を水平的に区別する。それらは互いにトレードオフしなければならない
   ことがある。
3. 垂直的な区別として、共存しなければならない複雑さと、排除するオプションがある
   複雑さの区別をする。

### The Three Sources of Complexity

単純は美であり、風雅は善であり、複雑は醜悪であり、滑稽は邪悪だ。

* 複雑さは高く付く。
* 複雑なソフトウェアは考えるのも、試験するのも、デバッグするのも、保守するのも難
  しい。
* 複雑さの対価は運用環境配備後が最も痛手となる。

すごいことを述べている：

> Traditionally, Unix programmers push back against these tendencies by
> proclaiming with religious fervor a rhetoric that condemns all complexity as
> bad.

Unix プログラマーは（他のそれと同じように）実装の複雑さを注目する傾向がある。基
本的にはプログラムを理解しようとするときに経験する困難さの度合いだ。

顧客や使用者はプログラムのインターフェイスの複雑さによって複雑さを見る傾向があ
る。表現力が弱く、簡潔でないインターフェイスは、わずかな高水準の操作ではなく、エ
ラーを起こしやすい、あるいは単に退屈な低水分の操作を数多く使用者に強いることにな
る。

この二つの指標によって左右されるのが、もっと単純な第三の指標、つまりシステム内の
コード総行数 (codebase size) だ。通常、これが最も重要な尺度だ。

その理由は、コードの欠陥密度（特定行数あたりのバグ数）は実装言語に依存せず一定で
ある傾向がある。行数が多いほどバグも多くなり、デバッグが開発で銭と時間の最もかか
る部分となる。

* 実装の複雑さ
* インターフェイスの複雑さ
* コード量

これら三つの尺度の妥協点を探らねばならぬときが難しい。

実装の単純さを維持するため、あるいはコードベースの規模を抑えるために主に設計され
た UI が、使用者に低水準の仕事を単に押し付けることがある。この種の設計上の失敗は
あまりにもよくあることだ、伝統的な呼び名がない。そこでこれを手作業の罠と呼ぶこと
にする。

極端に高密度で複雑な実装技術を使うことで、コードベースの規模を抑えようとする圧力
がシステムに実装の複雑さを連鎖的に引き起こし、デバッグ不可能な混乱を招くことがあ
る。これを馬糞罠と呼ぶ。

プロジェクト設計者が実装の複雑さを警戒するあまり、複雑だが統一された方法で問題全
体を解決する方法を拒否し、重複する即興的コードを大量に使って個々の問題を順番に解
決していくことがある。その結果、コードベースは肥大化し、保守性の問題は統一された
方法が受け入れられていた場合よりも深刻になる。この種の失敗はあまりにもよくある。
これは即興的罠と呼ぶことにする。

* 手作業の罠
* 馬糞罠
* 即興的罠

これらは複雑性の三つの顔であり、設計者が回避しようとして陥る罠の一部だ。

### Tradeoffs between Interface and Implementation Complexity

* Richard Gabriel という Lisp 界の長年の指導者がいる。
* 論文 *Lisp: Good News, Bad News, and How to Win Big*
  * Lisp 設計の特定の流儀を主張するのが主な目的だった。
  * しかし、その一節 [The Rise of *Worse Is Better*][Gabriel] が読者の記憶に残っ
    たという。

[Gabriel]: <https://www.dreamsongs.com/WorseIsBetter.html>

Gabriel の中心的な議論は、実装とインターフェイスの複雑さの間の具体的な両立不能関
係性についてであった。そこでは次の二つを対比している：

* インターフェイスの単純さを最重視する MIT 哲学
* 実装の単純さを最重視する New Jersey 哲学

を比較している。その提案は：

* MIT 哲学は抽象的にはより優れたソフトウェアをもたらすが、New Jersey モデルの方
  がより優れた伝播特性を持つ。

時間が経つにつれて、人々は New Jersey 式ソフトウェアにより多くの注意するようにな
り、その結果、より速く改善される。«Worse becomes better.»

> The tension between these approaches arises precisely because one can
> sometimes get a simpler interface if one is willing to pay implementation
> complexity for it, or vice versa.

それが trade-off だと述べているのだった。

長時間システムコールが割り込みをどう処理するかという例が最良のもの一つだ：

* MIT: システムコールからいったん退いて、割り込みが処理されたら自動的に再開する。
* New Jersey: システムコールは中断されたことを示すエラーを返し、使用者が再実行し
  なければならない。

前者は実装が難しいが、より単純なインターフェイスに至る。後者ははるかに単純に実装
できるが、より使いにくいプログラミングインターフェイスになる。

ソフトウェアシグナルの取り扱いは System-V 式と BSD 式があるが、前者は New Jersey
哲学に、後者は MIT 哲学にそれぞれ従っている。

両者の選択の根底にあるのはこうだ：目標が全体の複雑さを抑えることだとしたら、その
ためにはどこに銭を払うのが最善なのか。

例：HTTP 404 エラー応答は古典的な New Jersey 式解決法と言える。

* 設計の一つ一つについて、この問題を注意深く考える習慣を身につけろ。
* 複雑さは慎重に予算を組まなければならない費用だ。

### Essential, Optional, and Accidental Complexity

理想的な世界では、それぞれが最小限で上品で完全な、小さくて完璧な宝石のようなソフ
トウェアしか Unix プログラマーは作らない。しかし、現実では、複雑な解決策を必要と
する複雑な問題をしばしば引き起こす。

> You can't control a jetliner with an elegant ten-line procedure.

ジェット旅客機には必然的な (essential) 複雑さがある。飛行機は空中に留まらなけれ
ばならないため、単純性と機能を取り替えることはできない。

要求がより柔軟で、期待される機能と複雑さの両立不能性の妥協点を見出しやすいソフト
ウェアでは、設計上の問題を見極め、考えることは容易だ。

> (Here, and in the rest of this chapter, we will use ‘feature’ in a very
> general sense that includes things like performance gains or overall degree of
> interface polish.)

* 偶発的な (accidental) 複雑さは、指定された一連の機能を実装する最も単純な方法を
  誰かが見つけられなかったために起こる。優れた（再）設計によって取り除くことがで
  きる。
* 選択的な (optional) 複雑さは、何らかの望ましい機能と結びついている。プロジェク
  トの目的を変更することによってのみ排除することができる。

この二つの複雑性を区別しないと設計に関する議論が混乱する。プロジェクトの目的は何
かという問いが、単純性の美学や、人々が十分に賢かったかどうかという問いと混同され
てしまう。

### Mapping Complexity

> So far, we've developed two different scales for thinking about complexity.
> These scales are actually orthogonal to each other.

[Figure 13.1] では下の尺度がグラフの横軸と縦軸になっている：

* (+) 実装の複雑さ/インターフェイスの複雑さ/コード量 (-)
* (+) 偶発的な複雑さ/選択的な複雑さ/必然的な複雑さ (-)

<!-- Figure 13.1. Sources and kinds of complexity. -->
[Figure 13.1]: <http://www.catb.org/esr/writings/taoup/html/graphics/complexity.png>

TBW

### When Simplicity Is Not Enough

## A Tale of Five Editors

### ed

### vi

### Sam

### Emacs

### Wily

## The Right Size for an Editor

### Identifying the Complexity Problems

### Compromise Doesn't Work

### Is Emacs an Argument against the Unix Tradition?

## The Right Size of Software
