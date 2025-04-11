# Chapter 5. Textuality

[TOC]

<!-- ad-hoc: made or happening only for a particular purpose or need, not planned before it happens -->

> Interoperability, transparency, extensibility, and storage or transaction
> economy: these are the important themes in designing file formats and
> application protocols. Interoperability and transparency demand that we focus
> such designs on clean data representations, rather than putting convenience of
> implementation or highest possible performance first. Extensibility also
> favors textual protocols, since binary ones are often harder to extend or
> subset cleanly.

## The Importance of Being Textual

テキストストリームは、特別なツールを使わなくても、人間が簡単に読み書きや編集がで
きる。これらのフォーマットは透過的である（ように設計できる）。

> When you feel the urge to design a complex binary file format, or a complex
> binary application protocol, it is generally wise to lie down until the
> feeling passes.

バイナリー形式はダメだ。性能が心配なら、テキストストリームにアプリケーションプロ
トコルの下か上の階層で圧縮を施せばよいのだから。

> Binary formats usually specify the number of bits allocated to a given value,
> and extending them is difficult.

これは業務で経験がある。整数型として 32 ビットを勝手に想定していた時代のファイル
が 64 ビット時代になってダメになった。ファイルサイズをケチってかえって損をした。

バイナリー形式が本当に向いている場合は限定的だ：

> Formats for large images and multimedia are sometimes an example of the
> former, and network protocols with hard latency requirements sometimes an
> example of the latter.

バイナリー形式は拡張性に乏しいことにも注意。

> When you think you have an extreme case that justifies a binary file format or
> protocol, you need to think very carefully about extensibility and leaving
> room in the design for growth.

### Case Study: Unix Password File Format

ファイル `/etc/passwd` と等価な情報をバイナリー形式ファイルで置き換えるのは先述
の観点からも無理がある。本文ではこのファイルの場合に絞ってここで説明している。

テキスト形式であることの利点は例えば：

* 汎用テキストエディターで読み書き可能
* 汎用ツール (e.g. grep(1)) でテキスト内容を処理可能

CSV 形式を編集するときには、各欄に区切り記号を含めぬように注意しろ。

パスワードファイルはその用途上、バイナリー形式である利点が乏しい：

> Economy is not a major issue with password files to begin with, as they're
> normally read seldom and infrequently modified. Interoperability is not an
> issue, since various data in the file (notably user and group numbers) are not
> portable off the originating machine.

### Case Study: .newsrc Format

ファイル `.newsrc` についての考察。本書 Example 5.2 のコードを観察すると、これも
やはり可変長レコードを含む CSV の亜種だ。したがってバイナリー形式はダメ。

