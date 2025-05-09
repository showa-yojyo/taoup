# Chapter 15. Tools

[TOC]

## A Developer-Friendly Operating System

優れた IDE に慣れていると、Unix の方法論は偶発的で、見通しが悪く、原始的に見える
かもしれない。しかし、実はそこには秩序がある。

ツールに乏しい環境での単一言語プログラミングには、IDE は大いに意味がある。しか
し、Unix 環境では言語や実装の選択肢はもっと多岐にわたる。複数のコード生成器や自
作構成器、その他多くの標準ツールや自作ツールを使うのが一般的だ。

Unix でも IDE は存在する。しかし、仕様に制限のないさまざまなプログラミングツール
を IDE で制御するのは難しく、あまり使われていない。Unix は編集、コンパイル、デ
バッグの反復を中心としない、より柔軟なスタイルを推奨している。

コードの構築、コード構成の管理、プロファイリング、デバッグ、そしてこれらの仕事に
関連する多くの苦役を自動化することで、楽しい部分に集中できるようにするのが Unix
での開発戦術だ。

この章のツールのほとんどは *Programming with GNU Software* でよく説明されてい
る。

これらのツールの多くは、より時間がかかり、間違うことも多くなる手作業でできること
を自動化するものだ。学習曲線を登るための一時的な費用は十二分に回収できるはずだ。
より効率的にプログラムを書くことができ、低水準の細部に注意する必要がなくなり、設
計により多くの時間を費やすことができるようになる。

道具の習得は Unix の学習曲線の大きな部分だ。

## Choosing an Editor

最初の、そして最も基本的な開発用具は、プログラムを修正したり書いたりするのに適し
たテキストエディターだ。

本格的な編集作業では、二つのエディターが Unix プログラミングシーンを完全に支配し
ている。`vi` と Emacs だ。これらについては [Chapter 13] で、ソフトウェアの適切な
規模についての議論の一環として述べた。

この二つのエディターは対照的な設計哲学で、どちらも人気がある。Unix プログラマー
を対象とした調査では、常に両者がほぼ半々であり、他のエディターはほとんど存在しな
いことが示されている。

実用性の問題としても、Unix の教養の問題としても、これらのエディターについて知る
価値は他にもたくさんある。

### Useful Things to Know about `vi`

> The name of `vi` is an abbreviation for “visual editor” and is pronounced /vee
> eye/ (not /vie/ and definitely not /siks/!).

Unix 用に作られたスクリーン指向のエディターの中で最も長命で、今でも使われており、
Unix の伝統の神聖な一部となっている。

* 原版 `vi` は 1976 年開始の初期 BSD に存在したバージョン。現在は時代遅れ。
* 代わりとなるものは、4.4BSD に同梱され、BSD/OS, FreeBSD, NetBSD など、最近の
  4.4BSD の亜種に見られる新しい `vi` だ。

機能を拡張した亜種がいくつかあり、その中でも `vim` はおそらく最も人気があり、多
くの Linux が搭載している。すべての亜種はかなり似ており、原版から変更されていな
い芯コマンド集合を共にしている。

`vi` は Windows と MacOS に移植されている。

Unix 入門書のほとんどには `vi` の基本的な使い方を説明した章がある。

### Useful Things to Know about Emacs

> Emacs stands for ‘EDiting MACroS’ (pronounce it /ee´·maks/).

最初は 1970 年代後半に TECO というエディターでマクロの集合として書かれたもので、
その後何度か再実装された。

複雑性の議論では Emacs を過度に重量級だと考えている人が多くいることを指摘したが、
Emacs を学ぶために時間を投資することは、生産性において豊かな報酬を得ることができ
る。

Emacs は様々なプログラミング言語の構文を支援する強力な編集モードを多数支援してい
る。Emacs を他の開発用具と組み合わせることで、従来の IDE に匹敵する（場合によっ
ては凌駕する）機能を実現する方法がある。

