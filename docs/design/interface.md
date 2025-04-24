# Chapter 11. Interfaces

[TOC]

プログラムのインターフェイスはそのプログラムが人間や他のプログラムと通信する方法
すべての総体だ。UI のコードは通常、開発時間の 40% 以上を費やす。初動での失敗や時
間のかかる書き直しを避けるためには優れたデザインパターンを知ることが特に重要だ。

Unix の伝統的なインターフェイス設計における課題：

* 他のプログラムとの通信のための予測的 (anticipatory) 設計
* 驚き最小の法則

Unix のプログラムは相乗効果のある組み合わせで使用することでさらなる性能を得る。

プログラムインターフェイス設計に関する Unix の伝統の多くは、初めてそれに出会った
ときには奇妙で恣意的、あるいは GUI の時代には、まさに逆行しているとさえ思えるか
もしれない。しかし、さまざまな汚点や不規則性にもかかわらず、その伝統には学び理解
する価値のある内在論理がある。

起動後、プログラムは通常次の場所から入力やコマンドを受け取る：

* プログラムの標準入力に表示されるデータとコマンド
* X サーバーイベントやネットワークメッセージなど、プロセス間通信で渡される入力
* 既知の場所にあるファイル、機器、器具、装置

プログラムはすべて同じ方法で結果を出すことができる。出力は標準出力に向かう。

Unix には競合するインターフェイス様式がいくつかある。いずれもまだ存命であるのに
は理由があり、それぞれの状況に最適化されているからだ。仕事とインターフェイス様式
の適合性を理解しろ。

## Applying the Rule of Least Surprise

驚き最小の法則はソフトウェアに限らず、あらゆる種類のインターフェイスの設計におけ
る一般法則だ。

* 人間は一度に一つのことしか注意できないという事実からの帰結
* 驚きがあると、仕事ではなくインターフェイスに注目してしまう

したがって、使いやすいインターフェイスを設計するためには、可能な限り、まったく新
しいインターフェイスモデルを設計しないことが最善だ。目新しさは使用者にとって参入
障壁となる。

可能な限り、ユーザーがインターフェイス機能を使い慣れたプログラムに委譲できるよう
にすること：

> Wherever possible, allow the user to delegate interface functions to a
> familiar program.

使用者が大量のテキストを編集する必要があるプログラムでは、独自の統合エディターを
組み込むのではなく、使用者が指定できるエディターを呼び出すように書くべきだ
([Chapter 7])。

さらに：委譲できないときは、エミュレートせよ。

驚き最小の法則の目的は、インターフェイスを使うために使用者が吸収しなければならな
い複雑さ減らすことだ。エディターの例を続けると、内蔵エディターを実装しなければな
らない場合、エディターコマンドがよく知られた汎用エディターの部分集合であることが
最善であることを意味する。Bash にも Korn Shell にも、vi と Emacs の編集方式を選
択できる機能がある。

もう一つの例として、Unix 版の Web ブラウザーはテキスト欄が Emacs の既定キーバイ
ンディングの部分集合を認識することが挙げられている。なぜ Emacs かというと：

> The only way it could have been bettered was by choosing key bindings
> associated with some editor significantly more widely used than Emacs; and
> among Netscape's original user population there was no such animal.

これらの原則はインターフェイス設計の他の多くの分野にも適用できる。

> Or even that if you are designing an arcade-style game, it is wise to look at
> the gesture sets of previous games to see if you can give new users a feeling
> of comfort by allowing them to transfer joystick skills learned in other
> games.

この主張は格闘ゲームを想像するとわかりやすい（「波動拳コマンド」とか「ヨガフレイ
ム」とか言えばその筋の連中には話が完全に通じるという良さもある）。

## History of Interface Design on Unix

Unix の基本コマンドのほとんど (ls(1), cat(1), grep(1), etc.) は現在でも 1969 年の
最初の Unix から十年以上主流であった CLI の伝統を反映している。

1980 年以降、Unix は徐々に文字枡目端末での画面描画をやるようになる。プログラムは
コマンドラインとビジュアルインターフェイスを混在させるようになる。一般的なコマン
ドは画面に映らないキーストロークに束縛されるようになった。通常、キャレットを制御
するために使用される画面描画ライブラリーにちなんで curses プログラムと呼ばれた
り、それを使用した最初のアプリケーションにちなんで roguelike と呼ばれたりする。

1980 年代半ば、Xerox's Palo Alto Research Center で 1970 年代初頭から行われてい
た GUI の先駆的な研究の成果が計算機の世界全体に浸透し始めた。

* PC では PARC の研究が Apple Macintosh のインターフェイスに影響を与えた。
* それを通じて Microsoft Windows の設計に影響を与えた。

1987 年頃、X windowing system が Unix の標準的な GUI 機能となった。

X にはオープンソースであるという最大の長所があった。自由に再配布・変更可能なまま
であった。そのため、単一の販売会社の排他的な製品に肩入れしたがらない幅広い開発者
や後援企業から支持を集めることができた。

