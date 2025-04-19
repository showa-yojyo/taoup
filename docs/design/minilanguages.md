# Chapter 8. Minilanguages

[TOC]

プログラマーのエラー率（数百行あたりの欠陥数）は対象言語にほとんど依存しないとい
う研究がある。ということは、より少ない行数でより多くの作業を行うことができる高水
準言語は、バグもより少ないことを意味する。

特定の応用領域を一つ固定して、それに特化した言語を与えれば、プログラムの量を大幅
に減らせる。そのような言語の例：

* 組版言語各種 (`troff`, `eqn`, `tbl`, `pic`, `grap`)
* シェル道具 `awk`, `sed`, `dc`, `bc`
* ソフトウェア開発 (`make`, `yacc`, `lex`)

著者はこの種の領域固有言語を小規模言語 (minilanguage) と呼ぶことにしている。可能
な限り小さく単純に設計するのが賢明であることを強調したいので。※複雑な小規模言語
が存在しないとは主張していない。

小規模言語設計に至る正しい道の一本目は、小規模言語設計を使うと、あるプログラミン
グ問題の仕様を、汎用言語で支援するよりも引き締まった表現力豊かな記法で、一段上の
水準に押し上げることができるということをあらかじめ悟ることだ。

小規模言語設計にたどり着く二本目の道は、仕様書のファイル形式の一つが小規模言語に
似てきていることに気づくことだ。つまり、複雑な構造を開発し、制御しているアプリ
ケーションの動作を暗示しているのだ。

小規模言語設計に至るダメな道は、小出しに厄介な追加機能を拡張していくことだ。その
先例を一つ：

> the example every Unix guru will think of (and shudder over) is the
> `sendmail.cf` configuration file associated with the `sendmail` mail
> transport.

ダメな小規模言語をやってしまった場合の修正方法を後ほど Emacs Lisp の調査で見てい
くそうなので楽しみにしておく。

悪い小規模言語の設計に対する唯一の防御策は、良いそれの設計方法を知っていることし
かない。

## Understanding the Taxonomy of Languages

[Figure 8.1. Taxonomy of languages.][Figure 8.1] を頭に叩き込んでから本書の精読
を続ける。

* 基本的にはベン図であり、右の要素ほど increasing loopiness だ。
* 集合それぞれにも右の要素ほど何らかの性質が強くなるが、あまり重要ではなさそうだ？

> In [Chapter 5](./textuality.md) we looked at Unix conventions for data files.
> There's a spectrum of complexity in these.

イラストでは点線の仕切りや隣の集合との交わりで表現されている。いちばん低級である
のは名前と性質の間の単純な関係を作るファイルだ。イラストでは `/etc/passwd`,
`.newsrc` が相当する。

さらに尺度を上げるとデータ構造を相互変換する形態が出てくる。イラストでは SNG が
相当する。

> A structured data-file format starts to border on being a minilanguage when it
> expresses not just structure but actions performed on some interpretive
> context (that is, memory that is outside the data file itself).

* XML はこの境界をまたぐ傾向がある（イラストでは XSLT が相当）。
* ここで取り上げる例は GUI を構築するためのコードジェネレーター、Glade だ。

> Formats that are both designed to be read and written by humans (rather than
> just programs) and are used to generate code, are firmly in the realm of
> minilanguages.

* `yacc`, `lex` が典型的な例。
* マクロプロセッサーである `m4` もまた宣言的（イラスト中央の集合の左側）小規模言
  語だ。

Makefile については [Chapter 15](../implementation/tools.md) でやるそうだ。

イラスト中央の集合はよく見ると四分割されている：

> The spectrum of minilanguages ranges from declarative (with implicit actions)
> to imperative (with explicit actions).

* fetchmail(1) の実行制御構文は、非常に弱い命令型言語か、暗黙の制御フローを持つ
  宣言型言語のどちらと見なすこともできる。
* `troff` と PostScript 組版言語は多くの専門知識が組み込まれた命令型言語だ。