標準的な Emacs は GNU Emacs であり、最近の Unix で普遍的に利用できる。ソースと文
書は FSF の Web サイトで入手可能。

[XEmacs] はより優れた X インターフェイスを持っており、それ以外の機能はよく似てい
る。

Emacs は MS-DOS, Windows 95, NT にも移植されている。

!!! note

    Meadow というのが存在した気がする。

* Emacs には独自の対話型チュートリアルとべらぼうに充実したオンライン文書が用意さ
  れており、Emacs 起動画面にはその両方を呼び出す方法が既定で記載されている。
* 紙の入門書としては *Learning GNU Emacs* が良かろう。

Web ブラウザーやメールクライアントのテキストエリアにおける基本的なテキスト編集に
関するキーバインドは、純正 Emacs のそれがそのまま通じる。

### The Antireligious Choice: Using Both

`vi` と Emacs の両方を常用する人は、それぞれ異なる用途に使う傾向があり、両方を
知っていることに価値を見出す。

一般的に、`vi` はちょっとした作業（短いメール、システム設定の微調整など）に最適
である。特に、新しいシステムや遠隔システムを使っていて、Emacs の自作ファイルが手
元にない場合に便利だ。

Emacs が本領を発揮するのは、複雑な仕事を処理したり、ファイルを複数修正したり、編
集途中で他のプログラムの出力を使用したりしなければならない長時間セッションだ。

コンソールで X を使うプログラマーにとって、ログイン後すぐに大きなウィンドウで
Emacs を起動し、そのまま終了させないようにしておくのは普通のことだ。おそらく何十
ものファイルにアクセスし、複数の Emacs 子ウィンドウでプログラムを実行することす
らあり得る。

## Special-Purpose Code Generators

様々な特化用途に対して特別に設計されたコードを生成するツールが宿るという、長年に
わたる伝統が Unix にはある。

この伝統の由緒ある祈念碑は Version 7 以前まで遡り、1970 年代に原版の Portable C
Compiler を書くために実際に使われたものであり、lex(1) と yacc(1) だ。現代の後継
は flex(1) と bison(1) であり、GNU ツールキットの一部であり、現在でも多用されて
いる。

### `yacc` and `lex`

> `yacc` and `lex` are tools for generating language parsers.

解析器生成器は偶発的で場当たり的な実装よりもましなことをするための道具だ。解析器
生成器は文法仕様をより高い水準で表現できるようにするだけでなく、解析器の実装の複
雑さをコードのそれ以外の部分から遮断する。

ゼロから小規模言語を実装しようと考えているのであれば、おそらく `yacc` と `lex`
が C コンパイラーの次に重要な用具だろう。

それぞれの解析器は一つの関数コードを生成する：

* `lex`: 入力ストリームからトークンを取得する
* `yacc`: トークンの連なりが文法に合致するかどうかを解析する

`yacc` が生成する解析関数は通常、別のトークンを取得するたびに `lex` が生成する
トークン抽出関数を呼び出す。もし `yacc` が生成した解析関数に使用者が書いた C の
コールバックが全くなければ構文検査を行う。返り値は入力が期待した文法に合致してい
るかどうかを表す。

大半の場合、生成された解析器に組み込まれた使用者 C コードが、入力を解析する副次
的な効果として実行時データ構造をいくつか生成する。

小規模言語が宣言的であれば、アプリケーションはこれらの実行時データ構造を直接使用
することができる。もし使用者の設計が命令型小規模言語であれば、データ構造には構文
木が含まれ、すぐに何らかの評価関数に渡されることがある。

`yacc` のインターフェイスはかなり醜く、接頭辞 `yy_` を持つ大域的変数だ。これは C
言語の構造体よりも古いことによる。

`yacc` は C よりも古い。最初の実装は C の前身である B で書かれた。

`yacc` が生成する解析器は、解析エラーからの回復を試みるために、粗雑ではあるが効
果的な算法を用いるが、メモリーリークなどの問題を引き起こす可能性がある。

