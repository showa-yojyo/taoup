# Chapter 19. Open Source

[TOC]

* Unix は、その実践がオープンソースに最も近いときに繁栄し、そうでないときに停滞
  した。
* オープンソースの開発ツールは高品質である傾向がある。
* オープンソースの振る舞いのほとんどは長い歴史のある Unix の伝統的な慣習を強化し
  たものに過ぎない。
* Unix がオープンソース共同体から得た重要な民俗習慣の慣習の多くは、他の現代的 OS
  の開発者にも有益だ。

## Unix and Open Source

オープンソースの開発では、バグの叙述と修正が、例えば何らかの算法の実装とは異な
り、複数の並列部分課題に分割するのに適した課題であるという事実を利用している。試
作設計の近傍の可能性の探索も並列化しやすい。

AT&T 分割前の初期 Unix 共同体はオープンソースの典型的な例であった。

分割前の Unix コードは技術的にも法的にも専有財であったが、使用者・開発者共同体内
では共有財 (commons) として扱われていた。問題解決に最も強い意欲を持つ人々が奉仕
活動を自主的に行った。

参考資料：

* *The Cathedral and the Bazaar* (1999)
* *Understanding Open Source Software Development* (2002)

著者の内省的な述懐が続き、汲み取りにくいので残念だがカット。

オープンソース開発の規則は単純だ：

1. **ソースを公にする。**
   コードとそれを生み出す過程を公開する。第三者による査読を奨励する。他の人が
   コードを自由に修正し、再配布できるようにする。共同体を大きくする。

2. **早く、頻繁にリリースする。**
   リリースのテンポが速いと、効果的なフィードバックが素早く得られる。段階的なリ
   リースが少量であれば、実際のフィードバックに応じて軌道修正することも容易だ。
   最初のリリースが有望であることを実証しろ。コンパイルも実行もできない最初のリ
   リースはプロジェクトの命取りになる。
   コンパイルできないリリースは開発者がプロジェクトを完成させることができないこ
   とを示唆する。

3. **貢献には賞賛で報いる。**
   物質的な報酬を与えられないなら心理的な報酬を与えよう。人は往々にして金のため
   よりも評判のために懸命に働くものだ。

Henry Spencer: 規則 2. の系として、個々のリリースは、多くの準備が必要な、重大な
イベントであってはならない。

* すべてが完璧になるまで次のリリースを出荷できないと考えるな。
* バージョンが増えても動揺するな。

一般的に、任意のプロジェクトへの貢献者のほとんどは志願者であり、ソフトウェアの有
用性の向上や評判の誘因により貢献している。気軽な貢献者を奨励するには、彼らと中核
組の間に障壁を作らないことが重要だ。特権的地位を最小限に抑えたい。

多くのプロジェクトはバージョン管理システムを使ってネットワークからアクセス可能な
コードリポジトリーを保有している。自動化されたバグ追跡システムや差分追跡システム
の使用も一般的だ。

!!! note

    現代の GitHub のようなサービスを当時の言葉で説明していると解釈した。

Linux, Apache, Mozilla のようなプロジェクトは成功を収め、世間からの認知度も高く
なった。

秘密主義の習慣を捨て、工程の透明性と査読を優先させることが錬金術が化学になる決定
的な一歩だった。

## Best Practices for Working with Open-Source Developers

オープンソース共同体における習慣を構成するものの多くは、分散開発への自然な適応だ。
Unix の慣習が恣意的なものである場合、それらはしばしば 1980 年代初期の Usenet や
GNU プロジェクトの慣習や標準に遡る。

### Good Patching Practice

!!! note

    本文で述べられる差分に関するコツは現代では GitHub などのサービスにあるプルリクエストページ上で実践すればいい。

ほとんどの人は、自分のプロジェクトをリリースする前に、他人のソフトウェアに差分を
書くことでオープンソースソフトウェアに関わるようになる。今、他人のベースライン
コードに対してソースコードの変更点を書いたとする。その人はその差分を含めるかどう
かをどのように判断するだろうか。

彼らは差分提出者の流儀や通信行動から品質の手がかりを探す。

著者はこう言う：何百人もの見知らぬ人からの差分を長年扱ってきたが、自分の時間を尊
重し、思慮深く提示されたもので、技術的には偽物というのを見たことはめったにない。

#### Do send patches, don't send whole archives or files

