# Chapter 9. Generation

[TOC]

人間は制御フローを推論するよりもデータを視覚化する方が得意だ([Chapter 1])。

* 50 ノードのポインター木の図と 50 行のプログラムのフロー図の表現力と説明力を比
  べる。
* 変換テーブルを表現する配列初期化と、同等の `switch` 文を比較する。

データはプログラムロジックよりも扱いやすい。

設計の複雑さをできるだけ手続き的なコードからデータへと移し、人間が維持、操作する
のに便利なデータ表現を選ぶのが良い習慣だ。そのようなデータ表現を機械が処理しやす
い形に変換するのは人間の仕事ではなく機械の仕事だ。

高水準で宣言的な記法の重要な利点のもう一つは、コンパイル時の検査に適していること
だ (Henry Spencer)。

## Data-Driven Programming

データ駆動型プログラミングを行う場合、コードではなくデータ構造を編集することでプ
ログラムのロジックを変更できるように両者を設計する。

データ駆動型プログラミングはオブジェクト指向と混同されることがある。

* データ駆動型プログラミングでは、データは単なるオブジェクトの状態ではなく、プロ
  グラムの制御フローを定義するものであるということだ。
* データ駆動型プログラミングの主な関心事は、固定コードをできるだけ書かないことだ。

Unix はオブジェクト指向よりもデータ駆動型プログラミングの伝統が強い。

データ駆動型のプログラミングは、状態機械の記述と混同されることもある。 実際、状
態機械のロジックをテーブルやデータ構造として表現することは可能だが、手作業でコー
ド化された状態機械は、通常、テーブルよりもはるかに修正しにくい硬直したコードの塊
だ。

あらゆる種類のコード生成やデータ駆動型プログラミングを行う際の重要な規則とは、い
つでも問題を上流に押し上げることだ。生成コードや中間的表現を手でハックしてはいけ
ない。変換ツールを改善したり置き換えたりすることを考えろ。

### Case Study: `ascii`

著者が保守しているプログラム `ascii` はコマンドライン引数を ASCII 文字の名前とし
て解釈し、それに相当する名前をすべて報告しようとする、とても単純で小さいものだ。

!!! note
    端末で `ascii 10` を実行した例が掲載されているが、理解できない。

> One indication that this program was a good idea is the fact that it has an
> unexpected use — as a quick CLI aid to converting between decimal, hex, octal,
> and binary representations of bytes.

バイト数の二進表現変換としても使えると言っている？

主要ロジックを 128 分岐の `case` 文としてコード化することもできただろう。しか
し、これではコードがかさばり保守が難しくなる。

データ駆動型プログラミングを適用する。すべての記号名文字列をコード内のどの関数よ
りもかなり大きなテーブル構造に格納しておく：
<https://gitlab.com/esr/ascii/-/blob/master/nametable?ref_type=heads>

この構成により、コードを邪魔することなく、テーブルを編集するだけで、新しい記号名
を追加したり、既存の名前を変更したり、古い名前を削除したりすることが簡単にできる。

### Case Study: Statistical Spam Filtering

データ駆動型プログラミングの興味深い事例のひとつに、スパム（迷惑メール）を検出す
るための統計的学習アルゴリズムがある。メールフィルタープログラムの一群 (e.g.
popfile, spambayes, bogofilte) は単語の相関関係のデータベースを使い、パターン
マッチング条件ロジックを置き換えている。

この手のプログラムは画期的な論文 [*A Plan for Spam*][Graham] を契機に、インター
ネット上で急速に普及した。

> In his paper, Graham noted accurately that computer programmers like the idea
> of pattern-matching filters, and sometimes have difficulty seeing past that
> approach, because it offers them so many opportunities to be clever.

《賢くなる機会がたくさんある》！

統計的スパムフィルターは、スパムか否かを判断する使用者からのフィードバックを収集
することで機能する。そのフィードバックはスパム分類と単語や言い回しを結びつける統
計的相関係数や重みのデータベースになる。最も一般的なアルゴリズムは、条件付き確率
に関する Bayes の定理の些細な変形を使用しているが、多項式ハッシュなどの他の技法
も採用されている。

従来型のパターンマッチングフィルターの問題点は脆いことだ。業者も奮闘しているか
ら：

> Spammers are constantly gaming against the filter-rule databases, forcing the
> filter maintainers to constantly reprogram their filters to stay ahead in the
> arms race.

統計的スパムフィルターは先述のフィードバックからフィルター規則を独自に生成する。

統計的フィルターの経験から、使用される特定の学習アルゴリズムは、学習アルゴリズム
が重みを計算する元となるスパムデータセットの質よりも重要性がはるかに低いことが分
かっている。つまり、統計的フィルターの結果はアルゴリズムよりもデータの形によって
左右される。

