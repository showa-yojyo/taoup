# Chapter 3. Contrasts

Unix の古典的な方法と、他の主要な OS 固有の設計やプログラミング様式を比較するこ
とが、Unix の OS としての設計と、その周辺で発展してきたプログラム設計の哲学との
関連をたどるのに有益だと著者は言う。

<!-- condescending: treating someone as if you are more important or more intelligent than them -->

[TOC]

## The Elements of Operating-System Style

全体的に見て、OS に関する設計とプログラミングの様式は次の三つに起源があるという：

* OS 設計者の意図
* プログラミング環境における経費と制限が強制する統一性
* 成り行き任せの文化上の偏り

### What Is the Operating System's Unifying Idea?

Unix と他の OS を対比する際の最も基本的な質問は次のようなものだという：

> Does it have unifying ideas that shape its development, and if so how do they
> differ from Unix's?
>
> To design the perfect anti-Unix, have no unifying idea at all, just an
> incoherent pile of ad-hoc features.

Unix と正反対の OS とは何であるかを即答している。面白い。

### Multitasking Capability

> One of the most basic ways operating systems can differ is in the extent to
> which they can support multiple concurrent processes.

現代人の感覚からすると、複数プロセスの同時実行はあって当然だろうと考える。

次の事実は必修：

> Unix has *preemptive multitasking*, in which timeslices are allocated by a
> scheduler which routinely interrupts or pre-empts the running process in order
> to hand control to the next one. Almost all modern operating systems support
> preemption.

スケジューラーという主体が OS に存在して、プロセスの集合に対して実行期間の順序と
時間を計画的に割り当てる。次のプロセスが制御できるように、今のプロセスに割り込
み、つまり先取りして実行期間を充てがう。

なお、マルチユーザー機能はここでは忘れていい。

以上により、正反対の Unix の設計には次のいずれかを必要とする：

* マルチタスクをまったくサポートしない
* マルチタスクは支援するが、プロセス管理を多くの制約や特殊な状況で囲い込み、それ
  を実際に利用するのがかなり難しい

### Cooperating Processes

マルチプロセスの話題の次はプロセス間通信だ。

> In the Unix experience, inexpensive process-spawning and easy inter-process
> communication (IPC) makes a whole ecology of small tools, pipes, and filters
> possible.

プロセスの生成が高価であったり、制御が困難で柔軟性に欠けたりすることがあってはな
らない。

パイプ等のプロセス間通信手段の重要な性質に、通信するプログラム同士の機能分離を促
進するのに単純な水準に抑えるというものがある。

プロセス間通信手段がないシステムでは、プログラム間では精巧なデータ構造を共有する
ことで通信を行う。この構造の問題点は、通信するプログラムの種類が増えるとデータ構
造が平方オーダーで増大することだ。本書では MS Office 製品を例に挙げている。

<!-- promiscuous: 見さかいのない -->

以上により、正反対の Unix の設計には次のすべてを必要とする：

* プロセス生成を著しく高価なものにする
* プロセス制御を困難で柔軟性のないものにする
* プロセス間通信を支援しないか、中途半端に支援された後付けのものにする

### Internal Boundaries

最初のパラグラフはコマンド `rm -rf *` の実行に確認メッセージが出ない事実と、一般
に権限が異なる複数アカウントの支援との関係について述べていて興味深い。

Unix には少なくとも三階層の内部境界層がある。目的は悪意のある使用者やバグのある
プログラムから防護するというものだ：

* メモリー管理 (MMU)
* 特権グループ
* 安全機密上重要な機能を、信頼できるコードの可能な限り小さな断片に限定する

Unix はハードウェアのメモリー管理ユニット(MMU) を使って、別々のプロセスが他のプ
ロセスのメモリーアドレス空間に侵入しないようにしている。

一般アカウントのプロセスは、許可なく他のアカウントのファイルを変更したり、読んだ
りすることは不可能だ。

