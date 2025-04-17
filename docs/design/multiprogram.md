# Chapter 7. Multiprogramming

[TOC]

> The most characteristic program-modularization technique of Unix is splitting
> large programs into multiple cooperating processes.

ここでは cooperating に重点が置かれていると考える。

Unix はプログラムをより単純なサブプロセスに分割し、これらの間のインターフェイス
に集中することを奨励している。基本的な方法には次の三つがある：

* プロセス起動を安上がりなものにする
* プロセスが比較的かんたんに通信できるようにする方法（リダイレクト、パイプ、
  等々）を与える
* パイプやソケットを通して渡せる、単純で透過的なテキストデータ形式の使用を奨励す
  る

安価なプロセス起動と容易なプロセス制御は Unix 式のプログラミングを可能にする重要
な要素だ。

シェルでは、パイプで接続された複数のプロセス団をバックグラウンド、フォアグラウン
ド、その混合のどれであっても走らせることは比較的容易に設定可能だ。

プログラムを協調プロセスに分割することの利点と欠点：

* 大域的な複雑さを軽減する
* プロセス間の情報やコマンドの受け渡しに使われる通信規約の設計が難しい

> In software systems of all kinds, bugs collect at interfaces.

本当の課題は通信規格の構文ではなく論理、つまり、十分に表現力があり、膠着状態にな
らない規格を設計することだ。

## Separating Complexity Control from Performance Tuning

> First, though, we need to dispose of a few red herrings.

英語では、だいじなことから目を逸らさせる人や物をアカニシンと表現することがある。

<!-- red herring: a fact, idea, or subject that takes people's attention away from the central point being considered -->

> Our discussion is *not* going to be about using concurrency to improve
> performance.

関連性の高いアカニシンの一つはスレッドだという。

スレッドは大域的な複雑さを軽減するのではなく、むしろ増大させる。切実な必要性があ
る場合を除き、避けろ。

プログラムを協働プロセスに分割するもう一つの重要な理由は、より良い安全保障のため
だ：

* プログラムを setuid を必要とするプロセスとそれ以外の大きなプロセスに分割する。
* 前者は特権プロセスで、これだけが安全保障上重要なシステム資源へのアクセスが可能
  だ。
* 両プロセスを協働する。

脚注に setuid に関する補足がある：

> A setuid program runs not with the privileges of the user calling it, but with
> the privileges of the owner of the executable. This feature can be used to
> give restricted, program-controlled access to things like the password file
> that nonadministrators should not be allowed to modify directly.

少し調べたら `passwd` の例が出てきて、これなら setuid の概念を理解しやすいと思っ
た。次のようなものだ：この実行形式を一般使用者が実行するとその所有者である root
の権限でプロセスが走る。その結果、一般使用者であっても所有者が root であるファイ
ル `/etc/shadow` を変更することが可能となる。

## Taxonomy of Unix IPC Methods

最も単純な構成が最も良い。

### Handing off Tasks to Specialist Programs

術語 shell out を定義する一文：

> In the simplest form of interprogram cooperation enabled by inexpensive
> process spawning, a program runs another to accomplish a specialized task.
> Because the called program is often specified as a Unix shell command through
> the system(3) call, this is often called *shelling out* to the called program.

協調の流れ：

1. 呼び出されたプログラムは、キーボードと画面を継承し、完了まで実行される。
2. 終了すると、呼び出し元プログラムがキーボードと画面の制御を取り戻し、実行を再
   開する。

この型のプログラム間の通信がない協調において、交信規格設計は問題ではない。

Unix の典型的な shell out はテキストエディター呼び出しだ：

> In the Unix tradition one does *not* bundle purpose-built editors into programs
> that require general text-edited input. Instead, one allows the user to
> specify an editor of his or her choice to be called when editing needs to be
> done.

このために環境変数 `EDITOR` や `VISUAL` を呼び出し元プログラムとは独立して指定可
能なのだ。プログラムによっては固有の環境変数 (e.g. `GIT_EDITOR`) が存在すること
もある。

> The specialist program usually communicates with its parent through the file
> system, by reading or modifying file(s) with specified location(s); this is
> how editor or mailer shellouts work.

エディターに当たるほうが専門プログラムだ。

> They key point about all these cases is that the specialist programs don't
> handshake with the parent while they are running.

この文脈で言う handshake は交信確立とか応答確認などの意味に取れ。

