# Philosophy

[TOC]

## Culture? What Culture?

技術書であるのに、本書のあちらこちらに「文化」「技術」「哲学」などの言葉が飛び交
う理由は Unix が独自の文化を有するから仕方がない：

> But Unix has a culture; it has a distinctive art of programming; and it
> carries with it a powerful design philosophy. Understanding these traditions
> will help you build better software, even if you're developing for a non-Unix
> platform.

禅というか、仏教で言う顕教と密教のような考え方があるようだ：

> Senior engineers develop huge bodies of implicit knowledge, which they pass to
> their juniors by (as Zen Buddhists put it) “a special transmission, outside
> the scriptures”.

Unix は技術一辺倒ではないのだという強い主張を感じる：

> A very few software technologies have proved durable enough to evolve strong
> technical cultures, distinctive arts, and an associated design philosophy
> transmitted across generations of engineers.
>
> The Unix culture is one of these. The Internet culture is another — or, in the
> twenty-first century, arguably the same one.

## The Durability of Unix

前節の最後を受けてか、耐久度という観点で議論が展開される。

> Unix was born in 1969 and has been in continuous production use ever since.
> That's several geologic eras by computer-industry standards

まるで化石を論じるかのような書き出しだ。

> Much of Unix's stability and success has to be attributed to its inherent
> strengths, to design decisions Ken Thompson, Dennis Ritchie, Brian Kernighan,
> Doug McIlroy, Rob Pike and other early Unix developers made back at the
> beginning; decisions that have been proven sound over and over. But just as
> much is due to the design philosophy, art of programming, and technical
> culture that grew up around Unix in the early days.

初期 Unix を取り巻く設計哲学、プログラミング技術、技術文化とは何であるかをこのあ
と詳しく語ってくれるのだろう。

## The Case against Learning Unix Culture

このへんから、Unix 懐疑論者という新キャラが登場するという体で読み進めるとわかり
やすい。

> What confounds the skeptics' case is, more than anything else, the rise of
> Linux and other open-source Unixes (such as the modern BSD variants). Unix's
> culture proved too vital to be smothered even by a decade of vendor
> mismanagement. Today the Unix community itself has taken control of the
> technology and marketing, and is rapidly and visibly solving Unix's problems

## What Unix Gets Wrong

ここはもう一回目を通す。

> For a design that dates from 1969, it is remarkably difficult to identify
> design choices in Unix that are unequivocally wrong.

この牽制のやり方は習得しよう。

> But the cost of the mechanism-not-policy approach is that when the user *can*
> set policy, the user *must* set policy.

本節の結論は次だが、理解が少し難しい：

> So the flip side of the flip side is that the “mechanism, not policy”
> philosophy may enable Unix to renew its relevance long after competitors more
> tied to one set of policy or interface choices have faded from view.

## What Unix Gets Right

> Unix culture is worth learning because there are some things that Unix and its
> surrounding culture clearly do better than any competitors.

Unix とその文化をまとめて考えるのがコツだ。その優った文化として次を挙げている：

* オープンソースソフトウェアであること
* 移植性と標準が公開されていて誰でも使えること
* インターネット
* オープンソース共同体
* 柔軟性があること
* 工夫するのが楽しいこと
* Unix で得た教訓が他でも使えること

### Open-Source Software

このオープンソースという術語自体は 1998 年のものだが、それが指す概念はもっと以前
から存在していたという。

### Cross-Platform Portability and Open Standards

> The Unix API is the closest thing to a hardware-independent standard for
> writing truly portable software that exists.

Unix API が文書化されているという記述も重要。

> Binary-only applications for other operating systems die with their birth
> environments, but Unix sources are forever.

バイナリーとテキストの比較論は以降も現れる。

### The Internet and the World Wide Web

理論や仕様はどこにでもだれにでも使えるものであるかもしれないが、伝統となれば話は
別だ：

> The theory and specifications are available to anyone, but the engineering
> tradition to make them into a solid and working reality exists only in the
> Unix world.

インターネットにおける URL の概念は Unix ファイルシステムに由来する：

> In particular, the concept of the Uniform Resource Locator (URL) so central to
> the Web is a generalization of the Unix idea of one uniform file namespace
> everywhere. To function effectively as an Internet expert, an understanding of
> Unix and its culture are indispensable.

さらに、脚注で «Other operating systems have generally copied or cloned Unix
TCP/IP implementations» と述べている。

### The Open-Source Community

インターネットの隆盛と共同体の形成は分けて考えられない。

> Entire Unix operating systems, with complete toolkits and basic applications
> suites, are available for free over the Internet. Why code from scratch when
> you can adapt, reuse, recycle, and save yourself 90% of the work?

前半を端折って引用したが、有料既製品に負けない品質のシステムであるのに、という文
脈だ。