正反対の Unix の設計には次のすべてを必要とする：

* 暴走プロセスが実行中のプログラムを破壊、毀損可能であるように、メモリー管理を破
  棄、回避する。
* 特権グループが弱いか、存在しない。
* シェルや GUI 全体のような大量のコードを信頼する。それにより、当該コードにバグ
  があったり攻撃が成功したりすると、システム全体への脅威となる。

他者のファイルを改竄可能であるということは、例えば、マクロウイルスがワープロの制
御を奪取し、ハードドライブを初期化することの可能性を意味する。

### File Attributes and Record Structures

> Unix files have neither record structure nor attributes.

正反対の Unix の設計には次のすべてを必要とする：

* 面倒なレコード構造の集合を用意する。
* ファイル属性を追加する。システムがそれに大きく依存するようにする。

### Binary File Formats

本書の邦訳版を初めて読んだときに、最初に感動したのはこの節だったと記憶している。

バイナリーファイルがテキストファイルに劣る状況、理由は、次の二つをまずは憶えてお
けばいい：

* フィルターが役に立たない
* データファイルへのアクセスは専用ツールからのみとなる

後者の弊害は、開発者がデータファイルよりもツールを中心に考えるようになり、異なる
バージョンのデータファイルに互換性がなくなることだ。

> To design the perfect anti-Unix, make all file formats binary and opaque, and
> require heavyweight tools to read and edit them.

OS に直接関わらないファイルにも、これらの要件を求めていることに注意。

### Preferred User Interface Style

> The Unix lesson is the opposite: that weak CLI facilities are a less obvious
> but equally severe deficit.

CLI 機能が貧弱であることは目立たないものの、致命的な弱点であると考えるのが Unix
式だ。

> To design the perfect anti-Unix, have no CLI and no capability to script
> programs — or, important facilities that the CLI cannot drive.

正反対の Unix の設計には次のいずれかを必要とする：

* CLI がなく、かつプログラムをスクリプト化する機能がない
* CLI では操作できない重要な機能がある

### Intended Audience

PC ばかり利用していると、OS 設計はシステムを使用する人により決まるという観点が
すっぽりと抜け落ちる。次を読んで反省する：

> The design of operating systems varies in response to the expected audience
> for the system. Some operating systems are intended for back rooms, some for
> desktops. Some are designed for technical users, others for end users. Some
> are intended to work standalone in real-time control applications, others for
> an environment of timesharing and pervasive networking.

OS の重要な区分の一つにクライアントとサーバーがある。クライアントは次のように説
明される：

* 軽量
* 単一の使用者だけを支援する
* 小さな機械で稼働できる
* 用事が済んだら電源を切ることが可能であること
* プリエンプティブマルチタスクがない
* 低遅延のために最適化されている
* 派手な UI に資源の多くを費やしている

サーバーは次のように説明される：

* 重量級
* 連続稼動が可能
* 単位時間あたりの処理量が最適化されている
* 複数セッションを処理するために完全 pre-emptively multitasking である

> Unix is often said to have been written by programmers for programmers — an
> audience that is notoriously tolerant of interface complexity.

寛容なことが悪いことで知られるのは困ったものだ。

<!-- notoriously: in a way that is famous for something bad -->
<!-- abhor: to hate it very much, especially for moral reasons -->

> To design the perfect anti-Unix, write an operating system that thinks it
> knows what you're doing better than you do. And then adds injury to insult by
> getting it wrong.

これが禅の境地の一つか。

### Entry Barriers to Development

単なる使用者と開発者の間には高い壁がある。その壁となる重要な要因二つとは：

* the monetary cost of development tools
* the time cost of gaining proficiency as a developer

<!-- proficiency: 熟練度 -->

> Inexpensive tools and simple interfaces support casual programming, hobbyist
> cultures, and exploration. Programming projects can be small (often, formal
> project structure is plain unnecessary), and failure is not a catastrophe.
> This changes the style in which people develop code; among other things, they
> show less tendency to over-commit to failed approaches.

