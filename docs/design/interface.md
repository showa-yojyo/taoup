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

GUI と CLI が単純な対話型プログラムである卓上計算機の設計にどのように有用に適用
できるかを対比する。例は dc(1)/bc(1) vs xcalc(1) だ。

dc(1)/bc(1) については [Chapter 7] と [Chapter 8] で触れられた。これらのプログラ
ムはどちらも CLI だ。標準入力に式を入力し Enter を押すと式の値が標準出力に示され
る。

一方、xcalc(1) はクリック可能なボタンと電卓風の機器であり、単純な電卓を視覚的に
真似ている。

<!-- Figure 11.1. The xcalc GUI. -->

xcalc(1) の手法は初心者が慣れ親しんでいるインターフェイスを模倣しているため説明
するのが簡単だ。このプログラムの機能はすべて目に見えるボタンのラベルによって伝わ
る。これは驚き最小の法則の最も強い形であり、プログラムを使用するためにマニュアル
ページを読む必要のない、使用頻度の少ない初心者にとって真の利点だ。

しかし、電卓のほぼ完全な非透明性 (non-transparency) も継承している。複雑な式を評
価するとき、自分のキーストロークを見て正気確認をすることができない。例えば、

```raw
(2.51 + 4.6) * 0.3
```

のような式で小数点を間違えてしまうと問題になる。

一方、dc(1)/bc(1) では、式を作りながら間違いを編集することができる。インターフェ
イスは透明性がより高い。インタープリターは電卓の適度な大きさの見てくれに収まるも
のに限定されないので、より多くの機能（および条件文、変数、反復などの機能）を含む
ことができ、より表現力が豊かだ。もちろん mnemonic load も負うことになる。

* タイピングが得意な人なら CLI の方が簡潔だと感じるだろうし、苦手な人ならマウス
  クリックの方が早いと感じるかもしれない。
* `dc`/`bc` はフィルターとして使えるが、`xcalc` はまったくスクリプト化できない。

初心者にとっての使いやすさと熟練者にとっての実用性のトレードオフ：

* 暗算によるエラーチェックが難しくない状況でカジュアルに使うなら `xcalc` が優る
* より複雑な計算で、段階が正しいだけでなく、正しいことが見て取れなければなら
  ない場合や、他のプログラムで生成するのが最も便利な場合は `dc`/`bc` が優る

## Transparency, Expressiveness, and Configurability

> Unix programmers inherit a strong bias toward making interfaces expressive and
> configurable.

対象使用者に関する不確実性に対処するやり方が他の伝統的プログラマーと異なる。

Unix プログラマーはインターフェイスを表現的で透明なものにするのが通例であり、こ
れらの性質を得るために、使いやすさを犠牲にすることを厭わない (willing to
sacrifice ease)。

Unix プログラマーは «by programmers, for programmers» の精神だ。この姿勢の弊害は：

* (Henry Spencer) 高度に構成可能で表現力豊かなインターフェイスが完成した時点で、
  仕事は終わったと思い込む傾向があること
* (Henry Spencer) 構成可能性の裏返しとして、優れた既定値およびすべてをそれに設定
  する簡単な方法がさし迫った必要だ。
* (Henry Spencer) 表現力の裏返しとして、プログラムであれ、文書であれ、どこから始
  めて、どのようにして最も望まれる結果を達成するのかという導きが必要だ。

透明性の法則も影響する。Unix プログラマーが、制御オプションの集合を定義した RFC
やその他の標準に適合するように書いているとき、彼は自分の仕事はそれらのオプション
全てに完全で透過的なインターフェイスを与えることだと思いがちだ。

> His job is mechanism; policy belongs to the user.

Macintosh や Windows の開発者が「標準のその機能を支援する必要はない。使用者のほ
とんどは気にしないだろうし、彼らにとっては複雑であり過ぎる」と言うような場合、
Unix の開発者はこう言うだろう。「誰もこの機能やオプションを欲しがらないとは限ら
ない。したがって、我々はそれを支援しなければならない」。

