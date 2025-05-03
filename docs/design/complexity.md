# Chapter 13. Complexity

[TOC]

> But what *is* “as simple as possible”? How do you tell?

## Speaking of Complexity

1. ソフトウェアの複雑度とは何かを定義する。
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

> In [Chapter 4] we saw that accidental interface complexity often comes from
> non-orthogonality in the interface design — that is, failing to carefully
> factor the interface operations so that each does exactly one thing.

```raw
Non-orthogonality = (Interface complexity, Accidental complexity).
```

偶発的なコードの複雑さ（仕事を成し遂げるために必要以上にコードを複雑にすること）
は、多くの場合、時期尚早の最適化から生じる。

```raw
Premature optimization = (Implementation complexity, Accidental complexity).
```

コードベースの肥大化は、SPOT 規則に違反してコードを重複させたり、コードの整理が
不十分で再利用の機会が認識されなかったりすることが原因であることが多い。

```raw
Violating the SPOT rule = (Codebase size, Accidental complexity).
```

インターフェイスの必然的な複雑さは、ソフトウェアの基本的な機能要件を削ることなく
削減することは通常、できない。

```raw
Functional requirements = (Interface complexity, Essential complexity).
```

コードベースの必然的規模は開発ツールの選択と関連する。機能一覧が一定であればコー
ドベースの規模で最も重要な要因は、おそらく実装言語の選択 ([Chapter 8]) だから
だ。

```raw
Development tools = (Codebase size, Essential complexity).
```

> Sources of optional complexity are the most difficult to make useful
> generalizations about, because they so often depend on delicate judgments
> about which features it is worth paying the complexity cost for.

インターフェイスの選択的複雑さは、多くの場合、使用者の生活を楽にする便利な機能を
追加することから生じるが、プログラムの機能には必須ではない。

```raw
Convenience features = (Interface complexity, Optional complexity).
```

使用者の目に見える機能と使用される算法が一定を保っているという仮定下で、コード
ベース規模の増大は、コメントの追加、長い変数名の使用など、保守性を高めることを意
図したさまざまな慣行から生じることが多い。

```raw
Methodology overhead = (Codebase size, Optional complexity).
```

実装の選択的複雑さはプロジェクトに関わるすべてのものによって引き起こされる傾向が
ある。

```raw
EVERYTHING ELSE = (Implementation complexity, Optional complexity).
```

このプロットは複雑さの原因を対処する方法と、複雑さの種類を攻略する方法を教えるも
のだ。

* コードベースの規模はより良い道具で対処する。
* 実装の複雑さは算法をより適切に選択することで対処する。
* インターフェイスの複雑さには、人間工学や使用者心理を考慮した、より優れた双方向
  操作設計で対処しなければならない。コードを書くよりも難しい。
* 偶発的な複雑さは、もっと単純な方法があることに気づくことで解消できる。
* どのような機能が価値あるものなのか、文脈に依存した判断を下すことで、選択的複雑
  さを削減することが可能。
* 必然的複雑さを減らすには、対処する問題を根本的に再定義し、ひらめきを得ることで
  しか成し得ない。

<!-- epiphany: a moment of sudden and great revelation or realization -->

### When Simplicity Is Not Enough

Unix プログラマーはしばしば、選択的複雑さがすべて偶然的であるかのように話す（振
る舞う）。それ以上に、Unix の伝統には、選択的複雑さを受け入れるのではなく、機能
を削除することに強い執着がある。

> But computing resources and human thinking time, like wealth, find their
> justification not in being hoarded but in being spent.

これは名言。

> As with other forms of asceticism, one has to ask when design minimalism stops
> being a valuable form of self-discipline and starts being a mere hair shirt —
> a way to indulge those feelings of virtue at the expense of actually using
> that wealth to get work done.
<!-- asceticism: 苦行 -->
<!-- to indulge: to give someone anything they want and not to mind if they behave badly -->

これは文章が難しい。この質問はたいへん危険であり、優れた設計規律を完全に放棄する
議論になりやすい。しかし必要だ。
<!-- inexorably: in a way that continues without any possibility of being stopped -->
<!-- damnation: the act of sending someone to hell or the state of being in hell -->

## A Tale of Five Editors

事例研究に異なる Unix エディターを五つ使う。評価基準となる仕事は次だ：

* プレーンテキスト編集
* リッチテキスト編集：フォントの変更、色、テキスト区間の他の種類の性質（ハイパー
  リンクであることなど）を含む。このような編集ができるエディターは UI での属性の
  表示と、ディスク上のデータ表現 (HTML, XML, etc.) の間で変換可能。
