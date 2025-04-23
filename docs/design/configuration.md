# Chapter 10. Configuration

[TOC]

Unix ではプログラムは豊富な方法で環境と通信することができる。これらを起動環境照
会と対話型情報経路に分けるのが便利だ。この章では、起動環境照会に主に焦点を当てる。

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

### Case Study: The `.netrc` File

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

プログラムが起動すると、それにアクセス可能な環境は名前と値の対応を含む（名前と値
は両方とも文字列）。これらのうちいくつかは使用者が手動で設定するもので、その他は
ログイン時にシステムが設定したり、シェルや端末エミュレーターが設定したりする。

端末で `set` を実行すると現在定義されているシェル変数のすべてが示される。

!!! note
    Bash 内蔵 `set` の他、プログラムなら `env` や `printenv` も使う。

* C/C++ ではライブラリー関数 getenv(3) で環境変数の値を問い合わせることができる。
* Perl と Python は起動時に環境辞書オブジェクトを初期化する。
* 他の言語はこれら二つのモデルのどちらかに従うのが一般的だ。

!!! note
    `man 3 getenv` を確認したら、この関数とその亜種は文字列を戻り値で得るシグニチャーになっている。
    C 言語では珍しいような気がする。

    Python ならば `os.environ` が環境変数辞書オブジェクトだ。

### System Environment Variables

シェルから起動するプログラムには、それらが定義されていると期待して良い、よく知ら
れた環境変数がいくつかある。これらは、ローカルのドットファイルを読み込む**前に**
評価する必要があることが多い。代表的な環境変数：

`USER`, `LOGNAME`
:   (BSD, System V) このセッションに対するアカウントのログイン名

`HOME`
:   このセッションを実行している使用者のホームディレクトリー

`COLUMN`
:   端末ウィンドウ一行に何文字あるか

`LINES`
:   端末ウィンドウ一画面に何行あるか

`SHELL`
:   使用者のコマンドシェルの名前 (e.g. `/bin/bash`)

`PATH`
:   シェルが実行可能コマンドを探すときに検索するディレクトリーの集合

`TERM`
:   セッションコンソールまたは端末ウィンドウの端末型名 (e.g. `xterm-256color`)

    > `TERM` is special in that programs to create remote sessions over the network
    > (such as telnet and ssh) are expected to pass it through and set it in the
    > remote session.

これらのシステム環境変数の一部または全部は、シェル生成以外の方法でプログラムを起
動したときには設定されない場合があることに注意が要る。特に、TCP/IP ソケット上の
デーモンリスナーには、これらの変数が設定されていないことが多い。

環境変数が複数のフィールドを含む必要がある場合、特にそのフィールドが何らかの検索
パスとして解釈できる場合、区切り文字としてコロンを使う伝統があることに注意

* 変数 `PATH` はその代表だ。
* Bash や Korn Shell など、シェルによっては環境変数内のコロンで区切られたフィー
  ルドをファイル名として常に解釈するものがある。特に `~` は上記 `HOME` に置き換
  わる。

### User Environment Variables

環境変数は文字列でしかないなので、使用者定義の環境変数が役に立つ設計パターンは限
定的だ：

> *Application-independent preferences that need to be shared by a large number
> of different programs*

`VISUAL`, `EDITOR`
:   優先エディタープログラム（前者のほうがより preferred と考えられる）

`MAILER`
:   優先メールクライアント

`PAGER`
:   優先プレインテキスト閲覧プログラム (e.g. `/bin/less`)

`BROWSER`
:   優先 Web ブラウザー (e.g. `/usr/bin/wslview`)

!!! note
    `MAILER` を用いるアプリケーションを調べたが不明。

### When to Use Environment Variables

* 実行制御ファイル項目と違って、環境変数はアプリケーション別に複製する機会がない。
* 通常、環境変数はシェルセッションの起動ファイルで値を設定する。

一般に、使用者定義の環境変数は、ドットファイルを毎回編集するのが不便になるほど頻
繁に値が変わる場合に、効果的な設計の選択肢となり得る。このような環境変数は通常、
ローカルのドットファイルの後で評価されるべきであり、ファイル設定を上書きすること
が許されるようにしたい。