このような態度は Unix プログラマーが他の人と仕事をするときに衝突を引き起こす可能
性がある。

Unix の態度がどこまで適切かはさまざまである。相手の意見に耳を傾けることを学び、
反対意見の背景にある前提を理解することが賢明だ。[Chapter 6] の Audacity と KMail
の研究事例はそれに倣うべき良い例だ。

人が UI を直感的であるというのは、次を満たすそれをいう：

* 発見可能である
* 使用中は透明である
* 驚き最小の法則に従う

> Of these three rules, Least Surprise is the least binding; initial surprises
> can be coped with if discoverability and transparency make longer-term use
> rewarding.
<!-- be coped with: to deal successfully with a difficult situation -->

人々は、単純な操作が簡単で、インターフェイスのより難しい角を一歩ずつ吸収できるよ
うな発見経路がある限り、mnemonic load のかなり高い透明なインターフェイスについ
て、直感と思われるものを発達させることができる。

## Unix Interface Design Patterns

> There are no design patterns in graphical user interfaces themselves that are
> specifically native to Unix.

プログラムには複数のインターフェイスパターンに適合するモードがあることに注意。例
えば、コンパイラーのようなインタフェイスを持つプログラムは、コマンドラインでファ
イル引数が指定されていない場合、フィルターとして動作することがある。型変換プログ
ラムの多くはこのように動作する。

### The Filter Pattern

Unix に最も典型的に関連したインターフェイス設計パターンは、フィルターだ。フィル
タープログラムは標準入力のデータを受け取り、何らかの変換をし、その結果を標準出力
に送る。

フィルタの典型的な例は tr(1), grep(1), sort(1) だ。

grep(1) と sort(1) はコマンドラインで指定されたファイルからデータを入力すること
もできる。この場合、標準入力を読み込まず、あたかもその入力が、名前付きファイルを
順番に読み込んだ連結物であるかのように振る舞う。このような `cat` 風フィルターの
原型は cat(1) であり、コマンドラインで指定されたファイルを異なるように扱うアプリ
ケーション固有の理由がない限り、フィルターはこのように振る舞うことが期待される。

フィルターを設計する際には次を覚えておくとよい ([Chapter 1]):

1. Postel の処方箋を忘れるな。*Be generous in what you accept, rigorous in what you emit.*
2. 必要のない情報は決して捨てるな。
3. 雑音を決して加えるな。必要でない情報を加えないようにし、下流のプログラムに
   とって解析が難しくなるような再整形は避けろ。

> The term “filter” for this pattern is long-established Unix jargon.

「フィルター」はパイプの初日に使われるようになった。データの流れを表す配管の比喩
がすでに確立されていたため、「回路」が考慮されることはなかった。(Doug McIlroy)

### The Cantrip Pattern

単語 cantrip の意味については後述。

> No input, no output, just an invocation and a numeric exit status. A cantrip's
> behavior is controlled only by startup conditions.

初期条件や制御情報のごく単純な設定以外に、プログラムが使用者との実行時の対話を必
要としない場合にこのパターンを適用する。

例：

* clear(1)
* rm(1)
* touch(1)
* startx(1): X を起動するプログラム。

このデザインパターンはかなり一般的なものではあるが、従来は名前がつけられていな
かった。著者がこのように命名した。

> the term “cantrip” is my invention. (In origin, it's a Scots-dialect word for
> a magic spell, which has been picked up by a popular fantasy-role-playing game
> to tag a spell that can be cast instantly, with minimal or no preparation.)

この人気 RPG とは Dungeons & Dragons を指す。コマンドをゲームの呪文であるかのよ
うに見立てるのは当たり前のことだ。

### The Source Pattern

> A *source* is a filter-like program that requires no input; its output is
> controlled only by startup conditions.

典型的な例：

* ls(1)
* who(1)
* ps(1)