> Many people who write code under Unix do not think of it as writing code —
> they think of it as writing scripts to automate common tasks, or as
> customizing their environment.

これは手練れのプログラマー全員に共通する性質だと思う。

正反対の Unix の設計では、くだけたプログラミングが不可能だ。

## Operating-System Comparisons

最初の[グラフ][Fig.3.1]は、本節で調査する時分割 OS の家系図だ。

* 灰色箱は Unix 以外の OS
* 実線箱は本書執筆時点で存命の OS
* 矢印の実線、破線、点線は設計思想の影響度を大まかに示す（この順に強い）
* 要素 Unix は次のとおり：

  > The ‘Unix’ box includes all proprietary Unixes, including both AT&T and
  > early Berkeley versions. The ‘Linux’ box includes the open-source Unixes,
  > all of which launched in 1991.

### VMS

VMS は家系図では Windows NT の直接の祖先だ。知らない OS なので流し読む。

* VMS は Digital Equipment Corporation の小型計算機 VAX 用に開発された OS だ。
* VMS には完全な preemptive multitasking があるものの、プロセス生成がべらぼうに
  高くつく。
* VMS は長くて読みやすい COBOL 風システムコマンドとコマンドオプションを特徴とし
  ている。また、実行プログラムとコマンドライン構文については包括的なオンラインヘ
  ルプがある。
* VMS は立派な内部境界層がある：
* VMS ツールは当初高価で、インターフェイスも複雑だった。プログラマーの学習がたい
  へんだった。
* VMS はクライアント・サーバーの区別を先取りしていた。

### MacOS

家系図を見ると MacOS は始祖の一つに見える。実際のところは本文に記述がある。

> Except where specifically noted, the discussion here applies to pre-OS-X
> versions.

MacOS には Mac Interface Guidelines というたいへん強力な統一思想がある。

* アプリケーションの GUI の見てくれ、振る舞いを詳細に規定している。
* ガイドラインの一貫性は Mac 使用者の文化に大きな影響を与えた。

> All programs have GUIs. There is no CLI at all. Scripting facilities are
> present but much less commonly used than under Unix; many Mac programmers
> never learn them.

内部境界層の仕組みがかなり弱いことなどにより、安全保障を破ることが容易いとある。
そうする輩がほとんどいないからそうなっていない：

> The MacOS system of internal boundaries is very weak. There is a wired-in
> assumption that there is but a single user, so there are no per-user privilege
> groups. Multitasking is cooperative, not pre-emptive. All MultiFinder
> applications run in the same address space, so bad code in any application can
> corrupt anything outside the operating system's low-level kernel. Security
> cracks against MacOS machines are very easy to write; the OS has been spared
> an epidemic mainly because very few people are motivated to crack it.

Mac プログラマーは Unix プログラマーとは逆の方向に設計する傾向がある。つまり、エ
ンジンの外側からではなく、インターフェイスの内側から設計する。

> The intended role for the Macintosh was as a client operating system for
> nontechnical end users, implying a very low tolerance for interface
> complexity. Developers in the Macintosh culture became very, very good at
> designing simple interfaces.

以前述べられたように、OS は使用者に合わせて設計されるものだから、善悪の問題では
ない。

> Developers in the Macintosh culture became very, very good at designing simple
> interfaces.

Unix が旧型 MacOS から借用した考えもある：

> Classic MacOS has been end-of-lifed. Most of its facilities have been imported
> into MacOS X, which mates them to a Unix infrastructure derived from the
> Berkeley tradition. At the same time, leading-edge Unixes such as Linux are
> beginning to borrow ideas like file attributes (a generalization of the
> resource fork) from MacOS.

### OS/2

OS/2 はグラフで MS-DOS と VM/CMS を直接の先祖に持つ OS だ。

