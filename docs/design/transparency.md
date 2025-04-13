# Chapter 6. Transparency

[TOC]

「透明である」の定義：

> Software systems are transparent when they don't have murky corners or hidden
> depths. Transparency is a passive quality. A program is transparent when it is
> possible to form a simple mental model of its behavior that is actually
> predictive for all or most cases, because you can see through the machinery to
> what is actually going on.

予測可能性と言い換えてもいいかもしれない（社会科学系の知識人が使う語彙にある印象
がある）。

<!-- murky: dark and dirty or difficult to see through -->
<!-- machinery: a group of large machines or the parts of a machine that make it work -->

「発見可能である」の定義：

> Software systems are discoverable when they include features that are designed
> to help you build in your mind a correct mental model of what they do and how
> they work.

発見可能性の意味はわかりやすい：

> So, for example, good documentation helps discoverability to a user. Good
> choice of variable and function names helps discoverability to a programmer.

Unix プログラマーの言う elegant とは、数学者のそれと本質的に同等だ：

> Unix programmers, borrowing from mathematicians, often use the more specific
> term “elegance” for the quality Gelernter speaks of. Elegance is a combination
> of power and simplicity.

* こなれたコードは少しのことで多くのことを行う。
* こなれたコードは単に正しいだけでなく、目に見える形で、透明な形で正しい。
* こなれたコードは透明性と発見可能性がある。

## Studying Cases

<!-- intersperse: to put things of one type in different parts or places among other things -->

### Case Study: audacity

[Audacity] は Unix, Mac OS X, Windows 上で動作するサウンドファイル用のオープン
ソースエディターだ。

> The UI is superbly simple; the sound waveforms are shown in the audacity
> window. The image of the waveform can be cut and pasted; operations on that
> image are directly reflected in the audio sample as soon as they are
> performed.

音声波形がビットマップとして描画されているから、それを画像編集ソフトと同等のコマ
ンドで扱うことで作業する。

<!-- superbly: in a way that is extremely good or impressive -->

«Several features of this UI are subtly excellent and worthy of emulation» であ
り、ツール全体としては次の評価になる：

> The central virtue of this program is that it has a superbly transparent and
> natural user interface, one that erects as few barriers between the user and
> the sound file as possible.

### Case Study: fetchmail's `-v` option

メールプログラム [Fetchmail] には 60 を下らないコマンドラインオプションがある
が、最重要オプションは `-v` であるという。他の CLI でもしばしば見かけられる冗舌
フラグだ。動作は次のとおり：

> When `-v` is on, `fetchmail` dumps each one of its POP, IMAP, and SMTP
> transactions to standard output as they happen. A developer can actually see
> the code doing protocol with remote mailservers and the mail transport program
> it forwards to, in real time.

<!-- Example 6.1. An example fetchmail -v transcript. -->

オプション `-v` は `fetchmail` が行っていることを発見可能にする。ここでは通信規
約交換を見ることができるようにする。著者が自身の具体的な工夫を紹介している：

> This is *immensely* useful. I considered it so important that I wrote special
> code to mask account passwords out of `-v` transaction dumps so that they
> could be passed around and posted without anyone having to remember to edit
> sensitive information out of them.

<!-- immensely: to an exceedingly great extent or degree; extremely -->

デバッグライトから引き出される一般的な教訓：

> Don't let your debugging tools be mere afterthoughts or treat them as
> throwaways. They are your windows into the code; don't just knock crude holes
> in the walls, finish and glaze them.

<!-- throwaways: 使い捨て -->
<!-- crude: simple and not skilfully done or mad -->
<!-- glaze: 光沢を付ける -->

### Case Study: GCC

本書は C 言語に対する言及が多い。そのコンパイラーにも当然言及する。

> GCC is organized as a sequence of processing stages knit together by a driver
> program. The stages are: preprocessor, parser, code generator, assembler, and
> linker.

このうち、最初の三段階すべてが入出力のどちらもテキスト形式であることに注目する。

> With various command-line options of the gcc(1) driver, you can see not just
> the results after C preprocessing, after assembly generation, and after object
> code generation — but you can also monitor the results of many intermediate
> steps in parsing and code generation.

回帰テストは、ソフトウェアが変更される際に発生するバグを検出するためのテストだ。
ある固定されたテスト入力に対して、変更されたソフトウェアの出力を、既知の正しい出
力のスナップショットに対して継続的に検査するものだ。

中間形態がテキスト形式であるため、回帰テスト出力の差分を取れば発見、分析が容易だ。

> The design pattern to extract from this example is that the driver program has
> monitoring switches that merely (but sufficiently) expose the textual data
> flows among the components.

設計意図としては `fetchmail` のオプション `-v` と同じく、発見可能性を高めることだ。

### Case Study: kmail

[KMail] は KDE における GUI メールクライアントだ。Mozilla Thunderbird のようなも
のを想像すればいい。

ステータスバーのセンスが良い。よくある統計表示の他に、交信に関するメッセージも表
示する：

> If you watch closely during the send, you will observe that each line of the
> SMTP transaction with the remote mail transport is echoed into the *kmail*
> status bar as it happens.