Unix では上記のような報告プログラムはソースパターンに強く従う傾向があるので、そ
れらの出力は標準的なツールで絞り込むことができる。

### The Sink Pattern

> A *sink* is a filter-like program that consumes standard input but emits
> nothing to standard output. Again, its actions on the input data are
> controlled only by startup conditions.

このインターフェイスパターンは珍しく、よく知られた例はほとんどない。

* lpr(1): 標準入力で指定されたテキストやファイルを印刷キューに押し込む。
* mail(1) のメール送信モード。

シンクパターンのように見えるプログラムの多くは、標準入力からデータだけでなく制御
情報も受け取っており、実際には `ed` パターン（後述）のようなものだ。

スポンジという用語が、sort(1) のような、入力を処理する前に入力全体を読まなければ
ならないシンクプログラムに特に適用されることがある。

### The Compiler Pattern

コンパイラー風プログラムは標準出力も標準入力も使わない。その代わり、コンパイコマ
ンドラインからファイル名や材料名を受け取り、それらの名前を何らかの方法で変換し、
変換された名前で出力する。コンパイラー風は起動後に使用者による操作を必要としな
い。

このパターンはその枠組が cc(1)/gcc(1) であることからそう呼ばれる。画像ファイルの
変換や圧縮解凍を行うプログラムにも広く使われている。例：

* gif2png(1)
* gzip(1)
* gunzip(1)

おそらく ImageMagick の conjure(1) や ffmpeg(1) も該当するだろう。

一般に、コンパイラーパターンは、プログラムが複数の名前付き素材に関して動作する必
要があることが多く、かつ対話性を低くするように書ける（制御情報を起動時に与える）
場合に適したモデルだ。

コンパイラー風プログラムは容易にスクリプトにできる。

### The `ed` pattern

起動時以降も使用者との継続的な対話によって駆動される必要があるプログラムは多い。

* ed(1)
* ftp(1)
* sh(1)

> An actual sample ed(1) session will be included in [Chapter 13].

Unix のブラウザーやエディターに似たプログラムの多くは、編集対象の名前付き物資が
テキストファイル以外のものであってもこのパターンに従う。例：gdb(1).

このパターンのプログラムは容易にスクリプト化できない。このようなプログラムを動か
すには、通信規約と、呼び出しプロセスに対応する状態機械が必要になる。
[Chapter 7] の主プロセス制御の議論で指摘された問題が起こる。

それでも、対話的プログラムを完全に支援する最も単純なスクリプト可能なパターンだ。
ゆえに、後述の「分離エンジンとインターフェース」パターンの構成要素として、今でも
かなり有用だ。

### The Roguelike Pattern

> Roguelike programs are designed to be run on a system console, an X terminal
> emulator, or a video display terminal. They use the full screen and support a
> visual interface style, but with character-cell display rather than graphics
> and a mouse.

この節を読むときだけ頭をゲームモードに切り替えるのはありだ。

<!--
Figure 11.2. Screen shot of the original Rogue game.

                                                a) some food
                                                b) +1 ring mail [4] being worn
-----------------------              ########## c) a +1,+2 mace in hand 
|                     +###############          d) a +1,+0 short bow
|                     |                         e) 28 +0,+0 arrows
---------------+-------                         f) a short bow
               #                                i) a magnesium wand
               #                                g) a magnesium wand
             ###               ---------------- j) a potion of detect things
     --------+----------       |                l) a scroll of teleportation
     |                 |      #+                --press space to continue--
     |                 |      #|                 |             #
     |                 +#######|                 |            ##
     |                 |       |                 +##############
     --------+----------       -------------------             #
        ######                                                 #
  ------+----------                                            ######
  |...........@..!|                                                 #
  |...........%...|                 ----------------                #
  |...............|                #+              |          #######
  |...............+#################|              |          #
  |...............|                 |              +###########
  -----------------                 ----------------
Level: 3  Gold: 73     Hp: 36(36)   Str: 14(16) Arm: 4  Exp: 4/78
-->

コマンド：