X の設計者たちは“mechanism, not policy”を支持することを早くから決めていた。彼ら
の目的は X を可能な限りプラットフォーム間で柔軟かつ移植しやすくする一方、X プロ
グラムのルック＆フィールにできる限り制約を与えないことだった。

> This approach was the polar opposite of that taken by the Macintosh and
> Windows commercial products, which enforced particular look-and-feel policies
> by designing them right into the system.

X はウィンドウマネジャーを複数支援するように設計されている。ウィンドウマネジャー
の意味は脚注にある：

> A window manager handles associations between windows on the screen and
> running tasks. Window managers handle behaviors like title bars, placement,
> minimizing, maximizing, moving, resizing, and shading windows.

1990 年代半ば以降、最低性能 Unix 機でさえ X はありふれている。

新しいアプリケーションのための curses 式のインターフェイスの使用も減少しており、
以前はその様式で設計されていた新しいアプリケーションのほとんどは、現在では Xツー
ルキットを使用している。Unix の古い CLI 設計の伝統は今でも活気があり、多くの分野
で X とうまく競争していることは有益だ。

また、curses 式の文字枡目画面インターフェイスが標準的なままである、いくつかの特
定の応用分野があることも有益だ：

* テキストエディター
* メーラー
* ニュースリーダー
* チャットクライアントなどの対話型通信プログラム

以上の歴史的な理由から、Unix プログラムにはさまざまなインターフェイス様式がある：

* 行指向
* 文字枡目画面指向
* X に基づくもの

## Evaluating Interface Designs

プロジェクトについて設計を決定するとき、アプリケーションと使用者層に適した方式を
選んだり組み合わせたりする方法を知ることが肝要だ。

ここではインターフェイス方式を分類するために次の五つの基本指標を用いる。これらの
術後のうちいくつかは本書の最初のほうですでに現れたものだ：

* 簡潔性 concision <!-- without using unnecessary words -->
* 表現力 expressiveness
* 使いやすさ ease <!-- absence of difficulty or effort -->
* 透明性 transparency
* スクリプト可能性 scriptability

簡潔性の定義：

> A program interface is ‘concise’ when the length and complexity of actions
> required to do a transaction with it has a low upper bound (the measurement
> might be in keystrokes, gestures, or seconds of attention required).

表現力の定義：

> Interfaces are ‘expressive’ when they can readily be used to command a wide
> variety of actions.

最も表現力豊かなインターフェイスは、設計者が予期していなかった動作の組み合わせを
命令することができ、それにもかかわらず、使用者に有用かつ整合する結果を与えること
ができる。

* キーボードからの直接入力と、マウスで画面上の文字表示からクリックする方法は表現
  力は同等だ。キーボードの方がより簡潔だ。
* 複素数型があるプログラミング言語とない言語では、数学者や電気技師にとっては前者
  のほうが表現力がはるかに高い。

インターフェイスの使いやすさは、それを使うために使用者が特別に習得しなければなら
ないことがどれだけ多いかに反比例する。

透明性は [Chapter 6] で習った。

インターフェイスの透明性とは、使用している間、使用者が自分の問題、データ、プログ
ラムの状態について記憶しておく必要があることがどれだけ少ないかということだ。

いわゆる WYSIWYG インターフェイスは、透明性を最大化することを意図しているが、時
に逆効果になる。特に、関心領域を単純化し過ぎた見方を提示すると。

発見可能性という関連概念は、インターフェイス設計にも当てはまる。 発見可能性イン
ターフェイスは、文脈依存のヘルプを指し示す挨拶メッセージや、説明的な風船のポップ
アップなど、利用者が学習する際の支援がある。しかし、この議論では指標として使わな
いことにする。

コードと設計の透明性が、インターフェイスの透明性を含意するわけではないこと、ある
いはその逆でもないことに注意が要る。

インターフェイスのスクリプト可能性とは、他のプログラムから簡単に操作できることで
だ。スクリプト可能なプログラムは、他のプログラムから部品として容易に利用できるた
め、経費のかかる自力でのコーディングの必要性が減り、反復課題の自動化が比較的容易
になる。

反復課題の自動化は通常よりももっと注目されるべきものだ。

> Unix programmers, administrators, and users develop a habit of thinking
> through the routine procedures they use, then packaging them so they no longer
> have to manually execute or even think about them any more. This habit depends
> on scriptable interfaces. It is a quiet but tremendous productivity booster
> not available in most other software environments.

これらの指標に関して、人間とプログラムは異なる損失関数を持っている。特定の問題領
域における、初心者と熟練した人間の使用者も同様だ。

## Tradeoffs between CLI and Visual Interfaces

初期の Unix のテレタイプ CLI スタイルの有用性：

* 特に複雑な作業において、視覚的なインターフェイスよりも表現力が高い。
* スクリプト性が高い。

通常、CLI は簡潔さにおいても有利だ。

CLI の欠点は、ほとんどの場合、

* 使いやすくない。
* 透明性が低い。特に、技術者でない使用者は CLI は比較的不可解で学ぶのが難しいと
  感じる。

