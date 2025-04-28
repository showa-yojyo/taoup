# Chapter 12. Optimization

[TOC]

この見出しの章に対するエピグラフはこれしかない：

> Premature optimization is the root of all evil. -- C. A. R. Hoare

性能の最適化について Unix の経験が教えてくれる主なことは、いつ最適化してはいけな
いかを知る方法だ。

## Don't Just Do Something, Stand There!

プログラマーでできる最も強力な最適化技法とは何もしないことだ。

理由は Moore の法則の指数関数的効果だ。最も賢く、最も安く、そして多くの場合最も
早く能率を向上させる方法は、対象ハードウェアがより高性能になるのを数ヶ月待つこと
だ。ハードウェアとプログラマーの時間の費用比を考えると、稼働中のシステムを最適化
するよりも、時間を使った方がいいことがほとんどだ。

!!! note "TODO"
    * 数式対応 (MathJax or MkDoc plugin)
    * ビッグオー記法の説明が良いので控えておきたい。

平均的状況での実行時間や空間の使用量を二次から線形や線形対数に削減可能である場
合、またはより高次の状況から削減可能な場合に労力を注ぎ込むのが賢明だ。

何もしないことのもう一つの形はコードを書かないことだ。ないコードによってプログラ
ムが遅くなることはない。あるコードによって遅くなることはあっても、効率が悪くなる
ことはある。

## Measure before Optimizing

アプリケーションが遅過ぎるという現実的な証拠が得られたら、そのとき、そしてそのと
きに限り、コードの最適化を考えるときだ。しかし、その前に測定しろ。

[Chapter 1] の Rob Pike の六規則を思い出せ。どれだ？

直感はボトルネックがどこにあるのかを知る手がかりにはならない。Unix には、他のほ
とんどの OS とは異なり、プロファイラーが付属している。それを使え。

!!! note
    プロファイルの一般的な意味は a detailed description of someone or something だから、
    ここではプログラムの動作に関するそれだと解釈して通じる。

プロファイラーの結果を読むのは一種の芸術だ。繰り返される問題がいくつかある：

* 計装雑情報
* 外部からの遅延の影響
* 呼び出しグラフの上位ノードの重み付け

計装雑情報問題は基本的だ。プロファイラーはサブルーチンの入口と出口、またルーチン
のインラインコード内に一定間隔で実行時間を報告する命令を挿入することで機能する。
これらの命令自体も実行に時間がかかる。ごく短いサブルーチンでは呼び出し時間の比較
に雑情報が多く、実際よりも高く見える傾向がある。

ゆえに、最速最短のサブルーチンの時間は、多くの泡や空気を含んでいると考えた方が賢
明だ。しかし、これらのサブルーチンが頻繁に呼び出される場合は、多くの時間を食って
いる可能性がある。呼び出し回数の統計には特に注意を要する。

外部遅延の問題も基本的だ。プロファイラーの背後にはさまざまな遅延や歪みが存在す
る。最も単純なのは、予測不可能な待ち時間を伴う操作による間接費だ。

* ディスクやネットワークへのアクセス
* キャッシュフィル（キャッシュメモリーに読み込む操作）
* プロセスコンテキストの切り替え

特に、システム全体の性能に注目している場合はなおさらだ。これらの間接費にはランダ
ムな要素があるため、個々のプロファイリングの実行結果があまり役に立たない可能性が
あることが問題だ。

このような雑情報源の影響を最小限に抑え、平均的な事例で時間がどこに向かっているの
かをよりよく把握する一つの方法は、多くのプロファイリング実行の結果を加えること
だ。最適化を行う前にテストハーネスを構築し、プログラムの負荷を試験することには多
くの理由がある。最も重要な理由は、プログラムを変更する際に、そのプログラムが正し
いかどうかを回帰テストできることだ。

> Once you've done this, being able to profile repeated tests under load is a
> nice side effect that will often give you better information than a few runs
> by hand.

呼び出しグラフの上位モードが太り過ぎ、呼び出し先ルーチンではなく、呼び出し元ルー
チンに時間が割り当てられる傾向がある。例えば、関数コールの間接費は、しばしば呼び
出し元ルーチンに負わせる。マクロやインライン関数は、まともなコンパイラーを使って
いればプロファイリング報告にはまったく表示されない。