> The designers of the original newsreader chose transparency and
> interoperability over economy. The case for going in the other direction was
> not completely ridiculous; `.newsrc` files can get very large, and one modern
> reader (GNOME's Pan) uses a speed-optimized private format to avoid startup
> lag.

### Case Study: The PNG Graphics File Format

ここでバイナリー形式の例を見る。画像データをバイナリー形式で表現する理由が少なく
とも二つある：

> PNG is an excellent example of a thoughtfully designed binary format. A binary
> format is appropriate since graphics files may contain very large amounts of
> data, such that storage size and Internet download time would go up
> significantly if the pixel data were stored textually. Transaction economy was
> the prime consideration, with transparency sacrificed.

ちなみにここで言う transparency とは本書の意味でいうそれであり、画素の透明性とは
関係ない。PNG はアルファー値を扱う。

PNG 形式はチャンクやヘッダーの造りが良好であると述べる。著者の総評は次のとおり：

> The PNG standard is precise, comprehensive, and well written. It could serve
> as a model for how to write file format standards.

## Data File Metaformats

見出しの意味は術語としては構文と字句の規約のことで、次のどちらかの性質はあるもの
を指す：

* 規約が正式に標準化されている
* 規約がシリアライズ処理のためのライブラリーが標準で存在する程度には十分に確立さ
  れている

> It is good practice to use one of these (rather than an idiosyncratic custom
> format) wherever possible.

CSV, XML, JSON, YAML, TOML は data file metaformats だと言い切れる。

<!-- idiosyncratic: 奇異な、風変わりな -->

> In the following discussion, when we refer to “traditional Unix tools” we are
> intending the combination of grep(1), sed(1), awk(1), tr(1), and cut(1) for
> doing text searches and transformations.

基本的には行単位でテキスト検索・変換をするような CLI という意味に解釈する。

### DSV Style

> DSV stands for _Delimiter-Separated Values_.

ファイル `/etc/passwd` は値の区切り記号にコロンを用いる DSV だ。Unix ではコロン
が DSV の既定の区切り記号だ。

* DSV は表形式のデータに対してよく用いられる (e.g. `/etc/group`, `/etc/inittab`)
* DSV ファイルはバックスラッシュエスケープによってデータ欄に区切り記号を含めるこ
  とを支援することが期待される。

> This format is most appropriate when the data is tabular, keyed by a name (in
> the first field), and records are typically short (less than 80 characters
> long). It works well with traditional Unix tools.> 

* 区切り記号について、昔の慣習ではタブ文字が好まれており、cut(1) や paste(1) の
  既定にその傾向が現れている。
* タブ文字は空白文字と見分けがつきにくいので、好まれなくなっていった。

言われてみると `cut` を使うときはオプション `-d` を必ず指定する。

カンマ区切りの CSV 形式は «rarely found under Unix» だ。

MS Excel などの CSV の扱いがまずい理由を引用する。データ欄にカンマを含むものがあ
る場合に、データ欄全体を二重引用符で括るという対処法に問題があると述べている：

> ... encloses the entire field in double quotes if it contains the separator.
> If the field contains double quotes, it must also be enclosed in double
> quotes, and the individual double quotes in the field must themselves be
> repeated twice to indicate that they don't end the field.

そして次の問題を引き起こす：

* 解析の複雑さ（とバグに対する脆弱性）が増大する
* 書式規則が複雑で十分に規定されていないため、極端な場合の扱いが実装次第になる

### RFC 822 Format

> RFC 822 is the principal Internet RFC describing this format (since superseded
> by RFC 2822). MIME (Multipurpose Internet Media Extension) provides a way to
> embed typed binary data within RFC-822-format messages.

後続のパラグラフで RFC 822 書式の仕様を簡潔に述べている。実例は後で述べるように
容易に入手可能。

この metaformat が適しているデータ構造：

> More generally, it's appropriate for records with a varying set of fields in
> which the hierarchy of data is flat (no recursion or tree structure).

テキスト形式でありながらの弱点を抱える：

> Traditional Unix search tools are still good for attribute searches, though
> finding record boundaries will be a little more work than in a record-per-line
> format.

もう一つ。この書式が単品で使われることがないことから来る弱点がある：

> One weakness of RFC 822 format is that when more than one RFC 822 message or
> record is put in a file, the record boundaries may not be obvious

RFC 822 データがどのようなものであれか実例を見るにはこうする（メール本文は RFC
822 データの一部ではないとみなす）：

1. Thunderbird を開く
2. 受信箱から適当なメールを開く
3. `その他` ドロップダウンメニューから `ソースを表示` を選択する
4. テキストウィンドウの先頭から最初の空行までのデータを見る

### Cookie-Jar Format

Cookie-Jar 書式はプログラム fortune(1) がランダムな引用文のデータベースに使用し
ている書式だ。自然な順序付けや、単語レベル以上の区別可能な構造、テキストの文脈以
外の検索キーを持たないテキスト片に適する。

* 構造化されていないテキストからなるレコードの集まりに適している。
* レコードの区切り文字として、改行の後に `%%` or `%` を使用する。

Example 5.3. A fortune file example. の第二の引用は刀狩令か。

<!--
The people of the various provinces are strictly forbidden to have in their possession any swords, short swords, bows, spears, firearms, or other types of arms.
The possession of unnecessary implements makes difficult the collection of taxes and dues and tends to foment uprisings.
-->

> It's even better practice to use %%, and ignore all text from %% to
> end-of-line.

それは普通はコメントと呼ばれるものだ。

### Record-Jar Format

> Cookie-jar record separators combine well with the RFC 822 metaformat for
> records, yielding a format we'll call ‘record-jar’.

Cookie-Jar 書式における `%%` に関する考察はこの書式でも当てはまる。

> In a format like this it is good practice to simply ignore blank lines.

### XML

> XML is well suited for complex data formats （中略） though overkill for
> simpler ones. It is especially appropriate for formats that have a complex
> nested or recursive structure of the sort that the RFC 822 metaformat does not
> handle well.

XML の利点の一つは、構文を検査することで不正な形式、破損データ、不正に生成された
データを検出できることが多いことだ（データの意味まで調べずに済むことが多いの意）。

XML の最も深刻な問題は、従来の Unix ツールとは相性が悪いということだ。マークアッ
プの中にあるデータを見るのが難しい。XML ファイルが比較的まばらに記述されていれば
いいのだが。

### Windows INI Format

> The `DEFAULT` entry supplies values that will be used when a named entry fails
> to supply them.

これは知らなんだ。

* 読みやすい
* 設計は悪くない
* 従来の Unix スクリプトツール e.g. grep(1) とは相性が悪い

> It's not good for data with a fully recursive treelike structure (XML is more
> appropriate for that), and it would be overkill for a simple list of
> name-value associations (use DSV format for that).