!!! note

    オープンソースプロジェクトの環境が整備された現代では手動実践不要。

* diff(1) と patch(1) の双子はオープンソース開発の最も基本的な工具だ。
* 全体を送るよりも `diff` による差分のほうが良い理由は、先方がベースラインから変
  更したコードがある場合を考えればわかる。

#### Send patches against the current version of the code

!!! note

    要旨を現代風に解釈すると「プルリクエストブランチを先方指定のものにしろ」だ。

#### Don't include patches for generated files

提出する前に、patch(1) を適用して作り直すと自動的に再生成されるファイルを削除し
ろ。

!!! note

    まともなプロジェクトならば、バージョン管理リポジトリーの構成がそのようなファイルを登録不能にしている可能性が高い。

#### Don't send patch bands that just tweak RCS or SCCS $-symbols

例えば、RCS や CVS で使われる `$Id$` など、ソースコードに特別なトークンを入れ
て、ファイル更新が確定したときにバージョン管理システムによって展開されるようにし
ている人もいる。この手のコードは送らない方が配慮がある。

!!! note

    現代のコミット単位で履歴を管理する VCS ではこれを支持していないのではないか。
    少し調べた限りでは Git でも `.gitattributes` で構成すれば実現可能らしい。

#### Do use `-c` or `-u` format, don't use the default (`-e`) format

> The default (`-e`) format of diff(1) is very brittle.

オープンソース開発抜きで重要。オプション `-c` か `-u` を明示的に使うということを
理解しろ。

