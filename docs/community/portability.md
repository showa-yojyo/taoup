# Chapter 17. Portability

[TOC]

Unix は異なるプロセッサー族間で移植された最初 (Version 6 Unix, 1976-77) の量産
OS だ。

移植性はつねに Unix の主な利点の一つだ。

ハードウェア依存のコードは Unix 社会では悪い形式とみなされ、OS カーネルカーネル
のようなひじょうに特殊な場合にしか許容されない。

Unix プログラマーはソフトウェアを特定の腐りやすい技術に依存させることを避け、公
開標準に大きく依存する傾向がある。移植性のために書くというこのような習慣が Unix
の伝統に根付いているため、小さな単一用途のプロジェクトにさえ適用されている。これ
らの習慣は Unix 開発ツールキットの設計や、Unix の下で開発された Perl, Python,
Tcl などのプログラミング言語にも二次的な影響を与えている。

移植性の直接的な利点は、Unix ソフトウェアが元のハードウェアプラットフォームより
長生きするのが普通なので、ツールやアプリケーションを数年ごとに再発明する必要がな
いことだ。

移植性の間接的な利点は工法、インターフェイス、実装を単純化する効果がある。これは
プロジェクトの成功確率を高め、生存過程の維持費を削減する。

## Evolution of C

1973 年に開発された言語が、これほど変更を必要としなかったという事実は本当に驚く
べきことであり、計算機科学・工学の他のどこにも類似点がない。

[Chapter 4] では、C 言語が成功したのは、標準工法に近似した計算機上で、薄い接着剤
の層として機能したからだと論じたのだった。

### Early History of C

* BCPL (Basic Common Programming Language) → B インタープリター (1970) → C 言語
  (1971)
* Dennis Ritchie の オリジナル C コンパイラー (DMR) は Unix version 5, 6, 7 あた
  りで貢献した。
* 最近の C 言語の実装のほとんどは Steven C. Jhonson による PCC に依っている。
  Version 7 でデビューし、System V と BSD 4.x の両リリースで DMR コンパイラーを
  完全に置き換えた。
* 1976 年、Version 6 C は `typedef`, `union`, `unsigned int` を導入した。変数の
  初期化と複合演算子のいくつかで構文を変更した。
* C 言語に関する記述の原典は *The C Programming Language* (1978) だ。白本と呼ば
  れている。
* Version 7 C は `enum` を導入した。`struct` と `union` の値をコピー代入したり、
  引数として渡したり、関数から返したりできる第一級オブジェクトとして扱うようにし
  た。

Steve Johnson 氏によるヘッダーファイルに関する陳述が興味深い：

> Another major change in V7 was that Unix data structure declarations were now
> documented on header files, and included. Previous Unixes had actually printed
> the data structures (e.g., for directories) in the manual, from which people
> would copy it into their code. Needless to say, this was a major portability
> problem.

ANSI C Standard Draft:

* `const`/`volatile` を追加。
* `unsigned` 型修飾子があらゆる型に適用できるように一般化。対称性のため `signed`
  を追加。
* `auto` 配列、`struct` 型、`union` 型それぞれに対して初期化構文を追加。
* 関数プロトタイプを追加。

初期の C 言語における最も重要な変化は、ANSI C Standard Draft における定義参照へ
の切り替えと関数プロトタイプの導入であった。

初期の詳しい履歴は設計者 Ritchie による *The Development of the C Language*
(1993) を見ろ。

### C Standards

C 標準開発はオリジナルの精神を守ることに細心の注意を払い、新しい機能を発明するよ
りも、既存のコンパイラーでの実験を追認することに重点を置いた保守的な過程であっ
た。

言語への主な機能追加は 1986 年末までに決着し、この時点で K&R C と ANSI C を区別
するのが一般的になった。

ANSI C の中核部分については早期に決着がついたが、標準ライブラリーの内容をめぐる
論争は何年も続いた。

正式な規格が発行されたのは 1989 年末だ。この規格は 1990 年に ISO が主催者を引き
継ぎ、ISO/IEC 9899:1990として再指定された。この規格で記述されている言語バージョ
ンは一般に C89 または C90 として知られている。

著者のこぼれ話：

> The first book on C and Unix portability practice, *Portable C and Unix
> Systems Programming*, was published in 1987 (I wrote it under a corporate
> pseudonym forced on me by my employers at the time).

K&R 本の第二版は 1988 年に出版された。

