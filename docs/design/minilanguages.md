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

べらぼうに長い。

### Case Study: `fetchmail` Run-Control Syntax

### Case Study: `awk`

### Case Study: PostScript

### Case Study: `bc` and `dc`

### Case Study: Emacs Lisp

### Case Study: JavaScript

## Designing Minilanguages

### Choosing the Right Complexity Level

### Extending and Embedding Languages

### Writing a Custom Grammar

### Macros — Beware!

### Language or Application Protocol?

[Figure 8.1]: <http://www.catb.org/esr/writings/taoup/html/graphics/taxonomy.png>
[85]: <https://nwalsh.com/docs/tutorials/xsl/xsl/slides.html>