> Like Unix, OS/2 was built to be preemptively multitasking and would not run on
> a machine without an MMU (early versions simulated an MMU using the 286's
> memory segmentation). Unlike Unix, OS/2 was never built to be a multiuser
> system. Process-spawning was relatively cheap, but IPC was difficult and
> brittle. Networking was initially focused on LAN protocols, but a TCP/IP stack
> was added in later versions. There were no programs analogous to Unix service
> daemons, so OS/2 never handled multi-function networking very well.
>
> OS/2 had both a CLI and GUI. Most of the positive legendry around OS/2 was
> about the Workplace Shell (WPS), the OS/2 desktop. （中略） This is the one
> area of the design in which OS/2 achieved a level of capability which Unix
> arguably has not yet matched. The WPS was a clean, powerful, object-oriented
> design with understandable behavior and good extensibility. Years later it
> would become a model for Linux's GNOME project.

OS/2 は玄人向けではない使用者を想定して設計されたか：

> The intended audience for OS/2 was business and nontechnical end users,
> implying a low tolerance for interface complexity. It was used both as a
> client operating system and as a file and print server.

Unix ソフトウェアを移植するために EMX という環境が現れる：

> In the early 1990s, developers in the OS/2 community began to migrate to a
> Unix-inspired environment called EMX that emulated POSIX interfaces. Ports of
> Unix software started routinely showing up under OS/2 in the latter half of
> the 1990s.
>
> Anyone could download EMX, which included the GNU Compiler Collection and other
> open-source development tools.

OS/2 を研究することの関心の在処：

> OS/2 is interesting as a case study in how far a multitasking but single-user
> operating-system design can be pushed.

### Windows NT

なぜ見出しが Windows NT であるのか：

> All of Microsoft's operating systems since the demise of Windows ME in 2000
> have been NT-based; Windows 2000 was NT 5, and Windows XP (current in 2003) is
> NT 5.1. NT is genetically descended from VMS, with which it shares some
> important characteristics.

<!-- demise: death -->

例えば私が今使っている Windows 10 は Windows NT のバージョン 10.0 の一つだ。

Windows NT 核心技術は数年ごとに陳腐化する。技術の世代が変わるたびに、開発者は基
本的なことを別の方法で学び直す必要があった。

これは詳しく教えて欲しい：

> Socket programming has no unifying data object analogous to the Unix
> everything-is-a-file-handle, so multiprogramming and network applications that
> are simple in Unix require several more fundamental concepts in NT.

Preemptive multitasking は支援されているが、プロセス生成は高価。当時の Unix と
比べると最大で一桁高い。

スクリプト機能は弱く、OS はバイナリーファイル形式を多用する。

最初に本書を読んだときに、レジストリーに関する次の記述に膝を叩いた記憶がある。ア
プリケーション全部の構成を一箇所に封じるのはダメだ：

> System and user configuration data are centralized in a central properties
> registry rather than being scattered through numerous dotfiles and system data
> files as in Unix. This also has consequences throughout the design:
>
> * The registry makes the system completely non-orthogonal. Single-point
>   failures in applications can corrupt the registry, frequently making the
>   entire operating system unusable and requiring a reinstall.
> * The *registry creep* phenomenon: as the registry grows, rising access costs
>   slow down all programs.

NT の内部境界層はきわめて脆弱だ。本書では境界に穴があるという表現をしている。

DLL 地獄に関する分析。Python 開発でのまずい仮想環境の性質と似ている：

> Because Windows does not handle library versioning properly, it suffers from a
> chronic configuration problem called “DLL hell”, in which installing new
> programs can randomly upgrade (or even downgrade!) the libraries on which
> existing programs depend. This applies to the vendor-supplied system libraries
> as well as to application-specific ones: it is not uncommon for an application
> to ship with specific versions of system libraries, and break silently when it
> does not have them.

NT はどういう使用者を想定して設計されたのか：