* 通常は画面にエコーバックがない単一キーストロークだ。
* より手の込んだコマンドを入力するコマンドウィンドウを開くものもある。
* コマンド体系では矢印キーを多用する。

このパターンで書かれたプログラムは vi(1) か emacs(1) のどちらかをモデルにし、ヘ
ルプの取得やプログラムの終了といった一般的な操作にそれらのコマンドシーケンスを使
う傾向がある。これは驚き最小の法則による。

このパターンに関連する他のインターフェイス表現には、以下のようなものがある：

* 一行に一項目のメニューが使われる。選択中の項目が太字などの強調表示で描かれる。
* モード行。強調表示された画面行に表示されるプログラム状態の要約。画面下部または
  上部にあることが多い。

キーボードの h, j, k, l キーに関する約束事：

> a traditional but now archaic part of the roguelike pattern is the use of the
> h, j, k, and l as cursor keys whenever they are not being interpreted as
> self-inserting characters in an edit window; invariably k is up, j is down, h
> is left, and l is right.

そういえば Google 日本語入力では `zh`, `zj`, `zk`, `zl` をそれぞれ←↓↑→に変換でき
る。

このパターンに従ったプログラムは無数にある：

* vi(1)
* emacs(1)
* elm(1)
* pine(1)
* mutt(1), その他の Unixメールリーダーの大半
* tin(1)
* slrn(1), その他の Usenet ニュースリーダーの大半
* lynx(1)
* その他多数

ローグライクパターンはスクリプトを書くのが難しい。書こうとすることさえめったにな
い。また、Figure 11.2 を見ればわかるように、出力をプログラムで解釈するのもかなり
難しい。

このパターンには、マウスで操作する完全 GUI のような視覚的な滑らかさもない。ロー
グライクプログラムは依然として使用者にコマンドを習得させる必要がある。ローグライ
クパターンに基づいて作られたインターフェイスは «only hard-core hackers can love»
だ。このパターンは、スクリプト可能性もなく、初心者向け設計における最近の流行にも
適合していないという、両方の悪い面を持っているように思われる。

ローグライクプログラムは依然として人気がある。さらに、ローグライクパターンは広く
浸透しているため、Unix では GUI プログラムでさえもしばしばしのごうとする。このパ
ターンの人気が衰えない理由とは？

> Efficiency, and perceived efficiency, seem to be important factors. Roguelike
> programs tend to be fast and lightweight relative to their nearest GUI
> competitors.

マウスを動かすためにキーボードから手を離さなくて済むので、熟練タイピストはローグ
ライクプログラムを好むことが多い。

> Given a choice, touch-typists will prefer interfaces that minimize keystrokes
> far off the home row;

画面の使い方の分析。GUI 障害物で画面内が乱雑になることがない。ゆえに、他のプログ
ラムと使用者の注意を頻繁に共有しなければならないプログラムでの使用に適している。
先に挙げられたプログラム群にはその性質がある。

> the roguelike pattern tends to appeal more than GUIs to people who value the
> concision and expressiveness of a command set enough to tolerate the added
> mnemonic load.

それならゲームやエディターに向いているのは納得だ。

### The ‘Separated Engine and Interface’ Pattern

エンジン
:  応用領域に特化した核心算法と論理
インターフェイス
:  使用者からコマンドを受け付け、結果を示し、ヘルプや履歴などの業務

> In fact, this separated-engine-and-interface pattern is probably the one most
> characteristic interface design pattern of Unix.

Xerox PARC の初期の GUI の研究は、原型として model-view-controller パターンを提
案するに至った。

* モデルは Unix 界では通常エンジン（上の意味で）と呼ばれるものだ。データベース
  サーバーはモデルの典型的な例だ。
* ビューは問題領域物トを目に見える形に表現するものだ。MVC が本当にうまく分離され
  たアプリケーションでは、ビュー部分はモデルの更新を通知され、コントローラーに
  よって同期的に駆動されたり、明示的な更新要求によって駆動されたりするのではな
  く、独自に応答する。
