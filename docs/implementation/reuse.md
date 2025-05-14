# Chapter 16. Reuse

[TOC]

無駄な仕事をしないことはプログラマーにとって大きな美徳だ。

新しいプロジェクトのたびに火や車輪を再発明するのは無駄がひどく多い。思考時間は、
ソフトウェア開発に投入される他のすべての入力と比較して貴重であり、価値がある。し
たがって、すでに解決策が存在する古い問題を蒸し返すのではなく、新しい問題を解決す
るために費やせ。

(Henry Spencer) 再発明された車輪は往々にして四角い。

車輪の再発明を避ける最も効果的な方法は、他人の設計と実装を借りることだ。コードを
再利用することだ。

体系的な再利用は Unix プログラマーの最も重要な特徴的動作の一つであり、Unix を使
用した経験から、単発コードを急いで書くのではなく、最小限の新しい発明で既存の部品
を組み合わせて解法の基本形を作ろうとする習慣が備わるはずだ。

> The virtuousness of code reuse is one of the great apple-pie-and-motherhood
> verities of software development.

何だこの修辞は。<https://en.wiktionary.org/wiki/mom_and_apple_pie>

他の OS で経験を積んで Unix 共同体に入った開発者の多くは、体系的な再利用の習慣を
学んでいない。利益に反するように思えるのに、無駄や重複作業が横行している。このよ
うな機能不全に陥った行動がなぜ続いているのかを理解することが、それを変えるための
第一歩だ。

## The Tale of J. Random Newbie

なぜプログラマーは車輪を再発明するのか：

* 技術的な問題
* プログラマー心理
* ソフトウェア生産システムの経済的問題

この節の前半部分の概要：

* J. Random Newbie
    * 大学を出たばかりのプログラマーだ。
    * コード再利用の価値を教わり、それを適用しようという熱意がある。
    * 所与の道具やライブラリーをできるだけ賢く使いこなすことが、成功への近道だと
      考えている。
* プロジェクト
    * Newbie が配属されたプロジェクト。
    * 攻めたスケジュールが組まれている。
    * このプロジェクトでは利用ライブラリーが急所だ。
* 使用機材
    * プロジェクト責任者が開発言語だけでなく多くのライブラリーも含めて、適切と思
      われるツールや部品を集めた。
    * 部品の文書が不十分で、ライブラリーは専売使用許諾条件の下にある不透明なオブ
      ジェクトコードの塊であるからソースコードを読んで実際に何をしているのかを知
      ることもできない。

> Perhaps he has read Ed Yourdon's *Death March*, which as long ago as 1996
> noted that a majority of projects are on a time and resource budget at least
> 50% too tight, and that the trend is for that squeeze to get worse.

Newbie が再利用している部品には、予測不可能な、あるいは破壊的な動作をするエッジ
ケースがあるらしい。

Newbie は部品の問題に対して弥縫策を講じなければならない。コードは次第にいびつな
ものになっていく。おそらく、理論的には仕様の範囲内であるにもかかわらず、ライブラ
リーに何か重要なことをさせることができないような場所に何度かぶつかるだろう。

Newbie はひどく不満を募らせている。自分の未熟さだけでなく、他人の不注意や無能が
引き起こした問題の連鎖と格闘している。

Newbie がよほど幸運でない限り、プロジェクトの存続期間内にライブラリーのバグを修
正することはできないだろう。

ヤケクソになった Newbie は安定性の低いライブラリーを安定性の高いもので模し、独自
の実装をゼロから書き始めた。置き換えたコードは不透明な部品と弥縫策の組み合わせで
置き換えたものよりも比較的うまく動作し、デバッグもしやすい傾向がある。

他人のコードに依存しなければしないほど、より多くのコードを書くことができる。

!!! note

    著者の見解がここでようやく述べられる：