課題に特化した命令型小規模言語の中には、汎用インタプリターになりかけているものも
ある（イラスト中央集合の右端部分）。つまり、条件分岐とループ（または再帰）の両方
が制御構造として使われるように設計されている。これとは対照的に、偶発的にTuring完
全であるに過ぎない言語もある。

脚注：

> In practice, some Turing-complete languages would be far too painful to use
> for anything outside a specified and narrow problem domain.

* bc(1) と dc(1) インタープリターは明示的に Turing 完全である特殊な命令型小規模
  言語の良い例だ。

イラスト右集合内部には仕切線が描かれていないので、汎用度だけが違うと読める。

Emacs Lisp や JavaScript のように、特殊なコンテクストで実行される完全なプログラ
ミング言語として設計された言語まで来ると、汎用インタプリターとの境界線を越えるこ
とになる。

悲しいことに、最後のパラグラフが部分的に難しくてわからない。イラスト右集合の右か
ら二番目に `sh` と Tcl があるが……。

> With increasing generality there usually comes a richer ontology of data
> types. Shell and Tcl have relatively simple ontologies; Perl, Python, and Java
> more complex ones.

## Applying Minilanguages

小規模言語を使った設計には課題が二つある：

* 道具箱の中に便利な既存の小規模言語があり、それをそのまま適用できる場合を認識す
  ること。
* アプリケーションのために自作小規模言語を設計することが適切な状況を知ること。

### Case Study: `sng`

SNG は [Chapter 6](./transparency.md) で一度取り扱ったツールだ。

* SNG には PNG のようなバイナリーデータ形態にはない重要な特徴、透明性がある。
* 構造化データファイルは編集、変換、生成各ツールが互いの設計の前提を知ることなく
  協調することを可能にする。
* SNG が加えたものは «it's designed to be easy to parse by eyeball and edit with
  general-purpose tools» だ。

### Case Study: Regular Expressions

正規表現自体が小規模言語であるという見方は賛同するしかない。

> Regexps are so ubiquitous that the are hardly thought of as a minilanguage,
> but they replace what would otherwise be huge volumes of code implementing
> different (and incompatible) search capabilities.

Unix における最も単純な正規表現ツールは grep(1) であり、指定された正規表現に合致
する入力行をすべて出力に渡すフィルターだ。

正規表現には亜種のようなものがある：

1. Glob 表現 (glob expressions): Bash で言うワイルドカード `*`, `[...]`, `{...}`
   に対応する。
2. 基本正規表現 (basic regular expressions): オリジナルの grep(1) が受理する記
   法。
3. 拡張正規表現 (extended -): egrep(1) または `grep -E` が受理する記法。
4. Perl 正規表現 (Perl -): Perl, Python, `grep -P` が受理する記法。

正規表現を支援する新しい言語の設計慣習は Perl の亜種となる流れに落ち着いてきた。
英数字でない文字の前のバックラッシュはその文字をリテラルとして常に意味する。これ
で正規表現の扱いにおける混乱が少なくなる。

正規表現は小規模言語がいかに簡潔であるかを示す極端な例だ。単純な正規表現は、それ
を使わないのであれば何百行もの気難しくバグを起こしやすいコードで実装しなければな
らないような認識動作を表現するものだ。

### Case Study: Glade

Glade は GTK ツールキットライブラリー用の GUI 設計プログラム？だ。説明文を読む限
り、よくあるフォームデザイナーのようなものを想像する。本質はここ：

> The GUI editor produces an XML file describing the interface; this, in turn,
> can be fed to one of several code generators that will actually grind out C,
> C++, Python or Perl code for the interface. The generated code then calls
> functions you write to supply behavior to the interface.

生成コードが自作リスナー関数を呼び出し、動作を規定するものと考えられる。

GUI を記述するための Glade の XML は単純な領域固有の小規模言語の良い例だ。

Example 8.1. はおそらく `Hello World` というラベルを含むダイアログボックスか何か
を定義する XML コード全体だろう。

* Glade GUI は有効仕様を構造化されたデータファイルとして扱う。
* Glade コード生成器は GUI を実装するプログラムを記述するために有効仕様を用い
  る。

