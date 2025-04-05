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

### VMS

### MacOS

### OS/2

### Windows NT

### BeOS

### MVS

### VM/CMS

### Linux

## What Goes Around, Comes Around