* Newbie がとった行動は短期的な局所最適化であり、長期的な問題を引き起こす。
* より多くのコード行を書くことができるかもしれないが、生み出すものの実際の価値は
  再利用を成功させた場合と比べて大幅に下がる可能性が高い。
* 低水準で書かれ、車輪の再発明に大部分が費やされている場合、コードが多ければ多い
  ほど良いコードというわけではない。
* プロジェクトが変わるたびに、彼は多少なりとも新しい技術を学び、新しい車輪を発明
  し直さなければならないだろう。

> They will be poisonously ambivalent about code reuse, pushing inadequate but
> heavily marketed vendor components on their programmers in order to meet
> schedule crunches, while simultaneously rejecting reuse of the programmers'
> own tested code.

そのような文化の中で生まれるコードの再利用に最も近いものは、一度お金を払ったコー
ドは決して捨てることはできず、取り繕ったりクズを寄せ集めたりしなければならないと
いう信条だろう。このような文化が生み出す製品は時間の経過とともに次第に肥大し、バ
グだらけになっていくだろう。

## Transparency as the Key to Reuse

前節の物語は、再利用に対するさまざまな程度の圧力が互いに補強しあい、個々の原因か
らは直線的に予測できないような大きな問題を引き起こす方法を説明することを意図して
いる。

内部が見えないものは修正できない。実際、自明でない API を持つソフトウェアでは、
内部が見えないものを正しく使うことさえできない。

文書は原理的にも不十分だ。コードが体現しているすべての微妙な違いを伝えることはで
きない。

オブジェクトコードのみの部品はソフトウェアシステムの透明性を破壊する。

再利用しようとしているコードが閲覧も変更も可能であれば、再利用の不満ははるかに少
ない。コメントがよく書かれたソースコードはそれ自体が文書だ。ソースコードのバグが
修正できる。ソースはデバッグのために取り付けられ、コンパイルされるため、不明瞭な
場合での動作を簡単に調べることができる。そして、そ動作を変更する必要があれば変更
することができる。

ソースコードを要求するもう一つの重要な理由がある。Unix プログラマーが数十年にわ
たる絶え間ない変化を通して学んだ教訓は、ソースコードは長持ちするが、オブジェクト
コードは長持ちしないということだ。たとえソフトウェアを変更する意図も必要性もな
かったとしても、それを実行し続けるためには新しい環境で再構築しなければならない。

透明性の重要性とコード遺物問題が、再利用するコードが検査と変更に対して開かれてい
ることを要求する理由だ。

## From Reuse to Open Source

* Unix 初期では OS の部品、ライブラリー、関連がソースで頒布されていた。
* [Chapter 2] で述べられていたように、この伝統が途絶えたら Unix は勢いを失った。
* その後 GNU ツールキットと Linux が台頭し、オープンソースの価値が再発見された。

Unix 文化の中で最先端の開発を行うためには、次の両方を理解することが重要だ：

* オープンソースという明確なコンセプト
* 最も広く使われているオープンソースライセンス

コード再利用の理論と実践を議論する上で、オープンソースについてより具体的に考える
ことは有益だ。

ソフトウェア開発者は、使用するコードが透明であることを望んでいる。さらに、転職時
にツールキットや専門知識を失いたくはないだろう。 彼らは被害者であることに嫌気が
さし、鈍いツールや知的所有権の柵に苛立ち、車輪の再発明を繰り返さなければならない
ことにうんざりしている。

ソフトウェア開発者は職人や芸術家と同じだ。彼らは聴衆を持ちたいという欲求を含め、
芸術家の意欲と欲求を持っている。コードを再利用したいだけでなく、自分のコードが再
利用されることを望んでいる。

> Open source is a kind of ideological preemptive strike on all these problems.

J. Random Newbie の再利用に関するほとんどの問題の根源が

* クローズドソースの不透明性にあるというのならば、クローズドソースを生み出す制度
  的前提は打ち砕かれなければならない。