> Sometimes, user-set environment variables are used as a lightweight substitute
> for expressing a program preference in a run-control file.

上記のパターンは新しいプログラムには適用しない。

> The problem with the older style is that it makes tracking where your
> preference information lives more difficult than it would be if you knew the
> program had a run-control file under your home directory.

環境変数はシェルの rc ファイルのどこにでも設定できる。例えば Bash なら：

* `.profile`
* `.bash_profile`
* `.bashrc`

これらのファイルは雑線としていて壊れやすいので、オプション解析器を持つことによる
コードの間接費が大してないと判断されると、環境変数からドットファイルに環境情報が
移行する傾向がある。

### Portability to Other Operating Systems

環境変数の Unix からの移植性は非常に限られている。例えば Windows には Unix を手
本にした環境変数機能があり、実行形式検索パスを設定するために `PATH` 変数を使用す
るが、Unix シェルプログラマーが当然のように使用する他の変数のほとんどは援助され
ていない。

## Command-Line Options

Unix の伝統ではスクリプトからオプションを指定できるように、コマンドラインスイッ
チを使用してプログラムを制御することが推奨されている。これは、パイプやフィルター
として機能するプログラムでは特に重要だ。

Unix の伝統ではコマンドラインオプションはハイフン一つで始まる一文字だ。後続する
引数を取らないモードフラグオプションは一緒にまとめることができる。したがって：

> if `-a` and `-b` are mode options, `-ab` or `-ba` is also correct and enables
> both.

オプションの引数があれば、その後に続く（オプションで空白で区切られる）。このスタ
イルでは、大文字よりも小文字のオプションが優先される。大文字のオプションを使う場
合は、小文字のオプションの特別な変形にするのがよい。

* 小文字オプション名が好まれるのは Shift キーを押し続けるのに力が必要だから
* 同じような理由で `+` ではなく `-` が使われる

GNU スタイルでは、オプションキーワードの前に二つのハイフンをつける。読みやすいの
で今でも人気がある。

GNU スタイルのオプションは空白を区切らずに一緒にまとめることはできない。オプショ
ンの引数がもしあれば、空白か `=` 一文字で区切ることができる。

GNU スタイルを使用する場合、少なくとも最も一般的なオプションについては、一文字の
等価物を支援するのが良い習慣だ。

X ツールキットスタイルは、紛らわしいことに、ハイフン一つとキーワードオプションを
用いる。古典的な Unix スタイルとも GNU スタイルとも適切な互換性がなく、古い X 規
約との互換性が高いと思われない限り、新しいプログラムではなるべく使用しない。

多くのツールは、標準入力から読み込むようアプリケーションに指示する擬似ファイル名
として、いかなるオプション文字にも関連付けられない、素のハイフン `-` を受け入れ
る。また、二重ハイフン `--` をオプションの解釈を停止する合図として認識し、それに
続くすべての引数を文字通りに扱うことも慣例となっている。

ほとんどの Unix プログラミング言語には、古典的 Unix または GNU スタイルでコマン
ドラインを解析してくれるライブラリーが用意されている。

!!! note
    Python なら標準モジュール `argparse` がその一つだ。

### The `-a` to `-z` of Command-Line Options

時間の経過とともに、よく知られた Unix プログラムで頻繁に使われるオプションは、さ
まざまなフラグが何を意味するのかについて、緩やかな意味標準のようなものを確立して
きた。

* `-a`: all; add, append.  
  特に GNU 式の `--all` がある場合は `-a` の別名でしかない。
  追加の意味にする場合、削除オプション `-d` と対になりがちだ。
* `-b`: buffer, block size (e.g. du(1), df(1), tar(1)); batch (e.g. flex(1)).
* `-c`: command; check.  
  引数ありでコマンドの意味とする。この規約は特にシェルやインタープリターに強く適
  用したい。Cf. `-e`. 例としては sh(1), bash(1), python(1) などがある。
  引数なしで check の意味とする。
  コマンドに対するファイルの引数が正しいかどうかを検めるが、通常の処理は行わない。
  プログラムの構文検査オプションとしてよく使われる。例: getty(1), perl(1) など。