視覚的には無視しやすいという設計にしてあるのが急所で、一般人も専門家も困らせな
い。

> The really smart thing is to find a way to leave the details accessible, but
> make them unobtrusive.

<!-- unobtrusive: not noticeable; 目立たない -->

### Case Study: SNG

> The program `sng` translates between PNG format and an all-text representation
> of it (SNG or Scriptable Network Graphics format) that can be examined and
> modified with an ordinary text editor. Run on a PNG file, it produces an SNG
> file; run on an SNG file, it recovers the equivalent PNG. The transformation
> is 100% faithful and lossless in both directions.

ビットマップはテキスト的に表現することが可能であるはずとは思っていたが、こういう
ツールがやはり存在していた。

Example 6.2. An SNG Example はおそらく手動で作成したテキストだろう。

* PNG のバイナリーデータを編集するために特別なコードを必要としなくて済む。単に画
  像をテキスト表現に変換し、それを編集して元に戻せばいい。
* バージョン管理システムでは、テキストファイルはバイナリーブロブよりもはるかに管
  理しやすく、SNG 差分が有用であることがある。

PNG 内容全体に発見可能性を与えることで、より大規模なプログラムシステムの透過性を
促進する。

### Case Study: The Terminfo Database

> Terminfo entries live in a directory hierarchy, usually on modern Unixes under
> `/usr/share/terminfo`. Consult the terminfo(5) man page to find the location
> on your system.

実際に `ls /usr/share/terminfo` の出力を見ると、大量の一文字サブディレクトリーが
確認できた。さらに `ls /usr/share/terminfo/*` を実行すると……。

> Under each of these are the entries for each terminal type that has a name
> beginning with that letter. The goal of this organization was to avoid having
> to do a linear search of a very large directory;

Git のインデックスと同じ狙いだろう。

> Terminfo uses the file system itself as a simple hierarchical database. This
> is a superb bit of constructive laziness, obeying the Rule of Economy and the
> Rule of Transparency.

この編成のもうひとつの利点は、Unix のファイルシステム権限機構を使うことができる
ことだ。

対照的な例として Windows のレジストリーファイルを挙げている。

* Windows 本体とアプリケーションの両方が使用する
* 各レジストリーは単一の巨大なファイルに格納されている
* レジストリーを編集するには専用ツールが必要
* レジストリー項目を追加すればするほど平均アクセス時間が増加する
* レジストリーを編集するための標準 API がシステムから与えられていない

過去に邦訳版を読んだときにこの記述があったことははっきりと記憶している。

### Case Study: Freeciv Data Files

[Freeciv] はビデオゲームだそうだが、全然聞いたことがないので紹介文を丸々引用して
おく：

> Freeciv is an open-source strategy game inspired by Sid Meier's classic
> Civilization II. In it, each player begins with a wandering band of neolithic
> nomads and builds a civilization. Player civilizations may explore and
> colonize the world, fight wars, engage in trade, and research technological
> advances. Some players may actually be artificial intelligences; solitaire
> play against these can be challenging. One wins either by conquering the world
> or by being the first player to reach a technology level sufficient to get a
> starship to Alpha Centauri.

このゲームプログラムはデータファイルの取り扱いが優れているという。

* テキスト形式で記述する
* 文字列をゲームサーバー内の重要データの内部リストに組み立てる
* `include` ディレクティブがあり、設定ファイルの分割が可能（個別編集可能性）

ゲームエンジンのコードに触れることなく、データファイルの中で新しい宣言を作成する
だけで、国家や単位型を定義することができる。

ゲーム側が未知のプロパティー名を無視するという性質がある。これは一長一短がある：

* 起動中のデータファイル解析を中断することなく、プロパティーを宣言することができ
  る。これはゲームデータとゲームエンジンの開発をきれいに分離できることを意味する。
* 同時に、プロパティー名の誤字を検出できないことも意味する。

Freeciv データファイルの集合体を考えると、機能的には Windows のレジストリーに似
ている。しかし、どのプログラムもこれらのファイルに書き込みをしないため、Windows
レジストリーで指摘した不快な問題が突然持ち上がることはない。

## Designing for Transparency and Discoverability

透明性と発見容易性を設計するためには、コードを単純に保つためのあらゆる戦術を適用
する必要がある。この設計は機能するだろうかと考えた後に、次も自問する：

* 他の人が読めるか
* こなれているか

### The Zen of Transparency

> If you want transparent code, the most effective route is simply not to layer
> too much abstraction over what you are manipulating with the code.

プログラミング理論本は行き過ぎた抽象化を戒めることが多い。行き過ぎていない抽象化
が望ましい。

> Too many OO designs are spaghetti-like tangles of is-a and has-a
> relationships, or feature thick layers of glue in which many of the objects
> seem to exist simply to hold places in a steep-sided pyramid of abstractions.
> Such designs are the opposite of transparent; they are (notoriously) opaque
> and difficult to debug.

Unix プログラマーのやり方はこうだ。低く構える：