* 企業の縄張り意識が問題だとすれば、縄張り意識がいかに自滅的なものであるかを企業
  が理解するまで、それを攻撃するか迂回しなければならない。

したがって、1990 年代後半以降、オープンソース、その実践、その免許、その共同体に
ついて語ることなしに、コードの再利用のための戦略や戦術を推奨しようとしても、もは
や意味がない。別の場所ではこれらの問題が切り離せたとしても、Unix 界では表裏一体
だ。

## The Best Things in Life Are Open

インターネットでは文字どおり何 TB もの Unix ソースが利用可能だ。標準的なツールを
使えばほとんどのものを数分でビルドし、実行することが可能だ。その呪文とは：

```console
./configure
make
make install
```

だ。通常、インストールは root になる必要がある。

Unix 界の外から来た人（特に技術者でない人）は、オープンソースソフトウェアは商業
的なものよりも劣っていて、粗雑に作られていて信頼性が低く、節約するよりも多くの頭
痛の種を引き起こすと考えがちだ。

反論材料：

* 公開することによって仲間内での評判を危険にさらしている人が書いている。
* 会議、遡及的な設計変更、官僚的な間接費によって削られる時間が少ない傾向にある。

オープンソース共同体の人はバグを指摘することを恥ずかしがらず、その基準も高い。標
準以下の作品を世に送り出した作者は、自分のコードを修正するか撤回するという多くの
社会的圧力を経験し、もし選択するならば、それを修正する熟練した助けを得られる。そ
うして、成熟したオープンソースのパッケージは一般的に高品質であり、専売同等品より
も機能的に優れていることが多い。

オープンソースの現場と他との大きな違いは、リリースレベルが 1.0 であるということ
は、そのソフトウェアがすぐに使える状態であるということだ。バージョンが 0.90 以上
ならばコードが量産可能であることを示すかなり信頼性の高い兆候だ。

最近の Unix では C コンパイラー自体がほとんどオープンソースだ。The Free Software
Foundation の GNU コンパイラーコレクション (GCC) はたいへん強力で、文書も充実し
ており、信頼性も高いので、専売 Unix コンパイラー市場は事実上残っていない。そし
て、Unix 販売業者は自社でコンパイラーを開発するよりも、GCC を自社プラットフォー
ムに移植するのが普通になっている。

オープンソースパッケージを評価する方法は、その文書を読み、コードのいくつかにざっ
と目を通すことだ。また、そのパッケージがしばらくの間存在し、使用者からのフィード
バックをかなり取り入れてきたという証拠があれば、そのパッケージはかなり信頼できる
ものだと考えてよい。

配布物の `README` やプロジェクトのニュースや履歴ファイルに、原作者以外の何人の名
前が挙げられているかどうかが、成熟度や使用者からのフィードバックの量を測る良い指
標となる。

> Credits to lots of people for sending in fixes and patches are signs both of a
> significant user base keeping the authors on their toes, and of a
> conscientious maintainer who is responsive to feedback and will take
> corrections.

そのソフトウェアが独自の Web ページ、オンライン FAQ 一覧、メーリングリスト、ユー
ズネット・ニュースグループを持っている場合も吉兆だ。これらはすべて、そのソフト
ウェアの周りに関心共同体が育っていることを示す兆候だ。不発に終わったパッケージは
このような継続的な投資を得られない。

複数プラットフォームへの移植は使用者が多様化していることを示す貴重な指標でもあ
る。プロジェクトページが新しい移植を宣伝する傾向があるのはそれが信頼性を示すから
だ。

Linux 配布導入パッケージを見るのも品質を探る良い方法だ。 Linux やその他のオープ
ンソース Unix 導入パッケージ業者はどのプロジェクトが最善構成であるかについて多く
の専門的な知識を有する。彼らがリリースを統合する際に付加する価値の大部分だ。

## Where to Look?