1993 年、ワイド文字と Unicode を支援。(ISO/IEC 9899-1:1994)

規格の改訂は 1993 年に始まった。1999 年、ISO によって ISO/IEC 9899 (C99) が採択
された。きわめて多くの細かい機能が追加された。おそらくほとんどのプログラマーに
とって最も重要なものは、C++ 同様、どの時点でも変数を宣言できるようになったことだ
ろう。

C 言語の標準化は、標準化作業が開始される以前から、実用的でほぼ互換性のある実装が
多種多様なシステム上で実行されていたという事実によって、大いに助けられてきた。そ
のため、どのような機能を標準に含めるべきかについて議論することが難しくなった。

## Unix Standards

1973 年に Unix を C 言語で書き直したことで、移植や変更がかつてないほど容易になっ
た。その結果、Unix の祖先は早くから OS の一族へと分岐していった。

実世界の Unix は公開標準に忠実に従っているので、開発者はたまたま使っている Unix
の公式マニュアルのページよりも、POSIX 仕様のような文書に頼ることができる（頻繁に
そうしている）。

新しいオープンソース の Unix (Linux) では、OS の機能が公開されている標準規格を仕
様として設計されているのが一般的だ。

### Standards and the Unix Wars

Unix 標準の開発の最初の動機は AT&T と Berkeley の開発線分裂 ([Chapter 2]) だった。

1979 年の Version 7 から 4.x BSD Unix が派生。

1980 年の 4.1 BSD リリース後、BSD 線は Unix の最先端としての評判を急速に高めて
いった。重要な追加物：

* `vi`
* ジョブ制御機能：複数フォアグラウンドタスクとバックグラウンドタスクを管理する
* シグナル ([Chapter 7]) の改良
* TCP/IP ネットワーキング

1980 年に Berkeley は最も重要な追加機能である TCP/IP の開発契約を結んだものの、
三年間、外部リリースとして出荷されることはなかった。

1981 年の System III がその後の AT&T の開発の基礎となった。

* System III は Version 7 の端末インターフェイスをよりきれいな形に作り直した
* Berkeley の機能拡張とは互換性が全くない
* シグナル ([Chapter 7]) の古さはそのまま

1983 年にリリースされた System V Release 1 では、vi(1) などの BSD ユーティリティ
がいくつか組み込まれた。

1983 年、この隔たりを埋める最初の試みが出された。

* どこから：Unix 使用者団体 UniForum
* 何を：UniForum 1983 Draft Standard (UDS 83)

1983 年、4.2BSD によって問題が悪化。4.2BSD は TCP/IP ネットワーキングを含む多く
の新機能を追加し、祖先である Version 7 との微妙な非互換性を導入した。

1984 年の Bell 事業会社の分割と Unix 戦争 ([Chapter 2]) の始まりは問題を著しく
複雑にした。Unix 戦争中、技術標準化は協力的な技術者たちが推し進めるものとなった。

1984 年に AT&T が System V Release 2 (SVr2) を発表したとき、標準の設定において使
用者団体と協力することを宣言した。その年の UniForum Draft Standard の二回目の改
訂は SVr2 の API をたどり、影響を与えた。

その後の Unix 標準も、BSD の機能が明らかに機能的に優れている分野を除いては
System V に追従する傾向があった。例えば、現代の Unix 標準は、同じ機能に対する
BSD のインタフェイースではなく、System V の端末制御を記述している。

1985 年、AT&T は System V Interface Definition をリリース。UDS 84 を組み込んだ
SVr2 API のより正式な記述。後の改訂は System V リリース 3 と 4 のインターフェイ
スをだとった。SVID が POSIX 標準の基礎となり、最終的にシステムコールと C ライブ
ラリーコールをめぐる Berkeley と AT&T の紛争の大半を AT&T に有利に傾けた。

1985 年、ネットワーク上でファイルシステムを共有するための競合する API 標準がリ
リースされた：

* Network File System (NFS)
* Remote File System (RFS)

Sun の NFSが優勢だったのは、単なる仕様だけでなくオープンソースのコードも他と共有
することに積極的だったからだ。

この成功の教訓は RFS が純粋に論理的な根拠において優れたモデルであったからこそよ
り強く指摘されるべきであった。

1985 年以降、Unix の標準化の主要な推進力は IEEE に移った。IEEE 1003 委員会は
POSIX として一般に知られる一連の標準を開発した：

* システムコールと C ライブラリー機能
* シェルの詳細な語義と最小限のコマンド集合
* さまざまな非 C プログラミング言語用の詳細なバインディング