> For Unix programmers, seeing past the lure of clever pattern-matching was far
> easier than in other programming cultures without as strong an attachment to
> “Keep It Simple, Stupid!”

### Case Study: Metaclass Hacking in `fetchmailconf`

fetchmailconf(1) ドットファイル設定ツールには高水準オブジェクト指向言語による高
度なデータ駆動型プログラミングの有益な例が含まれている。

`fetchmail` 用のドットファイルは単純で古典的な Unix の自由形式構文を使用している
が、使用者が複数のサイトで POP3 や IMAP のアカウントを持っている場合、うんざりす
るほど複雑になることがある。Examle 9.1 として «a somewhat simplified version of
the `fetchmail` author's configuration file» が示されている。この作者とは本書著
者と同一だ。

<!-- Example 9.1. Example of fetchmailrc syntax. -->

`fetchmailconf` の設計目的は各種入力コントロールを備えた洒脱で人間工学的に正しい
GUI の背後に、ドットファイルの構文を完全に隠すことだった。しかし、それは GUI 操
作からファイルを簡単に生成することはできても、既存のファイルを読み込んだり編集し
たりすることはできなかった。

Python で `fetchmail` のドットファイル解析部と同じものを実装しかけたが、著者は
`fetchmailconf` が `fetchmail` 自身の解析部をフィルターとして使えるという事実を
利用できることに気づいた。

> I added a `--configdump` option to `fetchmail` that would parse `.fetchmailrc`
> and dump the result to standard output in the format of a Python initializer.

Example 9.2. はその出力例だとある。Python の複雑な `dict` オブジェクトに見える。

<!-- Example 9.2. Python structure dump of a fetchmail configuration. -->

これで Python インタープリターは `fetchmail --configdump` の出力を評価し、
`fetchmailconf` で利用可能な設定を変数 `fetchmail` の値として読み込むことが可能
になった。

次に必要なのは、この辞書オブジェクトを生オブジェクトの木に変換することで、

* `Configuration`
* `Site`
* `User`

の三種類のオブジェクトを取り付けることだ。これを言語によっては黒魔術呼ばわりされ
ることもある introspection により実装する：

> But Python's facilities for introspection and metaclass hacking are unusually
> accessible.

<!-- Example 9.3. copy_instance metaclass code. -->
<!-- Example 9.4. Calling context for copy_instance. -->

Example 9.3 から 9.4 までのコードをまとめる（一部改変）：

```python
def copy_instance(toclass, fromdict):
    for key, value in fromdict.items():
        setattr(toclass, key, value)

# The tricky part - initializing objects from the `configuration' 
# global.  `Configuration' is the top level of the object tree 
# we're going to mung 
Configuration = Controls()
copy_instance(Configuration, configuration)
Configuration.servers = []
for server in configuration['servers']:
    Newsite = Server()
    copy_instance(Newsite, server)
    Configuration.servers.append(Newsite)
    Newsite.users = []
    for user in server['users']:
        Newuser = User()
        copy_instance(Newuser, user)
        Newsite.users.append(Newuser)
```

急所は Python 内蔵関数 `setattr` でオブジェクトに属性を動的に付与できるというこ
とだ。

> Because `copy_instance` is data-driven and completely generic, it can be used
> on all three levels for three different object types.

Python が発明されたのは 1990 年だ。しかし、これは Unix の伝統の中で 1969 年まで
さかのぼる題目を反映している。

この設計問題をきれいに解決するためには、データ駆動型プログラミングの別々の二段階
が必要だった。

* `fetchmail` 自体を `fetchmailconf` のドットファイル解析器にすることができる
* `copy_instance` は汎用関数である可能性がある

再利用、単純化、一般化、直交性は Unix の禅の実践だ。

## Ad-hoc Code Generation

<!-- ad-hoc: made or happening only for a particular purpose or need, not
planned before it happens; 即興 -->

字句解析器 (tokenizer) や構文解析器 (parsers) を構築するような目的のために、Unix
は強力な特殊用途コード生成器を搭載している。しかし、コンパイラーの理論を知らなく
ても、また（エラーが発生しやすい）手続き型ロジックを書かなくても、より単純かつ軽
量なコード生成ツールがある。

### Case Study: Generating Code for the `ascii` Displays

`ascii` を引数なしで走らせると、画面出力は Example 9.5 のようになる。このヘルプ
部分の下に十進数、十六進数、コード名（もしくは文字そのもの）の表がある。

> This screen is carefully designed to fit in 23 rows and 79 columns, so that it
> will fit in a 24×80 terminal window.

!!! note
    環境に実際にインストールして出力を確認した。

プログラムソースの構成は次のとおり：

* テキストファイル `splashscreen` にコマンド `ascii -h` の出力の最初の一行以外全
  部の内容を記述しておく。
* C のソースには定義に `#include "splashscreen.h"` を含む関数がある（関数内部で
  ファイルをインクルードしていることに注意）。