Unix 界では多くのオープンソースが利用できるため、再利用するコードを見つける技は
他の OS の場合よりもはるかに大きな見返りをもたらす可能性がある。Unix で培うべき
最も有用な技の一つは、コードをつなぎ合わせるさまざまな方法をよく把握することであ
り、それによって Rule of Composition を使えるようになる。

再利用可能なコードを見つけるには灯台下暗し。Unix は再利用可能なユーティリティー
やライブラリーの豊富なツールキットを常時備えている。いくつかのキーワードで
`man -k` を検索するだけで有用な結果が得られることが多い。

> To begin to grasp something of the amazing wealth of resources out there, surf
> to [SourceForge], [ibiblio], and Freshmeat.net. Other sites as important as
> these three may exist by the time you read this book, but all three of these
> have shown continuing value and popularity over a period of years, and seem
> likely to endure.

この辺の見通しはさすが。

[SourceForge] は共同開発を支援するために特別に設計されたソフトウェアのデモ拠点で
あり、関連するプロジェクト管理サービスも完備している。単なるアーカイブではなく、
無料の開発ホスティングサービスであり、2003 年半ば現在、間違いなく世界最大のオー
プンソース活動の拠点となっている。

[Ibiblio] の Linux アーカイブは [SourceForge] 以前は世界最大だった。単にパッケー
ジを公開する受動的な場所ではあるが、WWW インターフェイスが優れている。また、
Linux Documentation Project の拠点でもあり、Unix 使用者や開発者にとって優れた資
料となる多くの文書を保管している。

Freshmeat は新しいソフトウェアのリリースを告知したり、古いソフトウェアを新しくリ
リースするためのシステムだ。使用者や第三者がリリースを批評することができる。

いくつかのインタープリター言語に特化した拠点もある：

> The [CPAN] archive is the central repository for useful free code in Perl. It
> is easily reached from the Perl home page.

現代でも活動中。

> The Python Software Activity makes an archive of Python software and
> documentation available at the Python Home Page.

Python Software Activity というのは現存しない。Python Software Foundation の前身
と考えられる。

> Many Java applets and pointers to other sites featuring free Java software are
> made available at the Java Applets page.

現代の Web ブラウザーを使う限りではアプレットは死んでいるので忘れていい。

開発者として時間を投資する最も価値ある方法の一つは、これらの拠点を見て回り、自分
が何を使えるかを学ぶことだ

コードを読むことは未来への投資だ。新しい技法、問題を分割する新しい方法、異なる方
式や取り組み方などをそこから学ぶことができる。コードを使うことも学ぶことも貴重な
報酬だ。学習したことを使わなかったとしても、他の人の解決策を見ることで問題の定義
が改善され、より良い解決策を自分で考え出す助けになるかもしれない。

まったく新しい問題はめったにないので、必要なものに近いコードを発見することはほと
んど可能だ。真に斬新なものであったとしても、それは誰かが解決したことのある問題と
遺伝的に関連している可能性が高い。

## Issues in Using Open-Source Software

オープンソースソフトウェアを利用したり再利用したりする際には大きな問題が三つある：

* 品質
* 文書
* 使用許諾条件

多くの高品質なオープンソースパッケージは文書が不十分なため、技術的にあるべき姿よ
りも役に立たない。

Unix の伝統はかなり階層的な文書を推奨する。

ソフトウェアパッケージやトピックのキーワード、HOWTO や FAQ といった文字列を含む
語句を Web 検索する価値がある。多くの場合、マニュアルページよりも初心者にとって
有用な文書を見つける。

オープンソースソフトウェアを再利用する上で最も深刻な問題は、パッケージの使用許諾
条件を理解することだ。

## Licensing Issues

パブリックドメインでないあらゆるものには著作権が（おそらく複数）ある。米国連邦法
では©表示がなくても、著者が著作権を有する。