* 構文認識：プログラミング言語のブロックの開始や終了を認識すると、自動的に字下げ
  階層を変更するようなことをする。構文を認識するエディターは、一般的に色やフォン
  トを変えて強調する。
* 一括コマンド出力の解析。エディター内部からコンパイルを実行し、エラーメッセージ
  を捕まえて、エディターを離れることなくエラー箇所を調べられるようにする。
* エディターコマンド間の状態を持続的に維持する補助子プロセスとの相互作用。この機
  能が存在する場合、強力な結果をもたらす：
    * エディターから VCS を動かすことができ、シェルウィンドウや別の道具に抜け出
      さずに、バージョン管理コマンドを実行できる。
    * エディターでデバッガーを前処理することが可能。例えばブレイクポイントで実行
      が停止すると、該当するファイルの行へ自動的に飛ぶ。
    * ファイル名が他のホストを参照していることを認識させることで、エディターで遠
      隔ファイルを編集することが可能。 適切なアクセス権があれば、そのようなエ
      ディターは scp(1) や ftp(1) を自動的に実行する。

どの事例のエディターにおいてもプレーンテキストを編集できる。より複雑な仕事をどの
ように処理するかについて、さまざまな度合いの選択的複雑さが見え始めている。

### ed

* プレーンテキスト編集の真に Unix 最小主義的な方法
* 単純かつ質素な CLI
* 画面表示はない

Unix オリジナルコードのほとんどはこのエディターで書かれた。DOS にあった Edlin は
`ed` を露骨に手本にしたものだと言う。

エディターの定義が、単にプレーンテキストファイルを作成し、修正できるようにするも
のだというならば、ed(1) はその仕事に完全に十分だ。

> Importantly to the Unix view of design correctness, it does nothing else.

Ken Thompson が以前の [QED] というエディターを意図的に簡略化したものが `ed` だと
いう見方が適切だ：

* 正規表現を用いる最初のエディターだった。これは `ed` に引き継がせた。
* マルチバッファー機能を有していた。これは捨てられた。

[QED]: <https://en.wikipedia.org/wiki/QED_(text_editor)>

ed(1) とその末裔すべての特筆すべき特徴は、コマンドのオブジェクト操作形式だ。

```raw
a
.
1s/f[a-z]x/dragon/
1,$p
w
q
```

行の範囲を指定するための比較的強力な構文があり、数値で指定したり、正規表現のパ
ターンマッチで指定したり、現在行と最終行の特別な短縮形で指定したりすることができ
る。エディター操作の大半はどの範囲にも適用可能だ。直交性の良い例だ。

ex(1) と呼ばれる、コマンドプロンプトのようないくつかの便利な対話機能を追加したも
のがある。ある種の異常なクラッシュの回復状況において、時折役に立つ。

すべての Unix に `ed` の実装が含まれており、ほとんどの Unix は `ex` も含む。

!!! note
    私の環境では `ex` は `vim` だ。

sed(1) ([Chapter 9]) も `ed` と密接に関連している。基本的なコマンドの多くは同じ
だが、標準入力からではなく、コマンドラインスイッチを通して呼び出されるように設計
されている。

### vi

オリジナルの vi(1) は ed(1) のコマンド集合に Rogue 風インターフェイスを取り付け
た最初の試みだった。`ed` と同様、`vi` のコマンドは一般的に単一キーストロークであ
り、熟練タイピストによる使用に特に適している。

オリジナルの `vi` には（これも `ed` 同様に？）使用者カスタマイズのいかなる形態も
なかった。そのことを `vi` 使用者は美徳と考えた。

> On this view, one of vi's most important virtues is that you can start editing
> immediately on a new Unix system without having to carry along your
> customizations or worrying that the default command bindings will be
> dangerously different from what you're used to.

これを読んで思ったが、Twitter のかつての某フォロワーサンがまさにノーカスタマイズ
主義者だった。

インターフェースは、コマンドモードかテキスト挿入モードのどちらかになっている。

* テキスト挿入モードでは、機能するコマンドはモード終了の <kbd>Esc</kbd> とキャ
  レット移動キーしかない。
* コマンドモードでは、入力テキストはコマンドとして解釈され、バッファー内容に奇妙
  な（破壊的な）ことを行う。

