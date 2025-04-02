# Chapter 2. History

本書執筆当時の 2003 年現在の Unix 文化がなぜ当時のありように見えるのかを説明する
ために Unix の歴史を概説する本章が割かれている。

!!! note "TODO"

    * 年表
    * 登場人物表

[TOC]

## Origins and History of Unix, 1969-1995

* Compatible Time-Sharing System (CTSS): 時分割方式が導入された始祖的システム
* Multics project: メインフレームコンピューターの対話的な時分割法を上品に支援す
  る、機能満載の「情報ユーティリティー」を作成する試み
* Unix: これらの系譜に連なる第三のシステム

最初の二つは 1960 年代の前半に誕生したようだ。

### Genesis: 1969–1971

本節と次節の見出しは聖書の最初の方の本の呼称にちなむ。

> Unix was born in 1969 out of the mind of a computer scientist at Bell
> Laboratories, Ken Thompson.

この一文は完全に暗記しろ。

時分割方式が実際に最初に導入されたのは 1962年で、これを搭載したシステムはまだ実
験的で «temperamental beasts» だった。

> The standard interactive device on the earliest timesharing systems was the
> ASR-33 teletype — a slow, noisy device that printed upper-case-only on big
> rolls of yellow paper. The ASR-33 was the natural parent of the Unix tradition
> of terse commands and sparse responses.

テレタイプという単語は標準入力に接続された端末のファイル名を表示するコマンドの
名前 tty(1) の由来だ。