### Unix Textual File Format Conventions

* 一行あたり一レコード
* 一行 80 字以内
* コメントは `#` から始まる
* バックスラッシュエスケープ
* フィールドの区切り文字として `:` または空白を使用する
* タブと空白の区別を重要視しない
* バージョン番号を含めるか、互いに独立した自己記述の塊として書式を設計する
* 浮動小数点丸め誤差の問題に注意する
* ファイルの一部だけを圧縮したり、バイナリー化したりする必要はない

> For complex records, use a ‘stanza’ format: multiple lines per record, with a
> record separator line of `%%\n` or `%\n`. The separators make useful visual
> boundaries for human beings eyeballing the file.

* 一行あたり一フィールドを持つか、`:` で終端するフィールド名キーワードでフィール
  ドを始める、RFC822 ヘッダーに似た書式を使う
* 行をまたいでフィールドを継続する書式を用意する

### The Pros and Cons of File Compression

> Many modern Unix projects, such as OpenOffice.org and AbiWord, now use XML
> compressed with zip(1) or gzip(1) as a data file format.

LibreOffice もアプリケーションデータを圧縮 XML ファイルにシリアライズする方法を
受け継いでいる。

> On the other hand, experiments have shown that documents in a compressed XML
> file are usually significantly smaller than the Microsoft Word's native file
> format, a binary format that one might imagine would take less space.

これは「一つことを巧くやる」という Unix 哲学の基本に適っている。

やや高度な分析：表現設計を圧縮方法から切り離すことで、実際のファイル解析に最小限
の変更を加えるだけで、将来的に異なる圧縮方法を使用できる可能性を残すことができ
る。

圧縮は透明性を阻害する：

> While a human being can estimate from context whether uncompressing the file
> is likely to show him anything useful, tools such as file(1) cannot as of
> mid-2003 see through the wrapping.

いちおうオプション `--uncompress`, `--uncompress-noreport` はあるが、解凍して
`file` を走らせるのと変わりない。

テキスト、バイナリー、圧縮テキストのどれが最適かは、ストレージの経済性、発見しや
すさ、閲覧ツールをできるだけ単純に書くことのどれを重視するかによって決まる。選択
肢と設計のトレードオフを見極めろ。