#### Case Study: The `mutt` Mail User Agent

[Mutt] は簡単な画面指向のインターフェイスを備えたメールクライアントだ。単一キー
ストロークのコマンドでメールを閲覧したり読んだりできる。

Mutt をメール作成で使う場合、使用者はコマンドライン引数としてアドレスを指定して
呼び出すか、返信コマンドの一つを使って呼び出す。このとき、Mutt は環境変数
`EDITOR` を参照する。メール本文執筆用に一時ファイル名を生成し、`EDITOR` の値を一
時ファイル名を引数として呼び出す。

> Almost all Unix mail- and netnews-composition programs observe the same
> convention.

要点はここから：

> An important variant of this strategy shells out to a small proxy program that
> passes the specialist job to an already-running instance of a big program,
> like an editor or a Web browser.

「すでに動作中の」というのがキモで、変数 `EDITOR` が指すプログラムが巨大で起動が
重いようなものでも、動作中のプロセスそのものがポップアップして、一時ファイルがそ
こに閲覧・編集可能な状態で現れることが使用者に期待される（そういう動作を促すよう
な代行プログラムを shell out する）。

また、本書では `EDITOR=emacsclient` だが、WSL 環境で Windows 側の Visual Studio
Code を使う場合にも同じ議論が適用される。設定は `EDITOR=code` だ。

### Pipes, Redirection, and Filters

Unix パイプの発明者は Doug McIlroy という人物だ：

> After Ken Thompson and Dennis Ritchie, the single most important formative
> figure of early Unix was probably Doug McIlroy. His invention of the *pipe*
> construct reverberated through the design of Unix, encouraging its nascent
> do-one-thing-well philosophy and inspiring most of the later forms of IPC in
> the Unix design (in particular, the socket abstraction used for networking).

パイプはどのプログラムも最初から標準入力と標準出力を利用できるという慣例に依存し
ている。

> Many programs can be written as *filters*, which read sequentially from
> standard input and write only to standard output.

パイプ操作は、あるプログラムの標準出力を別のプログラムの標準入力に接続する。こ
のように接続されたプログラムの連鎖をパイプラインと呼ぶ。例えば

```console
ls | wc
```

と書くと、現在のディレクトリ一覧の文字数、単語数、行数が表示される。

McIlroy 本人が気に入っているパイプラインの一つは `bc | speak` であるという。ゆっ
くりボイスに数字を読み上げさせるようなものだろう。

> It's important to note that all the stages in a pipeline run concurrently.

この性質があるので先のパイプラインは `ls > foo; wc < foo` よりも効率が良い。

パイプの大きな弱点は一方通行であることだ。 パイプライン成分はパイプを停止する以
外の方法で制御情報をパイプに戻すことはできない。

#### Case Study: Piping to a Pager

全部見るにはスクロールが必要であるほど出力が縦方向に長くなりがちな `ps` と、
標準入力を画面縦寸法に分割して表示する `more` を組み合わせる。

```console
ps | more
```

このようにタイプして ps(1) の出力を more(1) の入力に渡すと、それぞれのキースト
ロークの後に、プロセス一覧のページサイズの断片が順番に表示される。

> The ability to combine programs like this can be extremely useful. But the
> real win here is not cute combinations; it's that because both pipes and
> more(1) exist, *other programs can be simpler*.

* ps(1), ls(1), ... がそれぞれ個別にページャーを実装する必要がない。
* ページャーをカスタマイズしたい場合は `more` の部分だけをカスタマイズすればいい。

実際、現代では more(1) ではなく less(1) を利用するのが普通だ。後者は上にもスク
ロール可能だ。

#### Case Study: Making Word Lists

これは実際に実行してみるといい：

```console
tr -c '[:alnum:]' '[\n*]' | sort -iu | grep -v '^[0-9]*$'
```

標準入力には、本書の適当なパラグラフをコピー＆ペースト。するとこのパイプライン
は：

> Together, these generate a sorted wordlist to standard output from text on
> standard input.

#### Case Study: `pic2graph`

シェルスクリプトの一部が抜粋されているが、パイプは一箇所しかない。サブシェルの結
果をパイプで `groff` に流すという構造だ。

> All these details are hidden from the user, who simply sees PIC source go in
> one end and a bitmap ready for inclusion in a Web page come out the other.

次の観点によりこの例を示したとある：

