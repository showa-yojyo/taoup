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

対照的な例として、Windows のレジストリーファイルを挙げている。

TBD

### Case Study: Freeciv Data Files

## Designing for Transparency and Discoverability

### The Zen of Transparency

### Coding for Transparency and Discoverability

### Transparency and Avoiding Overprotectiveness

### Transparency and Editable Representations

### Transparency, Fault Diagnosis, and Fault Recovery

## Designing for Maintainability

[Audacity]: <https://www.audacityteam.org/>
[Fetchmail]: <https://www.fetchmail.info/>
[KMail]: <https://apps.kde.org/kmail2/>