使用許諾条件が重要な理由：著作権法上、誰が著作者とされるかは、特に多くの人の手が
入ったソフトウェアの場合、複雑な場合がある。

専売ソフトウェアの世界では許諾条項は著作権を保護するために企図されている。所有者
（著作権者）のためにできるだけ多くの法的領域を確保しながら、使用者に権利を少し与
える方法だ。著作権者が重要であり、使用許諾の論理は制限的だ。使用許諾条項の正確な
技術的内容は通常重要ではない。

著作権者は通常、使用許諾条件を保護するために著作権を行使する。無期限に存続させる
意図の下でコードを自由に利用できるようにする。特に、著作権者は既存の使用者が持っ
ているコピーの条件を変更することはできない。したがって、オープンソースソフトウェ
アでは著作権者はほとんど関係ない。だが、使用許諾条項は重要だ。

通常、プロジェクトの著作権者は、現在のリーダーまたは資金提供組織だ。プロジェクト
が新しいリーダーへ移管されたことは、著作権者の変更によって多くの場合知られる。

著作権を Free Software Foundation に譲渡することを選択するプロジェクトもある。こ
れは FSF がオープンソースを擁護することに関心があり、そのための弁護士もいるとい
う理論に基づく。

### What Qualifies as Open Source

使用許諾条件が伝達しうるいくつかの権利を区別する：

* 複製して再配布する権利
* 使用する権利
* 個人的な使用のために改変する権利
* 改変した複製物を再配布する権利

[The Open Source Definition] がオープンソース開発者間の社会契約の明確化として、
オープンソース共同体で広く受け入れられている。

> Its constraints on licensing impose the following requirements:
>
> * An unlimited right to copy be granted.
> * An unlimited right to redistribute in unmodified form be granted.
> * An unlimited right to modify for personal use be granted.

このガイドラインは改変バイナリーの再配布を制限することを禁止している（再配布して
よい）。

標準的な使用許諾条件 (MIT, BSD, Artistic, GPL/LGPL, MPL) はすべて OSD を満たして
いる。GPL のように、他の制限があるものもある。

非商用利用しか許可しない許諾条件は、たとえそれが GPL や他の標準的な許諾条件に基
づいていたとしても、オープンソースライセンスとして認められない：

> Such licenses discriminate against particular occupations, persons, and
> groups, a practice which the OSD's Clause 5 explicitly forbids.

Clause 5 を確認したらほぼ同じ文言だ。

> Selling the software as a product qualifies, certainly. But what if it were
> distributed at a nominal price of zero in conjunction with other software or
> data, and a price is charged for the whole collection?

OSD の目的の一つは、OSD に準拠するソフトウェアの流通経路にある人々が、自分たちの
権利が何であるかを知るために弁護士に相談する必要がないことを保証することだ。

OSD が個人、集団、職業に対する制限を禁じているのは、ソフトウェアの集まりを扱う
人々が、そのソフトウェアで何ができるかということに関して、微妙に異なる（そしてお
そらく矛盾する）制限の組み合わせ爆発に直面しないようにするためでもある。

国家によっては、特定の制限された技術を「ならず者国家」と呼ばれる国々に輸出するこ
とを禁止する法がある。OSD はそれらを否定することはできない。

### Standard Open-Source Licenses

[Chapter 19] も見ろ。

* [MIT]
* [BSD]
* [Artistic License]. これは知らない。
* [GPL]
* [LGPL]
* [MPL]

この章ではこれらの重要な違いは感染性だ。使用許諾条件が感染性を持つとは、使用許諾
ソフトウェアの派生物もその条項の下に置くことを要求することだ。

これらの使用許諾の下では、本当に心配しなければならない唯一の種類のオープンソース
の使用は、専売製品にフリーソフトウェアのコードを実際に組み込むことだ。

GPL は最も論争の的になっている感染性使用許諾条件だ。論争を引き起こしているのは
2.b 節で、GPL のプログラムの派生物はそれ自身が GPL であることを要求している：