* コントローラーは使用者の要求を処理し、それをコマンドとしてモデルに渡す。

実際には、V と C の部分は、どちらかが M に結合しているよりも密接に結合している傾
向がある。アプリケーションが M の V を複数要求する場合にしか、これらは分離されな
い傾向がある。

Unix では MVC の適用が他の場所よりもはるかに一般だ。それは、まさに強い «do one
thing well» 伝統があり、プロセス間通信が簡単で柔軟だからだ。

この技法の特に強力な形は、ポリシーインターフェイス（多くの場合、V と C 機能を組
み合わせた GUI）と、問題領域固有の小規模言語のインタプリター ([Chapter 8]) を含
むエンジン (M) とを結びつけるものだ。

#### Configurator/Actor Pair

インターフェイス部分がフィルターや使用者コマンドを必要としないデーモン風プログラ
ムの起動環境を制御する。

fetchmail(1) と fetchmailconf(1) の対は当パターンの良い例だ。

このデザインパターンによって、`fetchmail` と `fetchmailconf` のそれぞれが得意と
することに特化することができ、実際、それぞれの仕事領域に適した異なる言語で書くこ
とができる。

* 通常デーモンとしてバックグラウンドで実行される `fetchmail` は GUI コードで大き
  くなる必要はない。
* `fetchmailconf` は `fetchmail` から規模と複雑さの費用を要求することなく、精巧
  GUI に特化することができる。
* `fetchmailconf` と `fetchmailconf` の間の情報経路は狭く、明確に定義されている
  ため、コマンドラインや `fetchmailconf` 以外のスクリプトから `fetchmail` を動か
  すことが可能だ。

> The term “configurator/actor” is my invention.

#### Spooler/Daemon Pair

Configurator/Actor Pair の若干の変形は、バッチモードで（個々のジョブが使用者との
対話を必要としない場合で）共有資源へのシリアライズされたアクセスを必要とする状況
で有用だ。

当パターンでは、Spooler つまりフロントエンドは単にジョブ要求とデータを Spool 領
域に放つ。

* ジョブ要求とデータは単なるファイル
* Spool 領域は通常、単なるディレクトリー

ディレクトリーの場所とジョブ要求の形態は Spooler と Daemon が合意している。

Daemon はバックグラウンドで永遠に実行され、Spool ディレクトリーを能動的かつ反復
的に行うべき仕事を採取しようとする。ジョブ要求を見つけると、関連するデータを処理
しようとする。成功するとジョブ要求とデータは Spool 領域から削除される。

例：

* Unix の印刷システム lpr(1)/lpd(1). 前者と後者がそれぞれ Spooler/Daemon だ。
  Spool 領域には印刷対象ファイルが置かれる。
* at(1)/atd(1). 指定された時間にコマンドを実行するようスケジュールする。
* UUCP. 1990 年代初頭にダイヤルアップ回線でのメール転送によく使われていた Unix
  間コピープログラム。

Spooler/Daemon Pair パターンはメール転送プログラムにおいて依然重要だ。送信失敗時
にメールが Spool 領域に置かれる。後で送信を再試行する。

Spooler/Daemon Pair は通常次の四部構成だ。実際、最初の三つが存在することは、その
背後に Daemon が存在することを示す確実な手がかりとなる：

* a job launcher
* a queue lister
* a job-cancellation utility
* a spooling daemon

> The terms “spooler” and “daemon” are well-established Unix jargon. (‘Spooler’
> actually dates back to early mainframe days.)

#### Driver/Engine Pair

このパターンでは、前二つのものとは異なり、インターフェース部分は起動後にエンジン
にコマンドを供給し、エンジンからの出力を解釈する。エンジンはドライバーの主プロセ
スであってもよいし、エンジンとドライバーはソケットや共有メモリー、その他のプロセ
ス間通信法を使って通信してもよい。重要な点は次の二点だ：