<!-- Steve Johnson 氏による `yacc` のメモリーリークに対する解説がここにある -->

`lex` は字句解析器を生成する。grep(1) や awk(1) と同じ機能群に属しますが、合致す
るたびに任意の C コードを実行できるため強力だ。宣言的小規模を言語を入力とし、ス
ケルトン C コードを出力する。

`lex` が生成する字句解析器の仕事とは、雑に言えば逆 grep(1) のようなものだ：

* grep(1) は正規表現を受け取り、入力されるデータストリームに合致する一覧を返す。
* 字句解析器の呼び出しそれぞれは正規表現の一覧を受け取り、データストリームでどの
  表現が次に出現するかを示す。

<!-- Henry Spencer 氏の解説がここに来る -->

> `lex` was written to automate the task of generating lexical analyzers
> (tokenizers) for compilers. It turned out to have a surprisingly wide range of
> uses for other kinds of pattern recognition, and has since been described as
> “the Swiss-army knife of Unix programming”.

最も重要なのは、`lex` 仕様の小規模言語は、同等の手作り C 言語よりもはるかに高水
準でコンパクトであるということだ。オープンソース版である `flex` を Perl で使用す
るためのモジュールが用意されており、Python の PLY にも同様の実装が含まれている。

> `lex` generates parsers that are up to an order of magnitude slower than
> hand-coded parsers. This is not a good reason to hand-code, however

`yacc` は解析器を生成する。これもコンパイラーを書く作業の一部を自動化するために
書かれた。BNF に似た宣言型小規模言語で文法仕様を入力とし、文法の各要素に C コー
ドを関連付ける。呼び出されると、入力ストリームから文法に合致したテキストを受け取
る解析関数のコードを生成する。各文法要素が認識されると、解析関数は関連する C
コードを実行する。

Unix プログラマーの大半は汎用コンパイラーを書くことはないが、実行制御ファイル構
文や応用領域固有の小規模言語の解析器を書くにはとても便利だ。

`lex` と `yacc` はそれぞれの得意なものと不得意なものが反対であるような性質がある。

C 言語よりも高水準の言語で解析器を実装できるのであれば、次のパッケージのような同
等の機能を探せ：

* Python: PLY
* Perl: PY と Parse::Yapp
* Jav: CUP, Jack, YACC/M

マクロ処理器と同様に、コード生成器と前処理器の問題の一つは、生成コードのコンパイ
ル時エラーが、修正する必要がある場所ではなく、生成されたコード（手で編集したくな
い場所）に対する相対的な行番号を持つ場合があることだ。

* `yacc` と `lex` は `#line` 指令を生成することでこの問題に対処している。

> More generally, well-designed procedural-code generators should never require
> the user to hand-alter or even look at the generated parts. Getting those
> right is the code generator's job.

#### Case Study: The `fetchmailrc` Grammar

`fetchmail` の `run-control-file` 解析器の文法は `lex` と `yacc` の使い方の良い
中規模事例研究を与えてくれる。いくつか興味深い点がある。

ファイル `rcfile_l.l` の `lex` 指定はシェルのような構文の典型的な実装だ。二つの
補完規則が単一引用符または二重引用符の文字列を支援していることに注意。符号付き整
数リテラルを受け入れ、コメントを破棄する規則もかなり一般的だ。

ファイル `rcfile_y.y` にある `yacc` 指定は長いが簡単だ。Fetchmail の動作は何も行
わず、内部制御ブロックの一覧のビットをただ設定する。起動後、Fetchmail の通常の動
作モードは、遠隔サイトとの検索セッションを駆動するために各レコードを使用して、そ
の一覧を繰り返し歩くだけだ。

### Case Study: Glade

Glade ([Chapter 8]) はアプリケーションコード生成器の現代的な良い例だ。Glade を
Unix 的なものにしているのは次の機能だ：

* Glade GUI と Glade コード生成器は、単一の巨大一枚岩として接着されるのではな
  く、分離の規則、Separated Engine and Interface 設計パターンの法則に従う。