> This is an interesting example because it illustrates how pipes and filtering
> can adapt programs to unexpected uses. The program that interprets PIC,
> pic(1), was originally designed only to be used for embedding diagrams in
> typeset documents.

#### Case Study: bc(1) and dc(1)

これを読むまで勘違いしていたが、逆ポーランド記法は（逆だから）オペランドを先に書
く。演算子を後ろに書く。

* dc(1) プログラムは逆ポーランド記法 (RPN) からなるテキスト行を標準入力で受け取
  り、計算された答えを標準出力に出力する。
* bc(1) プログラムは従来の代数記法に似た、より精巧な中置構文を受け付ける。

古いバージョンの bc(1) は自身では計算を行わず、パイプ経由で dc(1) にコマンドを渡
していた。次のように役割を分担していた：

* bc(1) は変数の代入と関数の展開を行い、中置記法を逆ポーランド記法に変換する。
* dc(1) は RPN 変換された入力式を受け取って評価する。

このように機能を分離しておくことには利点がある：

> It means that users get to choose their preferred notation, but the logic for
> arbitrary-precision numeric calculation (which is moderately tricky) does not
> have to be duplicated. Each of the pair of programs can be less complex than
> one calculator with a choice of notations would be. The two components can be
> debugged and mentally modeled independently of each other.

#### Anti-Case Study: Why Isn't fetchmail a Pipeline?

パイプラインの単方向性とメールクライアントは相性が悪い。

> One of the things the fetcher program (`imap` or `pop`) would have to do is
> decide whether to send a delete request for each message it fetches.

現在の `fetchmail` の編成ではローカルの SMTP リスナーがメッセージの責任を引き受
けたことがわかるまで、POP/IMAP サーバーへの要求送信を遅らせることができる。本書
の小さい部品＋パイプライン編成ではその特性を失うことになる。

### Wrappers

ラッパーは呼び出されたプログラムに対して新しいインターフェイスを作成したり、それ
を特殊化したりするものだ。専門化といったほうがいいか？

* ラッパーは多くの場合、シェルパイプラインの詳細を隠すために使われる。
* 実行中に二つのプログラムが通信することはないため、関連する通信規約は存在しない。
* 呼び出されるプログラムの動作を変更する引数を備えるものがある。

#### Case Study: Backup Scripts

ワンライナーであってもラッパーはラッパーだ：

```bash
tar -czvf /dev/st0 "$@"
```

> This is a wrapper for the tar(1) tape archiver utility which simply supplies
> one fixed argument (the tape device `/dev/st0`) and passes to tar all the other
> arguments supplied by the user (“`$@`”).

まさに上の内容とよく似た、ストレージの内容を rsync(1) で別のストレージにバック
アップするスクリプトを用意することが普通にある。

### Security Wrappers and Bernstein Chaining

ラッパースクリプトの一般的な使い方の一つに安全保障ラッパーがある。安全保障スクリ
プトはある種の証明書を検査する守衛プログラムを呼び出し、守衛が返す値に基づいて条
件付きで別のプログラムを実行することができる。

> Bernstein chaining is a specialized security-wrapper technique first invented
> by Daniel J. Bernstein, who has employed it in a number of his packages.

この人物は暗号学教授でもある。

Bernstein 連鎖はパイプラインのようなものであり、連続する各段階がそれと同時に実行
されるのではなく、直前の段階を置き換えるものだ。

<!-- to confine: to limit an activity, person, or problem in some way -->

通常の応用例としては、保安特権を有するアプリケーションをある種の守衛プログラムに
閉じこめ、その守衛プログラムからより特権の低いアプリケーションに状態を渡すことが
できる。この技法を `exec`/`fork` で組み合わせて、複数のプログラムを貼り合わせる。

> Each program performs some function and (if successful) runs exec(2) on the
> rest of its command line.

次のような実例がある。説明文がチンプンカンプンで理解できなかった：

* rblsmtpd パッケージ
* qmail パッケージ
* qmail-popup プログラム

Bernstein 連鎖はアプリケーションの初期段階で特権を要し、それが不要となる後続処理
で特権を外したいときに便利だ。

この技法の良い性質：

* `exec` の後、子プログラムは真の使用者 ID を root に戻すことはできない。
* 連鎖に別のプログラムを挿入することでシステムの動作を変更できるので、単一プロセ
  スよりも柔軟性がある。

### Slave Processes