* Driver と Engine の双方向性
* Engine が独自のインターフェイスで単品で実行可能

Configurator/Actor よりも結合度が高いので書くのが難しい：

> the driver must have knowledge not merely about the engine's expected startup
> environment but about its command set and response formats as well.

Engine がスクリプト可能性のために設計されている場合、Driver が Engine 作者以外の
誰かによって書かれたり、ある Engine のフロントエンドに Driver が複数使われたりす
ることはよくある。例：

* gv(1), ghostview(1)/gs(1)
* xcdroast(1)/cdrecord(1)

<!-- Figure 11.3. The Xcdroast GUI. -->

xcdroast(1) は他の CLI ツールも呼び出す：

* cdda2wav(1): サウンドファイル変換
* mkisofs(1): ファイル一覧から ISO-9660 CD-ROM ファイルイメージを作成

(Steve Johnson) Driver/Engine 編成における重要な落とし穴は、Driver が Engine の
状態を理解しなければ、それを使用者に反映できないことが頻繁にあることだ。動作が実
質的に瞬時であれば問題ないが、時間がかかる場合にはフィードバックの欠如は重大な問
題となりうる。

Engine が正しいことをするだけでなく、Driver に何をしているかを通知し、Driver が
適切な反応を呈する奥ゆかしいインターフェイスを提示できるように設計することも重要
だ。

> The terms “driver” and “engine” are uncommon but established in the Unix
> community.

#### Client/Server Pair

Client/Server Pair は Driver/Engine Pair のようなものではあるが、Engine 部分は

* バックグラウンドで実行される
* 対話的に実行されることは期待されていない
* 独自の UI を有しない
* プログラムが起動されるたびに高く付く何かを実行するのを避ける意味がある

典型的な例：

* FTP を実装する ftp(1)/ftpd(1).
* sendmail(1) の二つのインスタンス。フォアグラウンドでは送信者、バックグラウンド
  では聴取者。
* Web ブラウザーと Web サーバー。
* psql(1)/postmaster(1)

これらの例はペア間のシリアライズされる通信規約が清浄であることが重要であるとい
う、Client/Server 構成の重要な特性を示している。

Separeted Engine and Interface プログラムはきれいな機能分離からこのような恩恵を
得られる可能性があるが、Client/Server の場合、共有資源の管理が本質的に難しいた
め、それを正しく行うことの見返りが特に高くなる傾向がある。

Client と Server を別々の計算機で実行できることの利点がたいへん大きいので、現代
では Client/Server Pair のほとんどは TCP/IP ソケットを使用している。

### The CLI Server Pattern

サーバープロセスが inetd(8) のようなハーネスプログラムによって呼び出されるのは
Unix の世界では普通のことで、ハーネスプログラムはサーバーの標準入力と標準出力が
指定された TCP/IP サービスポートに接続されていることを確認する。この役割分担の利
点のひとつは、ハーネスプログラムが起動するサーバー全てに対して、単一の用心棒とし
て機能することだ。

ハーネスプログラムの定義：

> A harness program is a wrapper whose job it is to make some special sort of
> resource available to the program(s) it calls. The term is most often used for
> test harnesses, which make available test loads and (often) examples of
> correct output for the actual output to be checked against.

古典的なインターフェイスパターンの一つは CLI サーバーだ：

* フォアグラウンドモードで起動されると標準入力から読み込んで標準出力に書き込む、
  単純な CLI インターフェイスを有するプログラムだ。
* バックグラウンドで起動されると、サーバーがこれを検出し、標準入力と標準出力を指
  定された TCP/IP サービスポートに接続する。

サーバーのほとんどのコードは、それがフォアグラウンドで実行されているのか、TCP/IP
ハーネスで実行されているのかを知ることも気にすることもないというのが要諦だ。

POP, IMAP, SMTP, HTTP サーバーは通常このパターンに従う。前述の Client/Server パ
ターンのどれかと組み合わせることができる。

> Though this pattern is quite traditional, the term “CLI server” is my
> invention.

