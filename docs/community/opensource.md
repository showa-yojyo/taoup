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
時にパッケージが見つけた環境に適応できることです。これは、開発者が見たこともない
プラットフォームでパッケージが動作することを可能にし、ソフトウェアの使用者共同体
が独自の移植を行うことを可能にするのに重要だ。

GNU autotools を使って移植性の問題を処理し、システム設定の探索を行い、`Makefile`
を調整しろ。使用者に `configure; make; make install` をさせろ。

コンパイル時になって使用者にシステム情報を尋ねるな。ソフトウェアはコンパイル時や
インストール時に必要と思われる情報を自分で判断できないようではダメだ。

可能な限り、POSIX のような標準に従ってプログラムし、システムに構成情報を求めるこ
とも控えろ。

#### Test your code before release

#### Sanity-check your code before release

#### Spell-check your documentation and READMEs before release.

#### Recommended C/C++ Portability Practices

### Good Distribution-Making Practice

### Good Communication Practice

## The Logic of Licenses: How to Pick One

## Why You Should Use a Standard License

## Varieties of Open-Source Licensing

## MIT or X Consortium License

### BSD Classic License

### Artistic License

### General Public License

### Mozilla Public License