* `-d`: debug.  
  デバッグメッセージのレベルを設定する。
  たまに delete や directory の意味を持つものがある。
* `-D`: define.  
  インタープリター、コンパイラー、特にマクロプロセッサーのようなアプリケーション
  で、あるシンボルの値を設定する。この意味は Unix プログラマーのほとんどが強く連
  想する。
* `-e`: execute, expression (e.g. xterm(1), perl(1), sed(1)); edit (e.g. crontab(1)).  
  編集オプションの場合、エディターを開いて何かのテキストを編集可能にする。
* `-f`: file (e.g. tar(1), awk(1), grep(1)); force (e.g. ssh(1), httpd(1)).  
  引数付きでファイル (`--file`) の意味とする。入力ファイルを指定するために用いら
  れる。
  引数なしでは強制の意味。通常は条件付きで実行される操作を強制的に実行する。これ
  はあまり一般的ではない。
  デーモンはこの二つの意味を合わせた形で `-f` を使用し、既定以外の場所から設定
  ファイルを強制的に処理する。例: , etc.
* `-h`: header (pr(1), ps(1)); help.  
  ヘッダー (`--header`) 行の意味では、プログラムが出力する表のヘッダーを有効化、
  抑制、修正する。
  ヘルプ (`--help`) オプションの意味である場合は、一般的にはそれほど多くない。  
  > for much of Unix's early history developers tended to think of on-line help
  > as memory-footprint overhead they couldn't afford. Instead they wrote manual
  > pages (this shaped the man-page style in ways we'll discuss in [Chapter 18]).
* `-i`: initialize (e.g. ci(1)); interactive (e.g. rm(1), mv(1)).  
  初期化フラグの場合、プログラムに関連する重要な資源やデータベースを初期状態に設
  定する。
  対話的フラグの場合、通常は確認の問い合わせをしないプログラムにそれをさせる。
* `-I`: include.  
  アプリケーションが検索した資源に、ファイル名やディレクトリ名を追加する。ソース
  ファイルのインクルードと同等の機能を持つ Unix コンパイラーはすべて、この意味で
  `-I` を使用する。
* `-k`: keep (e.g. passwd(1), bzip(1), fetchmail(1)); kill.  
  ファイル、メッセージ、各種資源に対する通常の削除を抑止する。
* `-l`: list (e.g. arc(1), binhex(1), unzip(1)); load (e.g. gcc(1), f77(1),
  emacs(1)); login (e.g. rlogin(1), ssh(1)); length; lock.  
  報告プログラムでは `-l` はほとんど必ず long を意味し、既定よりもより詳細に表示
  する。
* `-m`: message (e.g. ci(1), cvs(1)); mail; mode; mtime.  
  メッセージオプションは VCS プログラムのコマンドオプションでありがちだ。
* `-n`: number (e.g. head(1), tail(1), nroff(1), troff(1)); not (make(1)).  
  DNS 名を表示するネットワークツールの中には、代わりに生の IP アドレスを表示する
  オプションとして `-n` を受け付けるものがある。E.g. ifconfig(1), tcpdump(1).
  ちなみに `make -n` は憶えておくと便利だ。現代の CLI ならば `--dry-run` という
  GNU 式オプションの別名であることも多い。
* `-o`: output (e.g. as(1), cc(1), sort(1)).  
  コンパイラー風インターフェイスを持つもので、オプション `-o` が出力ファイルやデ
  バイスの名前を指定する以外の方法で使われるのを見るのは驚くことだ。
  通常の引数の後でも、引数の前でも、出力先を指定、認識できるようなロジックを持っ
  ている CLI は多い。
* `-p`: port (e.g. cvs(1), psql, smbclient(1), snmpd(1), ssh(1)); protocol (e.g.
  fetchmail(1), snmpnetstat(1)).  
  特に TCP/IP ポート番号を指定するオプションに `-p` を用いる。
* `-q`: quiet (e.g. ci(1), co(1), make(1)).  
  正常な結果または診断出力を抑制する。これはとても一般的だ。
* `-r` (also `-R`): recurse (e.g. cp(1), grep(1), ls(1)); reverse (e.g. ls(1),
  sort(1)).
* `-s`: silent (e.g. csplit(1), ex(1), fetchmail(1)); subject (mail(1), elm(1),
  mutt(1)); size.  
  ちなみに quiet `-q` と silent `-s` は通例別物とみなされる。後者のほうが強い。
* `-t`: tag (e.g. cvs(1), ex(1), less(1), vi(1)).  
  検索キーとして使用する場所を指定するか、プログラム用の文字列を指定する。特にテ
  キストエディターやビューワーで用いられる。
* `-u`: user (e.g. crontab(1), emacs(1), fetchmail(1), fuser(1), ps(1)).
* `-v`: verbose (e.g. cvs(1), chattr(1), patch(1), uucp(1)); version (e.g.
  cvs(1), chattr(1), patch(1), uucp(1)).  
  バージョン出力は次の `-V` が普通。
* `-V`: version (e.g. gcc(1), flex(1), hostname(1), etc.)  
  このスイッチがそれ以外の使われ方をするのはかなり驚く。
* `-w`: width (e.g. faces(1), grops(1), od(1), pr(1), shar(1)); warning (e.g.
  fetchmail(1), flex(1), nsgmls(1)).
* `-x`: debug (sh(1), uucp(1)); extract (e.g. tar(1), zip(1)).
* `-y`: yes (e.g. fsck(1), rz(1)).  
  プログラムが通常確認を必要とするような、破壊的な行為を許可する。
* `-z`: compression (e.g. bzip(1), GNU tar(1), zcat(1), zip(1), cvs(1)).

開発するプログラムのコマンドラインオプション文字を選ぶときは、類似のツールのマ
ニュアルページを見本にしろ。類似の機能に対して、先行者と同じオプション文字を使う
ようにしろ。

> Anybody who wrote a mail agent that used `-s` as anything but a Subject
> switch, for example, would have scorn rightly heaped upon the choice.

GNU プロジェクトは GNU コーディング標準のいくつかの `--` オプションについて従来
の意味を推奨している：[GNU coding standards](https://www.gnu.org/prep/standards/)

また、標準化されてはいないものの、多くの GNU プログラムで使われている長いオプ
ションも挙げている。必要なオプションが列挙されたものと似た機能を持っているなら
ば、驚き最小の法則に従って、その名前を再利用しろ。

### Portability to Other Operating Systems

Windows では GUI で隠されており、コマンドラインオプションの使用は推奨されていな
い。

MacOS classic やその他の純粋な GUI 環境には、コマンドラインオプションに相当する
ものがない。

## How to Choose among the Methods

* 実行制御ファイル
* 環境変数
* コマンドラインオプション

行儀の良い Unix プログラムでは、これらの場所を複数使用する場合、指定順に、後の設
定が前の設定を上書きするという強力な慣例がある。

> (there are specific exceptions, such as command-line options that specify
> where a dotfile should be found).

make(1) の `-e`, `--environment-overrides` のように、環境設定や rc ファイルの宣
言を上書きできるコマンドラインオプションを備えるのは良い習慣だ。

これらの場所のどれを見るかは、プログラムが起動の間にどれだけの永続的な設定状態を
保持する必要があるかによって決まる。

* 主にバッチモードで使用するように設計されたプログラム（例：パイプラインの始点や
  フィルター。ls(1), grep(1), sort(1), etc.）は通常、コマンドラインオプションで
  完全に構成される。
* 複雑な対話的動作をする大規模なプログラムは rc ファイルと環境変数に完全に依存
  し、通常の使用ではコマンドラインオプションはほとんど使用しない。X window
  manager のほとんどはこのパターンの良い例だ。

### Case Study: `fetchmail`

Fetchmail が使用する環境変数は `USER` と `HOME` の二つ。これらの変数はシステムが
初期化してある。

`HOME` の値はドットファイル `.fetchmailrc` を見つけるために使う。Fetchmail の構
成はいったん仕込むとまれにしか変更されないので適切だ。

Fetchmail にはシステム全体に対する構成ファイルの概念がない。

> the name of the local postmaster, and a few switches and values describing the
> local mail transport setup (such as the port number of the local SMTP
> listener)

これらをコンパイル時の既定値から変更することはめったにない。変更する場合は使用者
固有の方法で変更されることが多い。そのため、システム rc ファイルに対する需要はな
い。

Fetchmail はファイル `.netrc` からホスト、ログイン名、パスワードの三組を取得する
ことが可能だ。驚き最小の方法で認証情報を得ることが可能だ。

Fetchmail には精巧なコマンドラインオプション集合があり、rc ファイルが表現できる
ことをほぼ再現しているが完全ではない。

> The set was not originally large, but grew over time as new constructs were
> added to the .fetchmailrc minilanguage and parallel command-line options for
> them were added more or less reflexively.

なぜ rc ファイルで可能なことをコマンドラインからも可能であるようにしたかったかと
いうと、使用者がコマンドラインから実行制御の一部を上書きできるようにすることで
`fetchmail` をより簡単に自動化できるようにすることだった。しかし、大半のオプショ
ンにはその需要がないことが後で判明した。むしろ上述のオプション `-f` があれば十分
だった。

そもそも、オプション追加は経費ゼロではない：

> options increase the chances of error in code, particularly due to unforeseen
> interactions among rarely used options. Worse, they bulk up the manual, which
> is a burden on everybody. -- Doug McIlroy

実行制御ファイルの部分を文字列で与えるオプションを実装するという手法もある：

> A more powerful variant of this is what `ssh` does with its `-o` option: the
> argument to `-o` is treated as if it were a line appended to the configuration
> file, with the full config-file syntax available. -- Henry Spencer

### Case Study: The XFree86 Server

念のため：

> The X windowing system is the engine that supports bitmapped displays on Unix
> machines.

X サーバーは人を寄せ付けぬほど複雑なインターフェイスを備えている。さまざまなハー
ドウェアや使用者の好みに対応しなければならないのだ。それゆえ、X(1) と Xserver(1)
のページで文書化されている、すべての X サーバーに共通する環境照会は研究のための
有用な例となる。ここで調べる実装は XFree86 であり、Linux や他のオープンソース
Unix で使われている X の実装だ。

起動時、XFree86 サーバーはシステム全体用 rc ファイル `XF86Config` を調べる。

<!-- 
Example 10.2. X configuration example.

# The 16-color VGA server

Section "Screen"
    Driver      "vga16"
    Device      "Generic VGA"
    Monitor     "LCD Panel 1024x768"
    Subsection  "Display"
        Modes       "640x480" "800x600"
        ViewPort    0 0
    EndSubsection
EndSection
-->

Example 10.2 X configuration example を見ると、ホスト機の `Driver`, `Device`,
`Monitor` といった項目が確認できる。このような情報はマシンの全使用者に適用される
ため、システム全体の実行制御ファイルに記述するのは適切だ。

X は rc ファイルからハードウェア構成を取得すると、環境変数 `HOME` の値を使用し
て呼び出し元の使用者のドットファイル二つを見つける：

* `.Xdefaults`
* `.xinitrc`

> The `.Xdefaults` file specifies per-user, application-specific resources
> relevant to X (trivial examples of these might include font and
> foreground/background colors for a terminal emulator).

「X に関連する」という表現が設計上の問題を示しているという。何が `.Xdefaults` で
宣言されるべきで、何がアプリケーション固有のドットファイルに属するかが、必ずしも
明確ではない。

> The `.xinitrc` file specifies the commands that should be run to initialize
> the user's X desktop just after server startup. These programs will almost
> always include a window or session manager.

X サーバーにある数多くのコマンドラインオプションには、使用する場合、テスト実行の
たびにかなり頻繁に変化する可能性があり、実行制御ファイルに含めるには適していな
い。非常に重要なオプションは、サーバーの表示番号を設定するだ。複数のサーバーが単
一のホスト上で実行される場合、各サーバーは固有の表示番号を持つが、すべてのインス
タンスは同じ rc ファイルを共有する。

## On Breaking These Rules

この章で説明した規約をもし破るのであれば、「修理の規則」に従い、伝統的方法での物
事の試みが音を立てて破れるようにしろ。

[Chapter 3]: <../context/contrasts.md>
[Chapter 5]: <../design/textuality.md>
[Chapter 18]: <../community/documentation.md>