時折、子プログラムは、標準入出力に接続されたパイプを通じて、呼び出し元からデータ
を受け取り、呼び出し元にデータを返すという対話的な処理を行うことがある。この方式
では上述したどのパターンとも異なり、次の条件がある：

> both master and slave processes need to have internal state machines to handle
> a protocol between them without deadlocking or racing.

主プロセスは呼び出し元が自分のスレーブコマンドを設定できるようなコマンドラインス
イッチや環境変数を支援するのが良い習慣だ：

> Among other things, this is useful for debugging; you will often find it handy
> during development to invoke the real slave process from within a harness that
> monitors and logs transactions between slave and master.

自作プログラムにおいて主従プロセスの相互作用が怪しくなってきたと感じたら、ソケッ
トや共有メモリーのような技法を使って、peer-to-peer 編成への移行を考える潮時であ
ることがある。

#### Case Study: `scp` and `ssh`

scp(1) コマンドは ssh(1) を従プロセスとして呼び出し、`ssh` の標準出力から、プロ
グレスバーのアスキーアニメーションとして報告を再整形するのに十分な情報を傍受する。

### Peer-to-Peer Inter-Process Communication

通信やネットワーキングでは通常、双方向にデータが自由に流れる peer-to-peer の情報
経路が頻繁に必要となる。

#### Tempfiles

協調プログラム間で一時ファイルを用いて情報を交換するプロセス間通信技法手法は最も
古い。欠点はあるが、シェルスクリプトや、より精巧で協調的な通信方法が過剰な一回限
りのプログラムでは、今でも有用な手法だ。

この技法の問題点：

* 一時ファイルを削除する前に処理が中断された場合、ゴミが放置されがちだ。
* 一時ファイルに同じ名前を使った複数のプログラムのプロセス間で衝突が起こる。
* 一時ファイルを書き込む場所を攻撃者が知っている場合に、下記の問題が生じる。

問題点その二は程度の低いプログラマーがやりがちだ。現代なら対処法がさらにいろいろ
ある。

問題点その三：

> it can overwrite on that name and possibly either read the producer's data or
> spoof the consumer process by inserting modified or spurious data into the
> file. This is a security risk. If the processes involved have root privileges,
> this is a very serious risk.

<!-- to spoof: to pretend to be someone -->
<!-- spurious: based on false reasoning or information that is not true -->

先述のエディターの事例は一時ファイルのそれでもある。

#### Signals

信号はプロセス間通信機能として設計されたものではない。OS が特定のエラーや緊要の
イベントをプログラムに通知する方法として設計されたものだ。例：

* `SIGHUP` 信号は、ある端末セッションが終了すると、そのセッションから起動
  されたすべてのプログラムに送られる。
* `SIGINT` 信号は使用者が現在定義されている割り込み文字 (`C-c`) を入力すると、現
  在キーボードに接続されているすべてのプロセスに送られます。

信号はプロセス間通信の状況によっては役に立つこともある。POSIX 標準の信号集合には
この用途を目的とした信号 `SIGUSR1` と `SIGUSR2` が含まれている：

They are often employed as a control channel for *daemons* (programs that run
constantly, invisibly, in background), a way for an operator or another program
to tell a daemon that it needs to either reinitialize itself, wake up to do
work, or write internal-state/debugging information to a known location.

信号プロセス間通信でよく使われる技法は、いわゆる pid ファイルだ。プロセス ID を
含む小さなファイルを指す。

* 信号が必要なプログラムは pid ファイルを既知の場所に書き込む。
* 他のプログラムはその pid ファイルを読んでプロセス ID を知る。
* ロックファイルの役目を果たすこともある。

信号を N 個受信しても N 回処理するとは限らない。

> Depending on what variant of signals semantics the system supports, the second
> and later instances may be ignored, may cause an unexpected process kill, or
> may have their delivery delayed until earlier instances have been processed
> (on modern Unixes the last is most likely).

脚注に競合状態の定義が述べられている：

> A ‘race condition’ is a class of problem in which correct behavior of the
> system relies on two independent events happening in the right order, but
> there is no mechanism for ensuring that they actually will. Race conditions
> produce intermittent, timing-dependent problems that can be devilishly
> difficult to debug.

<!-- intermittent: not happening regularly or continuously -->

#### System Daemons and Conventional Signals

`SIGHUP` と `SIGTERM` について述べられている。

`SIGHUP` はもともとは、モデム接続を切断したときに発生するような、シリアル回線降
下時にプログラムに送信される信号だった。