> The intended audience for the NT operating systems is primarily nontechnical
> end users, implying a very low tolerance for interface complexity. It is used
> in both client and server roles.

NT プログラマーは趣味人と専門家に二分している：

> The result of this history is a sharp dichotomy between the design styles
> practiced by amateur and professional NT developers — the two groups barely
> communicate. While the hobbyist culture of small tools and shareware is very
> much alive, professional NT projects tend to produce monster monoliths even
> bulkier than those characteristic of ‘elitist’ operating systems like VMS.

<!-- dichtomy: 二分法 -->

当時の Unix 風シェル機能の使用可能性は次のとおりだが、現代ならば WSL 一択だ：

> Unix-like shell facilities, command sets, and library APIs are available under
> Windows through third-party libraries including UWIN, Interix, and the
> open-source Cygwin.

### BeOS

家系図によると BeOS は MacOS の子だ。

> BeOS tended to use binary file formats and the native database built into the
> file system, rather than Unix-like textual formats.

BeOS は GUI を好みつつも、CLI 支援も素晴らしい：

> The command-line shell of BeOS was a port of bash(1), the dominant open-source
> Unix shell, running through a POSIX compatibility library. Porting of Unix CLI
> software was, by design, trivially easy. Infrastructure to support the full
> panoply of scripting, filters, and service daemons that goes with the Unix
> model was in place.

これまでの記述から BeOS はかなり筋が良い OS のように思う。なぜ私が聞いたことがな
かったのが不思議だ。その理由は最後のパラグラフで窺い知れる。最後の一行を引用する：

<!-- astute: 抜け目がない -->

> BeOS finally succumbed in 2001 to a combination of anticompetitive maneuvering
> by Microsoft (lawsuit in progress as of 2003) and competition from variants of
> Linux that had been adapted for multimedia handling.

### MVS

> MVS (Multiple Virtual Storage) is IBM's flagship operating system for its
> mainframe computers.

メインフレームなら読まなくていいか？

> The unifying idea of MVS is that all work is batch; the system is designed to
> make the most efficient possible use of the machine for batch processing of
> huge amounts of data, with minimal concessions to interaction with human
> users.

メインフレームは大量データを処理するシステムに他ならない。そのせいなのか、通信機
能が生のファイルくらいしかない：

> Programs in a job communicate through temporary files; filters and the like
> are nearly impossible to do in a usable manner.

ということはファイルシステムは優れているのかと思いきや、そういうことはなかった：

> File system security was an afterthought in the original design. However, when
> security was found to be necessary, IBM added it in an inspired fashion:

<!-- afterthought: 後知恵 -->

> This did allow TCP/IP to supplant IBM's native SNA (Systems Network
> Architecture) as the network protocol of choice fairly seamlessly.

<!-- supplant: take the place or move into the position of -->

> Casual programming for MVS is almost nonexistent except within the community
> of large enterprises that run MVS.

メインフレーム機の日曜プログラマーのようなものは聞いたことがない。

### VM/CMS

これらも IBM のメインフレームだ。

> VM/CMS is IBM's *other* mainframe operating system. Historically speaking, it is
> Unix's uncle:

共通の祖先が CTSS であり、Unix と CTSS の間に Multics が来る。

> Although CMS is record-oriented, the records are essentially equivalent to the
> lines that Unix textual tools use.

テキストエディターとしては XEDIT が多用される。これはスクリーンエディターだ。

Rexx というシェルや Perl, Python と似たところのあるスクリプト言語がプログラミン
グを支援する。くだけたプログラミングができることが重要となる：

> Consequently, casual programming (especially by system administrators) is very
> important on VM/CMS. Free cycles permitting, admins often prefer to run
> production MVS in a virtual machine rather than directly on the bare iron, so
> that CMS is also available and its flexibility can be taken advantage of.
> (There are CMS tools that permit access to MVS file systems.)