### Flexibility All the Way Down

柔軟性の意味するところはこれがすべて：

> The many ways Unix provides to glue together programs mean that components of
> its basic toolkit can be combined to produce useful effects that the designers
> of the individual toolkit parts never anticipated.

Unix における部品・道具それぞれの特徴はこうだ：

> Unix tradition lays heavy emphasis on keeping programming interfaces
> relatively small, clean, and orthogonal — another trait that produces
> flexibility in depth.

Unix プログラムインターフェイスの集合は計量空間らしい。

### Unix Is Fun to Hack

> People who pontificate about Unix's technical superiority often don't mention
> what may ultimately be its most important strength, the one that underlies all
> its successes.

この言い回しは何かに使いたい。動詞 pontifacate など知らなかった。

> ‘Fun’ is therefore a sign of peak efficiency.

楽しいかどうかで効率性を計ることにするというのは面白い。

### The Lessons of Unix Can Be Applied Elsewhere

> Even non-Unix programmers can benefit from studying that Unix experience.
> Because Unix makes it relatively easy to apply good design principles and
> development methods, it is an excellent place to learn them.

Unix は優れた設計原則や開発手法を比較的簡単に適用できる対象であり、それらを学ぶ
のに最適な場所でもある。

Unix コードの大部分は ANSI C をサポートする OS ならば、それに直接移植することが
できるという意味でも can be applied elsewhere なのだ。

## Basics of the Unix Philosophy

この節は比較的長い。

> The ‘Unix philosophy’ originated with Ken Thompson's early meditations on how
> to design a small but capable operating system with a clean service interface.

Google で Ken Thompson を検索すると、猿渡哲也先生作品に出てきそうなモノクロ近影
写真が出てくる。

> The Unix philosophy (like successful folk traditions in other engineering
> disciplines) is bottom-up, not top-down.

これはよく憶えておく。どちらかを選べたらボトムアップだ。

Doug McIlroy, Rob Pike, Ken Thompson 各老師による Unix 評を、おそらく著者が独自
に要約したのがここから詳述される規則集だ。これらの価値が貴いという観点は現代でも
失われていないのでは：

* Modularity
* Clarity
* Composition
* Separation
* Simplicity
* Parsimony
* Transparency
* Robustness
* Representation
* Least Surprise
* Silence
* Repair
* Economy
* Generation
* Optimization
* Diversity
* Extensibility

### Rule of Modularity: Write simple parts connected by clean interfaces.

複雑さを抑制することがプログラミングの本質であるならば、どうすればよいか。複雑な
ものをほぐしてより小さい部分に分離する。それらの部分は後できれいにつながるようで
なければならない。そのような性質は modularity と呼ばれている。

> The only way to write complex software that won't fall on its face is to hold
> its global complexity down — to build it out of simple parts connected by
> well-defined interfaces, so that most problems are local and you can have some
> hope of upgrading a part without breaking the whole.

### Rule of Clarity: Clarity is better than cleverness.

> Code that is graceful and clear, on the other hand, is less likely to break —
> and more likely to be instantly comprehended by the next person to have to
> change it.

きれいなコードは壊れにくい。

### Rule of Composition: Design programs to be connected with other programs.

> Unix tradition strongly encourages writing programs that read and write
> simple, textual, stream-oriented, device-independent formats. Under classic
> Unix, as many programs as possible are written as simple *filters*, which take
> a simple text stream on input and process it into another simple text stream
> on output.

よく使う CLI はこの原則によく従っている。テキストであることがまずは必要であって、
さらに変な構造や書式がないこと。

> Text streams are to Unix tools as messages are to objects in an
> object-oriented setting. The simplicity of the text-stream interface enforces
> the encapsulation of the tools.

後世になって PowerShell のようなメッセージがほんとうにオブジェクトである CLI が
生まれる。

### Rule of Separation: Separate policy from mechanism; separate interfaces from engines.

> Thus, hardwiring policy and mechanism together has two bad effects: It makes
> policy rigid and harder to change in response to user requirements, and it
> means that trying to change policy has a strong tendency to destabilize the
> mechanisms.

分離の例を二つ挙げている：

* Emacs 方式。このエディターでは C 言語で書かれた編集要素を制御するのに、内蔵
  Lisp インタプリターを使用する。
* ソケット通信方式。フロントエンドとバックエンドを専用プロトコルで通信、協調させ
  る。

### Rule of Simplicity: Design for simplicity; add complexity only where you must.

技術マッチョはダメだ。

### Rule of Parsimony: Write a big program only when it is clear by demonstration that nothing else will do.

見出しにある parsimony という単語は知らなんだ。吝嗇くらいの意味か？

> ‘Big’ here has the sense both of large in volume of code and of internal
> complexity.