さらに重要なことは、時間報告ツールの多くは、サブルーチンで費やされた時間が呼び出
し元に負うような表示をすることだ。同じルーチンに複数の呼び出し元がある場合、呼び
出し元の時間から呼び出し元の時間を素朴に差し引いても有用な結果は得られない。複数
の呼び出し元を持つ便利関数の一般的な場合は特に厄介だ。

より透明性の高い結果を得るには、インラインコードではなく、上位ルーチンができるだ
け下位ルーチンの呼び出しで構成されるようにコードを構成する。

プロファイラーを個々の性能数値を収集するためのものではなく、興味深い変数の関数と
して性能がどのように変化するかを知るためのものと考えれば、プロファイラーを使うこ
とでより多くの知見が得られるだろう。興味深い変数とは次のようなものだ：

* 問題規模
* CPU 速度
* ディスク速度
* メモリー規模
* コンパイラー最適化
* その他関連するものすべて

## Nonlocality Considered Harmful

非局所性は有害と考えられる。

コードの中心となるデータ構造と時間制約が厳しいループがキャッシュから落ちることが
ないようにしたい。

対象計算機を演算装置 (the processor) からの距離によって配列されたメモリー型の階
層として考えろ：

* プロセッサ独自のレジスター
* 命令パイプライン
* L1 キャッシュ
* L2 キャッシュ
* 場合によっては L3 キャッシュ
* 主メモリー
* スワップ領域があるディスクドライブ

演算装置が高速化するにつれて、ストレージ階層間の速度比が上昇している。そのため、
キャッシュミスの相対的な費用は増加している。

計算機資源が急落するにつれ、大きなデータ構造に期待される費用は下落する。しかし、
隣接するキャッシュ階層間の費用の広がりも大きくなっているため、キャッシュの境界を
壊すのに十分な大きさであることの性能への影響も上昇している。
<!-- plummet: to fall very quickly and suddenly -->

> “Small is beautiful” is therefore better advice than ever, particularly with
> regard to central data structures that must live in the fastest possible
> cache. The advice applies to code as well; the average instruction spends more
> time being loaded than it does executing.

ループのアンロールのようなコンパイラの最適化はもはややる価値がないかもしれない。
三角関数の表は、キャッシュミスが引き起こされるのを増やすよりも、毎回再計算する方
が速いかもしれない。

多くの最適化は一時的なものであり、費用比率が変われば、悲観的な最適化に容易に変わ
る可能性がある。それを知る唯一の方法は測定して見ることだ。

## Throughput vs. Latency

> Another effect of fast processors is that performance is usually bounded by
> the cost of I/O and — especially with programs that use the Internet — network
> transactions.

演算装置が高速であれば CPU bound ということはないから、必然的に I/O bound という
ことになるという理解で良いか？

最も重要な問題は通信の往復をできるだけ避けることだ。ハンドシェイクを必要とする通
信規約の交信はすべて、接続待ち時間を深刻な速度低下に変える可能性がある。

> so many protocol designs lose huge amounts of performance to them.

> Anytime you can get a client to do something without having to contact the
> server, you have a tremendous win. -- Jim Gettys

経験則によれば、プロファイリングで指示があるまで、可能な限り低遅延で設計し、帯域
幅費用を無視するのがよい。帯域幅の問題は通信規約ストリームを圧縮するようなごまか
しによって開発の後半で解決する。

> getting rid of high latency baked into an existing design is much, much harder
> (often, effectively impossible).

アプリケーションを書くとき、高価な計算が何度も使われることを想定して一度だけ計算
するか、実際に必要になるときにしか計算しない（何度も起こり得る）という選択に直面
することがある。このようなトレードオフに直面するほとんどの場合、正しいのは低遅延
に偏ることだ。高価な演算を事前計算しようとしないことだ。短い起動時間と素早い応答
を選ぶ方がよい。

遅延を削減するための一般的な戦略：

* 起動費用を共有できる交信の一括処理
* 交信の重複を許容する
* キャッシュ

### Batching Operations

> Graphics APIs are frequently written on the assumption that the fixed setup
> cost for a physical screen update is large.

物理的な更新の適切な間隔をプログラマーが選ぶことで、クライアントの操作感は大きく
変わる。X サーバーも、ローグライクプログラムで使用される curses(3) ライブラリー
もこのように構成されている。