オブジェクト操作形式は `ed` から受け継いだ。拡張コマンドのほとんどはどの行範囲で
も自然な形で操作できる。

Emacs とは対照的に、内蔵汎用スクリプトの使用は普及しなかった。 その代わりに、`vi`
の実装はそれ自体に C のコードを追加することによって、C コードの構文認識やコンパイ
ラーのエラーメッセージの出力解析のようなことを行う個々の機能を成長させてきた。

子プロセスとの対話は支援されていない。

### Sam

[Sam]: <https://en.wikipedia.org/wiki/Sam_(text_editor)>

* [Sam] は 1980 年代半ばに Bell 研究所の Rob Pike が書いた。
* Plan 9 OS 用に設計された。
* `vi` よりも `ed` にずっと近い。

Sam が新たに取り入れた概念：

* curses(3) スタイルのテキスト表示
* マウスによるテキスト選択

> Each Sam session has exactly one command window, and one or more text windows.
> Text windows edit text, and command windows accept ed-style editing commands.
> The mouse is used to move between windows, and to select text regions within
> text windows.

著者はこれを、`vi` のインターフェイスの複雑さをほとんど捨てた、直交的でモードレ
スで清浄な設計だと評する。

* マウスを選択とバッファー間のフォーカスの迅速な変更に利用できることから、`vi`
  におけるコマンドモードと同等のものを必要としない。
* 何百もの拡張 `vi` コマンドは不要であり、したがって省略される。

Sam の興味深い特徴は二つの部分に分かれているということだ：

* ファイルを操作したり検索を行ったりするバックエンド
* 画面のインターフェイスを扱うフロントエンド

これは Separated Engine and Interface パターンの実例になっている。プログラムが
GUI を持っているにもかかわらず、遠隔サーバー上のファイルを編集するために低帯域幅
接続で簡単に実行できるという実用的な利点がある。また、フロントエンドとバックエン
ドを比較的簡単に変えられる。

設計上、リッチテキスト編集も、出力解析も、子プロセスとの対話も支援していない。

### Emacs

> Emacs is undoubtedly the most powerful programmer's editor in existence. It's
> a big, feature-laden program with a great deal of flexibility and
> customizability.

1. 最初の Emacs は Richard M. Stallman が設計した。
2. Lisp を内蔵した最初のバージョンは Bernie Greenberg のものだ。
3. 現在のバージョンは Greenberg のものから派生した Stallman のものだ。

Emacs にはプログラミング言語全体 ([Chapter 14]) が組み込まれており、それを使って
強力なエディター関数を書くことが可能だ。

!!! note
    この辺の Emacs の機能説明ノートは省略。よく知っている。

> The designers of Emacs built a programmable editor that could have
> task-related intelligence customized into it for hundreds of different
> specialized editing jobs. They then gave it the ability to drive other tools.
> As a result, Emacs supports dealing with all things textual in one shared
> context — files, mail, news, debugger symbols. It can serve as a customizable
> front end to any command with an interactive textual interface.

Emacs 最大のウリは個人的にはこのプログラム可能性だと思う。

Emacs は非 Unix 系 OS の統合開発環境 (IDE) が占める役割を果たしている ([Chapter
15])。

この能力は複雑さという代償を伴う。

> To use a customized Emacs you have to carry around the Lisp files that define
> your personal Emacs preferences.

現代ならこの点は解消された。

> Learning how to customize Emacs is an entire art in itself.

### Wily

[Wily]: <https://en.wikipedia.org/wiki/Wily_(text_editor)>
[Acme]: <https://en.wikipedia.org/wiki/Acme_(text_editor)>

[Wily] は Plan 9 エディター [Acme] のクローンだ。[Sam] と機能をいくつか共有して
いるが、根本的に異なる使用者体験を与えることを意図していた。

* エディターの必須条件である大域的検索と置換でさえ外部プログラムによって実現して
  いる。
* 内蔵コマンドはほとんどウィンドウ操作にしか関係しない。
* 可能な限りマウスを使うように設計されている。

  > The left mouse button is used to select text, the middle button to execute
  > text as a command (either built-in or external), and the right button to
  > search either Wily's buffers or the file system for text.

* メインウィンドウ内のテキストはすべて、動作や検索式になり得る。
* メニューは必要ない。
* ショートカットは複数のマウスボタンを同時に押し続けることで実現する。これらの
  ショートカットは常に、何らかの内蔵コマンドで中ボタンを使うのと同じだ。