## Application Protocol Design

データファイルの書式がテキスト形式であることの良い理由はすべて、アプリケーション
固有のプロトコルにも当てはまる。

> A CLI server with a command set that is designed for simplicity has the
> valuable property that a human tester will be able to type commands direct to
> the server process to probe the software's behavior.

読書案内：

> Every protocol designer should read the classic _End-to-End Arguments in
> System Design_ [Saltzer].

[Saltzer]: <https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf>

インターネットアプリケーションプロトコル設計の伝統は 1980 年以前は Unix とは別に
発展してきた。

SMTP, POP3, IMAP はインターネットハッカーの間でアプリケーションプロトコル規範と
みなされている。

### Case Study: SMTP, the Simple Mail Transfer Protocol

SMTP の交信例が示されている。参加者が二人しかいないチャット欄のようなものだ。

* `C:` から始まる行はメール送信側による
* `S:` から始まる行はメール受信側による
* 送信側の文字列はコマンド名＋引数が基本形で、メッセージ本文送信方式だけ変わる
* 受信側の文字列は戻り値＋情報
* コマンド `DATA` のペイロードは一つの点からなる行で終了する

> SMTP is one of the two or three oldest application protocols still in use on
> the Internet. It is simple, effective, and has withstood the test of time.

時の試練とは格好いい。

> The traits we have called out here are tropes that recur frequently in other
> Internet protocols. If there is any single archetype of what a well-designed
> Internet application protocol looks like, SMTP is it.

SMTP はインターネットアプリケーション通信規格の始祖のようなものだ。

### Case Study: POP3, the Post Office Protocol

> It is also used for mail transport, but where SMTP is a ‘push’ protocol with
> transactions initiated by the mail sender, POP3 is a ‘pull’ protocol with
> transactions initiated by the mail receiver.

メールクライアントの送信と受信コマンドがそれぞれ push, pull 通信規格だ。それも、
定期的、周期的、連続的、継続的に起こるものではない。

Example 5.8 は POP3 セッションの例だが、SMTP のそれと類似点が多い。

* `C:` 行と `S:` 行の存在
* 行指向
* サーバー側の文字列は戻り値＋情報
* ペイロードメッセージ区画の指示方式（ドット）

ただし戻り値の細部は異なる。

### Case Study: IMAP, the Internet Message Access Protocol

ダメ押しに IMAP も考察する。

IMAP ではペイロードの区切り方が少し異なる。ドットで終わらせる代わりに、その直前
にペイロードの長さを送信する。受信側にしてみればバッファリングが可能になる。

ここはわからない：

> Also, notice that each response is tagged with a sequence label supplied by
> the request; in this example they have the form A000n, but the client could
> have generated any token into that slot. This feature makes it possible for
> IMAP commands to be streamed to the server without waiting for the responses;
> a state machine in the client can then simply interpret the responses and
> payloads as they come back. This technique cuts down on latency.

IMAP は POP3 を置き換えるために設計された。インターネットアプリケーション通信規
格設計の優秀な例であり、研究、模倣の価値がある。

## Application Protocol Metaformats

データファイルでも通信規格でも、metaformats はシリアライズを簡素化する方向に進化
する。

### The Classical Internet Application Metaprotocol

推薦図書：

> *On the Design of Application Protocols*l

古典的インターネット通信規格の性質：

* テキスト形式
* 単一行の要求と応答を使用する
* ペイロードは複数行になることがある。ペイロードは、先行する長さをオクテットで指
  定するか、`.\r\n` という行で終端する。
* ピリオドで始まる行はすべて、ピリオドがもう一つ付加される
* 応答行はステータスコードの後に人間が読めるメッセージが続く

> One final advantage of this classical style is that it is readily extensible.
> （中略）
> SMTP, POP3, and IMAP have all been extended in minor ways fairly often during
> their lifetimes, with minimal interoperability problems.

