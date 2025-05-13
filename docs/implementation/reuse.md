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

> Perhaps he has read Ed Yourdon's *Death March*, which as long ago as 1996
> noted that a majority of projects are on a time and resource budget at least
> 50% too tight, and that the trend is for that squeeze to get worse.

!!! note

    この節はまとめにくい。工夫が必要。

> He is wrestling not merely with his own inexperience but with a cascade of
> problems created by the carelessness or incompetence of others — problems he
> can't fix, but can only work around.

他人のコードに依存しなければしないほど、より多くのコードを書くことができる。

より多くのコード行を書くことができるかもしれないが、生み出すものの実際の価値は再
利用を成功させた場合と比べて大幅に下がる可能性が高い。

プロジェクトが変わるたびに、彼は多少なりとも新しい技術を学び、新しい車輪を発明し
直さなければならないだろう。

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
./configure;
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

パブリックドメインでないあらゆるものには著作権があり、おそらく複数ある。米国連邦
法では©表示がなくても、著者が著作権を有する。

TBR

### What Qualifies as Open Source

### Standard Open-Source Licenses

### When You Need a Lawyer

[Chapter 2]: <../context/history.md>
[CPAN]: <https://www.cpan.org/>
[ibiblio]:<https://www.ibiblio.org/>
[SourceForge]: <https://sourceforge.net/>