> cause the whole of any work that you distribute or publish, that in whole or
> in part contains the Program or any part thereof, either with or without
> modifications, to be licensed at no charge to all third parties under the
> terms of this General Public License (...).

争点となる問題：

* ライブラリーのリンク
* GPL で許諾されたヘッダファイルのインクルード

米国の著作権法が派生とは何かを定義していないのが問題の一つ。

一方では、少し先の段落が述べる mere aggretation によって、GPL のソフトウェアをあ
自分の専売コードと同じメディアで出荷しても、それらが互いにリンクしたり呼び出した
りしないのであれば、確かに問題ない。それらは同じファイル形式やディスク上の構造で
動作する道具でさえあり得る。そのような状況は、著作権法上、一方を他方の派生物とす
ることはないだろう。

他方では GPL のコードを自分の専売コードに継ぎ接ぎしたり、GPL のオブジェクトコー
ドを自分のコードにリンクしたりすることは、確かに自分のコードを二次的著作物とし、
GPL であることを要求する。

一般には、一方のプログラムが他方のプログラムの二次的著作物になることなく、他方の
プログラムを子プロセスとして実行することができると考えられている。

> The case that causes dispute is dynamic linking of shared libraries. The Free
> Software Foundation's position is that if a program calls another program as a
> shared library, then that program is a derivative work of the library.

そんな見立てが許されるのか。

FSF は、GNU コンパイラーコレクションに付属する実行時ライブラリーを使い続けること
ができると人々を安心させるために、少し緩やかな Library GPL を特別に考案すること
になった。いつの間にか Less GPL に改名した。

条項 2.b の解釈は自分で選ばなければならない。

MPL と LGPL は GPL よりも限定された形で感染する：

> They explicitly allow linking with proprietary code without turning that code
> into a derivative work, provided all traffic between the GPLed and non-GPLed
> code goes through a library API or other well-defined interface.

### When You Need a Lawyer

> This section is directed to commercial developers considering incorporating
> software that falls under one of these standard licenses into closed-source
> products.

業務で使えるかもしれない。

我々は弁護士ではないこと、オープンソースソフトウェアで行いたいことの合法性につい
て疑問がある場合は、弁護士にすぐに相談すべきであるという趣旨の、控えめな免責事項
を述べることが期待されていることだ。

これらの使用許諾の文言は法律用語に匹敵するほど明瞭であり、そうであるように書かれ
ている。弁護士や裁判所は商業開発者以上に混乱しているのが実際のところだ。

この制度で訴えられた人はいない。

弁護士は自分が理解できないものに対しては職業的良心から強く疑ってかかる。技術的な
側面や作者の意図をオープンソースソフトウェアを使いたい開発者ほど理解していないに
もかかわらず、それに近づくべきでないと言う可能性が高い。

決定的な判例がない以上、作者の意向に沿うように目立った善意の努力をすることが、使
いたい開発者にできることの 99% であり、弁護士に相談することで得られる（または得
られない）かもしれない 1% の追加的な保護が違いを生むことはなさそうだ。

[Artistic License]: <https://dev.perl.org/licenses/artistic.html>
[BSD]: <https://opensource.org/license/BSD-2-Clause>
[Chapter 2]: <../context/history.md>
[Chapter 19]: <../community/opensource.md>
[CPAN]: <https://www.cpan.org/>
[GPL]: <https://www.gnu.org/licenses/old-licenses/gpl-1.0.txt>
[ibiblio]:<https://www.ibiblio.org/>
[LGPL]: <https://www.gnu.org/licenses/lgpl-3.0.en.html#license-text>
[MIT]: <https://opensource.org/license/mit>
[MPL]: <https://www.mozilla.org/en-US/MPL/2.0/>
[SourceForge]: <https://sourceforge.net/>
[The Open Source Definition]: <https://opensource.org/osd>