永続サービスデーモンは一括処理の Unix 固有の例だ。これを書く理由は二つ：

* 明白な方は共有資源の更新を管理するためだ。
* 微妙な方は、更新を処理しないデーモンであっても同様であるが、デーモンのデータ
  ベースを読み込む費用を複数の要求にまたがって徐々に清算するためだ。

後者の完璧な例が DNS サービスデーモン named(8) だ。秒間何千もの要求を処理しなけ
ればならないことがある。

> One of the tactics that makes named(8) fast is that it replaces parses of
> expensive on-disk text files describing DNS zones with accesses to a cache
> held in memory.

ディスクよりメモリー。

### Overlapping Operations

IMAP 要求は POP3 のそれとは異なり、クライアントが生成した要求識別子でタグ付けさ
れる ([Chapter 5])。サーバーが応答するとき、その応答は関連する要求のタグを含む。

POP3 は同期的であると言える：

> POP3 requests have to be processed in lockstep by both client and server; the
> client sends a request, waits for the response to that request, and only then
> can prepare and ship the next one

一方、IMAP 要求はタグ付けされているので重ね合うことができる。IMAP クライアントが
複数のメッセージを連れてきたいことを知っている場合、IMAP サーバーに複数の要求
（それぞれ異なるタグ）をストリーミングすることが可能だ。それぞれのタグが付けられ
た応答は、サーバーの準備ができたときに返される。クライアントがまだ後の要求を送り
出す途中に、初期の要求に対する応答が来ることもある。

遅延を削減したいのであれば、ブロッキングや中間結果待ちは致命的だ。

### Caching Operation Results

<!-- throughput: an amount of work, etc. done in a particular period of time -->

高価な結果を必要に応じて計算し、後で使用するためにキャッシュすることで、いいとこ
どり（低遅延と大容量処理能力）ができる。`named` は一括処理によってだけでなく、他
のDNSサーバーとの以前のネットワーク交信の結果をキャッシュすることによっても待ち
時間を削減する。

バイナリーキャッシュを用いることで、テキストデータベースファイルに関連する解析処
理の間接費を排除するという応用を考察することで、キャッシングにおける独自の問題と
トレードオフを説明することが可能だ。

これを機能させるためには、バイナリーキャッシュを見るコードすべてが、バイナリー
キャッシュとデータベースファイル両方のタイムスタンプを検査し、マスターであるテキ
ストの方が新しければキャッシュを再生成することを知らなければならない。あるいは、
マスターへの変更はすべて、バイナリー形式を更新するようなラッパーを通して行われな
ければならない。

この方法は機能させることはできるが、SPOT 規則 ([Chapter 4]) から予想されるような
欠点がある。データの重複はストレージの経済性をもたらさないことを意味する。本当の
問題は、キャッシュとマスター間の整合を保証するコードに漏れが生じやすく、バグが発
生しやすいことで有名だということだ。高頻度で更新されるキャッシュファイルは、タイ
ムスタンプ分解能が一秒であるため、微妙な競合状態を引き起こす可能性がある。

次のような単純な事例では整合性を保証することが可能だ（それぞれにおいて後者のファ
イルがキャッシュ）：

* Python における `.py` ファイルと `.pyc` ファイル
* Emacs における `.el` ファイルと `.elc` ファイル

この技法はキャッシュへの読み取りと書き込みの両方のアクセスが単一のプログラムを経
由するため機能する。

マスターの更新パターンが複雑になると同期コードに漏れが生じやすくなる。

一般的に、バイナリーキャッシュファイルは当てにならない技術であり、避けるのが最善
だ。

> The work that went into implementing a special-purpose hack to reduce latency
> in this one case would have been better spent improving the application design
> so it doesn't have a bottleneck there — or even on tuning to improve the speed
> of the file system or the virtual-memory implementation.

キャッシングが必要な状況にあると思ったら、なぜそう思うかを問うのが賢明だ。その問
題を解決することは、キャッシングソフトウェアの極端な状況すべてで正しくすることほ
ど難しくはないことがある。

[Chapter 1]: <../context/philosophy.md>
[Chapter 4]: <./modularity.md>
[Chapter 5]: <./textuality.md>