* GUI とコード生成器は、XML ベースのテキストデータファイル形式で連結しており、他
  のツールで読み込んで変更することが可能。
* 複数の対象言語を援助している。もっと増やすことも簡単だ。

この設計は Glade GUI 編集部品を置き換えることも可能であることを示唆している。

## `make`: Automating Your Recipes

プログラムソースはそれだけではアプリケーションにはならない。それをどのようにまと
め、パッケージの形にするかも重要だ。Unix ではこれらの工程を半自動化するツール
make(1) が使用可能だ。

* GNU `make` を支持する Unix のほとんどは GNU Emacs も支持する。
* GNU `make` の DOS と Windows への移植版は FSF から入手可能。

### Basic Theory of `make`

プロジェクト内のファイル間の依存関係は一つ以上のファイル `Makefile` に記述されて
いる。各 `Makefile` は一連の「製造」で構成され、それぞれプログラム `make`に、あ
る目標ファイルがあるソースファイルの集合に依存していることを伝え、ソースのどれか
が目標より新しい場合にする処理を記述する。

プログラム `make` はファイル名や拡張子から明らかな依存関係の多くを推測できるの
で、実際にすべての依存関係を書き出す必要はない。例えば、ファイル `myprog` がファ
イル `myprog.o`, `helper.o`, `stuff.o` に依存していることを `Makefile` に記述す
るとする。もしソースファイル `myprog.c`, `helper.c`, `stuff.c` があれば、`make`
はそれぞれの `.o` ファイルが対応する `.c`ファイルに依存していることを言われなく
ても知っており、`.c` ファイルから `.o`ファイルをビルドするための独自の標準処方箋
を使える。

Stuart Feldman 氏による `make` 誕生秘話があるので読んでおく。

非常に複雑な `Makefile` は、特に補助的な `Makefile` を呼び出す場合、ビルド工程を
単純化するどころか、むしろ複雑化の原因になりかねない。

*Recursive Make Considered Harmful* (1997) が警告していた。この論文の議論は広く
受け入れられるようになり、以前の慣習を覆すところまで来ている。

!!! note

    この論文は Google 検索などですぐに見つかるようだ。

`Makefile` と言えば行頭タブが使いにくいという印象があるが、これは設計ミスだそう
だ。Stuart Feldman 氏本人によると、`lex`/`yacc` に不慣れだったため、何かを単純に
するためにタブ文字を採用したそうだ。人気がすぐに出て、もう直せなくなった。

### `make` in Non-C/C++ Development

[Chapter 14] で説明したようなスクリプト言語は従来のコンパイルやリンクの手順は不
要かもしれないが、make(1) が手助けしてくれる依存関係がしばしば存在する。

例えば、[Chapter 9] の技法の一つを使って仕様ファイルからコードの一部を実際に生成
したとしよう。`make` を使って、仕様ファイルと生成されたソースを結びつけることが
できる。こうすることで、仕様を変更して作り直すたびに、生成されるコードも自動的に
作り直されるようになる。

`Makefile` を使って文書を作成する処方箋を表現することはよくある。この手法はマー
クアップ言語で書かれたマスターから、PostScript やその他の派生文書を自動的に生成
するのによく用いる。

#### Case Study: `make` for Document-File Translation

実際の `Makefile` を見ると理解が話が早い。[fetchmail] から見つけてきたファイルの
一部を抜粋する：