XML の冗長さを乗り越えれば、Glade マークアップはかなり単純な言語だ。次の二つを行
うだけだ：

* GUI ウィジェットの階層を宣言すること
* ウィジェットに属性を関連付けること

このような透明性と単純性は優れた小規模言語の証だ。

> The ultimate functional test of a minilanguage like this one is simple: can I
> hack it without reading the manual? For a significant range of cases, the
> Glade answer is yes.

例えば、ウィンドウ位置を変更したい場合は XML の

```xml
<position>GTK_WIN_POS_NONE</position>
```

周囲を書き換えればいいだろうという見当が付く。

Glade を使う利点は明らかだろう。コード生成に特化しているからだ。

### Case Study: m4

マクロ処理器 m4(1) はテキストの変換を記述するための宣言的な小規模言語を解釈する。

* プログラムはテキスト文字列を他の文字列に展開する方法を指定するマクロの集合だ。
* これらの宣言を `m4` で入力テキストに適用すると、マクロ展開が行われ、出力テキス
  トが得られる。
* `m4` は引数つきマクロ機能を有する。特定の固定文字列を別のものに変換する以上の
  ことを可能にする。

!!! note "TODO"
    実際に `sudo apt install m4` して `info m4` を見るのが良さそうだ。

マクロ言語は条件分岐と再帰を支援している。Turing 完全だ。

マクロ処理器は、通常、名前付き手続きやファイルインクルード機能が組み込まれていな
い小規模言語の前処理器として用いられる。これは土台となる言語の構文を拡張する簡単
な方法なので、`m4` との組み合わせでこれらの両方の機能を支援する。

よく知られた用途：

> Most system administrators now generate their `sendmail.cf` configuration
> files using an `m4` macro package supplied with the `sendmail` distribution.
> The macros start from feature names (or name/value pairs) and generate the
> corresponding (much uglier) strings in the `sendmail` configuration language.

!!! note "TODO"
    リンク追加

### Case Study: XSLT

XSLT は `m4` と同様、テキストストリームの変換を記述するための言語だ。単純なマク
ロの置換以上のことを行う。これは XML スタイルシートを記述するために使用される言
語だ。実用的なアプリケーションについては [Chapter 18
](../community/documentation.md) で見るようだ。

XSLT の特徴：

* 純粋に宣言的で Turing 完全だ。
* 再帰のみを支援し、ループは支援しない。
* 非常に複雑で、間違いなく本章の事例研究の中で習得が最も難しい言語だ。
* 型が限定されている。とりわけ、レコード構造や配列のような物がない。
* XSLT 処理器が標準入力を標準出力に絞り込むように設計されており、ファイルを読み
  書きする機能は限定的だ。

<!-- ontology: the part of philosophy that studies what it means to exist -->
<!-- ontology: a list of concepts and categories in a subject area that shows the relationships between them -->

「宣言的」が「単純」でも「弱い」でもないという点を説明するためにも、ここで XSLT
を紹介したと述べている。XML 文書を扱う必要があるなら、いつかは XSLT という難題に
直面しなければならないとも述べている。

読書案内：

> *XSLT: Mastering XML Transformations* is a good introduction to the language.
> A brief tutorial with examples is available on the [Web][85].

### Case Study: The Documenter's Workbench Tools

まず Documenter's Workbench Tools を知らないとついていけない：

