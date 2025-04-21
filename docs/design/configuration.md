# Chapter 10. Configuration

[TOC]

Unix ではプログラムは豊富な方法で環境と通信することができる。これらを起動環境ク
エリーと対話型チャンネルに分けるのが便利だ。この章では、起動環境クエリーに主に焦
点を当てる。

## What Should Be Configurable?

質問を逆にして、どのようなことが構成可能であってはならないのかと問う方が、おそら
くより有益だろう。Unix の実践はこのガイドラインをいくつか示している。

1. 自動検出可能なものに構成項目を用意するな
2. 最適化項目を備えるな
3. スクリプトラッパーやつまらぬパイプラインでできることを構成項目として設けるな

> A good rule of thumb is this: Be adaptive unless doing so costs you 0.7
> seconds or more of latency.

人間は 0.7 秒よりも短い待ち時間にはほとんど気づかない。だから柔軟に構えろと。

最適化オプションが使用者に与えるかもしれないわずかな性能の向上は、通常、インター
フェイスの複雑さに見合う経費ではない。オプションが多い構成ファイル形態は KISS の
教えに反する。

他のプログラムに仕事を手伝ってもらうことが簡単にできるのに、自分のプログラムの中
に複雑さを持ち込むな（以前のページャーの議論を思い出せ）。

項目の追加を考えているときに考慮する一般的な質問：

* この機能を省いてもいいのか
* この項目が不要になるような無害な方法でプログラムの通常の動作を変更できるか
* この項目は単なる化粧品か
* この項目で有効になる動作を別のプログラムにできないか

不必要な選択肢を増やすことは多くの弊害をもたらす。その中でも test coverage に与
える影響は深刻だ。

(Steve Johnson) よほど注意深く行わない限り、on/off 型項目を追加するとテストの量
が倍になることがある。項目が十個もあればテストは 1024 倍になる。

## Where Configurations Live

古典的には、Unix プログラムは起動時の環境の五つの場所で制御情報を探す：

1. `/etc` の下にある実行制御 (rc) ファイル
2. システムが設定した環境変数
3. 使用者の `HOME` にある実行制御（ドット）ファイル ([Chapter 3])
4. 使用者が設定した環境変数
5. プログラムを起動したコマンドラインでプログラムに渡されるオプションと引数。

これらの照会は通常、上記の順序で行われる。後の（よりローカルな）設定が前の（より
グローバルな）設定を上書きする。先に発見された設定は、後に構成ファイルデータを検
索する際に、プログラムが場所を計算するのに役立つ。

構成項目をプログラムに渡すためにどの仕組みを使うかを決めるとき、Unix の習慣で
は、プリファレンスの予想される寿命に最も近いものを使うことが要求される。つまり、

* 起動ごとに変更される可能性が高い環境設定はコマンドラインで指定する。
* めったに変更されないが、各使用者が掌握するべき環境設定には、使用者の `HOME` に
  ある構成ファイルで指定する。
* システム管理者がサイト全体に設定し、使用者が変更できないようにする必要がある環
  境設定情報にはシステム領域にある実行制御ファイルで指定する。

!!! note
    ソフトウェアを自作するときにはこの流れで構成するライブラリーを組み込め。

## Run-Control Files

「実行制御ファイル」を定義する：

> A run-control file is a file of declarations or commands associated with a
> program that it interprets on startup.

全使用者が共有する固有の構成がある場合、`/etc` の下に実行制御ファイルを持つこと
が多い。そのようなデータを集積する `/etc/conf` サブディレクトリーがある Unix も
ある。

使用者固有の構成情報は、多くの場合、使用者の `HOME` にある隠し実行制御ファイルに
格納されている。このようなファイルは、「ドットファイル」と呼ばれることが多いが、
ドットで始まるファイル名は通常、`ls` などからは見えないという Unix の慣例を悪用
していることによる。

!!! note
    現代なら XDG Base Directory 仕様というものがある。

プログラムは実行制御ディレクトリーやドットディレクトリーを持つこともある。これら
は、プログラムに関連するが、別々に扱うのが便利な複数の構成ファイルをまとめたたも
のだ。

どちらの形式でも、実行制御情報のある場所はそれを読み込む実行形式ファイルと同じ
basename を持つというのが現在の慣例だ。

例：プログラム `seekstuff` に関しては関連パスは次のようになっているだろう：

* `/etc/seekstuff`
* 使用者の `${HOME}/.seekstuff`