* C, Python, Perl プログラムのフロントエンドとして利用可能。ウィンドウが変更され
  たり、マウスで execute や search コマンドが実行されたりするたびに、それらに報
  告する。これらのプラグインは Emacs モードと同様の機能だが、Wily と同じアドレス
  空間では動作しない。
* Wily には `xterm` 類縁物と、それを編集フロントエンドとして使うメールツールが同
  梱されている。
* マウスに大きく依存しているため、character-cell-only 画面でも遠隔リンクなしでも
  使用不可能。
* プレーンテキストを編集する設計になっている。フォントは可変幅と固定幅の二つしか
  なく、リッチテキスト編集や構文認識を支援する仕組みはない。

## The Right Size for an Editor

本章の冒頭で作成した複雑性区分によって事例研究を検証していく。

### Identifying the Complexity Problems

どのテキストエディターにも、ある程度の必然的複雑性がある。四事例の中では、選択的
複雑性も偶発的複雑性も、これ以上に大きく異なることを示している。

四事例の中では ed(1) は最も複雑さが少ない。UI はきわめてコンパクトだ。

* コマンドの多くが p や l という接尾辞を付ければ、結果を表示したり一覧したりする
  という非直交的な特徴があるが、これがほとんど唯一。
* コマンド数が 30 未満であり、削除可能であるような選択的複雑性はあまりなく、偶発
  的複雑性を特定するのが難しい。

反面、`ed` のインターフェイスはテキストファイルを素早くめくるような基本的な編集
作業にはあまり適していない。

では「複数ファイルの視覚的な閲覧と編集を支援する」という目的を `ed` に追加したと
する。そうすると、Sam はこれを実現できる最小限の拡張機能ということになる。Sam 設
計者は次の点で素晴らしい判断をした：

> The fact that the designers did not change the semantics of the inherited ed
> commands is notable; they kept an existing, orthogonal set and added a
> relatively small set of capabilities that are themselves orthogonal.

Sam を検討する。選択的複雑度を大きくしている機能は二つ：

* 無限 undo 機能
* コマンド言語での正規表現に基づく反復機能

設計水準では Sam の偶発的複雑度を特定するのは難しい。インターフェイスは少なくと
もセミコンパクトで、ほぼ間違いなく厳密にコンパクトだ。出自を考えれば驚くものでは
ないことだが、Unix 設計の最高水準に達している。

次に `vi` を検討する。

* 何百ものコマンドがあり、重複が多くある。高々選択的複雑性であり、たぶん偶発的。
* 製作当時、キャレット移動をキーで行う必要があったので、モーダルインターフェイス
  は避けられなかった。
* コマンドの乱雑さの問題は比較的表面的だ。ほとんど無視することが可能。

問題としては即興的罠がもっとも深い：

> Over the years, `vi` has had progressively more and more special-purpose C
> code bolted onto it to perform tasks that Sam refuses to do and that Emacs
> would attack with Lisp code modules and subprocess control.

不要なときでも `vi` の全機能がメモリーに乗る。そこには選択的複雑性も偶発的複雑性
も含まれる。

Emacs と `vi` のコードベース規模の比率が `vi` にとって有利になる見込みはなさそう
だ：

> While `vi` fans like to talk about filtering buffers with external programs
> and scripts to do what Emacs's embedded scripting does, the reality is that
> `vi`'s `!` command cannot filter regions of an edit buffer selected at finer
> granularity than a range of lines (Sam and Wily, though they have no more
> subprocess management than `vi` does, can at least filter arbitrary text
> ranges, not just line ranges). All knowledge of file formats and syntaxes that
> vary at a finer granularity (and most do) has to be built in to C code if `vi`
> is going to have it available at all.

Emacs は十分に大きく、もつれた歴史があるので、選択的と偶発的複雑性を切り分けるの
は難しい。設計に含まれる偶発的なものを必然的なものから切り分けることから始める。

Emacs 設計の中で、もっともどうでもいい部分は Emacs Lisp だろう。

* 現在では内蔵スクリプト言語が備わっていることは必須だが、それが Python, Java,
  Perl であったとしてもエディター機能はほとんど変わらない。
* ただし、設計当時は Lisp が Emacs に適した性質をもつ唯一の言語だった。
* そういえば他の書籍でも Lisp は軽視されることがない。

任意のイベントを任意の内蔵関数や使用者定義関数に束縛する機能は死活的だ。

同梱されている膨大な拡張モードのライブラリーは偶然的だ（拡張を構築する能力は必然
的だが）。