次のシステムデーモンは再初期化（つまり rc ファイルを更新して再起動したい）の信号
として `SIGHUP` を受け付ける：

* bootpd(8)
* gated(8)
* inetd(8)
* mountd(8)
* named(8)
* nfsd(8)
* ypbind(8)

`SIGTERM` は `SIGKILL` とは異なりていねいに停止する。一時ファイルのクリーンアッ
プ、データベースへの最終更新のフラッシュなどを含むことが多い。

> When writing daemons, follow the Rule of Least Surprise:

これらの規約を使用し、手引書を読んで既存の手本を探すことだ。

#### Case Study: `fetchmail`'s Use of Signals

`fetchmail` をデーモンモードで走らせるときの挙動：

* 構成ファイルで定義されたすべてのリモートサイトからメールを定期的に収集する
* ユーザーの介入なしにポート 25 のローカル SMTP リスナーにメールを渡す
* 収集の試行と試行の間に使用者定義の間隔で sleep する

引数なしで `fetchmail` を起動するとデーモンがすでに起動中かどうかを調べる。

* No: 構成ファイルに従いながら上記のごとく起動する。
* Yes: 新しい `fetchmail` プロセスは古いそれに信号を送る。デーモンプロセスはすぐ
  に覚醒してメールを収集し、新しいプロセスは停止する。

#### Sockets

!!! note TODO
    ソケットプログラミングを全然知らないので内容が頭に入らない。出直してくる。

ソケットを介して通信するプログラム同士は通常、双方向のバイトストリームを見ること
になる。このバイトストリームの性質はこう：

* 直列化されている（バイト列は送信されたその順番に受信される）
* 信頼性が高い
* ソケットディスクリプターは一度取得すると、基本的にファイルのそれのように動作す
  る

次の警句はローカルマシンで閉じた I/O と、リモートマシンとの I/O との違いをわかり
やすく表現している：

> Local I/O is ‘yes/no’. Socket I/O is ‘yes/no/maybe’. And nothing can ensure
> delivery — the remote machine might have been destroyed by a comet. (Ken
> Arnold)

次の段落は何を述べているのか全くわからない。私の学習不足だ：

> At the time a socket is created, you specify a protocol family which tells the
> network layer how the name of the socket is interpreted. ...

双方向プロセス間通信にはソケットを使うのが通常は正しい：

> All modern Unixes support BSD-style sockets, and as a matter of design they
> are usually the right thing to use for bidirectional IPC no matter where your
> cooperating processes are located.

現代では、分散運用のためにコードを scale up する必要があることを想定しておくのが
よい。

> The separation of address spaces that sockets enforce is a feature, not a bug.

ソケットをそつなく使うには、ソケット間で使うアプリケーションプロトコルを設計する
ことから始めろ。アプリケーションプロトコル設計の議論については[第五章](./textuality.md)を見ろ。

##### Case Study: PostgreSQL

PostgreSQL の編成：

* サーバー (`postmaster`)
    * データベースファイルへ排他的にアクセスすることが可能。
    * マシン一台につきサーバープロセス一つが裏で稼働する。
    * TCP/IP ソケットを通して SQL で要求を聞く。テキスト形式で応答する。
    * 複数クライアントを同時に扱うことが可能。互いの要求を干渉しないように要求を
      直列化する。
* クライアントが少なくとも三つ
    * サーバーへのセッションを開始する
    * サーバーと SQL 交信を行う
    * データベースがどのように保存されているかは知らない
    * それぞれが異なる UI を備えることも可能。

このような構成は Unix データベースではごく一般的なもので、SQL クライアントと
サーバーを混在させることがしばしば可能なほどだ。

##### Case Study: Freeciv

[Freeciv] については[前章](./transparency.md)で。

> But more critical to the way it supports multiplayer gaming is the
> client/server partitioning of the code.

オンラインゲームであるので、アプリケーションがネットワークのあちらこちらに分散し
ているという前提に注意。

* 実行中のゲームの状態はゲームエンジンであるサーバープロセスが維持する。ゲームロ
  ジックはすべてサーバーが処理する。
* 実行中のプレイヤーは GUI クライアントを実行し、パケットプロトコルを通じて情報
  やコマンドをサーバーを相手に交換する。GUI の詳細はクライアントが処理する。クラ
  イアントによって異なるインターフェースが与えられている。

これは多人数参加型オンラインゲームの典型的な構成だ。