> Keeping glue layers thin is part of it; more generally, our tradition teaches
> us to build lower, hugging the ground with algorithms and structures that are
> designed to be simple and transparent.

### Coding for Transparency and Discoverability

> Transparency and discoverability, like modularity, are primarily properties of
> designs, not code.

* コールスタックが深くなり過ぎないか。
* コードに強力で目に見える不変性があるか。
* API の関数呼び出しは個別に直交しているか（一つの関数が多過ぎる引数によってさま
  ざまな挙動を呈してはいないか）。
* システムの高水準状態を把握するために、目立つデータ構造がひとつまみあるのか、単
  一の大域的特典掲示板があるのか。
* プログラム内のデータ構造やクラスと、それらが表現する実世界の実体との間に、きれ
  いな一対一の写像があるか。
* ある機能を担当しているコードを見つけるのが簡単か。
* マジックナンバー（説明のつかない定数）があるか。

> It's best for code to be simple.

[第四章](./modularity.md)のチェックリストと比較するといい。

### Transparency and Avoiding Overprotectiveness

隠すこととアクセスできないようにすることには重要な違いがある。

何をしているのか明らかにできないプログラムは、トラブルシューティングをはるかに困
難にする。

> Thus, experienced Unix users actually take the presence of debugging and
> instrumentation switches as a good sign, （中略） presence suggests one with
> enough wisdom to follow the Rule of Transparency.

GUI アプリケーションでは過剰防衛傾向がさらに強い。Unix 開発者が GUI に対して冷淡
である理由の一つは、設計者が予測した狭い範囲以外で GUI を介して操作しなければな
らない人にとってイラつくほど不透明になる点だ。

何をやっているのか不透明なプログラムは多くの仮定が組み込まれている傾向がある。

> Unix tradition pushes for programs that are flexible for a broader range of
> uses and troubleshooting situations, including the ability to present as much
> state and activity information to the user as the user indicates he is willing
> to handle. This is good for troubleshooting; it is also good for growing
> smarter, more self-reliant users.

<!-- reliant:  needing a particular thing or person in order to continue, to work correctly, or to succeed -->

Unix は使用者も成長する。

### Transparency and Editable Representations

透明性が難しい領域からそれが簡単な領域に問題を反転させるプログラムの価値。

> All three applications turn manipulation of their binary file formats into a
> problem to which human beings can more readily apply intuition and competences
> gained from everyday experience.

可逆的かつ無劣化に変換するという特性はきわめて重要であり、実装する価値がある。

> All the advantages of textual data-file formats that we discussed in Chapter 5
> also apply to the textual formats that sng(1), infocmp(1) and their kin
> generate.

ある種の複雑なバイナリーオブジェクトの編集を伴う設計上の問題に直面した場合、最初
に、編集可能なテキスト形式への逆写像を行うことができるツールを書くことが可能かど
うかを考えるのが良い。

> If the binary object is dynamically generated or very large, then it may not
> be practical or possible to capture all the state with a textualizer. In that
> case, the equivalent task is to write a browser.

これは難しいように聞こえるが、例えば psql(1) のようなものもブラウザーとみなせる。

テキスト化ツールやブラウザーを製作することが価値がある理由は：

* 学習経験を積む
* 検査やデバッグのために構造体の中身をダンプする能力を得る
* 試験負荷や異常な事例を簡単に生成できる
* 再使用可能コードを得る

### Transparency, Fault Diagnosis, and Fault Recovery

透明性は耐バグ性でもある：

> Yet another benefit of transparency, related to ease of debugging, is that
> transparent systems are easier to perform recovery actions on after a bug
> bites — and, often, more resistant to damage from bugs in the first place.

* Windows のレジストリーはバグのあるアプリケーションコードによって破損されやす
  い。これにより、システム全体が使用不能になる可能性がある。そうでなくても、レジ
  ストリーの破損がレジストリー編集ツールを混乱させると、復旧が困難になることがあ
  る。
* 対照的に、terminfo データベースは一枚岩のファイルではないので、項目一つ間違え
  たからといってデータセット全体が使用不能になるけではない。一枚岩であっても、
  termcap のような完全にテキスト化されている形式は、通常、単一障害点から回復可能
  な手段で解析される。
* SNG ファイルの構文エラーは破損した PNG 画像の読み込みを拒否するような特殊なエ
  ディターを必要とせず、手作業で修正することが可能。

テキスト化ツールやブラウザーなどの発見可能性ツールは故障診断をも容易にする。理由
は：

* テキスト化されたデータは人間がシステムの状態を検査しやすくする。
* 単一障害によって修復不可能なほど破壊されにくくする効果がある。

> Over and over again, the Rule of Robustness is clear. Simplicity plus
> transparency lowers costs, reduces everybody's stress, and frees people to
> concentrate on new problems rather than cleaning up after old mistakes.

## Designing for Maintainability

[Audacity]: <https://www.audacityteam.org/>
[Fetchmail]: <https://www.fetchmail.info/>
[Freeciv]: <https://freeciv.org/>
[KMail]: <https://apps.kde.org/kmail2/>