仮想機械の話がいきなり出て来た。

> Since the year 2000, IBM has been promoting VM/CMS on mainframes to an
> unprecedented degree — as ways to host thousands of virtual Linux machines at
> once.

VM/CMS と Linux 機の関係が述べられた。

<!-- unprecedented: 前例のない -->

### Linux

> Linux does not include any code from the original Unix source tree, but it was
> designed from Unix standards to behave like a Unix.

この後は、逆に、Linux が「古典的な」Unix の伝統から逸脱していることを示す方向性
をいくつか見ていく。

> Linux users and developers, on the other hand, have been adapting themselves
> to address the nontechnical user's fear of CLIs. They have moved to building
> GUIs and GUI tools much more intensively than was the case in old-school Unix,
> or even in contemporary proprietary Unixes.

GUI にも開発意識が向いているというのがまず一点。

> One consequence is that Linux features binary-package systems far more
> sophisticated than any analogs in proprietary Unixes, with interfaces designed
> (as of 2003, with only mixed success) to be palatable to nontechnical end
> users.

パッケージ管理システムを備えているというのがもう一点。例えば apt(8) のようなもの
だ。

> The Linux community wants, more than the old-school Unixes ever did, to turn
> their software into a sort of universal pipefitting for connecting together
> other environments. （中略） The long-term goal is subsumption; Linux emulates
> so it can absorb.

『ドラゴンボール』のセルのようなものだと考えられる。

<!-- subsumption: ???? -->

> The remaining proprietary Unixes (such as Solaris, HP-UX, AIX, etc.) are
> designed to be big products for big IT budgets.

AIX とは懐かしい。

## What Goes Around, Comes Around

因果応報というか自業自得というか……。

<!-- plausible: seeming likely to be true, or able to be believed; もっともらしい -->
<!-- subsume: to include or place within something larger or more comprehensive -->

> MacOS has been subsumed by a Unix derivative.

そうなの？

> Only Microsoft Windows remains as a viable competitor independent of the Unix
> tradition.

<!-- viable: able to work as intended or able to succeed; 上手くいきそうな -->

これは正しそうだ。

> We pointed out Unix's strengths in Chapter 1, and they are certainly part of
> the explanation. But it's actually more instructive to look at the obverse of
> that answer and ask which weaknesses in Unix's competitors did them in.

<!-- instructive: providing a lot of useful information; ためになる -->

この思考法は面白い。裏を返せば敵の弱みがわかる。

最も明白な共通の問題は非移植性だという。

ネットワークが普及した世界における OS の要件を三つ挙げている：

* 複数使用者機能（特権グループが複数あること）
* 強力な複数仕事機能
* 効率的なプロセス間通信

> But as the designers of BeOS noticed, the requirements of pervasive networking
> cannot be met without implementing something very close to general-purpose
> timesharing. Single-user client operating systems cannot thrive in an
> Internetted world.

汎用の時分割にひじょうに近いものを実装しなければ、ネットワークの中断時にそれを検
知し、自動再接続することができないという問題を分析していく。

> With non-Unix models for timesharing effectively dead by 1990, there were not
> many possible responses client operating-system designers could mount to this
> challenge.

> Retrofitting server-operating-system features like multiple privilege classes
> and full multitasking onto a client operating system is very difficult

* 旧バージョンのクライアントとの互換性を壊す可能性が高い
* 一般的に安定性や安全保障の問題が多く、脆弱かつ不満のある結果しかもたらさない

> As with buildings, it's easier to repair superstructure on top of a solid
> foundation than it is to replace the foundations without trashing the
> superstructure.

この比喩は良い。

> Thus, the Unix design proved more capable of reinventing itself as a client
> than any of its client-operating-system competitors were of reinventing
> themselves as servers

これは何か読解を誤っているのか、意味が汲めない。

[Fig.3.1]: <http://www.catb.org/esr/writings/taoup/html/graphics/os-history.png>