ソケット通信規約の使い分けに関するコメント。この本は 2003 年に執筆されたが、現代
でもこのように実装されるはずだ：

> The packet protocol uses TCP/IP as a transport, so one server can handle
> clients running on different Internet hosts. Other games that are more like
> real-time simulations (notably first-person shooters) use raw Internet
> datagram protocol (UDP) and trade lower latency for some uncertainty about
> whether any given packet will be delivered.

<!-- lag: the act of slowing down or falling behind -->

#### Shared Memory

通信を行うプロセスが同じ物理メモリーにアクセスできるのであれば、共有メモリーはそ
れらのプロセス間で情報を受け渡す最速の方法となる。

> Shared memory may be disguised under different APIs, but on modern Unixes the
> implementation normally depends on the use of mmap(2) to map files into memory
> that can be shared between processes.

Python でも名前が `mmap` というモジュールを使う。

共有メモリーを利用するプログラムは、通常、共有部にある手旗信号変数を使用して競合
と膠着の問題を自分で処理しなければならない。マルチスレッディングでの問題に似てい
るが、«more manageable because default is *not* to share memory» であり、より御
しやすい。

共有メモリーの応用例：

* Apache Web サーバー得点表機能：主プロセスと Apache 像の負荷共有プール間の通信。
* X の実装：クライアントとサーバーが同じマシンに常駐している場合。ソケット通信の
  オーバーヘッドを避けるために、ライアントとサーバー間で巨大な画像を受け渡す。

> The mmap(2) call is supported under all modern Unixes, including Linux and the
> open-source BSD versions; this is described in the Single Unix Specification.
> It will not normally be available under Windows, MacOS classic, and other
> operating systems.

本書出版時とは異なる可能性アリ。あるいは同名の機能があるが似て非なるものである可
能性アリ。

Unix のプロセス間通信は二通りに進化した：

> The BSD direction led to sockets. The AT&T lineage, on the other hand,
> developed named pipes (as previously discussed) and an IPC facility,
> specifically designed for passing binary data and based on shared-memory
> bidirectional message queues.

名前付きパイプはソケットに取って代わられたのだった。

低水準：

> The lower layer, which consists of shared memory and semaphores, still has
> significant applications under circumstances in which one needs to do
> mutual-exclusion locking and some global data sharing among processes running
> on the same machine.

共有メモリーと手旗信号機能 (shmget(2), semget(2), etc.) を使うことでネットワーク
通信核心部を介したデータコピーの経常的負担を避けることができる。

## Problems and Methods to Avoid

TCP/IP を介した BSD 流ソケットが Unix のプロセス間通信手法の主流だ。

時代遅れの手法の中にはまだ完全に死滅していないものもあり、他の OS から実用性に疑
問のある手法が輸入されている。

### Obsolescent Unix IPC Methods

Unix の歴史は時代遅れのプロセス間通信とネットワークモデルに結びついた API の死骸
にまみれている。

* 最終的には BSD ソケットが勝利し、プロセス間通信はネットワークに統合された。
* Unix の文書には歴史的遺物がまだ使われているかのような誤解を与えるような言及が
  ある可能性が高いので、知っておくと便利だ。

> The real explanation for all the dead IPC facilities in old AT&T Unixes was
> politics. The Unix Support Group was headed by a low-level manager, while some
> projects that used Unix were headed by vice presidents. They had ways to make
> irresistible requests, and would not brook the objection that most IPC
> mechanisms are interchangeable. -- Doug McIlroy

死因の真相が政治ならば、設計や性能は死ぬほどのものではなかったと解釈できる？

#### System V IPC

System V プロセス間通信機能は先述の共有メモリー機能を基にしたメッセージ送受機能
だ。

System V プロセス間通信機能は Linux や他の現代的な Unix にもある。遺物につき使わ
れることはあまりない。

#### Streams

大文字の方を中心に読むしかない。

Dennis Ritchie が考案したネットワーキング実装の再実装版 STREAMS に関する記述をこ
のノートでは拾っていく。

* STREAMS は System V 3.0 (1986) で初めて利用可能になった。
* STREAMS 機能はユーザープロセスとカーネル内の指定されたデバイスドライバーとの間
  の全二重インターフェイス（鉄道の複線を連想するといい？）を搭載していた。

  > The device driver might be hardware such as a serial or network card, or it
  > might be a software-only pseudodevice set up to pass data between user
  > processes.