<!-- readily: quickly, immediately, willingly, or without any problem -->

### HTTP as a Universal Application Protocol

アプリケーション通信規格の設計者は、汎用サービスプラットフォームとして Web サー
バーを使い、HTTP の上に専用目的通信規格を重ねる傾向が強まってきている。

> This is a viable option because, at the transaction layer, HTTP is very simple
> and general.

HTTP を簡単に説明している文があり有益。

* 要求は RFC-822/MIME 風書式のメッセージ
* ヘッダーは識別と認証情報を一般に含む
* 最初の行は URI で指定された資料に対するメソッド (GET, PUT, POST, etc.) 呼び出し
* 応答は RFC-822/MIME 書式のメッセージ

> Besides avoiding a lot of lower-level details, this method means the
> application protocol will tunnel through the standard HTTP service port and
> not need a TCP/IP service port of its own. This can be a distinct advantage;
> most firewalls leave port 80 open, but trying to punch another hole through
> can be fraught with both technical and political difficulties.

MDN にあるこの資料は HTTP を大づかみに理解するのにいい：
[An overview of HTTP - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)

### Case Study: The `CDDB/freedb.org` Database

唐突に始まる音楽 CD の話。PC などに再生装置が実装される昔からある規格であるた
め、アルバム名や曲名といった簡単な情報すらデータ規格に用意されていない。後付けで
音楽情報をダウンロードする仕組みがインターネットに存在する：

> There are (at least two) repositories that provide a mapping between a hash
> code computed from the track-length table on a CD and
> artist/album-title/track-title records. The original was `cddb.org`, but
> another site called `freedb.org` which is probably now more complete and
> widely used.

サービスは単純な CGI 問い合わせとして HTTP 上で実装されている。

この実装方針のおかげで、HTTP やさまざまなプログラミング言語のウェブアクセスライ
ブラリーといった既存の下部構造がすべて利用可能になり、このデータベースへの問い合
わせや更新を行うプログラムを支援することができる。

### Case Study: Internet Printing Protocol

IPP はネットワークからアクセス可能な印刷機を制御するための標準だ。

* IPP はトランスポート層として HTTP 1.1 を使用する
* 要求はすべて POST メソッド 呼出しによって渡される
* 応答は通常の HTTP 応答

> Most network-aware printers already embed a web server, because that's the
> natural way to make the status of the printer remotely queryable by human
> beings.

Printer Working Group の文書 [How to Use the Internet Printing Protocol
](https://www.pwg.org/ipp/ippguide.html) にある Overview にザッと目を通し、本書
のこれまでの説明と組み合わせればこの通信規約の例がおぼろげにわかるか。

### BEEP: Blocks Extensible Exchange Protocol

> BEEP (formerly BXXP) is a generic protocol machine that competes with HTTP for
> the role of universal underlayer for application protocols.

聞いたことがない。リンク切れは <https://beepcore.org/> に変えておけばいいか？

> BEEP also avoids the HTTP problem that all requests have to be
> client-initiated; it would be better in situations in which a server needs to
> send asynchronous status messages back to the client.

今なら Python や JavaScript で非同期プログラミングを知っているから言わんとするこ
とを理解するが、C/C++ しか知らないときに読んだら想像がつかなかっただろう。

> BEEP is still new technology in mid-2003, and has only a few demonstration
> projects.

### XML-RPC, SOAP, and Jabber

アプリケーション通信規格の設計では、要求とペイロードを構造化するために、MIME 内
で XML を使用する傾向にある。見出しの三つはすべて XML 文書型だ。

> XML-RPC and SOAP, considered as remote procedure call methods, have some
> associated risks that we discuss at the end of [Chapter 7](./multiprogram.md).

これらは後回しでいいか。第七章でもわからなかったらここに戻る。

> Jabber is a peer-to-peer protocol designed to support instant messaging and
> presence.

リンク先 (Jabber Software Foundation) は Chrome からの警告により閲覧不能。