データベースの非技術的使用者の多くは、SQL 構文を覚えなければならないことに抵抗が
あり、簡潔で表現力に乏しい GUI を好む。

最も強力な CLI は、限定目的のコマンドの集まりではなく、命令型の小規模言語
([Chapter 8]) だ。これらは使いにくく、一般的な使用者からは目立たないようにする必
要がある。インターフェイスの能力と柔軟性が最も重要なことである場合には無敵だ。適
切に設計されていれば、スクリプト可能性でも高い評価を得ることができる。

アプリケーションの中には、データベース照会とは異なり、もともと視覚的なものもあ
る。ペイントプログラム、Web ブラウザー、スライドプログラムの三つがその例だ。 こ
れらの応用領域に共通しているのは：

* 透明性が貴重であること
* 問題領域における素朴な動作自体が視覚的であること

ペイントプログラムは、操作する画像内の関係を把握するのが難しいという欠点がある。
例えば、繰り返し要素のある画像の構造を使用者に把握させるには、注意深く、思慮深い
設計が必要だ。これは視覚的インターフェイスの一般的な設計問題だ。

Audacity エディター ([Chapter 6]) のインターフェイス設計が成功したのは、音声応用
領域を（ステレオのイコライザー表示から借用した）単純な視覚的表現の集合に写像する
ことが特にきれいにできたからだ。

もともと視覚的でないアプリケーションでは、視覚的インターフェイスは初心者が行う単
純な一発課題や頻度の低い課題に最も適している（データベースの例で示した）。

CLI に対する抵抗は使用者が熟練するにつれて減少する傾向がある。

> In many problem domains, users (especially *frequent* users) reach a crossover
> point at which the concision and expressiveness of CLI becomes more valuable
> than avoiding its mnemonic load.

例えば、計算機初心者は GUI デスクトップの使いやすさを好むが、経験豊富な使用者は
シェルにコマンドを入力する方が好きであることを徐々に発見することが多い。

CLI はまた、問題の規模が大きくなり、定型的、手続き的、反復的な行動が多くなるにつ
れて有用性を増す傾向がある。例えば、WYSIWYG ワープロは手紙のような比較的小さく、
構造化されていない文書を執筆するための最も簡単な道だ。しかし、分節化されていて、
構成中に多くの大域的な書式変更や構造操作を必要とする、複雑な書籍規模の文書では、
通常、troff, Tex, XML 処理器のような小規模言語整形器がより効果的な選択となる。

もともと視覚的な領域であっても、問題の規模を拡大するとトレードオフは CLI に傾
く。指定された URL から Web ページを一つ取得して保存する必要があるなら、ポイント
アンドクリックでも構わない。しかし、与えられた 50 の URL の一覧に対応するページ
を取得して保存する必要がある場合、標準入力やコマンドラインから URL を読み取るこ
とができる CLI ツールを使えば無駄な動きを省くことができる。

別の例として、画像の色表を変更することを考える。ある色を変更したい場合、カラー
ピッカーによる視覚的なダイアログボックスはほとんど必須だ。しかし、表全体を指定さ
れた RGB 値の集合で置き換えたり、大量のサムネイルを作成してインデックスを作成し
たりする必要があるとする。これらは通常、GUI が指定する表現力に欠ける操作だ。適切
に設計された CLI やフィルタープログラムを呼び出すことで、はるかに簡潔に作業を行
うことができる。

GUI は単純にスクリプト化できない。GUI とのやりとりはすべて人間主導でなければなら
ない。

直接操作インターフェイスの暗黒面は、すべてを操作しなければならないことだ。
-- Don Gentner and Jacob Nielsen. *The Anti-Mac Interface*

この問題に対する典型的な Unix 古参者の見解は、むしろ理論的でない：

商業的な世界では、一般的に初心者モードが主流だ。なぜなら、

* 30 秒の試用で購入が決定されることが多いから
* GUI を使いこなせれば顧客援助の負担が最小限に抑えられるから

(Mike Lesk) 非 Unixシステムの多くは、例えば、百個や千個のファイルに対して何かを
する方法を提供してくれないので、非常にイライラさせられる。

素人にも専門家にも対応し、他のプログラムと協調し、問題領域が自然に視覚的であるか
どうかにかかわらず、CLI と GUI の両方を支持することが重要だ。

### Case Study: Two Ways to Write a Calculator Program

## Transparency, Expressiveness, and Configurability

## Unix Interface Design Patterns

### The Filter Pattern

### The Cantrip Pattern

### The Source Pattern

### The Sink Pattern

### The Compiler Pattern

### The ed pattern

### The Roguelike Pattern

### The ‘Separated Engine and Interface’ Pattern

### The CLI Server Pattern

### Language-Based Interface Patterns

## Applying Unix Interface-Design Patterns

### The Polyvalent-Program Pattern

## The Web Browser as a Universal Front End

## Silence Is Golden

[Chapter 6]: <./transparency.md>
[Chapter 7]: <./multiprogram.md>
[Chapter 8]: <./minilanguages.md>