興味深い特徴（私にはチンプンカンプン）：

> it is possible to push protocol-translation modules into the kernel's
> processing path, so that the device the user process ‘sees’ through the
> full-duplex channel is actually filtered.

この機能は、例えば、端末デバイス用の行編集規約を実装するために使用できる。あるい
は、IP や TCP のような規約をカーネルに直接配線せずに実装することもできる。

元々の Streams はとある厄介な機能を一掃する試みとして生まれたが、時代が進んでそ
の厄介事を生む環境が姿を消していくにつれ、STREAMS が有する柔軟性も有用性を失って
いったというようなことを述べている。

Linux をはじめとするオープンソースの Unix は STREAMS を事実上破棄 (have
effectively discarded) している。

### Remote Procedure Calls

遠隔手続き呼出しをインポートする企てがほとんど失敗する理由を考察している。

第一は遠隔手続き呼出しインターフェイスが容易に発見可能でないことだ：

> that is, it is difficult to query these interfaces for their capabilities, and
> difficult to monitor them in action without building single-use tools as
> complex as the programs being monitored

[第六章](./transparency.md)で原因を検討したのだった。

関連する問題として、より豊富な型シグネチャーを持つインターフェイスはより複雑に、
したがってより脆くなる傾向がある。次の文章に続くのだが、難し過ぎて意味が汲めない：

<!-- brittle: delicate and easily broken -->

> Over time, they tend to succumb to ontology creep as the inventory of types
> that get passed across interfaces grows steadily larger and the individual
> types more elaborate. Ontology creep is a problem because structs are more
> likely to mismatch than strings; if the ontologies of the programs on each
> side don't exactly match, it can be very hard to teach them to communicate at
> all, and fiendishly difficult to resolve bugs. The most successful RPC
> applications, such as the Network File System, are those in which the
> application domain naturally has only a few simple data types.

NFS のような最も成功した RPC アプリケーションはアプリケーションドメインが元から
わずかな単純データ型しか持たないものだ。

古典的な RPC では、物事を単純に保つのではなく、複雑で漠然とした方法で行うのは簡
単過ぎる。

* Windows COM と DCOM はいかに悪い方向に向かうかを示す典型的
* Apple は OpenDocを放棄した
* CORBA も Java RMI も、Unix の世界では姿を消していった

> Andrew S. Tanenbaum and Robbert van Renesse have given us a detailed analysis
> of the general problem in *A Critique of the Remote Procedure Call Paradigm*,
> a paper which should serve as a strong cautionary note to anyone considering
> an architecture based on RPC.

Unix の伝統は透明で発見可能なインターフェイスを強く好む。これは、Unix 文化がテキ
スト通信規約によるプロセス間通信に執着し続けている背景の一つだ。

> It is often argued that the parsing overhead of textual protocols is a
> performance problem relative to binary RPCs

これに対し、次の二点からバイナリー RPC のほうが遅延問題悪化傾向がはるかにあると
述べる：

* RPC インターフェイスは、ある呼び出しがどれだけのデータのシリアライズを伴うかを
  容易に予測できない
* RPC モデルはプログラマーがネットワーク交信を経費無料として扱うことを奨励する傾
  向がある

仮にテキストストリームが RPC より効率が劣ったとしても、次で取り戻せる：

* 開発時間を増やしたり、構造を複雑にしたりするよりも、ハードウェアを増強すること
  で対処可能。
* より単純、モデル化しやすい、理解しやすいシステムを設計する能力がある。

今日、RPCとUnixのテキストストリームへの愛着は、XML-RPCやSOAPのようなプロトコルに
よって、興味深い形で収束しつつある。 これらのプロトコルは、テキストで透過的であ
るため、Unixプログラマーにとっては、醜くて重いバイナリー・シリアライゼーション・
フォーマットよりも使いやすい。 Tanenbaumとvan Renesseが指摘したような一般的な問
題をすべて解決するわけではないが、テキストストリームとRPCの両方の長所を兼ね備え
ている。

> Today, RPC and the Unix attachment to text streams are converging in an
> interesting way, through protocols like XML-RPC and SOAP. （中略） they do in
> some ways combine the advantages of both text-stream and RPC worlds.

### Threads — Threat or Menace?

Unix の開発者にはスレッド（アドレス空間全体を共有するプロセス）を使用する伝統は
ない。スレッドは最近他から輸入されたものだという。