1990 年の最初のリリースに続き、1996 年に第二版（注：原文単数形）がリリースされ
た。ISO が ISO/IEC 9945 として採用した。

!!! note "TODO"

    主な POSIX 標準一覧

* オリジナルの POSIX 標準は後のすべての Unix 標準化作業の基礎となった。
* POSIX 標準は *POSIX Programmer's Guide* のような参照文献を通して、今でも権威と
  して引用されている。
* 事実上の Unix API 標準はいまだに「POSIX プラスソケット」であり、それ以降の標準
  は主に機能の追加と、珍しいエッジケースにおける適合性をより詳細に規定している。

1984 年、X/Open（後に Open Group と改名）結成。

* Unix 販売業者の共同団体

X/Open Portability Guides (XPGs) を開発した。

* XPGs は当初は POSIX 草稿と並行して発展し、1990 年以降は POSIX を組み込んで拡張
  した。
* XPG は POSIX とは異なり、最先端での一般的な慣習をより志向した。
* 1987 年の XPG2 は基本的に System V の curses(3) である端末処理 API を追加した。
* 1990 年の XPG3 では X11 API が統合された。
* 1992 年の XPG4 では ANSI C 標準への完全準拠が義務付けられた。
* XPG2, 3, 4 は国際化のサポートに重点を置き、コードセットとメッセージカタログを
  扱うための精巧な API を記述した。

1993 年、すべての主要 Unix 企業を含む 75 のシステムおよびソフトウェア販売業者が
Unixの共通定義を開発するために X/Open を支持することを宣言し、Unix 戦争は終結し
た。

1999 年、X/Open は POSIX の活動を吸収した。

2001 年、X/Open は Single Unix Standard version 3 を発行した。Unix API 標準化の
すべての糸が最終的に一つの束に撚られた。さまざまな Unix が共通の API に再集結し
たのだ。

### The Ghost at the Victory Banquet

この取り組みを支援してきた旧来の Unix 販売業者はオープンソース Unix の新派から厳
しい圧力を受けており、場合によっては専売 Unix を放棄しようとしていたのだ。

Single Unix Specification への適合性を検証するために必要な適合試験は高価だ。ほと
んどのオープンソース OS の配布業者には手が届かない。いずれにせよ、Linux はとても
速く変化するので、どのリリースも、おそらく認定を受ける頃には時代遅れになる。

### Unix Standards in the Open-Source World

1990 年代半ば、オープンソース共同体は独自の標準化活動を開始した。特に Linux は
POSIX のような Unix API 標準の可用性に依存する形でゼロから書かれていた。

新派の Unix にとっての問題はソースコードレベルでの API の互換性ではなかった。新
たな問題はソースの互換性ではなく、バイナリーの互換性だった。

昔は、それぞれの Unix は事実上独自のハードウェアプラットフォーム上で動いていた。
演算装置の命令集合や計算機構造には十分な種類があり、アプリケーションを動かすには
ソースレベルで移植する必要があった。

しかしその後、ミニコンやワークステーションの販売業者は安価な 386 ベースのスー
パーマイクロに席巻され、オープンソースの Unix が規則を変えた。業者はバイナリーを
出荷する安定したプラットフォームがなくなった。

Linux 市場が統合されるにつれて、真の問題は時間の経過とともに変化する速度であるこ
とが明らかになった。API は安定していたが、システム管理ファイル、ユーティリティー
プログラム、ユーザーメールボックス名やシステムログファイルへのパスの接頭辞のよう
なものの予想される場所は変わり続けていた。

1993 年に始まった新派の Linux と BSD 共同体自身の中で開発された最初の標準化の努
力は Filesystem Hierarchy Standard (FHS) だ。Linux Standards Base (LSB) に組み込
まれ、期待されるサービスライブラリーと補助アプリケーションの集合も標準化された。
この二つの標準は Free Standards Group の活動となり、2001 年までには旧式 Unix 業
者の中で X/Open のような役割を担うようになった。

## IETF and the RFC Standards Process

## Specifications as DNA, Code as RNA

## Programming for Portability

### Portability and Choice of Language

### Avoiding System Dependencies

### Tools for Portability

## Internationalization

## Portability, Open Standards, and Open Source

[Chapter 2]: <../context/history.md>
[Chapter 4]: <../design/modularity.md>
[Chapter 7]: <../design/multiprogram.md>