子プロセスとの相互作用は死活的だ。これがなければ Emacs のモードは期待された IDE
のような統合やさまざまなツールのフロントエンドたり得ない。

> Experience with small editors that clone the default keybindings and
> appearance of Emacs without emulating its extensibility is instructive.

二つ挙げている：

* [MicroEMACS]
* [Pico]

[MicroEMACS]: <https://en.wikipedia.org/wiki/MicroEMACS>
[Pico]: <https://en.wikipedia.org/wiki/Pico_(text_editor)>

Wily は Emacs と比較するのが面白い。Sam と同様、選択的複雑度は低く、Wily の UI
は一ページで簡潔でありながら効率的に説明可能だ。

* キーストロークや入力ジェスチャーに機能を束縛することが不可能（マウス限定）
* ごく基本的なテキスト挿入・削除を除く編集機能は、エディター外部にあるプログラム
  など（次のいずれか）で実装しなければならない：
    * 単品のスクリプト
    * Wily の入力イベントを傍受する特別な共生プロセス

Emacs が Lisp 拡張で実装するような選択的複雑性は、特別な共生物で分配される。この
仕組みには利点がある：

* 使用者が選ぶ言語で共生物を書くことができる。
* エディタープロセス外で動作するため、Wily 本体に悪影響を与えることがない。

二つ目の利点を裏返せば欠点となる。Wily 自身は Unix ツールによる子プロセスとの相
互作用を直接行えない。

構文を意識した編集やリッチテキストへの興味を放棄しており、Wily もその Plan 9 の
祖先である Acme もこれらのことはできない。

### Compromise Doesn't Work

Sam と `vi` の比較は、少なくともエディターに関しては、`ed` の最小主義と Emacs の
完全装備指向の間で妥協しようとする試みがあまり上手くいかないことを強く示唆してい
る。

* `vi` これを試みたが、結局どちらの徳も得るところか、即興的罠にはまった。
* Wily は即興的罠を回避したが、Emacs の能力には及ばないし、それに近づくために
  はそれぞれの対話型共生体に自作プロセスインターフェイスを要求しなければならない。

> Evidently something about editors tends to push them in the direction of
> increasing complexity.

すべてが Zawinski の法則とも呼ばれる「ソフトウェア拡張の法則」に従って進化する傾
向がある：

> Every program attempts to expand until it can read mail. Those programs which
> cannot so expand are replaced by ones which can.

Zawinski はより一般に、次を主張している：

> all really useful programs tend to turn into Swiss Army knives.

Unix 界以外での、大規模で統合されたアプリケーションスイートの商業的成功はスイス
アーミーナイフ説を裏付ける傾向があり、Unix の最小主義哲学に対して異議を直接的に
唱えている。

Zawinski の法則が正しい限りにおいて、あるものは小さくあることを望み、あるも
のは大きくあることを望むが、その中間は不安定であることを示唆している。

Emacs と Wily の例から、モノが大きくなりたがる理由がさらにわかる。編集とバージョ
ン管理（メール、デバッグなど、編集以外の何か）は、実装者の視点からは別々の仕事
だ。しかし、使用者は、同じファイル名やバッファーの内容を渡さなければならないプロ
グラムの間を往復することに時間と注意を費やすよりも、テキストの断片を指し示すこと
ができる単一の大きな環境で仕事をしたいことがよくある。

もっと一般的に、Unix 環境全体を共同体による設計の一つの作品と見なすとしよう。そ
うすると、「小さくて鋭い道具」という信仰、インターフェイスの複雑さとコードベース
規模を抑えようという圧力は、まさに手作業の罠に導かれることがある。

> the user has to maintain all the shared context himself, because the tools
> won't do it for him.

話をエディターに戻すと：

* Sam は `vi` が間違ったものであることを示している。
* Wily は Emacs の広大さを回避するために頑張ったが、構文を認識することができない
  ために失敗に終わった。
* Wily は、つまり Emacs の設計思想を因習を捨て去って整理したものは、正しいものな
  のかもしれない。

選択的複雑性の価値は誰かが選択する目的によって異なり、ある仕事に関連するテキスト
指向ツールすべての間で、その仕事の状況、場面、背景を共にする能力は価値がある。

### Is Emacs an Argument against the Unix Tradition?

昔気質の Unix プログラマーの間で `vi` や Emacs が受けなかった理由は、それらが醜
いからだ。(Doug McIlroy)