> The theme of computers being viewed not merely as logic devices but as the
> nuclei of communities was in the air; 1969 was also the year the ARPANET (the
> direct ancestor of today's Internet) was invented. The theme of “fellowship”
> would resonate all through Unix's subsequent history.

Unix の語源は先述の Multics と関係が大いにある：

> The original spelling was “UNICS” (UNiplexed Information and Computing
> Service), which Ritchie later described as “a somewhat treacherous pun on
> Multics”, which stood for MULTiplexed Information and Computing Service.

<!-- treacherous: 不実な -->

Unix 初のアプリケーションは nroff(1) の先祖であり、今で言うならばワープロのよう
に機能するものだ：

> Unix's first real job, in 1971, was to support what would now be called word
> processing for the Bell Labs patent department; the first Unix application was
> the ancestor of the nroff(1) text formatter.

### Exodus: 1971–1980

元々の Unix はアセンブラーで書かれていて、そのアプリケーションはアセンブラーとイ
ンタープリター型言語が混在したもので書かれていた。後者は B 言語と呼ばれるものだ。
そこから C 言語が誕生する：

> But B was not powerful enough for systems programming, so Dennis Ritchie added
> data types and structures to it. The resulting C language evolved from B
> beginning in 1971;

1973 年、Thompson と Ritchie は Unix を C 言語で書き直すことに成功した。本書のこ
のページにある巨大な装置 (PDP-11) を撮影した写真に二人が写っている。立っているヒ
ゲの男のほうが Ritchie だ。

1974 年、二人の論文が月刊誌 *Communications of the ACM* で発表される。Unix を初
めて世に知らしめた。論文公表後、世界中の研究所や大学が Unix を試す機会を求めて殺
到した。ただし、次の事情があり Unix は製品にはならなかった：

> Under a 1958 consent decree in settlement of an antitrust case, AT&T (the
> parent organization of Bell Labs) had been forbidden from entering the
> computer business. Unix could not, therefore, be turned into a product;

あるバージョンまでの Unix は現代からは部分的に認識できないところがあるようだ：

> The first Unix of which it can be said that essentially all of it would be
> recognizable to a modern Unix programmer was the Version 7 release in
> 1979.

「基本的にそのすべてが認識できる」バージョンは 1979 年以降のものということにな
る。

> The first Unix user group had formed the previous year. By this time Unix was
> in use for operations support all through the Bell System, and had spread to
> universities as far away as Australia, where John Lions's 1976 notes on the
> Version 6 source code became the first serious documentation of the Unix
> kernel internals.

Bell System というのは AT&T を含む企業系（構造）だ。John Lion という人物による
*Lions's Commentary on Unix 6th Edition* というのはおそらく個人的な目的で書かれ
た Unix カーネル内部に関するソースコードに関するノートだったと考えられるが、これ
が本格的な文書になった。

* 1978 年、最初の Unix 企業である Santa Cruz Operation が操業を開始する。
* 同年、Whitesmiths Ltd. が最初の商用 C コンパイラー Whitesmiths C を販売する。
* 1980 年までには、Seattle のソフトウェア会社が Unix ゲームを出荷した。

一方で Microsoft は製品としての Unix に愛着を持ち続けるようなことはなかった：

> But Microsoft's affection for Unix as a product was not to last very long
> (though Unix would continue to be used for most internal development work at
> the company until after 1990).

### TCP/IP and the Unix Wars: 1980-1990

カリフォルニア大学 Berkeley 校は Unix 開発において早くから重要な場所だった。次の
引用文中の当時大学院生 Bill Joy は vi(1) の作者でもあることを憶えておく：

> The first BSD release had been in 1977 from a lab run by a then-unknown grad
> student named Bill Joy. By 1980 Berkeley was the hub of a sub-network of
> universities actively contributing to their variant of Unix. Ideas and code
> from Berkeley Unix (including the vi(1) editor) were feeding back from
> Berkeley to Bell Labs.

ARPANET というネットワークはごく限定的な島を接続していたという前提がないと次の記
述にピンと来ないだろう。予備知識が要る：

> Before TCP/IP, the Internet and Unix cultures did not mix. Dennis Ritchie's
> vision of computers as a way to “encourage close communication” was one of
> collegial communities clustered around individual timesharing machines or in
> the same computing center; it didn't extend to the continent-wide distributed
> ‘network nation’ that ARPA users had started to form in the mid-1970s. Early
> ARPANETters, for their part, considered Unix a crude makeshift limping along
> on risibly weak hardware.
>
> After TCP/IP, everything changed. The ARPANET and Unix cultures began to merge
> at the edges, a development that would eventually save both from destruction.

とにかく、TCP/IP 以後でなければインターネットと Unix 文化が融合していないことを
憶えておく。

先ほどの Bill Joy は Sun Microsystems (1982-2010) の創業者の一人でもある：

> Sun Microsystems founders Bill Joy, Andreas Bechtolsheim, and Vinod Khosla set
> out to build a dream Unix machine with built-in networking capability.

ネットワーク機能が内蔵された夢の Unix 機。

C/C++ に関する記述を簡単にまとめる：

* C 言語は五年ほどでアセンブラーを駆逐した。
* 1900 年代初頭までに C/C++ はアプリケーションプログラミングでも優位に立つ。
* 1990 年代後半には他のコンパイル言語は時代遅れになった。

> By 1983 there were no fewer than six Unix-workalike operating systems for the
> IBM-PC: uNETix, Venix, Coherent, QNX, Idris, and the port hosted on the Sritek
> PC daughtercard.

あくまで Unix-workalike なのであって、System V だろうが BSD だろうが、Unix の移
植はまだ存在しなかったとある。

現代の感覚では信じられないが、Unix の将来性に PC や Microsoft が無関係であるかの
ように振る舞ったことだ。例えば：

> Sun Microsystems failed to see that commoditized PCs would inevitably become
> an attack on its workstation market from below.

Unix戦争の第一段階の話になる。System V と BSD の対立という内部闘争だ。闘争にはい
くつかの水準があり、技術的なものや文化的なものがあった。

> The divide was roughly between longhairs and shorthairs;

年配者らしい言い回しだ。藤子先生の『定年退食』を思い出して意味がわかった。

> programmers and technical people tended to line up with Berkeley and BSD, more
> business-oriented types with AT&T and System V.

長髪族に相当するのは前者だ。

Larry Wall が革命的なコマンドを引っ提げて Unix 世界に登場する：

> But something else happened in the year of the AT&T divestiture that would
> have more long-term importance for Unix. A programmer/linguist named Larry
> Wall quietly invented the patch(1) utility. The patch program, a simple tool
> that applies changebars generated by diff(1) to a base file, meant that Unix
> developers could cooperate by passing around patch sets — incremental changes
> to code — rather than entire code files.

さすがに patch(1) や diff(1) の意義については承知している。

> 1985 was also the year that Richard Stallman issued the GNU manifesto and
> launched the Free Software Foundation. Very few people took him or his GNU
> project seriously, a judgment that turned out to be seriously mistaken.

Richard Stallman, GNU, Free Software Foundation という言葉はまとめて憶える。

> This was followed in 1985 by the POSIX standards, an effort backed by the
> IEEE. These described the intersection set of the BSD and SVR3 (System V
> Release 3) calls, with the superior Berkeley signal handling and job control
> but with SVR3 terminal control. All later Unix standards would incorporate
> POSIX at their core, and later Unixes would adhere to it closely. The only
> major addition to the modern Unix kernel API to come afterwards was BSD
> sockets.

この辺を読んでいて思いついた。年表にまとめたほうがいいか？

> In 1986 Larry Wall, previously the inventor of patch(1), began work on Perl,
> which would become the first and most widely used of the open-source scripting
> languages. In early 1987 the first version of the GNU C compiler appeared, and
> by the end of 1987 the core of the GNU toolset was falling into place: editor,
> compiler, debugger, and other basic development tools. Meanwhile, the X
> windowing system was beginning to show up on relatively inexpensive
> workstations.

> More rounds of Unix fighting Unix ensued.

> The 1990 release of Windows 3.0 — the first successful graphical operating
> system from Redmond — cemented Microsoft's dominance, and created the
> conditions that would allow them to flatten and monopolize the market for
> desktop applications in the 1990s.

1989 年から 1993 年までの数年間は Unix の黒歴史だと述べている。そして：

> The GNU project failed to produce the free Unix kernel it had been promising
> since 1985, and after years of excuses its credibility was beginning to wear
> thin. PC technology was being relentlessly corporatized. The pioneering Unix
> hackers of the 1970s were hitting middle age and slowing down.

もう一つの反省点は経済的なものだ：

> Hardware was getting cheaper, but Unix was still too expensive. We were
> belatedly becoming aware that the old monopoly of IBM had yielded to a newer
> monopoly of Microsoft, and Microsoft's mal-engineered software was rising
> around us like a tide of sewage.

### Blows against the Empire: 1991-1995

最初のあらグラフは帝国製のコードを一掃する努力への言及だ。その次のパラグラフで
Linus Torvalds の名前が登場する：

> In August 1991 Linus Torvalds, then an unknown university student from
> Finland, announced the Linux project. Torvalds is on record that one of his
> main motivations was the high cost of Sun's Unix at his university. Torvalds
> has also said that he would have joined the BSD effort had he known of it,
> rather than founding his own.

BSD を知らなかったので、Torvalds 氏が自ら Linux プロジェクトを発足させたというわ
けか。BSD にせよ Linux にせよ、当時はほとんど重視されなかったとある。

> It would take another two years and the great Internet explosion of 1993–1994
> before the true importance of Linux and the open-source BSD distributions
> became evident to the rest of the Unix world.

AT&T との訴訟が影響して Berkeley の主要開発者たちが Linux に鞍替えする機運が生じ
る。BSD は三分裂。Unix 界における主導権は Linux に移っていった。

> The demand for cheap Internet was created by something else: the 1991
> invention of the World Wide Web.

Internet と WWW の術語の使い分けに注意。Web のほうが Internet の応用なのだ。

> By late 1993, Linux had both Internet capability and X. The entire GNU toolkit
> had been hosted on it from the beginning, providing high-quality development
> tools.

それは良かった。

昔気質の Unix 開発者で、より柔軟な考えを持つ数人は、誰もが使える安価な Unix
システムという夢が、意外な方向から近づいてきたことに気づき始めたとある。

> It was a bricolage that bubbled up out of the Internet by what seemed like
> spontaneous generation, appropriating and recombining elements of the Unix
> tradition in surprising ways.

「ありあわせのもので仕事したもの」で、Unix の伝統の要素を驚くような方法で流用、
組み替えたものだった。

> Elsewhere, corporate maneuvering continued. AT&T divested its interest in Sun
> in 1992; then sold its Unix Systems Laboratories to Novell in 1993; Novell
> handed off the Unix trademark to the X/Open standards group in 1994; AT&T and
> Novell joined OSF in 1994, finally ending the Unix wars. In 1995 SCO bought
> UnixWare (and the rights to the original Unix sources) from Novell. In 1996,
> X/Open and OSF merged, creating one big Unix standards group.

> But after 1995, the story of Unix became the story of the open-source
> movement. There's another side to that story; to tell it, we'll need to return
> to 1961 and the origins of the Internet hacker culture.

## Origins and History of the Hackers, 1961-1995

> But since 1990 the story of Unix is largely the story of how the open-source
> hackers changed the rules and seized the initiative from the old-line
> proprietary Unix vendors. Therefore, the other half of the history behind
> today's Unix is the history of the hackers.

### At Play in the Groves of Academe: 1961-1980

> The AI Lab programmers appear to have been the first to describe themselves as
> “hackers”.

> Socially, they were young, exceptionally bright, almost entirely male,
> dedicated to programming to the point of addiction, and tended to have streaks
> of stubborn nonconformism — what years later would be called ‘geeks’.

> The most famous of these hackers, Richard M. Stallman, became the ascetic
> saint of that religion.

### Internet Fusion and the Free Software Movement: 1981-1991

> After 1983 and the BSD port of TCP/IP, the Unix and ARPANET cultures began to
> fuse together. This was a natural development once the communication links
> were in place, since both cultures were composed of the same kind of people
> (indeed, in a few but significant cases the same people).

> But TCP/IP networking and slang were not the only things the post-1980 hacker
> culture inherited from its ARPANET roots. It also got Richard Stallman, and
> Stallman's moral crusade.

> Among his many inventions was the Emacs editor.

> Most of RMS's early contributors were old-time ARPANET hackers newly decanted
> into Unix-land, in whom the ethos of code-sharing ran rather stronger than it
> did among those with a more Unix-centered background.

> His behavior and rhetoric half-consciously echoed Karl Marx's attempts to
> mobilize the industrial proletariat against the alienation of their work.

> His program went way beyond maintaining a codebase, and essentially implied
> the abolition of intellectual-property rights in software. In pursuit of this
> goal, RMS popularized the term “free software”, which was the first attempt to
> label the product of the entire hacker culture.

> However, despite his determined efforts over more than fifteen years, the
> post-1980 hacker culture never unified around his ideological vision.

> In 1987–1988 the X development prefigured the really huge distributed
> communities that would redefine the leading edge of Unix five years later.

> After 1995 the debate over RMS's ideology took a somewhat different turn.
> Opposition to it became closely associated with both Linus Torvalds and the
> author of this book.

### Linux and the Pragmatist Reaction: 1991-1998

> Linus Torvalds neatly straddled the GPL/anti-GPL divide by using the GNU
> toolkit to surround the Linux kernel he had invented and the GPL's infectious
> properties to protect it, but rejecting the ideological program that went with
> RMS's license.

> Torvalds became a hero on Internet time; by 1995, he had achieved in just four
> years the kind of culture-wide eminence that RMS had required fifteen years to
> earn — and far exceeded Stallman's record at selling “free software” to the
> outside world. By contrast with Torvalds, RMS's rhetoric began to seem both
> strident and unsuccessful.

> In 1995, Linux found its killer app: Apache, the open-source webserver.

HTTP サーバーといえば Apache しかないだろうと思うが、1995 年が意外に近い過去であ
ることに驚く。

> The one thing Torvalds did not offer was a new ideology — a new rationale or
> generative myth of hacking, and a positive discourse to replace RMS's
> hostility to intellectual property with a program more attractive to people
> both within and outside the hacker culture. I inadvertently supplied this lack
> in 1997 as a result of trying to understand why Linux's development had not
> collapsed in confusion years before.

> For most hackers and almost all nonhackers, “Free software because it works
> better” easily trumped “Free software because all software should be free”.

> In early 1998, the new thinking helped motivate Netscape Communications to
> release the source code of its Mozilla browser.

## The Open-Source Movement: 1998 and Onward

> By the time of the Mozilla release in 1998, the hacker community could best be
> analyzed as a loose collection of factions or tribes that included Richard
> Stallman's Free Software Movement, the Linux community, the Perl community,
> the Apache community, the BSD community, the X developers, the Internet
> Engineering Task Force (IETF), and at least a dozen others. These factions
> overlap, and an individual developer would be quite likely to be affiliated
> with two or more.

> After 1995 Linux acquired a special role as both the unifying platform for
> most of the community's other software and the hackers' most publicly
> recognizable brand name.

ここがいちばん難しい：

> There was one exception: Richard Stallman and the Free Software Movement.
> “Open source” was explicitly intended to replace Stallman's preferred “free
> software” with a public label that was ideologically neutral, acceptable both
> to historically opposed groups like the BSD hackers and those who did not wish
> to take a position in the GPL/anti-GPL debate. Stallman flirted with adopting
> the term, then rejected it on the grounds that it failed to represent the
> moral position that was central to his thinking. The Free Software Movement
> has since insisted on its separateness from “open source”, creating perhaps
> the most significant political fissure in the hacker culture of 2003.

## The Lessons of Unix History

Unix 史に現れる反復パターンの最大規模のものはこうだ：

> when and where Unix has adhered most closely to open-source practices, it has
> prospered. Attempts to proprietarize it have invariably resulted in stagnation
> and decline.

歴史から得た教訓その一：

> The lesson for the future is that over-committing to any one technology or
> business model would be a mistake — and maintaining the adaptive flexibility
> of our software and the design tradition that goes with it is correspondingly
> imperative.

教訓その二はこう：

> the low-end/high-volume hardware technology almost always ends up climbing the
> power curve and winning.

その二はどこから引き出されたか：

> We saw it happen as minicomputers displaced mainframes, workstations and
> servers replaced minis, and commodity Intel machines replaced workstations and
> servers. The open-source movement is winning by commoditizing software. To
> prosper, Unix needs to maintain the knack of co-opting the cheap plastic
> solution rather than trying to fight it.