実行制御ファイルは通常、プログラム起動時に一度だけ読み込まれ、書き込まれることは
ない。相互運用性と透明性の両方が、人間が読み、普通のテキストエディターで変更でき
るように設計されたテキスト形式を推し進める ([Chapter 5])。

実行制御ファイルの内容の意味はともかく、構文については、広く守られている設計規則
がある。

プログラムがある言語のインタプリターである場合、起動時に実行される、その言語の構
文によるコマンドの単なるファイルであることが期待される。Unix の伝統は、あらゆる
種類のプログラムを特殊目的言語や小規模言語として設計することを強く推奨しているの
でこれは重要だ。この種のドットファイルを使ったよく知られた例：

* Unix コマンドシェル各種
* Emacs

実行制御構文に関する通常の流儀：

1. コメントを援助する。記号 `#` で始めるものとする。構文は `#` の前の空白も無視
   するようにし、構成内容と同じ行にあるコメントを援助する。
2. 陰湿な空白の区別をしない。つまり、空白やタブの連続を、構文的には単一の空白と
   同じように扱う。書式が行指向であれば行末の空白やタブを無視すると良い。
3. 複数の空白行やコメント行を単一の空白行として扱う。
4. ファイルを、空白で区切られた単純なトークンの列または行として単語の集まりのよ
   うに扱う。
5. しかし、空白が埋め込まれたトークンのための文字列構文をサポートする。
6. バックスラッシュ構文を援助する。標準的なパターンは C コンパイラーが援助してい
   るバックスラッシュエスケープ構文だ。

<!-- insidious: (of something unpleasant or dangerous) gradually and secretly causing harm -->

他方で、シェル構文のいくつかの点は rc 構文で模倣しないほうがいい：

* 引用符と括弧のひどく凝った規則
* ワイルドカードと変数置換のための特殊なメタキャラクター

> It bears repeating that the point of these conventions is to reduce the amount
> of novelty that users have to cope with when they read and edit the
> run-control file for a program they have never seen before.

これらの標準流儀はトークン化とコメントに関する規則のみを記述している。実行制御
ファイルの名前、その上位レベルの構文、および構文の意味的解釈は、通常アプリケー
ション固有のものだ。

> Sharing run-control file formats in this way reduces the amount of novelty
> users have to cope with.

ファイル `.netrc` は使用者のホストとパスワードを追跡しなければならないインター
ネットクライアントプログラムが共有するものと考えられる。このドットファイルが存在
すれば、通常、これから情報を取得することができる。

### Case Study: The .netrc File

ファイル `.netrc` は標準的な規則が機能している良い例だ。

<!-- Example 10.1. A .netrc example. -->

このファイルを見たことがなくても、目で見て簡単に解析できることに注意。
`machine`/`login`/`password` の三組の集合で、それぞれが遠隔ホストのアカウントを
記述している。このような透明性は重要だ。

> It economizes the far more valuable resource that is *human* time, by making
> it likely that a human being will be able to read and modify the format
> without having to read a manual or use a tool less familiar than a plain old
> text editor.

このファイルが複数のサービスの情報を与えるために使用されるということは、機密性の
高い情報を一箇所に保存するだけでよいという利点があるということだ。

このファイルはオリジナルの Unix FTP クライアントプログラムのために設計された。
GNU のサイトにヘルプを発見したのでリンクを記しておく：
[The .netrc file (GNU Inetutils)](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html)

すべての FTP クライアントで使用され、いくつかの `telnet` クライアントや
smbclient(1) コマンドラインツール、`fetchmail` でも理解される。

遠隔ログインでパスワード認証が必要なインターネットクライアントを書いている場合、
驚き最小の法則から `.netrc` の内容を既定として使用することが求められる。

### Portability to Other Operating Systems

ほとんどの非 Unix OS に欠けている重要な点：

* 真の複数使用者機能
* 使用者別ホームディレクトリー概念

例えば、DOS と ME までの Windows にはそのような概念がまったくない。古い話だが。

> Windows NT has some notion of per-user home directories (which made its way
> into Windows 2000 and XP), but it is only poorly supported by the system
> tools.

現代では Windows 11 まで登場したが、文脈からこれも NT に含まれると解釈するべきだ
ろう。

## Environment Variables

### System Environment Variables

### User Environment Variables

### When to Use Environment Variables

### Portability to Other Operating Systems

## Command-Line Options

### The -a to -z of Command-Line Options

### Portability to Other Operating Systems

## How to Choose among the Methods

### Case Study: fetchmail

### Case Study: The XFree86 Server

## On Breaking These Rules

[Chapter 3]: <../context/contrasts.md)>
[Chapter 5]: <../design/textuality.md>