量としても質としてもデカいということ？

### Rule of Transparency: Design for visibility to make inspection and debugging easier.

> A particularly effective way to ease debugging is to design for *transparency*
> and *discoverability*.

透明である、発見可能である、を定義する：

> A software system is *transparent* when you can look at it and immediately
> understand what it is doing and how. It is *discoverable* when it has
> facilities for monitoring and display of internal state so that your program
> not only functions well but can be seen to function well.

デバッグ機能は後付けであってはならない。

### Rule of Robustness: Robustness is the child of transparency and simplicity.

著者はソフトウェアが堅牢であるということを次のように定義している：

> Software is said to be *robust* when it performs well under unexpected
> conditions which stress the designer's assumptions, as well as under normal
> conditions.

思っていたより厳しい意味だった。

どうすれば堅牢に作れるのか。方法は二つあるという。それが見出しの後半だ。これらの
概念も改めて定義される：

> We observed above that software is *transparent* when you can look at it and
> immediately see what is going on. It is *simple* when what is going on is
> uncomplicated enough for a human brain to reason about all the potential cases
> without strain. The more your programs have both of these qualities, the more
> robust they will be.

### Rule of Representation: Fold knowledge into data, so program logic can be stupid and robust.

知識をデータに折り重ねる！

> Even the simplest procedural logic is hard for humans to verify, but quite
> complex data structures are fairly easy to model and reason about.

これはなぜだろうか。

データ構造の複雑さとコードの複雑さのどちらを選ぶかといえば、前者を選ぶべきだとい
うことになる。

この後に C 言語のポインターの話が続くのが不穏だ。

### Rule of Least Surprise: In interface design, always do the least surprising thing.

高名な「驚き最小の原則」だ。

> Therefore, avoid gratuitous novelty and excessive cleverness in interface
> design. If you're writing a calculator program, ‘+’ should always mean
> addition! When designing an interface, model it on the interfaces of
> functionally similar or analogous programs with which your users are likely to
> be familiar.

何が意外である（ない）かは、使用者による。

最後に引用されている Henry Spencer 氏の言葉には誰もが思い当たる状況があるだろ
う：

> The flip side of the Rule of Least Surprise is to avoid making things
> superficially similar but really a little bit different. This is extremely
> treacherous because the seeming familiarity raises false expectations. It's
> often better to make things distinctly different than to make them almost the
> same.

<!-- superficially: うわべでは -->
<!-- treacherous: 裏切りの、油断ならぬ -->

### Rule of Silence: When a program has nothing surprising to say, it should say nothing.

この規則の元々の理由は、単に出力そのものが高く付いた時代がかつてあったからだ：

> This “silence is golden” rule evolved originally because Unix predates video
> displays. On the slow printing terminals of 1969, each line of unnecessary
> output was a serious drain on the user's time.

まずは：

> Well-behaved Unix programs do their jobs unobtrusively, with a minimum of fuss
> and bother. Silence is golden.

もう一つ：

> Well-designed programs treat the user's attention and concentration as a
> precious and limited resource, only to be claimed when necessary.

<!-- predate: 前から存在する -->
<!-- unobtrusively: 目立たずに -->

### Rule of Repair: Repair what you can — but when you must fail, fail noisily and as soon as possible.

失敗するならやかましく、かつ早く失敗しろ。

> Well-designed programs cooperate with other programs by making as much sense
> as they can from ill-formed inputs; they either fail noisily or pass strictly
> clean and correct data to the next program in the chain.

<!-- cope: 対処する -->
<!-- heed: 心に留める -->

> McIlroy adjures us to *design* for generosity rather than compensating for
> inadequate standards with permissive implementations.

<!-- adjure: 命じる-->
<!-- generosity: 寛大な -->

### Rule of Economy: Programmer time is expensive; conserve it in preference to machine time.

本書執筆時点でさえマシン性能は十分なものだった。プログラマーの時間を節約すること
が重要なのは言うまでもないとある。

> In the early minicomputer days of Unix, this was still a fairly radical idea
> (machines were a great deal slower and more expensive then).

ただし、著者はこの格言がどういうわけか現実にはまだ浸透していないと考えている。

> And indeed this is happening within the Unix world, though outside it most
> applications shops still seem stuck with the old-school Unix strategy of
> coding in C (or C++).

### Rule of Generation: Avoid hand-hacking; write programs to write programs when you can.

手作業を忌避しろというよりは、プログラムを書くプログラムを書けというのが主旨らし
い。

> Human beings are notoriously bad at sweating the details. Accordingly, any
> kind of hand-hacking of programs is a rich source of delays and errors. The
> simpler and more abstracted your program specification can be, the more likely
> it is that the human designer will have gotten it right. Generated code (at
> every level) is almost always cheaper and more reliable than hand-hacked.
>
> We all know this is true (it's why we have compilers and interpreters, after
> all) but we often don't think about the implications.