* ファイル `splashscreen.h` を `Makefile` で生成するように仕込む。ルールはファイ
  ル `splashscreen` に依存し、それを `sed` でエスケープ文字関係を処理する。

そのため、プログラムが `make` されると、ファイル `splashscreen` は一連の出力関数
呼び出しに自動的に変換され、C 前処理器によって適切な関数に `#include` される。

データからコードを生成するように編成した利点は二つある：

* 編集可能なヘルプ画面と表示画面を同一に保つことができる（透明性を促進する）。
* C のコードにまったく触れることなく、ヘルプ画面を自由に変更することができ、次の
  ビルドで自動的に正しい処理が行われる。

> This is an almost trivial example, but it nevertheless illustrates the
> advantages of even simple and ad-hoc code generation. Similar techniques could
> be applied to larger programs with correspondingly greater benefits.

### Case Study: Generating HTML Code for a Tabular List

Web ページに表形式のデータを載せたい場合を考える。次のような表をブラウザーに描か
せたい：

```raw
Aalat         David Weber             The Armageddon Inheritance
Aelmos        Alan Dean Foster        The Man who Used the Universe
Aedryr        Steve Miller/Sharon Lee Scout's Progress
Aergistal     Gerard Klein            The Overlords of War
Afdiar        L. Neil Smith           Tom Paine Maru
Agandar       Donald Kingsbury        Psychohistorical Crisis
Aghirnamirr   Jo Clayton              Shadowkill
```

HTML テーブルコードを手書きするとどうなるか。名前を追加するたびに `<tr>` タグと
`<td>` タグを手書きで追加しなければならない。これではすぐに面倒になってしまう。

まず、データを CSV 形式で用意しておく（区切り文字はコロン）：

```raw
Aalat         :David Weber                 :The Armageddon Inheritance
Aelmos        :Alan Dean Foster            :The Man who Used the Universe
Aedryr        :Steve Miller/Sharon Lee     :Scout's Progress
Aergistal     :Gerard Klein                :The Overlords of War
Afdiar        :L. Neil Smith               :Tom Paine Maru
Agandar       :Donald Kingsbury            :Psychohistorical Crisis
Aghirnamirr   :Jo Clayton                  :Shadowkill
```

しかし、明示的な区切り文字があることで、フィールド値の編集中にスペースキーを2回
押してしまい、それに気づかないという事態を防ぐことができる。

そして、シェル, Perl, Python, Tcl などでこのファイルを HTML の表に加工するスクリ
プトを書き、項目を追加するたびにそれを実行する。昔ながらの Unix のやり方では以下
のような読みにくい sed(1) を実行することになる：

```console
sed -e 's,^,<tr><td>,' -e 's,$,</td></tr>,' -e 's,:,</td><td>,g'
```

* `sed` のオプション `-e` を三回使うのがコツ。それぞれ行頭挿入用、行末挿入用、コ
  ロン置換用。
* コマンド `s` の区切り文字はお馴染みの `/` ではなく `,` をここでは用いている。
  おそらく HTML 終了タグ内の `/` と紛れるから避けた。

あるいは、awk(1) だとこうなる：

```console
awk -F: '{printf("<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n", $1, $2, $3)}'
```

* 著者は `awk` を避ける傾向があるようだが、この例に関しては使い物になる。

最初の HTML を手作業でハックしたり、データベースを作成して検証したりするのに必要
な時間よりは、これらのスクリプトの作成とデバッグのほうが確実に短い（著者はそれぞ
れのツールで五分と述べている）。

> The combination of the table and this code will be much simpler to maintain
> than either the under-engineered hand-hacked HTML or the over-engineered
> database.

この方法で問題を解決するさらなる利点：

* マスターファイルが普通のテキストエディターで簡単に検索・修正可能。
* 変換スクリプトを微調整することで、さまざまな表から HTML への変換を実験したり、
  grep(1) フィルターをパイプラインの前に置くことで、報告の部分集合を簡単に作成し
  たりできる。

ここで実際に設計したのは、内容と形態の分離であり、生成スクリプトがスタイルシート
として機能するものだ。

教訓：

* 作業を可能な限り減らせ。
* データをコードの形にしろ。
* 道具に頼れ。
* 方策と仕組みを切り離せ。

> Expert Unix programmers learn to see possibilities like these quickly and
> automatically. Constructive laziness is one of the cardinal virtues of the
> master programmer.

[Chapter 1]: <../context/philosophy.md>
[Graham]: <https://www.paulgraham.com/spam.html>