### Language-Based Interface Patterns

問題領域固有の小規模言語 ([Chapter 8]) の長所は、Unix シェルに代表されるように、
言語に基づく CLI を Unix インターフェイスの重要な様式にしている。

このパターンの長所は dc(1)/bc(1) と xcalc(1) を比較した事例研究でよく示されてい
る。

最も強力な Unix デザインパターンの一つは、GUI フロントエンドと CLI 小規模言語
バックエンドの組み合わせだ。この種のよく設計された例は必然的にかなり複雑になる
が、小規模言語で実現できることのごく一部を網羅するために必要な間に合わせのコード
の量に比べれば、はるかに単純で柔軟性が高いことがよくある。

最近のデータベーススイートは通常どこでも一つ以上の GUI フロントエンドと報告作成
で構成され、そのすべてが SQL のような言語を使用して共通のバックエンドと対話す
る。このパターンは主に Unix の下で発展してきたものであり、他の場所よりも Unix の
方がよりよく理解され、より広く適用されている。

Unix 界では Emacs がこのパターンの最もよく知られた例の一つだ。

GIMP の Script-fu 機能も良い例だ。これを使えば Scheme を使って GIMP をスクリプト
化できる。Tcl, Perl, Python を使ったスクリプトも可能だ。これらの言語で書かれたプ
ログラムはプラグインインターフェイスを通じて GIMP の内部を呼び出せる。

## Applying Unix Interface-Design Patterns

スクリプトとパイプライン ([Chapter 7]) を容易にするためには、できるだけ単純なイ
ンターフェイスパタンを選ぶのが賢明だ。

上述した単一部品パターンの多くは、起動時間後に使用者による操作を必要としないこと
が強調されている。使用者は人間でなく、別のプログラムであることが多いため、これは
スクリプト性を最大化する、価値のある機能だ。

* 初心者や非技術的な使用者に適した GUI やデザインパターンと、
* 熟練者の役に立ち、スクリプト可能性を最大化する GUI やデザインパターン

との間には、強く本質的な緊張関係がある。

「最も単純なパターンを選択する」ことと、GUI を作成する要件が矛盾する場合、Unixの
方法は、プログラムを二つに分割し、Separeted Engine and Interface デザインパター
ンを適用することだ。

### The Polyvalent-Program Pattern

1. プログラムの応用領域論理は、文書化された API を持つライブラリーの中にあり、他
   のプログラムと連結することができる。他の世界に対するプログラムのインターフェ
   イス論理は、ライブラリーの上に薄い層がある。あるいは、異なる UI スタイルを持
   つ層がいくつかあり、そのどれでもライブラリーに連結することができる。
2. バッチモードで対話的コマンドを実行する Cantrip, Compiler-like, CLI パターンの
   いずれかである UI モードがある。
3. GUI であり、中心ライブラリーに直接連結されるか、CLI を駆動する別プロセスとし
   て動作する UI モードがある。
4. 最新の汎用スクリプト言語を使ったスクリプティングインターフェイスモードがある。
5. curses(3) を使ったローグライクなインターフェイスがオマケで存在する。

<!-- Figure 11.4. Caller/callee relationships in a polyvalent program. -->

GIMP は実際にこのパターンを満たしている。

## The Web Browser as a Universal Front End

多くのアプリケーションでは、自作 GUI フロントエンドを全く書かず、むしろ Web ブラ
ウザーをその役割に押し付けることが理にかなうようになった。この取り組み方には利点
が多くある：

* 手続き的な GUI コードを書く必要がない。代わりに、所望の GUI をそれに特化した言
  語 (HTML, JavaScript) で記述することが可能。
* アプリケーションを即座にインターネット対応にできる。
* アプリケーションの細かい表現の詳細（フォントや色など）を、ブラウザーの環境設定
  や CSS のような仕組みによって、使用者が自分好みに変えられる。
* Web インターフェイスの一様な要素が使用者の学習作業を大幅に容易にする。