> `troff` is the center of a suite of formatting tools (collectively called
> Documenter's Workbench or DWB), all of which are domain-specific minilanguages
> of various kinds.

ほとんどは `troff` マークアップのための前処理器か後処理器だ。Free Software
Foundation 版のものは groff(1) といい、機能が拡張されている。

* 本格的なインタプリターになりかけている命令型小規模言語の良い例だ。
* 条件法と再帰はあるがループはない。Turing 完全であるのは偶然だ。

後処理器は通常、`troff` 使用者には見えない。

> The original `troff` emitted codes for the particular typesetter the Unix
> development group had available in 1970; later in the 1970s these were cleaned
> up into a device-independent minilanguage for placing text and simple graphics
> on a page.

後処理器はこの言語を現代の画像プリンターが実際に受け入れることができるものに変換
する。

前処理は `troff` 言語に機能を実際に追加する。一般的なものは：

* tbl(1): 表を作成する
* eqn(1): 数式を組版する
* pic(1): 図式を作図する

その他、grn(1), refer(1), bib(1) などがある。これらすべてのオープンソース等価版
は `groff` に同梱されている。

> The grap(1) preprocessor provided a rather versatile plotting facility; there
> is an open-source implementation separate from `groff`.

その他の前処理器の中には、オープンソースでの実装がなく、もはや一般的に使わ
れていないものもある。例えば ideal(1) や chem(1) だ。

これらの前処理器それぞれは小規模言語を受け取り、それを `troff` 要求にコンパイル
する。具体的には：

> it is supposed to interpret by looking for a unique start and end request, and
> passes through unaltered any markup outside those (`tbl` looks for
> `.TS`/`.TE`, `pic` looks for `.PS`/`.PE`, etc.).

たいていの前処理器は互いに干渉することなく、任意の順序で実行可能だ。モノによって
は、例えば `chem` と `grap` はどちらも `pic` コマンドを発行するので、パイプライ
ンでは `pic` の前に来なければならない。

化学式、数式、表、書誌、プロット、図式を含む仮想的な論文を対象とした、
Documenter's Workbench 処理パイプラインの例を本書から引用する：

```console
cat thesis.ms | chem | tbl | refer | grap | pic | eqn | groff -Tps > thesis.ps
```

この種のビルドレシピは一度構成すれば、繰り返し使用するために Makefile やシェルス
クリプトラッパーに収めておけばいい。

これらの前処理器が扱う問題の範囲は、小規模言語モデルの能力をある程度示している。
WYSIWYG ワープロに同等の知識を埋め込むのは至難の業だ。

> The pipeline architecture supports plugging in new, experimental preprocessors
> and postprocessors without disturbing old ones. It is modular and extensible.

Documenter's Workbench はパイプ、絞り込み、小規模言語の能力の初期の見本であり、
その見本は後の Unix の設計の多くに影響を与えた。個々の前処理器の設計は効果的な小
規模言語の設計がどのようなものかについて、より多くの教訓を含む。

> Sometimes users writing descriptions in the minilanguages do unclean things
> with low-level troff markup inserted by hand.

マークアップを手動でいじるのは不潔だ。

前処理器言語は比較的きれいな、シェルのような構文を持っており、データファイル
フォーマットの設計について [Chapter 5](./textuality.md) で説明した慣習の多くに
従っている。

Documenter's Workbench の少なくとも三つの小規模言語に共通する題の一つは意味を宣
言的に取り扱うことだ。この考え方は GUI ツールキットにも見られる。

この辺で pic(1) プログラムに図式配置を与えるコードを考察しているが、割愛。

<!-- Example 8.4. Taxonomy of languages — the pic source. -->

pic(1) の例は小規模言語に共通の設計主題を反映していて、それは Glade にも反映され
ている。つまり、制約に基づく推論をカプセル化し、それを動作に変換するために小規模
言語を用いる。

> The `pic2graph` script we used as a case study in [Chapter 7] was an ad-hoc
> way to accomplish this, using the retrofitted PostScript capability of
> groff(1) as a half-way step to a modern bitmap format.

GNU plotutils パッケージには pic2plot(1) という、より清浄な解決策がある。

> The code was split into a parsing front end and a back end that generated
> troff markup, the two communicating through a layer of drawing primitives.

モジュール性があるので、pic2plot(1) は GNU `pic` の解析段階を切り離し、最新の描
画ライブラリーを用いて描画を再実装した。

### Case Study: `fetchmail` Run-Control Syntax

Example 8.5. としてファイル `fetchmailrc` の例が示される。この実行制御ファイルは
命令型小規模言語と見なすことができる。

<!-- Example 8.5. Synthetic example of a `fetchmailrc`. -->

* 条件分岐も再帰もループもない。明示的な制御構造はまったくない。
* 単なる関係ではなく動作を記述するので、Glade GUI 記述のような純粋に宣言的な構文
  とは区別される。

複雑なプログラムのための実行制御小規模言語は、この宣言言語と非常に弱い命令型言語
のどっちつかずにしばしばなる。

### Case Study: `awk`

前半の `awk` に関する概要はザッと目を通す程度でいい。

当研究事例は `awk` が模倣の手本にはならないことを指摘する。

* 1990 年以降はほとんど使われなくなった。
* 新しいスクリプト言語、特に Perl に取って代わられた。

もともと `awk` は報告書生成のための小さくて表現力豊かな特殊目的言語として設計さ
れた。残念なことに、`awk` は複雑さ対能力曲線の悪い点に設計されていることが判明し
た。

> Awk has also fallen out of use because more modern shells have floating point
> arithmetic, associative arrays, RE pattern matching, and substring
> capabilities, so that equivalents of small awk scripts can be done without the
> overhead of process creation. -- David Korn

* 1987 年に Perl が登場してから数年間は `awk` の方が小さくて高速な実装だったとい
  う理由だけで競争力を維持していた。しかし、計算サイクルとメモリーの経費が下がる
  につれて、そういう倹約指向は力を失っていった。
* 2000 年になる頃には `awk` は古参の Unix ハッカーのほとんどにとって単なる思い出
  に過ぎなくなっていた。

* 機械資源は時間とともに安くなるが、プログラマーの頭の中の空間は高くなる一方だ。
* 最近の小規模言語は一般的だが非コンパクトなものと、専門的だが非常にコンパクトな
  ものに両極化している。

  > specialized but noncompact simply won't compete

### Case Study: PostScript

> PostScript is a minilanguage specialized for describing typeset text and
> graphics to imaging devices.

* Xerox Palo Alto Research Center で行われた設計作業を基に Unix に輸入された。
* 1984 年に初めて商用リリースされた後、何年もの間、Adobe 社の独占製品としてのみ
  利用可能。
* 1988年 にオープンソースに近い許諾条件でクローンされ、以来 Unix でのプリンター
  制御の事実上標準となっている。

PostScript は機能的には `troff` マークアップに似ている。どちらもプリンターやその
他の画像デバイスを制御するためのもので、通常はプログラムやマクロパッケージが生成
する。

PostScript は言語として一から設計されており、はるかに表現力が豊かで強力である。

PostScript で書かれた画像のアルゴリズム記述は描画するビットマップよりもはるかに
小さいため、記憶域や通信帯域幅を食わない。

PostScript は明示的に Turing 完全であり、条件分岐、ループ、再帰、名前付き手続き
を支援している。整数、実数、文字列、配列があるが、構造体に相当するものはない。

全部で 400 ほどある操作のうち、基本的なものは 40 ほどある。例えば：

* ページ上に文字列を描く
* 現在のフォントを設定する
* グレーレベルや色を変更する
* 線分、円弧、Bezier 曲線を描く
* 閉領域を塗りつぶす
* くり抜き領域を設定する

その他の PostScript 操作は算術演算、制御構造、手続きを実装する。これらにより反復
画像や定型画像を、画像を組み合わせるプログラムとして表現する。

PostScript の有用性の一端は SVG 性にある。ビットマップよりもはるかにかさばらず、
デバイスの解像度に依存せず、ネットワークケーブルやシリアル回線でより速く移動でき
る。

> PostScript is often implemented as firmware built into a printer.

Firmware とはハードウェア（この場合は印刷機）が機能し、機器上で動作する他のソフ
トウェアと通信できるようにする基本的な機会命令を与えるソフトウェアのことをいう。

オープンソースの実装である Ghostscript は PostScript をさまざまなグラフィック形
式や（ちょっとした）プリンター制御言語に変換することが可能だ。他のほとんどのソフ
トウェアは PostScript を最終的な出力形式として扱い、PostScript 対応の画像処理デ
バイスに渡すことを意図しているが、編集したり、目で見たりすることはできない。

PostScript はたいへんよく設計された特殊用途制御言語の例であり、模範として注意深
く研究する価値がある。

### Case Study: `bc` and `dc`

これらは命令型の例だ。

> `dc` is the oldest language on Unix; it was written on the PDP-7 and ported to
> the PDP-11 before Unix itself was ported. -- Ken Thompson

この二つの言語の領域は無制限精度の算術演算だ。他のプログラムからは、そのような計
算に必要な特殊技法を気にすることなく、これらの言語を使ってそのような計算を行うこ
とができる。

SNG や Glade マークアップ同様、これらの言語の強みの一つはその単純さだ。dc/bc そ
れぞれの記法さえ知ってしまえば、これらの言語の対話的操作について目新しいことはほ
とんどない。驚き最小の法則だ。

* 条件分岐とループの両方を持ち、Turing 完全である
* 型は非常に制限されており、無制限精度の整数と文字列しかない。

dc/bc はインタプリター型小規模言語と完全なスクリプト言語の境界線上にある。

ユーザー定義手続きのライブラリーを支援する能力はプログラミング可能性という付加的
な利便性を与える。これは命令形言語の最も重要な利点だ。

dc/bc のインターフェイスは単純なので、他のプログラムやスクリプトはこれらのプログ
ラムを主プロセスとして呼び出すことで、これらのすべての機能に簡単にアクセスできる。

### Case Study: Emacs Lisp

個人的には xyzzy 使用者だったので、この節の主張を誤解することはないと信じたい。

特殊用途のインタープリタ型言語は、単に特定の課題を達成するための主プロセスとして
実行されるのではなく、構造全体の核となることができる。

Emacs は Lisp の方言で構築されており、編集バッファーに対する動作を記述することと、
従プロセスを制御することの両方の素を備えている。

Emacs が編集操作や他のプログラムのフロントエンドを記述するための強力な言語を中心
に構築されているという事実は、通常の編集以外にも多くのことに使用できるということ
を意味する。

Emacs の「モード」はユーザー定義のライブラリーであり、Emacs Lisp で書かれたプロ
グラムであり、エディターを特定の仕事に特化させるものだ。

Emacs のモードで実装されるさまざまな機能の例：

* メール送受信（システムメールサービスを従プロセスとして使う）
* Usenet ニュース送受信
* Web 閲覧
* チャットプログラムのフロントエンド
* カレンダー
* Emacs 独自の電卓プログラム、
* Emacs Lisp モードとして書かれたゲーム

### Case Study: JavaScript

この節で研究するのはクライアント側 JavaScript だ。以下、単に JavaScript と記す。

> JavaScript is an open-source language designed to be embedded in C programs.

これは知らなんだ。

* JavaScript コードを含む Web ページを通じた使用者への攻撃を防ぐため、その機能は
  厳しく制限されている。
* ディスクファイルの内容を直接変更することは不可能。
* ネットワーク接続を独自に開始するとは不可能。

上の制約があるので JavaScript は汎用言語とは言い難い。

JavaScript は現在、ブラウザーの DOM と呼ばれる単一の特別なオブジェクトの値を読み
書きすることで、その環境と相互作用する。

JavaScript は次の理由から興味深い研究になる：

* 実際にその場にいなくても入手できる汎用言語に限りなく近い。
* 単一の DOM オブジェクトを介した JavaScript とそのブラウザー環境の間の結びつき
  はよく設計されており、他の埋め込み状況の手本として役立つ可能性がある。

## Designing Minilanguages

### Choosing the Right Complexity Level

### Extending and Embedding Languages

### Writing a Custom Grammar

### Macros — Beware!

### Language or Application Protocol?

[Chapter 7]: <./multiprogram.md>
[Figure 8.1]: <http://www.catb.org/esr/writings/taoup/html/graphics/taxonomy.png>
[85]: <https://nwalsh.com/docs/tutorials/xsl/xsl/slides.html>