* [Context format](https://www.gnu.org/software/diffutils/manual/html_node/Context-Format.html)
* [Unified format](https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html)

#### Do include documentation with your patch

ソフトウェアの機能に使用者から見える追加や変更を加えるのであれば、適切な手引書や
文書への変更も含めろ。

優れた文書は通常、堅実な貢献と迅速で汚いハックを分ける最も明らかなきざしだ。

#### Do include an explanation with your patch

現代で言えばプルリクエストの description に相当する：

> Your patch should include cover notes explaining why you think the patch is
> necessary or useful. This is explanation directed not to the users of the
> software but to the maintainer to whom you are sending the patch.

* 「このパッチで更新された文書を参照してください」とだけ言うのはダメだ。
* パッチを適用することで起こるかもしれない悪いことを率直に伝えるのもいい。

<!-- featuritis:  excessive ongoing expansion or addition of new features in a product -->

#### Do include useful comments in your code

悪いコメントを入れておくと責任者がそれを削る。

#### Don't take it personally if your patch is rejected

!!! note

    提出したパッチが却下される理由は質が低いからと考えていいと思う。

### Good Project- and Archive-Naming Practice

管理者の負担が増えるにつれ、投稿の一部または全部を（手動ではなく）自動で処理する
傾向が強まっている。このため、プロジェクト名やファイル名が、プログラムが解析し理
解できる規則的なパターンに適合することが重要になってる。

#### Use GNU-style names with a stem and major.minor.patch numbering

アーカイブファイルがすべて GNU 流の名前、つまり、すべて小文字の英数字からなる語
幹の接頭辞、ハイフン、バージョン番号、拡張子、その他接尾辞を持つ名前であれば皆に
とって便利だ。

語幹は音節を区切るために `-` または `_` を含むことができる。

ソースアーカイブとバイナリーアーカイブを区別する必要がある場合、異なる種類のバイ
ナリーを区別する必要がある場合、何らかのビルドオプションをファイル名に表現する必
要がある場合は、バージョン番号の後に付ける拡張子として扱え。例：

| ファイル | 内容 |
|----------|------|
| `foobar-1.2.3.src.tar.gz` | ソース一式 |
| `foobar-1.2.3.bin.tar.gz` | バイナリー |
| `foobar-1.2.3.bin.i386.tar.gz` | i386 バイナリー |
| `foobar-1.2.3.bin.i386.static.tar.gz` | i386 バイナリー静的リンク版 |
| `foobar-1.2.3.bin.SPARC.tar.gz` | SPARC バイナリー |

!!! note

    バージョン部に関しては現代では semantic versioning を適用すればよい。

#### But respect local conventions where appropriate

> Some projects and communities have well-defined conventions for names and
> version numbers that aren't necessarily compatible with the above advice.

この本を含むその筋の権威のおかげでローカルルールが縮小していく傾向がある。

#### Try hard to choose a name prefix that is unique and easy to type

語幹接頭辞はプロジェクトのすべてのファイルで共通であるべきで、読みやすく、入力し
やすく、覚えやすいものでなければならない。

* `_` は使わない。
* 正当な理由なく大文字や小文字を変えたりしない。
    * 人間の目から見た自然な検索順序を狂わせる。
    * マーケティング（訳しにくい概念）に暗い人が賢くなろうとしているように見える。

既存プロジェクトの語幹名とかぶってはいけない。

### Good Development Practice

多くの貢献者を得て成功するプロジェクトと、関心を集められずに停滞するプロジェクト
の違いを生む行動とは？

#### Don't rely on proprietary code

市販の言語やライブラリー、その他コードに依存するとはオープンソース共同体では無礼
な行為とされている。オープンソースの開発者はソースを査読できないコードを信用しな
い。

#### Use GNU Autotools

構成選択はコンパイル時に行うべし。オープンソースの頒布の重要な利点は、コンパイル
時にパッケージが見つけた環境に適応できることだ。これは、開発者が見たこともないプ
ラットフォームでパッケージが動作することを可能にし、ソフトウェアの使用者共同体が
独自の移植を行うことを可能にするのに重要だ。

GNU autotools を使って移植性の問題を処理し、システム設定の探索を行い、`Makefile`
を調整しろ。使用者に `configure; make; make install` をさせろ。

コンパイル時になって使用者にシステム情報を尋ねるな。ソフトウェアはコンパイル時や
インストール時に必要と思われる情報を自分で判断できないようではダメだ。

可能な限り、POSIX のような標準に従ってプログラムし、システムに構成情報を求めるこ
とも控えろ。

#### Test your code before release

優れた試験集合によってリリース前に回帰試験を簡単に実行できる。強力で使いやすい試
験枠組を使うことでソフトウェアに段階的に試験を追加することが可能だ。

試験集合を配布することで、使用者共同体は自分たちの移植を試験してから、それを組に
還元することができる。

さまざまなプラットフォームで試験をするように開発者に奨励しろ。そうすれば、通常の
開発の一環として、移植性の欠陥についてコードを継続的に試験するようになる。

試験集合が `make test` で実行できるようにしておくのが良い実践だ。

#### Sanity-check your code before release

人間が見落としがちな錯誤を発見する合理的な工具を使用しろ。

C/C++ に関するコツ：

* GCC ならばオプション `-Wall` を使ってコンパイルし、リリース前に警告すべてが消
  えるようにコードを修正しろ。
* 可能な限りすべてのコンパイラーでコードをコンパイルしろ。異なるコンパイラーは異
  なる問題をしばしば見つける。
* `lint` を実行しろ。
* メモリーリークやその他の実行時エラーを探す工具を実行しろ。Electric Fence と
  Valgrind はオープンソースで利用可能な良い工具だ。

Python プロジェクトに関しては PyChecker プログラムが有用だ。

!!! note

    現代なら Ruff あたりだろう。

Perl を書いているなら `perl -c` でコードを検めろ。場合によっては `-T` も付けろ。
`perl -w` と `use strict` は必ず使え。

!!! note

    * `-c` は構文解析のみを行い、コードを実行しない。
    * `-T` は脆弱コードを検出するのに使うらしい。
    * `-w` は GCC の `-Wall` だろう。

#### Spell-check your documentation and READMEs before release

ずさんなコード、コンパイルすると警告が出るコード、`README` ファイルやエラーメッ
セージのミススペリングはすべて、その背後にある技術もずさんだと使用者に思わせる。

#### Recommended C/C++ Portability Practices

ANSI 機能を完全に使ってかまわない（特に関数プロトタイプ）。

GCC `-pipe` オプションや入れ子関数のような、コンパイラー固有の機能が利用可能であ
ると仮定するな。

移植性のために必要なコードは単一領域に分離しろ。サブディレクトリーを使うのが良
い。移植性に問題のあるコンパイラー、ライブラリー、OS のインターフェイスは、この
ディレクトリーのファイルで抽象化しろ。

> A portability layer is a library (or perhaps just a set of macros in header
> files) that abstracts away just the parts of an operating system's API your
> program is interested in. Portability layers make it easier to do new software
> ports.

移植層を分離して設けておくことで、あるプラットフォームに詳しい専門家が、移植層以
外のことを理解することなく、ソフトウェアを移植することが可能になる。

移植層はアプリケーションを単純にもする。複雑なシステムコールの全機能をソフトウェ
アが必要とすることはまれだ。抽象インターフェイスを持つ移植層は、システムから限定
された必要な機能しか持ち込ませないことを可能にし、アプリケーションコードを単純に
する。

> A “platform” is always selected on at least two axes: the compiler and the
> library/operating system release. In some cases there are three axes, as when
> Linux vendors select a C library independently of the operating system
> release.

プラットフォーム数はこの三構成要素の積になる。一方、ANSI や POSIX 1003.1 のよう
な言語とシステムの標準を使えば、機能集合は比較的制約される。

実装が大きく異なる場合（例：共有メモリーマッピング）には、異なるプラットフォーム
用の移植性のあるコードを別々のファイルに移し、違いが最小限の場合（例：現在の時刻
を知る）には、移植性のあるコードを単一ファイルのままにしておく。

(Doug McIlroy) `#ifdef` は最後の手段だ。

`#ifdef` の使用は移植層の中では（うまく制御されていれば）許される。移植層の外で
は `#include` 条件に限定しろ。

システムの他の部分の名前空間には決して侵入しない。

コーディング標準を選択する。複数のコーディング標準を使って構築されたソフトウェア
を保守するのはあまりにも困難で経費がかかるため、何らかの共通の流儀を選択しなけれ
ばならない。コードの一貫性と清潔さが最優先事項であり、標準自体の詳細は大差の二着
目だ。

### Good Distribution-Making Practice

解凍したときにどうなるべきか。

#### Make sure tarballs always unpack into a single new directory

配布物を作業ディレクトリーに解凍する tarball をビルドすることは最も迷惑だ。すで
にそこにあるファイルを上書きしてしまう可能性がある。

作業ディレクトリーの直下にある単一の最上位ディレクトリーに解凍されるように作れ。
例えば `foo-0.23.tar.gz` という名前で tarball を作る場合には、解凍サブディレクト
リーの名前が `foo-0.23` となるように作れ。

!!! note

    Example 19.1 はこれを実現する `Makefile` のスケッチだが、慣れていないと読めない。

#### Include a `README`

> By ancient convention (originating with Dennis Ritchie himself before 1980,
> and promulgated on Usenet in the early 1980s), this is the first file intrepid
> explorers will read after unpacking the source.

<!-- promulgate: to announce something publicly, especially a new law: -->
<!-- intrepid: brave -->

`README` ファイルは短く、読みやすいものであるべきだ。紹介、導入にする。詩のよう
にはするな。`README` に書くべきこと：

1. プロジェクトの簡単な説明
2. プロジェクトの Web サイト
3. 開発者のビルド環境とあるかもしれない移植性の問題についての覚書
4. 重要なファイルやサブディレクトリー
5. ビルド、インストール手順、またはそれを含むファイル (e.g. `INSTALL`) への指示
6. 保守者、クレジット一覧、またはそれを含むファイル (e.g. `CREDITS`) への指示
7. 最近のプロジェクトのニュースか、それを含むファイル (e.g. `NEWS`) への指示
8. プロジェクトのメーリングリストのアドレス

!!! note

    `NEWS` ファイルはもしかしたらバージョン別の更新ログかもしれない。

> At one time this file was commonly `READ.ME`,

そうだったかもしれない。

#### Respect and follow standard file-naming practices

標準的最上位ファイル名一覧：

* `README`
* `INSTALL`
* `AUTHORS`
* `NEWS`
* `HISTORY`
* `CHANGES`
* `COPYING`, `LICENSE`
* `FAQ`

大文字のファイル名はビルド部品ではなく、パッケージに関する人間が読めるメタ情報で
あるという慣習がある。

`FAQ` ファイルは救済の意味がある。ある質問がプロジェクトに関してよく出てきたら、
それを `FAQ` に書け。そして、使用者が質問やバグ報告を送る前に `FAQ` を読むように
誘導する。よく育てられた `FAQ` はプロジェクト保守者の負担を一桁以上減らす。

各リリースのタイムスタンプが入った `HISTORY` や `NEWS` ファイルを持つことは価値
がある。とりわけ、特許侵害訴訟を起こされたときに、先行技術を立証するのに役立つこ
とがある。

!!! note

    現代ではリポジトリー自体がオープンだから、その心配は当時よりかなり薄れた。

#### Design for upgradability

ソフトウェアのリリースの変更の中には後方互換性がないものもあり得る。インストール
された複数のバージョンのコードが同じシステム上で共存できるように、インストール配
置を設計しろ。ライブラリーの場合は特に重要だ。

Emacs, Python, Qt 各プロジェクトではバージョン番号付きディレクトリーという、これ
を扱うための良い慣習がある。

取引先プログラムは必要なライブラリーのバージョンを指定しなければならない。イン
ターフェイスが壊れるよりはましだ。

#### Under Linux, provide RPMs

!!! note

    使わせてもらうことはよくあるが、自分で作る未来がないので割愛。

#### Provide checksums

バイナリーファイルについてはチェックサムを用意しろ。これにより、バイナリーが破損
していないか、トロイの木馬のコードがねじ込まれていないかを確認する。

この目的には暗号学的に安全なハッシュ関数を使用するのが最善だ

* GPG パッケージは `--detach-sign` オプションでハッシュを与えろ。
* GNU `md5sum` も同様。

出荷する各バイナリーファイルについて、プロジェクトの Web ページにはチェックサム
とそれを生成するために使用したコマンドの一覧を示せ。

### Good Communication Practice

インターネット上で目に見える形でプロジェクトの存在を示すことは、使用者や共同開発
者の募集に役立つ。

#### Announce to Freshmeat

!!! note

    本書では Freshmeat がちょくちょく現れてきたが、現存しないので忘れていい。

> Bad example: “Announcing the latest release of FooEditor, now with themes and
> ten times faster”. Good example: “Announcing the latest release of FooEditor,
> the scriptable editor for touch-typists, now with themes and ten times
> faster”.

#### Announce to a relevant topic newsgroup

自分のアプリケーションに直接関係する Usenet のトピックグループを見つけて、そこで
も発表しろ。コードの機能が関連するところにしか投稿するな。

例えば Perl で書いた IMAP サーバーに問い合わせるプログラムをリリースする場合、確
かに comp.mail.imap には投稿するのが筋だ。しかし、そのプログラムが Perl の最先端
の技術を示す有益な例でない限り、comp.lang.perl には投稿しないのが筋だ。

発表にはプロジェクトの Web サイトの URL を含めるべし。

!!! note

    Usenet という単語が当然のように現れるのにとまどっている。

#### Have a website

プロジェクトの周囲に使用者や開発者の共同体を作ろうとするなら Web サイトを持つの
が当然だ。

Web サイトに掲載する標準的なもの：

* プロジェクト憲章（存在意義、対象者など）
* プロジェクトソースのダウンロードリンク
* プロジェクトのメーリングリストへの参加方法の説明
* FAQ 一覧
* プロジェクト文書の HTML バージョン
* 関連プロジェクトや競合プロジェクトへのリンク

<!-- charter: a document issued by a government that gives rights to a person or group -->

教育の行き届いたプロジェクトの Web サイトに関しては [Chapter 16] を見ろ。

!!! note

    現代なら GitHub やその競合サービスで上記の事項を十分実現可能だ。

#### Host project mailing lists

プロジェクトの協力者たちが連絡を取り合ったり、パッチを交換したりできるよう、非公
開の開発リストを持つのが標準的なやり方だ。また、プロジェクトの進捗を知らせたい人
のための告知名簿を持つのも良かろう。

「非公開」の開発名簿をどの程度非公開にするかということが重要だ。設計の議論に広く
参加することは良いことでありがちだが、名簿が比較的開かれていれば、遅かれ早かれ、
新規使用者から質問を受けることになる。新規使用者は初歩的な質問をしないようにと文
書に記しておくだけでは解決しない。

告知用メールアドレス一覧は厳重に管理する必要がある。このような名簿の目的は、何か
重要なことが起こったときに知りたいが、日々の詳細については聞きたくないという人た
ちに対応することだ。

!!! note

    Twitter で良さそうだ。

#### Release to major archives

主なオープンソースのアーカイブサイトについては、[Chapter 16] Where Should I
Look? の節を見ろ。

!!! note

    プログラミング言語によっては定番のサイトが存在する。それを使え。

## The Logic of Licenses: How to Pick One

使用許諾条項の選択には、作者がそのソフトウェアを使って人々が何をするかに制限を
加えたい場合、どのような制限を加えるかについての決定が含まれる。

全く制限を設けたくなければ知的財産権消失状態にするのだ。これを行う適切な方法は、
各ファイルの先頭に以下のような文章を含める：

> Placed in public domain by J. Random Hacker, 2003.  Share and enjoy!

誰でもテキストのどの部分でも好きなようにできる。これほど自由なことはない。

しかし、オープンソースのソフトウェアが実際に知的財産権消失状態になることはほとん
どない。

* コードの所有権を利用して、開かれた状態を維持したいと考えるオープンソース開発者
  もいる。
* オープンソース使用許諾条件すべてに共通していることの一つは、保証の放棄だ。

## Why You Should Use a Standard License

オープンソース定義に準拠した広く知られた使用許諾条項は解釈の伝統が確立されている。
可能な限り、OSI サイトに掲載されている標準使用許諾条項のいずれかを採用しろ。

独自の使用許諾条項を作成しなければならない場合は必ず OSI の認定を受けろ。そうす
ることで多くの議論や間接費を避ける。

法の教義では、裁判所は許諾条項や契約を、それが生まれた共同体の期待や慣習に従って
解釈することになっている。したがって、裁判制度が最終的に対処しなければならなく
なったときに、オープンソース共同体の慣習が決定的になることを期待する十分な理由が
ある。

## Varieties of Open-Source Licensing

### MIT or X Consortium License

最も緩い種類のフリーソフトウェアライセンスは、著作権と許諾条項のコピーがすべての
改変版に保持されている限り、改変を複製、利用、改変、再配布する権利を無制限に認め
るものだ。この許諾条件を受け入れると、保守者を訴える権利を放棄することになる。

X Consortium の標準使用許諾条項の雛形は [OSI のサイト][MIT]にある。

### BSD Classic License

次に制限の少ない種類の許諾条件。著作権と許諾条項のコピーが改変版のすべてに保持さ
れ、パッケージに関連する広告や文書に謝辞が述べられている限り、改変コピーを複製、
利用、改変、再配布する権利を無制限に認める。被許諾者は保守者を訴える権利を放棄し
なければならない。

オリジナルの BSD License はこの種の許諾条件として最もよく知られている。

また、著作権者を変更し、宣伝の要求を省略した(事実上 MIT License と同等にした)
BSD License の軽微な変種を見かけることも珍しくない。

[BSD License の雛形][BSD]

### Artistic License

次に制限の厳しい種類の許諾条件。複製、使用、ローカルでの改変に関する無制限の権利
を認めるものだ。改変されたバイナリーの再配布は許容されるが、改変ソースの再配布は、
作者とフリーソフトウェア共同体の利益を守ることを意図した形で制限される。

Perl のために考案され、Perl 開発者共同体で広く使われている Artistic License はこ
の種のものだ。要求が二つ：

* 改変ファイルに対して、改変されたという prominent notice を含めること。
* 変更を再配布する人々には、自由に利用できるようにし、それをフリーソフトウェア共
  同体に広める努力をすること。

[Artistic License の雛形][Artistic]

### General Public License

GNU 一般公衆使用許諾条項（およびその派生版である LGPL）は唯一、最も広く使われて
いるフリーソフトウェアライセンスだ。Artistic License 同様、改変ファイルに
prominent notice があれば、改変ソースの再配布を認めている。

GPL は、GPL の下にある部分を含むプログラムはすべて GPL であることを要求する。

このような余計な要求があるため、GPL は一般的に使われている他のどの使用許諾条件よ
りも制限的だ。Perl はこれらを避けるために Artistic License を開発したのだ。

[What is Copyleft?](https://www.gnu.org/licenses/copyleft.en.html)

### Mozilla Public License

Mozilla Public License はオープンソースのソフトウェアを支援するが、閉じたソース
のモジュールや拡張機能と連結されている場合がある。この許諾条件は配布されたソフト
ウェアが開かれたままであることを要求するが、定義された API を通して呼び出された
アドオンが閉じたままであることを許容する。

[Mozilla Public License 1.1][MPL]

[Chapter 16]: <../implementation/reuse.md>
[BSD]: <https://www.opensource.org/licenses/bsd-license.html>
[MIT]: <https://opensource.org/license/mit>
[Artistic]: <https://www.opensource.org/licenses/artistic-license.html>
[MPL]: <https://www.mozilla.org/en-US/MPL/1.1/>