短所もある：

* Web が強制するバッチスタイルの対話が難しい
* ステートレスプロトコルを使った永続的セッションの管理が難しい

CGI はきめ細かな相互作用性をうまく対応していない。また、テンプレートシステム、ア
プリケーションサーバー、埋め込みサーバースクリプトも、徐々に CGI に取って代わり
つつある。この節ではこれらすべてを CGI と呼ぶ。

CGI は基本的にバッチ式の相互作用であり、パンチされたカードを入力ホッパーに落とし
て印字されたものが戻ってくるのとそれほど変わらない。JavaScript を使って使用者と
やりとりし、メッセージにまとめてサーバーに送ることでより使いやすくすることができ
る。

!!! note
    Java の話題は割愛。

複数の CGI フォーム間でセッション情報を維持するのは厄介だ。サーバーは CGI 更新間
のクライアントセッションに関する状態を保持しないので、同じ使用者による以前の
フォーム送信と後のフォーム送信を接続するためにそれに頼ることはできない。これを回
避する標準的な方法は：

* 連鎖フォーム
* クッキー

> When you chain forms, you arrange for the CGI for the first form to generate a
> unique ID in an invisible field of the second form, and for the second and all
> subsequent forms to pass that ID to their successors.

クッキーは環境変数に類似した、より直接的でない方法で同様の効果を与える。

どちらの場合でも、CGI は ID をセッションインデックスとして使い（あるいはクッキー
で状態を直接キャッシュし）、セッションの多重化を明示的に処理する必要がある。

> That per-user state can be a problem; it eats resources, and it has to be
> timed out, because between transactions there is no way to know that the user
> is still on the other end of the wire.

CGI とクッキーで十分なのに、Java やアプリケーションサーバーに依存した重量級設計
を行おうとするな。できるだけ単純なパターンを選ぶのが最善だ。

Web Browser as a Universal Front End の取り組み方の問題は、CGI バックエンドがブ
ラウザー環境から容易に分離できないことだ。

> The Unix answer is a three-tier architecture — Web forms calling CGIs which
> call commands. The automation interface is the commands.

## Silence Is Golden

[Chapter 1] では、沈黙の規則を習った：よく設計された Unix プログラムでは面白いこ
とや驚くようなことは何も言わないので黙っていろ。

標準エラーには本当のエラーしか送らず、要求されていないデータはまったく送らない方
がよい：

> If your CLI program emits status messages to standard output, then programs
> that try to interpret that output will be put to the trouble of interpreting
> or discarding those messages (even if nothing went wrong!).

画面の縦の空間は貴重だ。

迷惑メッセージは人間の帯域幅を無造作に浪費する。

データを失う可能性のある操作を保護する必要がある場合を除いて、GUI を確認ポップ
アップで散らかすな。

一般的に、使用者がすでに知っていることを伝えるのは悪い流儀だ。インターフェイスの
設計は全体として驚き最小の法則に従うべきだが、メッセージの内容は驚き最大の法則に
従え。

このルールは、確認プロンプトに対してさらに大きな効力を持つ。

> Constantly asking for confirmation where the answer is almost always “yes”
> conditions the user to press “yes” without thinking about it, a habit that can
> have very unfortunate consequences. Programs should request confirmation only
> when there is good reason to suspect that the answer might be “no no no!”

確認プロンプトがまったくない場合、インターフェイスに本当に必要なのは undo コマン
ドだという兆候かもしれない。

デバッグのためにおしゃべりな進捗メッセージが必要な場合は、verbosity スイッチを
使って既定で無効にしろ。本番用にリリースする前に、できるだけ多くの通常メッセージ
を、verbosity がオンのときしか表示されるないようにしろ。

[Chapter 1]: <../context/philosophy.md>
[Chapter 6]: <./transparency.md>
[Chapter 7]: <./multiprogram.md>
[Chapter 8]: <./minilanguages.md>
[Chapter 13]: <./complexity.md>