```makefile
FAQ: fetchmail-FAQ.html $(srcdir)/dist-tools/html2txt
	AWK=$(AWK) $(SHELL) $(srcdir)/dist-tools/html2txt $(srcdir)/fetchmail-FAQ.html >$@

FEATURES: fetchmail-features.html $(srcdir)/dist-tools/html2txt
	AWK=$(AWK) $(SHELL) $(srcdir)/dist-tools/html2txt $(srcdir)/fetchmail-features.html >$@

NOTES: design-notes.html esrs-design-notes.html $(srcdir)/dist-tools/html2txt
	   echo "This file contains two articles reformatted from HTML." > $@ \
	&& echo "------------------------------------------------------" >> $@ \
	&& echo "" >> $@ \
	&& AWK=$(AWK) $(SHELL) $(srcdir)/dist-tools/html2txt $(srcdir)/design-notes.html >>$@ \
	&& AWK=$(AWK) $(SHELL) $(srcdir)/dist-tools/html2txt $(srcdir)/esrs-design-notes.html >>$@
```

いずれもソースが HTML ファイルで、目標がプレーンテキストファイルだ。本文では
`lynx -dump` でテキストを得るとあるが、リポジトリーにある版では専用スクリプトを
用いるように改良したようだ。

### Utility Productions

一般的な `Makefile` で最も多用される目標のいくつかは、ファイル依存性をまったく表
現していない。 配布パッケージを作ったり、ゼロからビルドするためにオブジェクト
ファイルをすべて削除したりといった、開発者が機械化したい手順を束ねるためのもの
だ。

`all`
:  プロジェクトのすべての実行可能ファイルを作成する必要がある。通常、明示的な規
   則を持たない。一般的には、これは `Makefile` の最初の規則であるべきで、開発者
   が引数なしで`make` を走らせると実行する。

`test`
:  プログラムの自動化されたテストスイートを実行する。通常、単体試験の集合で構成
   され、開発過程において後退や不具合、その他の期待される動作からの逸脱を発見す
   る。

   `test` はソフトウェア最終使用者が、インストールが正しく機能していることを確認
   するために使用することもできる。

`clean`
:  `all` を作成する際に通常作成されるファイルをすべて削除する。
   `make clean` はソフトウェアをビルドする工程を初期状態に直すはずだ。

`dist`
:  ソースアーカイブを tar(1) などを用いて作成する。このアーカイブは単品で出荷す
   ることができ、別の計算機でプログラムをリビルドするために使用することができ
   る。この目標は配布用アーカイブを作成する前に、`make dist` がプロジェクト全体
   をリビルドするように、`all` に依存するのと同等のことを行うはずだ。

`distclean`
:  ソースを `make dist` でまとめる場合に含めるもの以外をすべて捨てる。

`realclean`
:  `Makefile` を使ってリビルドできるものをすべて捨てる。

`install`
:  プロジェクトの実行ファイルと文書をシステムディレクトリーにインストールし、一
   般使用者がアクセスできるようにする（通常 root 権限が必要）。実行ファイルが機
   能するために必要なデータベースやライブラリーを初期化または更新する。

`uninstall`
:  `make install` によってシステムディレクトリーにインストールされたファイルを削
   除する（通常 root 権限が必要）。これにより `make install` を完全に取り消すこ
   とができる。

これらの標準的な目標を使用する利点の一つは、プロジェクトの暗黙のロードマップを形
成することだ。

目標を上記のものに限定する必要はない。ひとたび `make` を習得すれば、プロジェクト
ファイルの状態に依存するちょっとした作業を自動化するために、`Makefile` という機
械を使うことがますます多くなるだろう。`Makefile` はこれらを置くのに便利な中心的
な場所だ。

### Generating Makefiles

### Version-Control Systems

### Why Version Control?

### Version Control by Hand

### Automated Version Control

### Unix Tools for Version Control

## Runtime Debugging

## Profiling

### Combining Tools with Emacs

### Emacs and `make`

### Emacs and Runtime Debugging

### Emacs and Version Control

### Emacs and Profiling

### Like an IDE, Only Better

[Chapter 8]: <../design/minilanguages.md>
[Chapter 9]: <../design/generation.md>
[Chapter 13]: <../design/complexity.md>
[Chapter 14]: <./languages.md>
[fetchmail]: <https://gitlab.com/fetchmail/fetchmail>
[XEmacs]: <https://www.xemacs.org/>