著者は `vi` 使用者による Emacs の攻撃と、まだ `ed` に執着している筋金入りの守旧
派による `vi` への攻撃があると言っている。
<!-- exuberance:  the quality of feeling energetic, or the behaviour of someone who feels this way -->

Unix プログラマーは過剰よりも気品を賞揚する伝統を維持してきた。

Emacs の広大さを発明したのは、Artificial Intelligence Lab の Richard M. Stallman
だった。計算機科学の研究機関の中でも最も裕福な研究所だ。彼は Unix プログラマーの
ような最小主義にこだわらず、自分のコードに最大限の能力と余地を求めた。

> The central tension in the Unix tradition has always been between doing more
> with less and doing more with more.

Emacs に対する賛否両論はこの緊張の例証だという。

Unix プログラマーが最小主義の原則に固執するあまり、現実を無視する過ちに対処する
方法は二つある：

* 大きいものは実際に大きいということを否定する
* 独断的でない複雑性についての考え方を発展する

先ほどは Emacs が Lisp と拡張を置き換えたら、という思考実験をした。Emacs が肥大
している原因は拡張ライブラリーが巨大だからだという非難からそういう仮説を立てたわ
けだが、これはシステムにあるシェルスクリプトの集合が巨大だから `/bin/sh` が肥大
しているというようなものだ。

> Emacs could be considered a virtual machine or framework around a collection
> of small, sharp tools (the modes) that happen to be written in Lisp.

Emacs の中に汎用言語があると肥大化したように感じるからという理由で Emacs に反対
するのは、シェルに条件分岐や `for` ループがあるからという理由でシェルスクリプト
を使うのを拒否するのと同じくらい愚かだ。シェルスクリプトを使うためにシェルを学ぶ
必要がないように、Emacs を使うために Lisp を学ぶ必要もないのだ。

拒絶に陥る可能性を回避し、Emacs が有用であると同時に巨大であること、つまり Unix
最小主義に対する反論であることを認めよう。

## The Right Size of Software

Unix 式の小さくて尖った道具は、ツール間の通信を容易にする枠組の中に存在しない限
り、データの共有に苦労する。Emacs は枠組であり、«unified management of shared
context» は Emacs の選択的複雑性を買うものだ。

Emacs はファイルシステムをテキストバッファーと補助プロセスの世界と統合し、シェル
の枠組をほとんど置き去りにしている。 Wily もバッファーと補助が中心だが、シェル枠
組を取り込んでいる。最近のデスクトップ環境は GUI のための通信枠組を備え、これも
シェル枠組を置き去りにしている。

枠組は道具の生態系の住処になる：

* シェルはシェルスクリプト
* Emacs は Lisp モード
* デスクトップ環境は GUI の群れ

これは最小限の法則 (Rule of Minimality) を示唆している：

> Choose the shared context you want to manage, and build your programs as small
> as those boundaries will allow.

* これは本章冒頭の Einstein の名言に適う。
* The shared context の選択に注意を集中することになる。
* この法則は枠組だけでなく、アプリケーションやプログラムシステムにも適用される。

The shared context の大きさについてずさんになりがちだ。Zawinski の法則の背後にあ
る圧力は、便利であるからといって context を share したがるアプリケーションの風潮
がある。あまりに重く、多くの仮定を持ち運ぶことになり、複雑、肥大、巨大なプログラ
ムを書くことになりがちだ。

> The corrective to this tendency comes straight from the old-school Unix
> hymnbook. It is the Rule of Parsimony: *Write a big program only when it is
> clear by demonstration that nothing else will do.

その時とは、問題を分割しようとして失敗した時だ。

1. 小規模プログラムの解決策を探す。
2. 単一の小プログラムでは解決できない場合、既存の枠組の中で小プログラムを連携さ
   せ、それで攻める。
3. 両方の取り組みが失敗したら、その場合に限り、大規模プログラムなり新規枠組なり
   を自由に作る。

枠組を作るときは分離の法則 (the Rule of Separation) を適用する。

* 枠組は仕組みであり、方策は持たない。
* 枠組を使うモジュールには、多くの振る舞いを組み込む。

> Circumstances alter cases, and exercising good judgment and good taste is what
> software designers are for.

[Chapter 4]: <./modularity.md>
[Chapter 8]: <./minilanguages.md>
[Chapter 9]: <./generation.md>
[Chapter 14]: <../implementation/languages.md>
[Chapter 15]: <../implementation/tools.md>