### Rule of Optimization: Prototype before polishing. Get it working before you optimize it.

まず試作で、それから最適化だ。

* «90% of the functionality delivered now is better than 100% of it delivered
  never» Kernighan and Plauger
* «Premature optimization is the root of all evil» Donald Knuth; 完全版は本書脚
  注参照。
* «Make it run, then make it right, then make it fast» Kent Beck

最適化には局所的なものと大域的なものがある。早過ぎる前者は後者を阻害すると言って
いる：

> A prematurely optimized portion of a design frequently interferes with changes
> that would have much higher payoffs across the whole design, so you end up
> with both inferior performance and excessively complex code.

設計の観点からも試作することには意味がある：

> Using prototyping to learn which features you don't have to implement helps
> optimization for performance; you don't have to optimize what you don't write.

### Rule of Diversity: Distrust all claims for one true way.

> Even the best software tools tend to be limited by the imaginations of their
> designers.

設計者の想像には限界がある。

Unix の伝統では、ただ一つの真の方法のような考えを疑念であると考える。そして、次
のようなものを良しとする：

> It embraces multiple languages, open extensible systems, and customization
> hooks everywhere.

<!-- embrace: 抱擁する→受け入れる→採用する -->

### Rule of Extensibility: Design for the future, because it will be here sooner than you think.

Unix 愛好家は技術者というより芸術家に近いようだ。

> Never assume you have the final answer. Therefore, leave room for your data
> formats and code to grow; otherwise, you will often find that you are locked
> into unwise early choices because you cannot change them while maintaining
> backward compatibility.

データ形式とコードは拡張性を意識して設計しろということだ。さらに実践的なことを述
べられる：

> When you design protocols or file formats, make them sufficiently
> self-describing to be extensible. Always, always either include a version
> number, or compose the format from self-contained, self-describing clauses in
> such a way that new clauses can be readily added and old ones dropped without
> confusing format-reading code.

例えば自作アプリケーションデータを XML ファイルで入出力可能にする設計だとすると、
ファイルの最初の方に `<version>` のような要素を格納してしかるべきだ。

## The Unix Philosophy in One Lesson

かの有名な KISS 原則を紹介する節。忘れたらこの巨大な画像を確認して欲しい。本書の
残りの部分で読者がその方法を学ぶ助けとするつもりだと述べている。

## Applying the Unix Philosophy

Unix の教えを標語的にして一覧にしたもの（完全版ではないと断ってある）がある。

自分の言葉で表現し直して以下に綴る：

* 送信元と送信先に依存しないフィルターであり得るものはそうであって然るべきだ。
* データストリームはテキストであって然るべきだ。
* データベースレイアウトとアプリケーションプロトコルはテキストであって然るべきだ。
* 複雑な UI は複雑なバックエンドから分離してあって然るべきだ。
* C 言語で書く前にインタプリター言語で試作する。
* 一つの言語しか使わないとプログラムが複雑になり過ぎる可能性がある場合、かつその
  場合に限り、一つの言語ですべてを書くより、複数の言語を混ぜるほうがいい。
* 受け入れは寛大に、送り出しは厳格に。
* 絞り込む際には不要な情報を捨ててはいけない。
* 必要な仕事をするだけの小さなプログラムを書け。

ここで言う C 言語は現代ならそれ以外の違う言語でもあり得る。コードが面倒な高級言
語くらいの意味に解釈したい。

> We'll see the Unix design rules, and the prescriptions that derive from them,
> applied over and over again in the remainder of this book.

Unix の設計規則とそこから派生した方策は、当然ではあるが、他の伝統的なソフトウェ
ア工学のベストプラクティスに収束する傾向がある。

## Attitude Matters Too

> If you don't know what the right thing is, do the minimum necessary to get the
> job done, at least until you figure out what the right thing is.

言われなくてもそうすると言いたいところだが、実際は意外にそうではない。

> You have to believe that software design is a craft worth all the
> intelligence, creativity, and passion you can muster.

<!-- muster: 奮い起こす -->

Unix の哲学を正しく行うにはかなりの意思の強さが要ると言う。必要以上に頑張ること
なく、賢く働き、余分な努力は後に取っておく。道具を活用し、自動化する。そんな態度
であれと述べ、こう語りかけられる：

> If this attitude seems preposterous or vaguely embarrassing to you, stop and
> think; ask yourself what you've forgotten. Why do you design software instead
> of doing something else to make money or pass the time? You must have thought
> software was worthy of your passion once....

馬鹿らしいとはさすがに思っていないが、熱が失せているのは確かだ。