Unix はプロセス起動が安く付くので、独自のアドレス空間を持つ軽量プロセスに対して
スレッドの代用品には適切でない。

> the idea of threads is native to operating systems with expensive
> process-spawning and weak IPC facilities.

定義上、通常プロセスの娘（原文）スレッドは皆同じ大域的記憶域を共有する。

> The task of managing contentions and critical regions in this shared address
> space is quite difficult and a fertile source of global complexity and bugs.

<!-- fertile: fertile land or soil is able to produce -->

スレッドは、互いの内部状態を知り過ぎてしまうため、バグの発生源となりやすい。プロ
セス間通信ならばアドレス空間が自動的にカプセル化しているが、そういうものがない。
それゆえ、スレッド化されたプログラムは、通常の競合問題だけでなく、タイミングに依
存する全く新しい区分のバグに悩まされる。

TLS という記憶域が発明された。

> Threads often prevent abstraction. In order to prevent deadlock, you often
> need to know how and if the library you are using uses threads in order to
> avoid deadlock problems. Similarly, the use of threads in a library could be
> affected by the use of threads at the application layer. -- David Korn

まだある。スレッド化には従来のプロセス分離に対する利点を損なう性能代価がある。
スレッド化によってプロセスコンテキストを高速に切り替える経常費用をある程度取り除
くことはできるが、スレッド同士が互いに踏み合わないように共有データ構造をロックす
ることは同じくらい代償が付く。

この問題は根本的であり、対称型マルチプロセッシングのための Unix カーネルの設計に
おいても継続的な問題であった：

> As your resource-locking gets finer-grained, latency due to locking overhead
> can increase fast enough to swamp the gains from locking less core memory.

読書案内：

> For more discussion and a lucid contrast with event-driven programming, see
> *Why Threads Are a Bad Idea*.

## Process Partitioning at the Design Level

関連技法一覧：

* 一時ファイル
* 主従プロセス関係
* ソケット
* 遠隔手続き呼出し
* それ以外の双方向プロセス間通信

上記の技法はある水準では等価だ。違いは次の縁にある。

* プログラムがどのように通信を確立するか
* いつどこでメッセージの表現形式変換を行うか
* どのような種類の一時保存問題が発生するか
* どの程度までメッセージの不可分性を保証するか

PostgreSQL のクライアントとサーバーはソケットを介して通信する。他の双方向プロセ
ス間通信方式を仕様しても設計の型はほとんど同じだろう。

サーバーとクライアントに分割して双方向通信をするという設計はアプリケーションの複
数の実体が、すべての実体間で共有される資源へのアクセスを管理する必要がある状況で
特に効果的だ。次のどちらでもいい：

* 単一のサーバープロセスが資源の競合を管理する
* 協力し合う同格の実体それぞれが死活的な資源を管理する

この分割設計は命令サイクルを大量に消費するアプリケーションを複数のサーバーに分散
させるのにも役立つ。インターネットを介した分散計算に適していることがある。

これらの peer-to-peer プロセス間通信技術はすべて似ている。評価判断は主に次だ：

* プログラム複雑度の経常費用
* 設計にもたらす不透明性の程度

> This, ultimately, is why BSD sockets have won over other Unix IPC methods, and
> why RPC has generally failed to get much traction.

スレッドは根本的に異なる。異なるプログラム間の通信ではなく、単一プログラムのプロ
セス内での時分割方式のようなものだ。

> threading is strictly a performance hack. It has all the problems normally
> associated with performance hacks, and a few special ones of its own.
>
> Accordingly, while we should seek ways to break up large programs into simpler
> cooperating processes, the use of threads within processes should be a last
> resort rather than a first.

スレッドよりプロセスと憶えておこう。

> If you can use limited shared memory and semaphores, asynchronous I/O using
> SIGIO, or poll(2)/select(2) rather than threading, do it that way. Keep it
> simple;

次の三つの組み合わせは特に危険であるという：

* スレッド
* 遠隔手続き呼び出しインターフェース
* 重量級のオブジェクト指向設計

この手のプロジェクトに巻き込まれたら逃げ出してもいいとまで述べている。

実世界でのプログラミングは複雑性をどうにかするのがそのすべてだ。

> Tools to manage complexity are good things. But when the effect of those tools
> is to proliferate complexity rather than to control it, we would be better off
> throwing them away and starting from zero.

[Mutt]: <http://www.mutt.org/>
